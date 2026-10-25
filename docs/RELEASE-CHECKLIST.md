# Version 1.0.0 checks and scope

Completed:

- Source author, affiliation, date and model version updated; executable physics definitions unchanged.
- FeynRules source, FeynCalc-patched FeynArts pair and Python-3-adapted UFO included.
- File hashes verified against provenance.json.
- UFO import verified: one Majorana HNL, 219 vertices in total, 144 containing the HNL.
- Photon-Higgs contact amplitudes regenerated with MadGraph5_aMC 3.5.3 from an isolated copy: all 18 flavour/kinematic points agree with the recorded benchmark and independent Dirac trace; photon Ward and coefficient-interference checks pass.
- Personal absolute paths removed from distributed records.
- Usage instructions, input conventions and software citations included.

Scope:

- Numerical validation covers the photon-Higgs contact subset. It is not a new calculation of loop matching, a test of every vertex, or a general cross-generator validation.
- The model is one Majorana HNL with universal lepton couplings, not three independent flavour-aligned HNLs or a Dirac HNL.
- FeynArts files are the FeynCalc-patched pair used in the analysis.
- Regeneration settings are documented; full regeneration of both exports has not been repeated for this release. Distributed exports are the working snapshots, with metadata or Python-compatibility changes described in the documentation.

Publication sequence: finalize the licence for original contributions, make the repository public, tag the verified commit as v1.0.0, archive the release with Zenodo, and add the DOI to the citation metadata and manuscript. No DOI is implied before an actual archive record exists.
