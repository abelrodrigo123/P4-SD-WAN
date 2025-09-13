#!/usr/bin/env bash
# Apaga offloads en todas las NIC tipo eth*/en* dentro del contenedor
for IF in /sys/class/net/*; do
  IFACE=$(basename "$IF")
  case "$IFACE" in
    lo) continue ;;
    eth*|en*) : ;;
    *) continue ;;
  esac
  ethtool -K "$IFACE" rx off tx off gso off gro off tso off tx-checksum-ip-generic off 2>/dev/null || true
done
