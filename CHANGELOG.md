# v1.0.0 — Gauge-invariant HNL dipole portal models

FeynRules source, FeynCalc-patched FeynArts models and Python-3-adapted UFO used in the associated HNL dipole-portal studies.

## Contents

- One Majorana HNL with real dipole couplings universal across the three lepton flavours.
- Electroweak-invariant dipole interactions, including their Higgs/Goldstone and non-Abelian gauge contacts.
- Installation and parameter-card instructions, software versions, input conventions and citation metadata.
- Import/inventory checks, source hashes and a reproducible MadGraph photon-Higgs contact check against an independent numerical Dirac trace.

## Validation

The 18-point tree contact test passes in an isolated copy with MadGraph5_aMC 3.5.3. It checks all three neutrino flavours, coefficient interference and scaling, and photon transversality. The nonzero amplitudes reproduce the recorded values in the tested environment.

The model files are those used in the associated analyses. Header edits and Python-compatibility adjustments do not change their physics. This release does not include a Dirac model, a three-independent-HNL flavour model, a loop-counterterm UFO, or a complete fit-reproduction package. The FeynArts pair is intended for FeynCalc's patched FeynArts. Full export regeneration has not been rerun for release packaging.

## References

N. Vignaroli, *New avenues for the neutrino dipole portal exploration at the energy frontier*, JHEP 10 (2025) 125, arXiv:2507.01130.

N. Vignaroli, *Indirect probes of heavy neutral leptons through the dipole portal at FCC-ee*, in preparation.
