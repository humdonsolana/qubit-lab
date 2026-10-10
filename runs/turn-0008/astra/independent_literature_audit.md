# Independent literature audit: pressure-quenched Hg1223, 151 K

**Cutoff/retrieval: October 10, 2026.** Folder: `/workspace/runs/turn-0008/astra`. Scope: independent reproduction of PNAS **10.1073/pnas.2536178123**, the FeSe antecedent, and alleged 2022–2023 Bi2212/Hg1223 PQ reports. This is not a same-paper measurement extraction. No candidate submission or QPU job.

## Conclusions

- **No qualifying independent experimental reproduction was found through the cutoff.** This is a bounded literature-search outcome, not proof of universal absence. The forward citations inspected are news, reviews/perspectives, theory, or experiments on other materials.
- **FeSe PQ is a genuine 2021 PNAS experimental paper**, DOI **10.1073/pnas.2108938118**, reporting retained ambient-pressure onset Tc up to **37 K**. It is a same-research-network antecedent, not an independent Hg1223 replication. [2]
- **Earlier public cuprate PQ disclosure does exist:** a primary 2023 plenary slide deck labels **Hg1223 (2022)** and **Bi2212 (2017)**. It is preliminary same-network presentation evidence; no corresponding stand-alone 2022–2023 experimental journal report was identified. [3]
- **Do not count press reprints as reproduction.** The target paper's first-online date is **March 9, 2026**, issue date **March 17, 2026**; arXiv **2603.12437** was submitted **March 12, 2026**. May/April/August coverage does not establish a new experiment. [1]

## Operational definition

A qualifying independent reproduction must report new Hg1223 samples and a separately executed PQ experiment, with superconductivity measured after decompression at ambient pressure near 151 K. A citation, calculation, outside institution's web page, conference abstract, or successful PQ of a different material is insufficient. Argonne/Intellectual Ventures participation in the original collaboration is not a second replication. Independence and experimental reproduction are separate tests.

## What was searched versus what was found

### General discovery searches

Queries actually used included:

```text
"10.1073/pnas.2536178123" reproduction
"2536178123" "reproduced"
"Hg1223" replication 2026 pressure quenched
"Hg1223" "pressure-quench" "independent"
"Hg1223" "replication" "September" "2026"
Chu 2023 pressure quench Bi2212 Hg1223 IEEE presentation pdf
"Bi2212" "Hg1223" "PQ"
"Hg1223" "pressure quench" "2022"
"Bi2212" "pressure quench" "2017"
"Bi2212" "pressure-quench"
"The Retention" "Bi2212"
"Hg1223" "pressure quench" "2025" APS
site:uh.edu "University of Houston Physicists Break" "2026"
site:anl.gov "151 K" "2026"
"Kazibwe" "Mapping the Superconducting"
"Lamar" "EXPO 2026" "Abstracts"
```

**Found:** original Hg paper and duplicate arXiv entry, original FeSe paper, 2023 primary slides, two real 2022 review records, a 2025 APS 149 K abstract, 2026 theory/other-material papers, a same-network high-pressure conference abstract, and institutional/news coverage. **Not found:** a qualifying independent 151 K Hg1223 PQ experiment or a stand-alone 2022–2023 cuprate-PQ experimental journal article. Search-result prediction registries, commercial claims, blogs, and social discussions were not used as scientific evidence.

### Structured index checks

Europe PMC core-record searches, page size 100:

```text
DOI:10.1073/pnas.2536178123

(Hg1223 OR "Hg-1223" OR "HgBa2Ca2Cu3O8")
AND (quench OR quenched OR replication OR reproduction)
AND FIRST_PDATE:[2026-01-01 TO 2026-10-10]

("pressure quench" OR "pressure-quench" OR "pressure quenching")
AND (Bi2212 OR "Bi-2212" OR Hg1223 OR "Hg-1223")
AND FIRST_PDATE:[2022-01-01 TO 2023-12-31]
```

Observed: DOI lookup **1 hit**; 2026 Hg search **5 hits**; 2022–2023 Bi/Hg search **0 hits**. The five were the target paper, PNAS *In This Issue*, *Metallic Oxides and the Overlooked Role of Bandwidth* (**10.1021/acs.chemmater.5c02578**), Li–Mg hydride theory below, and PNAS programmatic perspective **10.1073/pnas.2520324123**. Zero indexed antecedent hits did not prove nonexistence: the slides were found separately.

Europe PMC forward-citation endpoint for PMID **41802058** returned **3** records. OpenAlex work **W7134283102**, filtered to dates on/before October 10, returned **8**. The three Europe PMC records were all in the OpenAlex set. These are index snapshots, not eight confirmations. OpenAlex's FeSe work **W3167352516** returned **54** forward records, scanned for antecedent leads—not exhaustively assessed for FeSe reproduction.

### Forward-citation exclusion ledger

Classification uses original publisher/author abstracts or publisher-deposited metadata. News is admitted only for its publication type/provenance, not experimental claims.

| Record | DOI | Why not Hg1223 PQ reproduction |
|---|---|---|
| *Room-Pressure Superconductor Breaks Temperature Record* | 10.1103/physics.19.37 | APS **Research News**, March 13, 2026; covers the original experiment. |
| *Physics news on the Internet: April 2026* | 10.3367/ufnr.2026.03.040117 | News compilation, not original experimental research. |
| *Leveraging mechanical frustration in the flatland…* | 10.1063/5.0338010 | June 10 perspective proposing a strain platform; abstract explicitly does not claim achieved superconductivity in the proposed systems. |
| *High-temperature superconductivity and exotic physics in nickelate systems* | 10.1016/j.physrep.2026.06.003 | Nickelate review. Date caveat: OpenAlex gives July 4; Crossref supplies October issue dating without an exact day. |
| *Compression behaviour of ErH3 synthesized at non ambient conditions* | 10.1088/1361-648x/ae8fac | Er-hydride synthesis/XRD/Raman experiment; different material and measurements. Europe PMC first-publication date August 6. |
| *Superconductivity at 31 K in a Stage-1 Sodium-Intercalated Graphite* | 10.1021/jacs.6c10866 | August 1 Na-intercalated graphite experiment, not Hg1223. |
| *Designing Ambient Pressure Superconductivity in Li–Mg-Based Hydrides…* | 10.3390/ma19163465 | August 16 computational hydride predictions; no Hg1223 experiment. |
| *Superconductivity in Ruddlesden–Popper nickelates: a review…* | 10.1088/1361-6633/ae9aae | Nickelate review; publisher-deposited online date September 9. |

**Newest directly checked relevant primary research:** *Microscopic mechanism of high-temperature superconductivity revealed by ab initio studies on hole-doped multilayer cuprates HgBa2Ca2Cu3O8 under pressure*, **10.1103/qqvw-ltth**, PR Research **8, 043024**, published **October 8, 2026**; author preprint **arXiv:2606.08181**. The publication date was confirmed in APS-deposited Crossref metadata. The authors' abstract describes first-principles/variational calculations, not pressure-quench experiments. [4]

A Lamar-hosted EXPO 2026 abstract is also **not an outside-lab replication**: presenter **Sudaice Kazibwe**, mentor **Liangzi Deng**, coauthors **Habamahoro/Davis/Chu**, affiliation **UH/TcSUH**. Its topic is the high-pressure cuprate phase diagram, not retained ambient-pressure 151 K PQ. Hosting institution and experimental provenance must not be conflated. [5]

## FeSe antecedent

Deng et al., PNAS **118, e2108938118**, **10.1073/pnas.2108938118**, first online **July 7, 2021**, issue **July 13, 2021**; author preprint **arXiv:2104.05662**, April 12, 2021. Original experimental paper, not merely a press release. [2]

It reports retained ambient-pressure **onset Tc up to 37 K**, quenching from **4.15 GPa at 4.2 K**, and **26.5 K** in Cu-doped FeSe from **6.32 GPa at 4.2 K**. Its detailed text distinguishes high-Tc-phase retention to roughly **200 K** from retention of some other phases to **300 K**. The broad abstract's “some phases” surviving 300 K is not evidence that the 37 K superconducting state tolerates room-temperature storage. These are the originating authors' measurements, not independent later Hg1223 validation. [2]

## What really exists for prior Bi2212/Hg1223 PQ?

### A genuine 2023 primary presentation

Deng/Chu-network CEC–ICMC plenary, **Honolulu, July 11, 2023**, posted in **IEEE-CSC/ESAS/CSSJ Superconductivity News Forum, October 2023**. I inspected extracted text and the **screenshot of PDF page 51 (zero-based 50)**. The plot labels **Hg1223 (2022)** and **Bi2212 (2017)**. Hg connects a high-pressure point near 150 K to an ambient-pressure point near 140 K and a higher question-marked point. The Bi trace is approximately 95 K. These are preliminary disclosure claims, not independent or peer-reviewed validation. The parenthetical years are not established publication dates. [3]

### Two actual 2022 reviews—not the missing experimental papers

Publisher pages directly verified:

- Chu, Deng, Wu, *The Retention and Study of High-Pressure-Induced Phases in High- and Room-Temperature Superconductors*, JSNM **35, 987–995**, **10.1007/s10948-021-06117-0**, published **January 20, 2022**.
- Chu, Deng, Wu, *The Retention of High-Pressure-Induced High-Tc Superconductivity at Ambient Pressure*, JSNM **35, 1733–1741**, **10.1007/s10948-022-06162-3**, published **February 28, 2022**.

Both publisher records explicitly classify them as **reviews**. Accessible abstracts identify successful PQ of **Sb, FeSe, Cu-doped FeSe**; the second describes adaptation to cuprates as a possibility. They verify bibliographic existence, not a separate experimental cuprate-PQ report. Subscription-gated full texts were not read; absence from their abstracts/reference lists is not proof of absence anywhere in the full articles. [6, 7]

A **2024 proceedings article**, **10.1088/1757-899X/1302/1/012010**, appeared in the FeSe citation graph. Attempted PDF endpoints returned HTML/403, so it remains an unresolved full-text lead, not evidence for or against a 2022–2023 journal report.

### A real later precursor: March 2025 APS abstract

The APS archive verifies **“A New Record Tc of 149 K in HBCCO at Ambient without Pressure by PQP,” March 19, 2025, 1:54–2:06 PM**, presenter **Ching-Wu Chu**, with UH and Intellectual Ventures coauthors. This is important prior public disclosure of an elevated ambient-pressure PQ claim, but **149 K, not 151 K**, and the original network, not independent reproduction. The abstract's publication list cites FeSe 2021 and IEEE HP144, not a separate Hg1223 journal article. [8]

### Conflations to avoid

The genuine Bi2201/Bi2212 PNAS paper **10.1073/pnas.1819512116** (2019; author manuscript **arXiv:1901.10404**) concerns high-pressure Tc resurgence, not the retained ambient-pressure PQ experiment needed here. **arXiv:2312.16402** (2023) concerns computational Hg1223 pressure-dome behavior, not PQ reproduction. [9, 10]

## Press, republication, and duplicate records

- **UH, March 10, 2026:** *University of Houston Physicists Break Superconductivity Temperature Record*. Original institutional announcement of the same paper—not a second experimental report. [11]
- **HPCAT, April 10, 2026:** institutional highlight explicitly identifies UH/Argonne collaboration and links the same experimental DOI. No independent reproduction. [12]
- **ScienceDaily, May 27, 2026:** its own provenance field declares **University of Houston-supplied material**, potentially edited for style/length. This is republication provenance, not scientific evidence. Its journal-reference field points to **10.1073/pnas.2520324123**, the companion perspective; that is not the experimental Hg DOI. [P1]
- **APS Physics, March 13, 2026:** explicitly **Research News** about the original experiment. Not reproduction. [P2]
- arXiv **2603.12437**, PNAS, PubMed and PMC represent **one underlying Hg paper**.
- Companion PNAS **10.1073/pnas.2520324123**, *The path to room-temperature superconductivity: A programmatic approach*, shares originating-network authors and is a perspective, not independent Hg1223 PQ validation. [13]

Secondary coverage is not relied on for scientific findings. A reprint site's self-declared source is used only as primary evidence of its own republication provenance.

## Confidence / limitations

**High confidence:** identities and dates of the Hg/FeSe papers; duplicate arXiv identity; 2023 deck labels and provenance; real 2025 APS abstract; exclusion of identified theory/news/other-material items. **Moderate-to-high confidence:** no publicly discoverable qualifying independent reproduction through October 10, 2026. **Moderate confidence:** no stand-alone 2022–2023 experimental cuprate-PQ journal paper located; paywalls and proceedings/index coverage limit the negative inference.

No direct Google Scholar/Scopus/Web of Science audit. Europe PMC is incomplete for condensed matter; index dates need not be first-online dates. Some browser fetches were challenged; FeSe full text was independently retrieved using requests. The 2024 proceedings full text remains inaccessible. Search snippets were not treated as full experimental verification. Failure to locate reproduction does not establish refutation or misconduct.

**Suggested lead wording:** “No independent experimental reproduction of the 151 K Hg1223 PQ result was located through October 10, 2026. Same-network antecedents include FeSe PNAS 2021, public cuprate-PQ slides in 2023, and a 149 K APS abstract in 2025; no corresponding stand-alone 2022–2023 cuprate-PQ experimental journal paper was identified.”

## Primary sources and locators

[1] Deng et al., **10.1073/pnas.2536178123**, PMCID **PMC12993975**; arXiv **2603.12437**. citeturn0search0turn0search1

[2] Deng et al., **10.1073/pnas.2108938118**, PMCID **PMC8285973**; author-hosted published copy. citeturn5search14turn5search1

[3] Original 2023 plenary slide deck, page 51; title/date on page 1. citeturn1view0turn2view6

[4] Authors' manuscript **arXiv:2606.08181**; publication metadata **10.1103/qqvw-ltth**. citeturn1view3

[5] Original EXPO 2026 author abstract, PDF page 13, Lamar-hosted. citeturn6search12

[6] Original publisher record **10.1007/s10948-021-06117-0**; used only for its own metadata/abstract. citeturn2view2

[7] Original publisher record **10.1007/s10948-022-06162-3**; same restriction. citeturn2view3

[8] Original APS meeting abstract, March 19, 2025. citeturn6view0

[9] Original authors' manuscript **arXiv:1901.10404**, linked to **10.1073/pnas.1819512116**. citeturn2view1

[10] Original authors' manuscript **arXiv:2312.16402**. citeturn1view6

[11] UH institutional announcement; provenance only. citeturn5view0

[12] HPCAT institutional announcement; provenance only. citeturn1view4

[13] Authors' PNAS perspective **10.1073/pnas.2520324123**, PMCID **PMC12994211**; inspected directly using requests.

[P1] ScienceDaily identifier **260527023220**; solely its own source/date/republication declaration. citeturn2view4

[P2] APS Research News **10.1103/physics.19.37**; article type/provenance only. citeturn3search6

```text
Primary deck:
https://snf.ieeecsc.org/files/ieeecsc/slides/Chu%20presentation.pdf
2025 APS abstract:
https://meetings-archive.aps.org/smt/2025/mar-m23/13/
FeSe author copy:
https://pdai.phys.rice.edu/pdffiles/e2108938118.pdf
Lamar original abstract booklet:
https://www.lamar.edu/undergraduate-research/_files/documents/2026-2027/book-of-abstracts-pt-1-expo-26.pdf
Structured discovery:
https://www.ebi.ac.uk/europepmc/webservices/rest/search
https://www.ebi.ac.uk/europepmc/webservices/rest/MED/41802058/citations
https://api.openalex.org/works
Publication-date verification:
https://api.crossref.org/works/10.1103/qqvw-ltth
```

## Artifacts

- `independent_literature_audit.md` — requested report, saved via write_file.
- `audit_literature_metadata.py` — rerunnable index/Crossref helper; emits JSON to stdout.
- `audit_literature_metadata_summary.json` — manually persisted observed counts/identifiers, not raw responses.

Initial run_shell attempt to persist raw JSON failed with PermissionError. Helper was revised to emit stdout; summary and report were saved with write_file. No failed raw archive is claimed as a successful artifact.
