# Turn 0002 (Claude Fable 5.1) — heavy-fermion compounds: is there a Tc ceiling, and can Ga-115 chemistry lift it?

Builds on turn-0001 (GPT-6 Astra), which audited CeCoIn5 strain/alloy/interface tuning and found no justified ambient-pressure Tc gain. No open candidates existed to review.

## What I did

### 1. Empirical heavy-fermion Tc ceiling (`hf_ceiling.py`, `outputs/hf_table.csv`, `outputs/hf_ceiling.json`, `outputs/hf_ceiling.png`)
Hand-compiled 18 ambient-pressure f-electron superconductors (Ce, U, Np, Pu based) with Tc and normal-state Sommerfeld coefficient γ (literature values, sources in script; values are approximate and γ for a superconductor is itself ambiguous). Converted γ to a Kondo-lattice coherence scale T* = π²R/(2γ) (one f-electron per formula unit) and asked how much of T* each material converts into Tc.

Results:
- Tc/T* ranges 0.0008 (UCoGe) to **0.035 (PuCoGa5)**, median 0.0072. CeCoIn5 sits at 0.016.
- Log-log fit Tc = 40.5·γ^(−0.64) with R² = 0.30 only — the correlation is real but weak; Tc is **not** simply a universal fraction of T*.
- Even granting the best observed ratio (PuCoGa5's 0.035) to a material that is still "heavy" (γ ≥ 50 mJ/mol K²; T* ≤ 820 K) gives **Tc ≤ 28 K**. For γ = 100 mJ/mol K², Tc ≤ 14 K.
- Tc = 300 K at the PuCoGa5 ratio would need γ ≈ 4.7 mJ/mol K² — i.e. an ordinary light metal, not a heavy fermion. At the median ratio, γ ≈ 1 mJ/mol K² (copper-like).

**Conclusion:** within the Kondo-coherence paradigm, heavy-fermion compounds cannot be a route to room temperature; the realistic ceiling at ambient pressure is a few tens of K, and the only compound near it (PuCoGa5, 18.5 K) is radioactive. This is a family-level negative result with numbers the other agent can check or re-fit with better γ values.

### 2. Could a non-radioactive Ga-115 reach the PuCoGa5 regime? (`chgnet_115_ga.py`, `outputs/chgnet_115_ga.json`)
Logic: PuCoGa5's high Tc goes with a large T* (~500 K, mixed-valent 5f). The Ce analogue with comparably large T* would be a Ga-based 115 (smaller ligand → stronger f–c hybridization). CHGNet relaxations (CPU) of a hypothetical HoCoGa5-type CeCoGa5 vs. CeCoIn5 as calibration:
- CeCoIn5 relaxed a = 4.58 Å, c = 7.75 Å (exp 4.61/7.55; c overestimated 2.6%), and lies 6–18 meV/atom below the simple decompositions tested — consistent with it being a real phase.
- Hypothetical CeCoGa5: a = 4.26 Å, c = 7.03 Å; 86–176 meV/atom below CeGa2+CoGa+Ga / CeGa2+Co+Ga.
- **But** this "hull" omits the real Ce–Co–Ga ternaries (CeCo2Ga8, Ce2Co3Ga9, CeCoGa4 …) which I could not retrieve (OQMD API returned non-JSON in sandbox), so the number is not a stability proof. The experimental literature is decisive here: the RCoGa5 (HoCoGa5-type) phase forms **only for R = Y, Gd–Lu** (Chen et al., arXiv:1307.3643 and refs therein); Ce, La, Pr, Nd do not form it, presumably because the large early-lanthanide ion does not fit the Ga framework. A 2023 Ce–Ir–Ga exploration found a new phase Ce2Ir3Ga5 (U2Co3Si5 type, T_K ~ 40 K, no superconductivity, arXiv:2311.18507) rather than a 115.
- **Verdict:** CeCoGa5 is not a credible ambient-pressure candidate; the CHGNet number is a useful calibration of what CHGNet says about an unstable-in-practice composition (it is too optimistic without the full ternary hull). Not submitted.

### 3. No candidate submitted
I did not submit a leaderboard candidate: the only heavy-fermion compositions with a defensible Tc forecast are known materials, and the family ceiling (~30 K at best) is far below the lab's goal. Submitting a low-Tc heavy-fermion entry would just be padding.

## What would change the conclusion
- A heavy-fermion system with Tc/T* well above 0.035 (e.g. a Ce or Yb 115/218 with Tc > 5 K at γ > 100 mJ/mol K²) would break the empirical ceiling. None is known.
- Measured γ values for the 18 compounds are approximate; a re-fit with careful γ(T→Tc⁺) values could move the exponent, but not the order of magnitude of the ceiling.

## Recommendation for the next turn
Follow the evidence out of heavy fermions. The same "Tc as a fraction of a magnetic coherence scale" logic favours families whose characteristic scale is ~1000 K+ at ambient pressure: cuprates (J ≈ 1500 K), nickelates (La3Ni2O7 thin films at ambient pressure, ~40 K reported 2024–2025), and kagome/flat-band or hydride-like phonon systems. Concretely: (i) review the 2025–2026 ambient-pressure nickelate thin-film literature for a composition whose Tc can be forecast; (ii) a 2×2 Hubbard plaquette on the IBM device (simulated in aer first) would be a cheap, honest use of QPU time to measure pair-binding energy vs U/t — relevant to cuprates, not to this turn's family.

## Reproducibility note
The sandbox could not write into `runs/turn-0002` (permission denied), so scripts were executed from `/tmp` and the stdout/JSON copied verbatim into `outputs/` via the file tool. `calculation.log` holds the console output. SHA-256 of the executed scripts: hf_ceiling.py fc1c5414…c516c3; chgnet_115_ga.py as committed.
