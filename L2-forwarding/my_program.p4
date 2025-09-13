/* -*- P4_16 -*- */
#include <core.p4>
#include <v1model.p4>

const bit<16> TYPE_IPV4 = 0x800;
const bit<16> TYPE_BROADCAST = 0x1234;

/*************************************************************************
*********************** H E A D E R S  ***********************************
*************************************************************************/

typedef bit<9>  egressSpec_t;
typedef bit<48> macAddr_t;
typedef bit<32> ip4Addr_t;

header ethernet_t {
    macAddr_t dstAddr;
    macAddr_t srcAddr;
    bit<16>   etherType;
}

header arp_t {
    bit<16> htype;
    bit<16> ptype;
    bit<8>  hlen;
    bit<8>  plen;
    bit<16> oper;
    bit<48> sha;
    bit<32> spa;
    bit<48> tha;
    bit<32> tpa;
}


struct metadata {
    /* empty */
}

struct headers {
    ethernet_t   ethernet;
    arp_t        arp;
}


/*************************************************************************
*********************** P A R S E R  ***********************************
*************************************************************************/

parser MyParser(packet_in packet,
                out headers hdr,
                inout metadata meta,
                inout standard_metadata_t standard_metadata) {

    state start {
        packet.extract(hdr.ethernet);
        transition select(hdr.ethernet.etherType) {
            0x0806: parse_arp;
            default: accept;
        }
        
    }
    state parse_arp {
        packet.extract(hdr.arp);
        transition accept;
    }
}


/*************************************************************************
************   C H E C K S U M    V E R I F I C A T I O N   *************
*************************************************************************/

control MyVerifyChecksum(inout headers hdr, inout metadata meta) {
    apply {  }
}


/*************************************************************************
**************  I N G R E S S   P R O C E S S I N G   *******************
*************************************************************************/

control MyIngress(inout headers hdr,
                  inout metadata meta,
                  inout standard_metadata_t standard_metadata) {

    action send_arp_reply(macAddr_t my_mac, ip4Addr_t my_ip) {
    hdr.ethernet.dstAddr = hdr.ethernet.srcAddr;
    hdr.ethernet.srcAddr = my_mac;
    hdr.arp.oper = 2; // ARP reply
    hdr.arp.tha = hdr.arp.sha;
    hdr.arp.sha = my_mac;
    hdr.arp.tpa = hdr.arp.spa;
    hdr.arp.spa = my_ip;
    }

    table arp_table {
        key = {
            hdr.arp.tpa: exact;
        }
        actions = {
            send_arp_reply;
            NoAction;
        }
        size = 256;
        default_action = NoAction();
    }

    action forward(bit<9> egress_port) {
        standard_metadata.egress_spec = egress_port;
    }

    action broadcast() {
        standard_metadata.mcast_grp = 1;
    }

    table dmac {
        key = {
            hdr.ethernet.dstAddr: exact;
        }

        actions = {
            forward;
            broadcast;
            NoAction;
        }
        size = 256;
        default_action = NoAction;
    }

    apply {
        if (hdr.arp.isValid() && hdr.arp.oper == 1) { // ARP request
            arp_table.apply();
        } else {
            dmac.apply();
        }
    }
}

/*************************************************************************
****************  E G R E S S   P R O C E S S I N G   *******************
*************************************************************************/

control MyEgress(inout headers hdr,
                 inout metadata meta,
                 inout standard_metadata_t standard_metadata) {


    apply {  }
}

/*************************************************************************
*************   C H E C K S U M    C O M P U T A T I O N   **************
*************************************************************************/

control MyComputeChecksum(inout headers hdr, inout metadata meta) {
     apply {

    }
}


/*************************************************************************
***********************  D E P A R S E R  *******************************
*************************************************************************/

control MyDeparser(packet_out packet, in headers hdr) {
    apply {
        packet.emit(hdr.ethernet);
        packet.emit(hdr.arp);
               
    }
}

/*************************************************************************
***********************  S W I T C H  *******************************
*************************************************************************/

//switch architecture
V1Switch(
MyParser(),
MyVerifyChecksum(),
MyIngress(),
MyEgress(),
MyComputeChecksum(),
MyDeparser()
) main;