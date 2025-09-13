echo "Aplicando reglas tc de checksum en los enlaces del host..."
for d in h1-e1 h2-e1 s1-e1 s1-e2 s1-e4 s2-e1 s2-e2 s2-e4; do
  sudo tc qdisc del dev "$d" clsact 2>/dev/null
  sudo tc qdisc add dev "$d" clsact
  sudo tc filter add dev "$d" egress protocol ip flower action csum ip tcp udp
done
echo "Reglas tc aplicadas."
