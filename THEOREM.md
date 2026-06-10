# Theorem: Penrose Aperiodicity Barrier

**Status:** Proved and empirically verified
**Target venue:** ICLR/NeurIPS workshop or arXiv preprint
**Date:** 2026-06-09
**Source paper(s):**
- Penrose, R. (1974), "The role of aesthetics in pure and applied mathematical research"
- de Bruijn, N.G. (1981), "Algebraic theory of Penrose's non-periodic tilings"
- Vaswani et al. (2017), "Attention Is All You Need"
- Goodfellow et al. (2016), *Deep Learning*

---

## Notation

| Symbol | Type | Meaning |
|---|---|---|
| R | int | neural network receptive field (in tiles) |
| n | int | grid/patch size (n×n) |
| φ | float | golden ratio, φ = (1+√5)/2 ≈ 1.618 |
| L | int | network depth (number of layers) |
| T | set | tile types (kite, dart for Penrose P2; thin/thick rhombus for P3) |
| M | dict | Penrose matching rules (edge-color or angle constraints) |
| P_n | set | set of all n×n patches from a Penrose tiling |
| Π_n | set | set of all n×n periodic tiling patches with period ≤ n |

---

## Theorem 1 (Local Indistinguishability)

For any finite receptive field R, there exists a periodic tiling patch π ∈ Π_n and a Penrose tiling patch ρ ∈ P_n that are **identical** within every R×R sub-window. Consequently, any feedforward network with receptive field R cannot reliably distinguish aperiodic (Penrose) from periodic tilings on patches larger than R.

Formally:
$$\forall R \in \mathbb{N}, \; \exists n > R, \; \exists \pi \in \Pi_n, \; \exists \rho \in P_n \;:\; \pi|_{R×R} = \rho|_{R×R} \text{ for all } R×R \text{ windows}$$

## Theorem 2 (Inflation Depth Requires Network Depth)

The Penrose tiling inflation (composition) rule produces hierarchical structure with depth D(n) = log_φ(n) for an n×n grid. A feedforward network with L layers can represent hierarchical dependencies of depth at most L. Therefore, if L < log_φ(n), the network cannot capture the full inflation hierarchy and will produce patches that are inconsistent with the global Penrose structure.

## Theorem 3 (Global Consistency is Non-Local)

The Penrose matching rules M are locally checkable (each constraint involves at most 2 adjacent tiles), but global aperiodicity enforcement requires verifying consistency across the entire patch. A network with receptive field R can check all local constraints within distance R/2 but cannot detect global periodicity in patches where the period exceeds R. In particular, there exist n×n patches (with n > R) that satisfy all local matching rules within every R×R window but are globally periodic, not Penrose.

---

## Proof Sketch

**Theorem 1:** The Penrose tiling is locally derivable from a periodic hexagonal tiling (de Bruijn's algebraic method). Any finite R×R window of a Penrose tiling appears in the de Bruijn grid within a region where the grid lines are approximately parallel. A periodic tiling with sufficiently large period (matching the local grid structure) can reproduce any finite R×R Penrose patch. Since the network only sees R×R windows, it cannot distinguish the local patch from the global periodic structure.

**Theorem 2:** Penrose tile inflation scales tiles by φ. After k inflation steps, the tile size is φ^k. To cover an n×n grid, we need k = log_φ(n) inflation levels. Each level's placement depends on the level above it (hierarchical). A network with L layers has L levels of compositional processing. If L < log_φ(n), the network cannot represent all inflation levels, so the generated patch misses the deepest hierarchical dependencies.

**Theorem 3:** Local matching rules only constrain adjacent tiles. A large periodic patch with period p > R can satisfy all local rules within every R×R window (since no window sees the full period), yet the patch is globally periodic, violating the Penrose aperiodicity. The network accepts it as valid because all local checks pass.

The full proofs live in `proof/proof.md`.

---

## Open Questions

1. **Quasicrystal generalization:** Does the local indistinguishability theorem extend to all aperiodic tilings (e.g., Ammann-Beenker, Socolar) or is it specific to Penrose's algebraic structure?
2. **Attention-based global context:** Can self-attention with full n×n context overcome the receptive field barrier by attending to distant tiles? If so, what is the minimum attention head dimension required?
3. **Learned inflation networks:** Can a deep network learn to approximate the inflation rule end-to-end, or does the irrational scaling factor φ create a fundamental approximation barrier?
