# Astra Turn 5 — independent numerical validation and small-output archive

Date: 2026-10-10. Scope: the local publisher workbook and computed outputs in `/tmp/astra5/results`; not a new superconducting-temperature prediction or an audit of other papers. High confidence in the numerical reproduction below, conditional on this supplied workbook. No external redownload or independent physical identification of sweep direction was performed.

## Work actually performed

Read `analyze_nickelate_data.py`, `run_analysis.py`, and the complete `summary.json`. Wrote and executed `independent_validation.py` against `publisher_source.xlsx` without importing or executing the original analysis functions. Reconstructed Figure 5 arrays from the workbook and obtained exact numeric equality with both CSVs. Calculated centered least-squares slope/R2 and refit each leave-one-out fold with `numpy.linalg.lstsq` (not the original SciPy `linregress`). Independently grouped the Figure 2b curves with Python dictionaries, using nearest-even rounded temperature bins and separate median T/rho, and calculated threshold roots by explicit segment interpolation (not `numpy.interp`). Independently calculated unbinned roots after stable ascending-temperature sorting, preserving workbook order at equal temperatures.

Execution: `python independent_validation.py --source /tmp/astra5/results --out /tmp/astra5/validation` returned exit code 0. Environment: Python 3.11.17, NumPy 2.4.6, pandas 2.3.3, SciPy 1.17.1, openpyxl 3.1.5. Assertions checked workbook hash/size, Figure 5 arrays, regression, lower bound, A11 omission, and 48 aging fraction comparisons (four curves x three widths x four fractions). These are actual checks; other curves' operational values were copied but not independently recomputed in this audit.

## Duplicate-c lower bound: verified

The source Figure 5b has 18 rows, 11 positive entries, and seven zero-coded entries [S1, Figure 5b; S2]. Repeated c values are equal at published precision, not evidence of identical microscopic strain.

| c (angstrom) | listed onset values (K) | minimum possible worst residual (K) | irreducible SSE (K^2) |
|---|---|---:|---:|
| 20.23163 | 32.962, 30.1 | 1.431 | 4.095522 |
| 20.56135 | 42.44, 26.2 | 8.120 | 131.868800 |

For a deterministic function of c alone, both predictions at each repeated c must be identical. The minimax error is half the pair's spread; the squared-error optimum is its mean. Summed duplicate SSE is **135.964322 K^2**; dividing by all 18 rows gives RMSE lower bound **2.7483765106776117 K**, exactly matching `summary.json`. This is an algebraic lower bound on fitting the listed response codes, **not a validated physical Tc-model error**. Restricting to the 11 positive rows gives corresponding bound **3.5157350453483986 K**. Zero codes are not treated here as established physical Tc=0.

## Positive-only descriptive regression: verified

On the 11 positive Figure 5b rows, independent OLS gave:

- slope **-9.195710093062827 K/angstrom**;
- intercept **220.61609713324535 K**;
- R2 **0.08116827937045645**;
- leave-one-row-out RMSE **6.401722198856325 K**.

Differences from the summary are <1e-9 in all compared quantities. This is a selected positive-only descriptive fit, not a causal strain coefficient or independently validated predictor. The summary's separate zero-coded naive regression was inspected, but was not independently recalculated in this task. Author-onset labeling is inherited from the supplied source analysis; no new author Tc or measured-zero definition is inferred from these calculations.

## Aging half-resistivity crossings: independently verified

Definition used: linearly interpolate rho at 50 K, set target to half that reference, scan adjacent points with lower-point rho <= target and upper-point rho > target below 50 K, and choose the highest ascending-temperature crossing. This is **rho(T)/rho(50 K)=0.5, not author Tc/onset and not measured zero resistance**. Ascending sorting does not identify a physical warming sweep. Each stable-sorted raw curve yielded one upward half-threshold crossing.

| Source Figure 2b label | raw, stable sort (K) | 0.1-K median bins (K) | 0.25-K median bins (K) | 0.5-K median bins (K) |
|---|---:|---:|---:|---:|
| O3-annealed | 22.096395185185216 | 22.101323654683693 | 22.106147104514740 | 22.103919415393650 |
| 8 days | 14.339982340425534 | 14.339949118464666 | 14.349132470575695 | 14.355240054368167 |
| 20 days | 6.173542589821603 | 6.173577488838744 | 6.176403290033493 | 6.178385440287745 |
| O3 annealed again | 18.212049469056474 | 18.209589537910045 | 18.217185796484046 | 18.205119226055757 |

Independent binned half-threshold calculations agree with the archived operational CSV to maximum absolute difference **3.552713678800501e-15 K**. All 48 aging fraction checks (0.9, 0.5, 0.1, 0.01) agree, including missing crossings, with maximum finite difference **7.105427357601002e-15 K**. Largest half-crossing shift from the stable raw result among these bins is **0.015257713942633089 K** (8 days, 0.5-K bins). These tiny arithmetic differences and bin shifts are not experimental uncertainty estimates. Null crossings are unobserved within the available range, not Tc=0.

### Actual raw-data tie caveat

Raw curves contain repeated temperatures: 4,077 excess repeated-T rows for O3-annealed, 23 for 8 days, 49 for 20 days, and 88 for reannealed. A supplemental direct `numpy.interp` check after pandas stable sorting reproduced the independent raw results to floating-point precision. Changing only the sort to quicksort changed O3-annealed to **22.10265333333331 K**; the other three half crossings were unchanged. The difference is due to equal-temperature ordering at the reference: stable rho50 **0.2922420000000006**, quicksort rho50 **0.2923639999999995** mOhm cm. Near 50 K, the workbook contains multiple values at both 49.9996 and 50.0001 K. Stable sorting preserves original tie order but does not remove this reference ambiguity. Accordingly the raw value is convention-specific, not a unique physical observable. Median-binned estimates reproduce reliably here.

## Missing source Figure 1c A11 and code assessment

Direct workbook inspection found **2,421 numeric temperature cells, zero numeric resistivity cells, and zero valid paired rows** for A11. It is absent from the archived operational CSV. No imputation or invented A11 resistivity was used.

The original `analyze_nickelate_data.py` has no empty-curve guard; invoking it directly would fail to make a valid strict-JSON summary when it encounters the missing A11 resistivity column. The existing `run_analysis.py` explicitly skips empty paired curves before processing and simplifies an otherwise dead conditional bin expression. This compatibility runner is therefore required for regeneration. Its hard-coded `rows[-2]` selects the 0.25-K row correctly under the current fixed [.1,.25,.5] order, though it is brittle if that order changes. The summary's phrase 'warming crossing' cannot itself establish measurement sweep direction. These issues and caveats were reported before any change; **neither original analysis file nor the original computed outputs was changed**. Only independent validation code and archive/report files were added.

## Archive and byte verification

Saved all four requested files through the `write_file` tool, not shell writes to the turn folder. A subsequent shell read compared `read_bytes()` of every archived file to its `/tmp/astra5/results` original and asserted exact equality, including final newline. All passed:

| Archived file | bytes | SHA-256 |
|---|---:|---|
| `outputs/summary.json` | 4734 | `f5e78d971d123946c30c507a8a83b23ce4f3e76f1f9ea574122a0e821843d8a1` |
| `outputs/figure5a.csv` | 91 | `53c1c2e21ef26efb8c5998c9a18ed25a4d38442562fe9a898b0fc330f0072884` |
| `outputs/figure5b.csv` | 285 | `6fc0aeed360d938f7234bfab344790e96a6dcc487b30a5cf6bba32df2ceffe5d` |
| `outputs/operational_thresholds.csv` | 11373 | `6d7bf6758936ad23b8743de58fef101cc9519632dc54830f2d62d4b9bf04cb2f` |

Also saved the small independent table `outputs/aging_independent.csv` and reproducible `independent_validation.py`. The independently generated full JSON remains in temporary storage at `/tmp/astra5/validation/independent_checks.json`; its substantive results are recorded above.

## Provenance, sources, and regeneration

[S1] Local publisher source workbook `/tmp/astra5/results/publisher_source.xlsx`, 13,454,360 bytes, SHA-256 `33012becd28a8578bd1342cb67a05c38dc10abffb7e3b86973c5dabb82f9ad6d`. This matches the original summary's source hash and byte count. Publisher regeneration URL (as supplied by the original code):

```
https://media.springernature.com/original/springer-static/esm/art%3A10.1038%2Fs41586-024-08525-3/MediaObjects/41586_2024_8525_MOESM1_ESM.xlsx
```

[S2] Local `figure5a.csv`, `figure5b.csv`, `operational_thresholds.csv`, `summary.json`, independently checked as described above. Figure 5a has five rows and Figure 5b 18 rows. These are numerical source citations, not a fresh publisher-content retrieval.

[S3] Unarchived raw curves `/tmp/astra5/results/extracted_raw_curves.csv`, 2,088,194 bytes, SHA-256 `9ed446484d8e62c8cb56d2bd009f2cc518927c3dd9718d040b689fbe8e4b43d6`. No large workbook or raw curve copy was written into the turn folder.

Analysis code hashes at validation:

- `analyze_nickelate_data.py`: `00c78320be1cddb186c950e7aae36804f82de455ac5667685c66c4c6d3265a1d`.
- `run_analysis.py`: `22b693739b02796d4f611515adbedb4710fe582dad3fdd0fb4c912acff3914a8`.
- `independent_validation.py`: `c97de2a3a9e46b5621ad8a0502dead7026e26a2a58d24c4a1911c4c6cdb37237`.

Regenerate in a writable temporary directory:

```bash
python run_analysis.py --out /tmp/astra5/regenerated
python independent_validation.py --source /tmp/astra5/regenerated --out /tmp/astra5/revalidated
```

The runner downloads the publisher workbook afresh. Verify its hash against S1 before interpreting comparisons. Exact regenerated CSV bytes may depend on library versions; the archived files are byte-exact copies of the supplied originals, not substitutions regenerated with a new environment.

**Conclusion:** requested lower bound and positive-only regression confirmed; aging half thresholds confirmed and insensitive to the tested median bins on a ~0.016-K scale, with a documented raw-reference tie-order ambiguity. No superconducting candidate, new Tc prediction, or quantum job was submitted.
