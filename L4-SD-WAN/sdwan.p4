/* -*- P4_16 -*- */
#include <core.p4>
#include <v1model.p4>

/* ---- Tipos y constantes ---- */
typedef bit<9>  egressSpec_t;
typedef bit<48> macAddr_t;
const bit<16> ETHERTYPE_IPV4 = 0x0800;

/* ---- Cabeceras ---- */
header ethernet_t {
    macAddr_t dstAddr;
    macAddr_t srcAddr;
    bit<16>   etherType;
}
header ipv4_t {
    bit<4>   version;
    bit<4>   ihl;
    bit<8>   diffserv;
    bit<16>  totalLen;
    bit<16>  identification;
    bit<3>   flags;
    bit<13>  fragOffset;
    bit<8>   ttl;
    bit<8>   protocol;
    bit<16>  hdrChecksum;
    bit<32>  srcAddr;
    bit<32>  dstAddr;
}
header tcp_t {
    bit<16> srcPort;
    bit<16> dstPort;
    bit<32> seqNo;
    bit<32> ackNo;
    bit<4>  dataOffset;
    bit<3>  reserved;
    bit<9>  flags;
    bit<16> window;
    bit<16> checksum;
    bit<16> urgentPtr;
}
header udp_t {
    bit<16> srcPort;
    bit<16> dstPort;
    bit<16> length_;
    bit<16> checksum;
}

/* ---- Estructuras ---- */
struct headers_t {
    ethernet_t ethernet;
    ipv4_t     ipv4;
    tcp_t      tcp;
    udp_t      udp;
}
struct metadata_t {
    bit<1>  prio_hit;
    bit<16> l4_len;     // longitud L4 (solo TCP) calculada en ingress
}

/* ---- Parser ---- */
parser MyParser(packet_in packet,
                out headers_t hdr,
                inout metadata_t meta,
                inout standard_metadata_t sm) {
    state start {
        packet.extract(hdr.ethernet);
        transition select(hdr.ethernet.etherType) {
            ETHERTYPE_IPV4: parse_ipv4;
            default: accept;
        }
    }
    state parse_ipv4 {
        packet.extract(hdr.ipv4);
        transition select(hdr.ipv4.protocol) {
            6:  parse_tcp;
            17: parse_udp;
            default: accept;
        }
    }
    state parse_tcp { packet.extract(hdr.tcp); transition accept; }
    state parse_udp { packet.extract(hdr.udp); transition accept; }
}

/* ---- VerifyChecksum (vacío) ---- */
control MyVerifyChecksum(inout headers_t hdr, inout metadata_t meta) { apply { } }

/* ---- Ingress ---- */
control MyIngress(inout headers_t hdr,
                  inout metadata_t meta,
                  inout standard_metadata_t sm) {

    action drop()                  { sm.egress_spec = 0; }
    action forward(egressSpec_t p) { sm.egress_spec = p; }
    action prio_forward(egressSpec_t p) {
        sm.egress_spec = p;
        meta.prio_hit = 1w1;
    }

    table prio_tcp_dst { key = { hdr.tcp.dstPort : exact; } actions = { prio_forward; NoAction; } size = 64; }
    table prio_tcp_src { key = { hdr.tcp.srcPort : exact; } actions = { prio_forward; NoAction; } size = 64; }
    table prio_udp_dst { key = { hdr.udp.dstPort : exact; } actions = { prio_forward; NoAction; } size = 64; }
    table prio_udp_src { key = { hdr.udp.srcPort : exact; } actions = { prio_forward; NoAction; } size = 64; }

    table dmac {
        key = { hdr.ethernet.dstAddr : exact; }
        actions = { forward; drop; }
        size = 1024;
        default_action = drop();
    }

    apply {
        meta.prio_hit = 1w0;
        meta.l4_len   = 16w0;  // por defecto

        /* calcular l4_len para TCP: totalLen - (ihl<<2) */
        if (hdr.ipv4.isValid()) {
            bit<16> ihl_bytes = ((bit<16>)hdr.ipv4.ihl) << 2;
            meta.l4_len = (bit<16>)(hdr.ipv4.totalLen - ihl_bytes);
        }

        if (hdr.tcp.isValid()) { hdr.tcp.checksum = 16w0;prio_tcp_dst.apply(); prio_tcp_src.apply(); }
        if (hdr.udp.isValid()) { hdr.udp.checksum = 16w0;prio_udp_dst.apply(); prio_udp_src.apply(); }

        if (meta.prio_hit == 1w0) {
            dmac.apply();
        }
    }
}

/* ---- Egress ---- */
control MyEgress(inout headers_t hdr,
                 inout metadata_t meta,
                 inout standard_metadata_t sm) { apply { } }

/* ---- ComputeChecksum (sin if, solo llamadas permitidas) ---- */
control MyComputeChecksum(inout headers_t hdr, inout metadata_t meta) {
    apply {
        /* IPv4 header checksum */
        update_checksum(
            hdr.ipv4.isValid(),
            { hdr.ipv4.version, hdr.ipv4.ihl, hdr.ipv4.diffserv, hdr.ipv4.totalLen,
              hdr.ipv4.identification, hdr.ipv4.flags, hdr.ipv4.fragOffset,
              hdr.ipv4.ttl, hdr.ipv4.protocol, hdr.ipv4.srcAddr, hdr.ipv4.dstAddr },
            hdr.ipv4.hdrChecksum,
            HashAlgorithm.csum16);

        /* TCP: pseudoheader + payload (usa meta.l4_len calculada en ingress) */
        update_checksum_with_payload(
            hdr.tcp.isValid() && hdr.ipv4.isValid(),
            { hdr.ipv4.srcAddr, hdr.ipv4.dstAddr, 8w0, 8w6,  meta.l4_len },
            hdr.tcp.checksum,
            HashAlgorithm.csum16);

        /* UDP: pseudoheader + payload (la longitud viene en el propio header UDP) */
        update_checksum_with_payload(
            hdr.udp.isValid() && hdr.ipv4.isValid(),
            { hdr.ipv4.srcAddr, hdr.ipv4.dstAddr, 8w0, 8w17, hdr.udp.length_ },
            hdr.udp.checksum,
            HashAlgorithm.csum16);
    }
}

/* ---- Deparser ---- */
control MyDeparser(packet_out packet, in headers_t hdr) {
    apply {
        packet.emit(hdr.ethernet);
        packet.emit(hdr.ipv4);
        packet.emit(hdr.tcp);
        packet.emit(hdr.udp);
    }
}

/* ---- Switch ---- */
V1Switch(
    MyParser(),
    MyVerifyChecksum(),
    MyIngress(),
    MyEgress(),
    MyComputeChecksum(),
    MyDeparser()
) main;
