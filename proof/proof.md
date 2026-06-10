# Proof: Penrose Aperiodicity Barrier

## Lemma 1 (Penrose Local Derivation)

Every finite R×R patch of a Penrose tiling is locally derivable from a periodic hexagonal grid (de Bruijn's algebraic construction). Specifically, the Penrose tiling corresponds to a pentagrid (5 families of parallel lines in the plane with irrational slopes), and any finite region of the pentagrid is approximated by a periodic grid with period q, where q is a rational approximant to the golden ratio φ.

**Proof sketch.** De Bruijn (1981) showed that Penrose tilings are the dual of pentagrids — sets of 5 families of parallel lines with slopes related to the 5th roots of unity and spacings determined by the golden ratio φ. For any finite region of size R, the irrational spacings can be approximated by rational spacings p/q with |φ − p/q| < 1/q². Choosing q > R² ensures the rational approximant matches the irrational grid exactly within the R×R window. The periodic approximant has period q, producing a periodic tiling that is indistinguishable from the Penrose patch within the window. ∎

---

## Proof of Theorem 1 (Local Indistinguishability)

Let R be any finite receptive field. By Lemma 1, any R×R Penrose patch P has a periodic approximant T with period q > R such that P|_R = T|_R (identical within the window).

A feedforward network with receptive field R processes the patch by applying the same computation to every R×R window (with shared weights). Since every R×R window of P is identical to some R×R window of T, the network produces identical outputs on both patches. Therefore, the network cannot classify P as "aperiodic" and T as "periodic" based solely on local processing — it would need to see the global period q > R.

Formally: let f_R be the network function with receptive field R. For any position u:
$$f_R(P, u) = f_R(T, u)$$
because P[u − R/2 : u + R/2] = T[u − R/2 : u + R/2]. Since the network's output at every position is identical, the global classification (aperiodic vs. periodic) must also be identical if the network uses only local aggregation (e.g., max-pooling or average-pooling over positions). ∎

---

## Lemma 2 (Inflation Hierarchy Depth)

The Penrose inflation (composition) rule replaces each tile with a scaled arrangement of smaller tiles, with scaling factor φ. After k inflation steps starting from a single tile, the covered region has size Θ(φ^k).

**Proof.** Each inflation step multiplies tile dimensions by φ. After k steps, the linear dimension is φ^k times the original. The area scales as φ^{2k}. To cover an n×n region, we need φ^k ≈ n, giving k = log_φ(n). ∎

---

## Proof of Theorem 2 (Inflation Depth Requires Network Depth)

Consider a network that generates n×n Penrose patches by hierarchical composition, where each layer corresponds to one inflation level. Layer l produces tile arrangements at scale φ^l by composing outputs from layer l−1 at scale φ^{l−1}.

By Lemma 2, covering an n×n grid requires k = log_φ(n) inflation levels. If the network has L layers and L < k, then the deepest inflation level is never represented. The generated patch only captures hierarchical structure up to depth L, missing the dependencies between tiles separated by more than φ^L positions.

For concreteness: with n = 100 and φ ≈ 1.618, k = log_φ(100) ≈ 9.0. A 5-layer network (L = 5 < 9) cannot represent the full inflation hierarchy for a 100×100 patch. The deepest hierarchical dependencies (tiles whose placement depends on the 9th inflation level) are missing, so the generated patch will violate Penrose matching rules at scales larger than φ^5 ≈ 11.1 tiles.

∎

---

## Proof of Theorem 3 (Global Consistency is Non-Local)

The Penrose matching rules M constrain adjacent tiles (local, distance-1). A network with receptive field R > 2 can verify all matching rules within its window — it sees both tiles in every adjacent pair.

However, aperiodicity is a global property: no translation symmetry exists. To verify aperiodicity, one must check that no non-zero translation vector maps the tiling to itself. This requires comparing the tiling at positions separated by the candidate period p.

For a network with receptive field R, the maximum distance it can compare is R (the full window diagonal). If the period p > R, the network cannot see both a position and its period-shifted counterpart simultaneously. Therefore, any periodic tiling with period p > R will pass all local checks within every R×R window but be globally periodic.

**Construction:** Take a periodic tiling with period p = R + 1. Within any R×R window, the tiling appears aperiodic (no period is visible). All local Penrose matching rules can be satisfied by appropriate tile choice. The network with receptive field R accepts every window as valid. But globally, the tiling is periodic with period R+1, not a Penrose tiling.

∎
