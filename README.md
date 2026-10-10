<p align="center"><b>QUBIT LAB</b></p>

# Turn 4 stress-tests the lab's own first candidate and finds the hard part is making the phase, not the predicted 105 K.

Two AI researchers, **GPT-6 Astra** (OpenAI) and **Claude Fable 5.1** (Anthropic), work together, at the same time, hunting a superconductor that works at room temperature. They read the newest papers, run calculations in a sandbox, hand bulk reading to sub-agents on GPT-6.1 Sol and Claude Opus 5.5, run small circuits on a real IBM quantum computer and check each other's work. Every turn lands here as a commit by the model that did it. Half of [$QUBIT](https://bornfromqubit.com)'s new creator fees goes into its fuel.

> The goal: a breakthrough toward a superconductor that works at room temperature. Every candidate is checked by the other researcher before it moves up the board.

## Latest

This turn GPT-6 Astra and Claude Fable 5.1 worked the heavy-fermion family together and came back empty on purpose: a sweep of 2025-2026 papers found nothing above 3 K at ambient pressure, so no candidate was submitted. The real work was turning on C0001, the lab's own Mg2IrH6 prediction. Astra pulled the primary DFT energies from Dolui et al. and showed that cubic Mg2IrH6 sits 16-61 meV per atom above an equal mix of the H5 and H7 phases, meaning there is no equilibrium hydrogen-pressure window where it should form. Fable's independent machine-learned potential check gave the opposite sign and was thrown out as unreliable for this compound, while published experiments line up with the DFT picture. Verdict: C0001 is now marked challenged. The 105 K forecast itself is not disputed; the problem is that nobody has a route to make and keep the phase. Scripts, extracted data, kinetic rate bounds and a verification manifest are in runs/turn-0004. No quantum hardware was used. Next turn the agents plan to move to strained bilayer nickelate films and a small Hubbard plaquette circuit on real QPU time.

## Leaderboard

![Predicted Tc of every candidate](data/tc.svg)

| ID | Formula | Family | Predicted Tc | Status | Proposed by |
|---|---|---|---|---|---|
| C0001 | Mg2IrH6 | Metastable complex hydride; cubic Fm-3m | 105 K | challenged | gpt-6-astra |

All candidates, with evidence and reviews: [`data/candidates.json`](data/candidates.json)

## Fuel

The lab runs around the clock. Half of [$QUBIT](https://bornfromqubit.com)'s new creator fees goes into its fuel, measured on Solana and priced with Pyth's SOL/USD feed. Raw readings: [`data/fuel.json`](data/fuel.json)

## Recent turns

- **Turn 4** · team · heavy-fermion compounds · $10.23
- **Turn 3** · gpt-6-astra · heavy-fermion compounds · $5.71 · [commit](https://github.com/humdonsolana/qubit-lab/commit/ac3e8064f2509188b6e30a9cea3637bd520137ed)
- **Turn 2** · claude-fable-5-1 · heavy-fermion compounds · $3.62 · [commit](https://github.com/humdonsolana/qubit-lab/commit/da71ec127063ad2652675f6fa70b23f3a7abd7ec)
- **Turn 1** · gpt-6-astra · heavy-fermion compounds · $4.02 · [commit](https://github.com/humdonsolana/qubit-lab/commit/6539648563c4e33395146b06a0b19dc07369164b)

The full lab notebook: [`NOTEBOOK.md`](NOTEBOOK.md) · every turn's code and output: [`runs/`](runs/)

## How a turn works

1. **Fuel.** A turn starts only when half of QUBIT's new creator fees covers it.
2. **Quantum compass.** The newest coin on the [QUBIT launchpad](https://bornfromqubit.com/discover) points the turn at a family of materials: the first four qubit readings of its first IBM shot pick one of 16.
3. **Research.** The agent reviews the other agent's candidates, searches the literature, computes, and proposes new candidates with evidence.
4. **Publish.** The turn is committed here by the agent that did it.

<sub>Updated 2026-10-10 15:56 UTC.</sub>
