"""Tc/J audit for bulk iron-based superconductors.
Tests the Qin & Yang (npj Quantum Mater. 10, 13 (2025), doi:10.1038/s41535-025-00733-y)
intrinsic bound Tc/J <= 0.04-0.07 against neutron-derived exchange couplings of Fe-based parents.
Exchange values (S*J, meV, J1a/J1b/J2 Heisenberg fits to spin waves) are transcribed from memory of
the cited INS papers and flagged 'unverified' -- re-check before quoting precisely.
Family Tc_max = best ambient bulk Tc reached by doping that parent's family.
Ran in /tmp/f7 (turn folder not shell-writable); outputs copied verbatim.
"""
import json, math
kB = 0.08617  # meV/K
rows = [
 # name, SJ1a, SJ1b, SJ2, family Tc_max (K), family record compound, INS source
 ("CaFe2As2", 49.9, -5.7, 18.9, 34.0, "Ca1-xNaxFe2As2 ~34 K", "Zhao et al. Nat. Phys. 5, 555 (2009) [unverified transcription]"),
 ("BaFe2As2", 59.2, -9.2, 13.6, 38.0, "Ba0.6K0.4Fe2As2 38 K", "Harriger et al. PRB 84, 054544 (2011) [unverified transcription]"),
 ("SrFe2As2", 30.8, -5.0, 21.7, 37.0, "Sr0.6K0.4Fe2As2 ~37 K", "Ewings et al. PRB 83, 214519 (2011) [unverified transcription]"),
 ("NaFeAs",   40.0, 16.0, 19.0, 25.0, "NaFe1-xCoxAs / LiFeAs <=25 K", "Zhang et al. PRB 90, 140502(R) (2014) [unverified transcription]"),
 ("LaFeAsO",  44.6, -6.0, 25.0, 58.6, "Sm0.8Th0.2FeAsO0.775F0.225 58.6 K (1111 family record)", "Ramazanoglu et al. PRB 87, 140509 (2013) [uncertain values]"),
 ("FeTe",    -17.5,-51.0, 21.7, 14.5, "FeTe1-xSex ~14.5 K", "Lipscombe et al. PRL 106, 057004 (2011) [unverified transcription]"),
]
out = []
for name, j1a, j1b, j2, tc, rec, src in rows:
    defs = {
      "J1a":            j1a,
      "J1_avg":         0.5*(j1a+j1b),
      "J1_avg+J2":      0.5*(j1a+j1b)+j2,
      "max(|J1a|,|J1b|,|J2|)": max(abs(j1a),abs(j1b),abs(j2)),
    }
    ratios = {k: (kB*tc/v if v>0 else None) for k,v in defs.items()}
    out.append(dict(parent=name, SJ1a=j1a, SJ1b=j1b, SJ2=j2, family_Tc_max_K=tc, record=rec, source=src,
                    J_definitions_meV=defs, Tc_over_J=ratios))
    print(f"{name:10s} Tc_max={tc:5.1f} K  " + "  ".join(f"{k}:{(r if r is None else round(r,3))}" for k,r in ratios.items()))
# What J is needed for the bar and for room temperature under the bound?
need = {}
for T in (58.6, 133.0, 151.0, 300.0):
    need[T] = {f"ratio_{r}": round(kB*T/r,1) for r in (0.04,0.07,0.10)}
    print(f"T={T} K needs J(meV) = {need[T]}")
# Ceiling implied by the largest Fe-based NN exchange (BaFe2As2 SJ1a=59.2 meV)
Jmax = 59.2
ceil = {r: round(r*Jmax/kB,1) for r in (0.04,0.07,0.10)}
print("Ceiling from J=59.2 meV:", ceil)
json.dump(dict(rows=out, J_needed_meV=need, ceiling_K_from_J59p2=ceil), open("outputs/fe_tc_over_j.json","w"), indent=1)
