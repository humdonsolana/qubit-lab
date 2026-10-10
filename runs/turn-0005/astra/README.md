# Turn 0005 — Astra: nickelate evidence and oxygen-retention audit

Date: **2026-10-10**. Wild-card direction: **ambient-pressure bilayer nickelate films**. These are substrate-constrained films, not unloaded bulk specimens. No room-temperature claim, new composition-specific Tc forecast, or discovery is made.

## Result

**Prioritize reproducible phase coherence and oxygen retention before extrapolating Tc from lattice constants.** I reanalysed the numerical source workbook for Ko et al., DOI `10.1038/s41586-024-08525-3`, rather than digitizing a plot or assigning CHGNet energies a Tc. Fable owns the complementary structure/Hubbard-model work; no quantum hardware was used by Astra.

### 1. An insufficient predictor was quantitatively identified

- Source Figure 5a provides five in-plane-lattice/onset rows, of which just two have positive reported onsets. Three zero entries represent no observed transition, **not measured physical Tc=0**. A two-point line has no residual degrees of freedom to establish predictive error.
- In Figure 5b, the **11 positive-onset rows** give an out-of-plane c-only descriptive linear fit with **R²=0.08117**, slope **−9.196 K/Å**, and leave-one-row-out RMSE **6.402 K**. This selected fit is not a causal strain coefficient or a validation on unseen compositions.
- Incorrectly treating seven zero-coded nonobservations as exact Tc=0 changes the slope to **+38.166 K/Å**. The sign reversal is a data-handling warning, not evidence of either physical law.
- At the same **published** c=20.56135 Å, two reported onsets are **42.44 and 26.20 K**. Any deterministic c-only fit has at least an **8.12-K worst residual** on that pair. Equality at source precision is not proof of identical microscopic structure; no universal model-error bound is claimed.

### 2. A direct, reproducible aging target

For Figure 2b I used a deliberately operational criterion: highest ascending-temperature crossing of **rho(T)/rho(50 K)=0.5**, after 0.25-K median bins and linear interpolation. Sorting does not establish actual warming/cooling sweep direction. These numbers are **neither the authors' onset temperatures nor measured zeros**.

| Source label | Operational half-resistivity crossing (K) | rho(5 K)/rho(50 K) |
|---|---:|---:|
| O3-annealed | 22.106 | 0.08014 |
| 8 days | 14.349 | 0.21041 |
| 20 days | 6.176 | 0.41964 |
| O3 annealed again | 18.217 | 0.18664 |

Independent implementation reproduced all **48 aging fraction checks** (four samples, three bin widths, four fractions), including absent crossings. Maximum finite discrepancy was 7.11e-15 K. Testing bins of 0.1, 0.25 and 0.5 K changed half-crossings by at most 0.016 K from the stated stable-sorted raw convention. This is numerical robustness, **not experimental uncertainty**. Repeated raw temperatures make the unbinned interpolation convention-dependent; see `validation.md`.

This aging/reannealing comparison supports controlled processing/retention experiments. It does **not** isolate oxygen loss from structural evolution, determine diffusion barriers, or prove that a protective cap raises Tc.

## Literature audit and decision

Primary source details are in `nickelate_audit_independent.md` and `literature_and_test_plan.md`.

- Zhou et al., DOI `10.1093/nsr/nwag151` (2026): ~63-K onset and ~30-K measured zero in S1; S2 has ~56-K onset/~37-K zero; magnetic response begins ~23 K. Do not combine the best onset and zero from different samples or call onset a bulk coherence temperature.
- Osada et al., DOI `10.1038/s41563-026-02695-3`: La2SmNi2O7 has ambient onset ~41 K but zero ~6 K; the 67-K upper transition requires 16 GPa.
- Geometry alone is not sufficient: primary preprint `arXiv:2609.00542` reports tetragonal La2SrNi2O7−δ with straight interlayer Ni–O–Ni and no superconductivity within its investigated conditions.
- More oxygen is not always better: DOI `10.1038/s41563-025-02351-2` finds interstitial-oxygen ordering suppressing **pressure-induced** superconductivity. This is a warning against oxygen-maximization, not a quantified film-aging mechanism.

**No new leaderboard candidate is justified by this audit.** Numeric Tc for a new composition would require an independently validated model or composition-matched evidence. Existing C0001 (Mg2IrH6) remains challenged on phase access from Turn 4; this turn does not upgrade it. The concrete next target is a controlled, matched-film oxygen-retention study described in the test plan. This is an experimental proposal, not an AI-predicted high-Tc material.

## Reproduction and artifacts

Use the compatibility runner (not `analyze_nickelate_data.py` alone):

```bash
python run_analysis.py --out /tmp/astra5/regenerated
python independent_validation.py --source /tmp/astra5/regenerated --out /tmp/astra5/revalidated
```

Dependencies: Python 3.11, numpy, scipy, pandas, requests, openpyxl. Actual versions and hashes are in `validation.md`. The runner skips source Figure 1c A11: its temperature column has 2,421 values but its resistivity column is empty. Nothing was imputed.

Artifacts:
- `analyze_nickelate_data.py`, `run_analysis.py`: publisher download, provenance, operational thresholds, descriptive fits; actual executed code.
- `independent_validation.py`, `validation.md`: independent numerical reconstruction and caveats.
- `outputs/{summary.json,figure5a.csv,figure5b.csv,operational_thresholds.csv,aging_independent.csv}`: archived results.
- `nickelate_audit_independent.md`: independent primary-literature audit.
- `literature_and_test_plan.md`: exact sources, negative controls and proposed falsification.

The shell UID cannot write this turn directory. Analysis ran under `/tmp/astra5`; small outputs were copied via the file tool and verified **byte-for-byte**. Large raw data are not archived: the 13,454,360-byte publisher workbook is reproducibly fetched by the script, expected SHA-256 `33012becd28a8578bd1342cb67a05c38dc10abffb7e3b86973c5dabb82f9ad6d`. A future publisher revision must be treated as a different input, not silently compared. `validation.md` also records the extracted raw-curve hash. No personal data, secrets, or keys saved.
