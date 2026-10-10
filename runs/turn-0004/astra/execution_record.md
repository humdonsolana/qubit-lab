# Execution and provenance record — 2026-10-10

Working folder: `/workspace/runs/turn-0004/astra`.

1. Messaged Fable at start to divide work: Astra heavy-fermion strain audit plus balanced phase-access gates; Fable independent C0001 CHGNet/literature review and new-heavy-fermion sweep.
2. Spawned one primary-source literature auditor; report: `heavy_fermion_audit.md`. Astra also retrieved the CeRu2 publisher page directly.
3. `python phase_access_gates.py > calculation.log 2>&1` failed before execution because the shell user could not create the log in the working folder. No scientific result came from this attempt.
4. An identical copy ran in `/tmp/qubit_t4_astra/`, producing **five CSVs** and `outputs/summary.json`. ODE/gauge/conservation/root checks passed. stdout was saved to `/tmp/qubit_t4_astra/calculation.log`. Exact summary persisted with the file-write tool.
5. Retrieved Dolui's arXiv2310.07562v2 HTML with requests/BeautifulSoup and the fetch tool. Parsed base64 .res blocks from Appendix XI, not digitized plot values. `extract_dft_gates.py --html /tmp/qubit_t4_astra/dolui.html` ran on an identical temporary-directory copy. Atom counting, common pseudopotentials/PBEsol600eV, formula normalization and grand-potential checks passed.
6. A compact projection of full DFT JSON was created in the execution directory and persisted as `outputs/dft_gate_compact.json`. It retains source, numerical headers, raw-block SHA256, counts, formula units, normalized energies and results. Only repeated metadata/volumes were removed. The extractor regenerates full metadata and five numerical structures.
7. Both persisted JSONs matched their execution-directory counterparts **byte-for-byte**. Both executed script copies also matched repository files exactly.
8. `python verify_saved_results.py` ran read-only in the repository directory and passed. It uses Decimal header parsing for independent normalization/reaction checks and recomputes kinetic/storage thresholds:

```
DFT balanced W: MgIrH-1-Mg2IrH7-Fm-3m -0.2858000000005 eV/reaction
DFT balanced W: MgIrH-1-Mg2IrH7-R-3m -1.0919000000005 eV/reaction
Kinetic gate: 0.9 max rate ratio 0.028860939377390454
Kinetic gate: 0.99 max rate ratio 0.0015512834674030838
All committed-result checks passed; no network or writes required.
```

## Persisted versus regenerated

Committed summary hashes:

- `outputs/summary.json`: `82487e9997fcff20e841f68bf43fab4d6eb8ec3e60f23a733cea260cda691091`
- `outputs/dft_gate_compact.json`: `94113398e457eded8c82d27565b767f16dd2c49ea33f23dc9c38cb9b86216577`

Large CSVs, source HTML, raw .res blocks and full DFT JSON remain in the temporary directory and are **not claimed to be committed**. Scripts regenerate them. No secrets, credentials, personal data or QPU jobs. A subagent-created permission-probe file may remain; it is not scientific evidence.

## Citation limitations

References and assumptions: `source_inputs.json`. Early chat citation markers, including those in the attempted correction, were invalid and are all withdrawn. Verified DOI/arXiv identifiers and retrieved numerical data are authoritative. Hansen's rendered body date differs from its version header; no claim of a newly posted version relies on that date.
