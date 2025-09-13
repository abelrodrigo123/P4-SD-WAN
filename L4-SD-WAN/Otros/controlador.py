#!/usr/bin/env python3
import sys, os, grpc, argparse, binascii
from p4.v1 import p4runtime_pb2, p4runtime_pb2_grpc
from google.protobuf import text_format

# Utilidades mínimas
def mac_bytes(mac):
    return bytes(int(x,16) for x in mac.split(':'))

def port_bytes(p):
    return (p).to_bytes(2, byteorder='big')

def write_table_entry(p4info, stub, device_id, election_id, table, match, action, params):
    te = p4runtime_pb2.TableEntry()
    te.table_id = p4info.tables[table].preamble.id
    for m in match:
        mf = te.match.add()
        mf.field_id = p4info.tables[table].match_fields[m['field']].id
        if m['type'] == 'exact':
            mf.exact.value = m['value']
    te.action.action.actor.action.action_id = p4info.actions[action].preamble.id
    for pid, val in params:
        p = te.action.action.actor.action.params.add()
        p.param_id = p4info.actions[action].params[pid].id
        p.value = val
    stub.Write(p4runtime_pb2.WriteRequest(
        device_id=device_id,
        election_id=election_id,
        updates=[p4runtime_pb2.Update(type=p4runtime_pb2.Update.INSERT, entity=p4runtime_pb2.Entity(table_entry=te))]
    ))

class P4Info:
    def __init__(self, txt):
        self.actions = {}
        self.tables = {}
        p4 = p4runtime_pb2.P4Info()
        with open(txt, 'r') as f: text_format.Merge(f.read(), p4)
        for a in p4.actions:
            self.actions[a.preamble.name] = a
        for t in p4.tables:
            # index match fields por nombre corto
            mf_idx = { mf.name.split('.')[-1]: mf for mf in t.match_fields }
            t.match_fields = mf_idx
            self.tables[t.preamble.name] = t

def open_channel(addr):
    return grpc.insecure_channel(addr)

def set_pipeline(stub, device_id, election_id, p4info_txt, json_path):
    with open(json_path, 'rb') as f:
        blob = f.read()
    p4info = p4runtime_pb2.P4Info()
    with open(p4info_txt, 'r') as f:
        text_format.Merge(f.read(), p4info)
    req = p4runtime_pb2.SetForwardingPipelineConfigRequest(
        device_id=device_id,
        election_id=election_id,
        action=p4runtime_pb2.SetForwardingPipelineConfigRequest.VERIFY_AND_COMMIT,
        config=p4runtime_pb2.ForwardingPipelineConfig(p4info=p4info, p4_device_config=blob)
    )
    stub.SetForwardingPipelineConfig(req)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--s1-ip",   default="172.17.2.1")
    ap.add_argument("--s2-ip",   default="172.17.2.2")
    ap.add_argument("--grpc",    type=int, default=9559)
    ap.add_argument("--s1-id",   type=int, default=1)
    ap.add_argument("--s2-id",   type=int, default=2)
    ap.add_argument("--p4info",  default="sdwan.p4rt.txt")
    ap.add_argument("--json",    default="sdwan.json")
    ap.add_argument("--prio-port", type=int, default=6000)
    ap.add_argument("--eth1-port", type=int, default=1)
    ap.add_argument("--eth2-port", type=int, default=2)
    ap.add_argument("--eth4-port", type=int, default=4)
    # MACs
    ap.add_argument("--mac-h1", default="02:fd:00:00:00:01")
    ap.add_argument("--mac-h2", default="02:fd:00:00:01:01")
    args = ap.parse_args()

    # Carga p4info (para IDs)
    p4info = P4Info(args.p4info)

    # Conecta s1 y s2
    s1 = p4runtime_pb2_grpc.P4RuntimeStub(open_channel(f"{args.s1-ip}:{args.grpc}"))
    s2 = p4runtime_pb2_grpc.P4RuntimeStub(open_channel(f"{args.s2-ip}:{args.grpc}"))
    election = p4runtime_pb2.Uint128(high=0, low=1)

    # Instala pipeline
    set_pipeline(s1, args.s1_id, election, args.p4info, args.json)
    set_pipeline(s2, args.s2_id, election, args.p4info, args.json)

    # Shorthands
    T = {
        "dmac"         : "MyIngress.dmac",
        "tcp_dst"      : "MyIngress.prio_tcp_dst",
        "tcp_src"      : "MyIngress.prio_tcp_src",
        "udp_dst"      : "MyIngress.prio_udp_dst",
        "udp_src"      : "MyIngress.prio_udp_src",
    }
    A = {
        "fwd"          : "MyIngress.forward",
        "pfwd"         : "MyIngress.prio_forward",
    }

    # --- S1 ---
    # Bridging por MAC destino (camino normal por eth2)
    write_table_entry(p4info, s1, args.s1_id, election,
        T["dmac"],
        match=[{"field":"ethernet.dstAddr", "type":"exact", "value": mac_bytes(args.mac_h2)}],
        action=A["fwd"],
        params=[( "egress_port", port_bytes(args.eth2_port) )]
    )
    write_table_entry(p4info, s1, args.s1_id, election,
        T["dmac"],
        match=[{"field":"ethernet.dstAddr", "type":"exact", "value": mac_bytes(args.mac_h1)}],
        action=A["fwd"],
        params=[( "egress_port", port_bytes(args.eth1_port) )]
    )
    # Reglas prioritarias por puerto -> forzar eth4
    for tbl in ("tcp_dst","tcp_src","udp_dst","udp_src"):
        write_table_entry(p4info, s1, args.s1_id, election,
            T[tbl],
            match=[{"field": ("tcp.dstPort" if "dst" in tbl and "tcp" in tbl else
                              "tcp.srcPort" if "src" in tbl and "tcp" in tbl else
                              "udp.dstPort" if "dst" in tbl else "udp.srcPort"),
                    "type":"exact",
                    "value": args.prio_port.to_bytes(2,"big")}],
            action=A["pfwd"],
            params=[("egress_port", port_bytes(args.eth4_port))]
        )

    # --- S2 ---
    write_table_entry(p4info, s2, args.s2_id, election,
        T["dmac"],
        match=[{"field":"ethernet.dstAddr", "type":"exact", "value": mac_bytes(args.mac_h1)}],
        action=A["fwd"],
        params=[("egress_port", port_bytes(args.eth2_port))]
    )
    write_table_entry(p4info, s2, args.s2_id, election,
        T["dmac"],
        match=[{"field":"ethernet.dstAddr", "type":"exact", "value": mac_bytes(args.mac_h2)}],
        action=A["fwd"],
        params=[("egress_port", port_bytes(args.eth1_port))]
    )
    for tbl in ("tcp_dst","tcp_src","udp_dst","udp_src"):
        write_table_entry(p4info, s2, args.s2_id, election,
            T[tbl],
            match=[{"field": ("tcp.dstPort" if "dst" in tbl and "tcp" in tbl else
                              "tcp.srcPort" if "src" in tbl and "tcp" in tbl else
                              "udp.dstPort" if "dst" in tbl else "udp.srcPort"),
                    "type":"exact",
                    "value": args.prio_port.to_bytes(2,"big")}],
            action=A["pfwd"],
            params=[("egress_port", port_bytes(args.eth4_port))]
        )

    print("[done] Tablas L2 + prioridad por puerto instaladas (sin recomputar checksums).")

if __name__ == "__main__":
    main()
