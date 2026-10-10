# Independent audit: heavy-fermion “ceiling”
Turn 3 — 2026-10-10. Audit only; no candidates, structural calculations or QPU jobs.

## Verdict
**The arithmetic reproduces; the family-wide exclusion does not follow.** The selected data support low priority for conventional ambient-pressure heavy-fermion tuning toward 300 K, not a universal 28–30 K upper bound. Confidence is **high** in the numerical and logical audit, **moderate** in quantitative extrapolations from the table.

## Read-only checks
Read `../turn-0002/hf_ceiling.py`, `README.md`, `outputs/hf_table.csv`, and `outputs/hf_ceiling.json`. The requested root-level JSON is absent; the actual JSON is under `outputs/`. Recomputed the CSV with NumPy/SciPy without executing the earlier script or modifying earlier files.

| Quantity | Recomputed result |
|---|---:|
| Rows | 18 |
| Maximum Tc / gamma-derived scale (PuCoGa5) | 0.03472024 |
| Median ratio | 0.00722069 |
| Log-log slope / prefactor / R² | −0.636557 / 40.4700 / 0.297714 |
| Conditional Tc at gamma = 50 / 100 mJ mol⁻¹ K⁻² | 28.490 / 14.245 K |
| Conditional gamma for 300 K, maximum / median ratio | 4.74833 / 0.98750 mJ mol⁻¹ K⁻² |

No mJ-to-J error was found. But the ceiling simplifies exactly to

`Tc_new <= max_sample(Tc * gamma) / gamma_new = 1424.5 / gamma_new`

(gamma in mJ mol⁻¹ K⁻²). **The gas constant and scale conversion cancel:** the calculation assumes the largest observed product bounds all future materials; it does not independently establish that bound.

Without PuCoGa5, slope = −0.48435, R² = 0.23892 and the gamma-50 ceiling = 19.8 K. Without all Pu rows, slope = −0.31543 and R² = 0.14299. A conventional iid OLS 95% slope interval is approximately [−1.155, −0.118], ignoring selection, family correlations and gamma uncertainty. The fit is descriptive; neither it nor the sample maximum supplies a universal prediction bound.

## Scale and multiband assumptions
For a **3D parabolic degenerate quasiparticle band**, with n carriers per formula unit,

`gamma_molar = (pi²/2) R n / TF`.

Setting n = 1 gives an effective Fermi-temperature proxy, **not an identity for Kondo-lattice coherence T***. Nominal f-electron count does not establish carrier count. Multiple such bands give `gamma = (pi²/2) R sum_i(n_i/TF_i)`; dimensionality and nonparabolic dispersion change the conversion. These are model derivations, not measured band/carrier parameters for this table.

Primary two-fluid work gives CeCoIn5 coherence T* ≈ **45 K** [1], versus **141.48 K** here. Using 45 K gives Tc/T* ≈ **0.0511**, already above 0.03472. This does not violate the table's *gamma-defined* ratio; it shows why that ratio cannot be called a universal *coherence-scale* ratio. Yang–Pines explicitly distinguish Tc/T* from kBTc/EF; their table gives PuCoGa5 T* = 430 K and Tc/T* = 0.043, and pressure-optimized CeRhIn5 ratio 0.062 [2]. The pressure example is not an ambient-pressure counterexample. Their proposed kBTc/EF maximum near 0.03 is phenomenology within that model, not a rigorous bound on every family mechanism.

CeCoIn5 thermal-conductivity/specific-heat experiments propose heavily paired sheets and light pockets with negligible gaps [3]. Total gamma thus needs band-resolved justification before it is used as a unique pairing-scale measure. This undermines the one-scale proof; it does **not** demonstrate a light-band route to 300 K.

## Concrete data/interpretation issues
1. **Ce2PdIn8 normalization/value discrepancy.** The cited 2009 paper explicitly estimates gamma ≈ **1 J mol⁻¹ K⁻² per formula unit**, not the CSV's 550 mJ [4]. A later polycrystal study reports high-field gamma ≈ **1220 mJ mol⁻¹ K⁻²**, Tc = 0.7 K and logarithmic normal-state Cel/T [5]. The row needs an exact source and mol-Ce versus mol-formula-unit declaration; this audit cannot certify that 550 is simply a factor-two error. The 2009 pair (0.68 K, 1000 mJ) under n=1 gives **41.03 K and 0.01657**, rather than 74.60 K and 0.009116. Two equivalent carriers would double the inferred scale, but two Ce atoms do not establish that assumption.
2. **Incompatible gamma extraction regimes.** Petrovic supports CeCoIn5's 290 mJ as C/T above 2.5 K, and describes an inverse spin-fluctuation-scale relationship as an estimate [6]. Ce2PdIn8 has nonconstant NFL C/T [5]; the CSV explicitly uses a hidden-order-reconstructed URu2Si2 value. Temperature, field, subtraction and extrapolation protocols are missing. C/T just above Tc is not necessarily a T→0 Sommerfeld constant.
3. **Maximum-value uncertainty.** Primary PuCoGa5 spectroscopy work reports specific-heat gamma estimates **77–95 mJ** [7]. At 95, the conditional ratio is **0.04284**, gamma-50 ceiling **35.15 K**, and gamma required for 300 K **5.858 mJ**. This does not approach 300 K but makes 28 K an unjustifiably precise hard limit.
4. **README falsifier is numerically incorrect.** “Tc > 5 K at gamma > 100” need not exceed 1424.5. At gamma = 100, Tc must exceed **14.245 K**; at Tc = 5, gamma must exceed **284.9 mJ**. The general test is Tc × gamma > 1424.5, with consistent normalization.
5. **Gamma ≥ 50 is an imposed cutoff**, not a derived physical bound. Molar gamma depends on carrier count, formula-unit normalization and band DOS; a small total value alone does not show every quasiparticle is light. The 18 hand-selected rows have no completeness test or uncertainties.

## Calibrated conclusion
Retain the conditional statement: **if a new material shares the relevant one-scale physics and gamma normalization, has gamma ≥ 50 mJ, and never exceeds this sample's maximum Tc × gamma, then Tc ≤ 28.49 K** (roughly 35 K using the cited Pu gamma alternative). For 300 K at gamma = 50, the script-defined ratio would be **0.3656**, **10.53 times** the observed maximum: a substantial extrapolation, not a contradiction of a proven physical bound.

Replace the family exclusion with: **“This dataset offers no evidence for an ambient-pressure 300 K heavy-fermion route; extrapolation within its empirical regime predicts much lower Tc. A family-wide exclusion remains unproven.”** Better gamma values alone cannot repair the missing bound; independent coherence measurements, band/carrier normalization and a justified pairing-scale constraint are needed.

## Primary sources checked
[1] Nakatsuji, Pines & Fisk, *Probing the Kondo Lattice*, arXiv:cond-mat/0304587; published as *Two Fluid Description of the Kondo Lattice*, PRL 92, 016401 (2004). DOI: 10.1103/PhysRevLett.92.016401.
[2] Yang & Pines, *Emergence of superconductivity in heavy-electron materials*, PNAS 111, 18178–18182 (2014), Table 1; arXiv:1410.1840. DOI: 10.1073/pnas.1422100112.
[3] Tanatar et al., *Unpaired Electrons in the Heavy-Fermion Superconductor CeCoIn5*, PRL 95, 067002 (2005); arXiv:cond-mat/0503342. DOI: 10.1103/PhysRevLett.95.067002.
[4] Kaczorowski et al., *Emergence of a superconducting state from an antiferromagnetic phase in single crystals of the heavy fermion compound Ce2PdIn8*, PRL 103, 027003 (2009), p. 3; arXiv:0906.1881. DOI: 10.1103/PhysRevLett.103.027003. Used for explicit gamma normalization, not endorsement of its magnetic-phase interpretation.
[5] Kaczorowski et al., *Heavy-fermion superconductivity in Ce2PdIn8*, Solid State Communications 150, 411–414 (2010), p. 3; arXiv:1001.4607. DOI: 10.1016/j.ssc.2009.12.007.
[6] Petrovic et al., *Heavy-Fermion Superconductivity in CeCoIn5 at 2.3 K*, J. Phys.: Condens. Matter 13, L337 (2001); arXiv:cond-mat/0103168.
[7] Daghero et al., *Strong-coupling d-wave superconductivity in PuCoGa5 probed by point-contact spectroscopy*, Nature Communications 3, 786 (2012). DOI: 10.1038/ncomms1785.

Output: `hf_ceiling_independent_review.md` only. No earlier files modified; no candidate invented or submitted. Targeted audit, not an exhaustive October 2026 literature census.
