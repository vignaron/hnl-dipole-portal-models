# Gauge-invariant HNL dipole portal models

FeynRules, FeynArts and UFO implementations of the gauge-invariant HNL dipole portal, prepared for version 1.0.0. Repository: https://github.com/vignaron/hnl-dipole-portal-models.

## Physics and conventions

One Majorana HNL couples universally to the three SM lepton flavours through

`Ldip = g' CB (Lbar sigma^{mu nu} N_R) Htilde B_{mu nu} + g CW (Lbar sigma^{mu nu} tau^I N_R) Htilde W^I_{mu nu} + h.c.`,

with `tau^I = sigma^I/2`. CB and CW have units GeV^-2 in the exported model. The Higgs, Goldstone and non-Abelian contact interactions are included. The photon coupling is `d_gamma = e v (CB + CW/2)/sqrt(2)`.

This model is NOT an export of three independent flavour-aligned HNLs. At quadratic order, its universal diagonal pole response agrees with that benchmark when the flavour trace is treated consistently. Off-diagonal flavour amplitudes and general collider observables do not inherit that equivalence. No Dirac UFO is included.

## Files

- `feynrules/`: source used for the GI UFO export.
- `feynarts-feyncalc/`: exact FeynCalc-patched `.mod`/`.gen` used for loop work. These are not advertised as unpatched standalone FeynArts files.
- `ufo/dipole_GI_UFO/`: Python-3-adapted UFO used in the MadGraph validation.
- `validation/`: recorded check and a portable import/inventory check.
- `provenance.json`: hashes and origin roles of copied files.
- `docs/RELEASE-CHECKLIST.md`: release checks and scope.
- `CHANGELOG.md`: version notes.

See [Usage and provenance](docs/USAGE-AND-PROVENANCE.md) for parameter cards, regeneration settings, software versions and validation limits.

## Quick checks

From this repository directory run `python3 validation/check_ufo.py`. This tests import, the Majorana HNL declaration and vertex inventory; it is not a loop-matching check.

For MadGraph5_aMC@NLO 3.5.3, copy `ufo/dipole_GI_UFO` into its `models` directory and use `import model dipole_GI_UFO`. Set dipoles through LHA block `HNLDIPOLE`, entries 1 and 2, because the name CW may collide with the weak-angle parameter. Units are GeV^-2, so 1 TeV^-2 = 1e-6 GeV^-2.

For FeynCalc/FeynArts, copy the model pair into the FeynArts `Models` directory, keeping a backup of any existing files. Use a fresh Mathematica kernel with FeynCalc 10.2.1 and its patched FeynArts 3.12. The gauge-parameter and matching checks belong to the associated analysis; importing the model alone does not reproduce the fit.

## Provenance and credit

The dipole-portal extension was implemented by Natascia Vignaroli using FeynRules.

The current manuscript is *Indirect probes of heavy neutral leptons through the dipole portal at FCC-ee* (in preparation). The direct-search theory is discussed in N. Vignaroli, *New avenues for the neutrino dipole portal exploration at the energy frontier*, JHEP 10 (2025) 125, arXiv:2507.01130. These models were used in the analyses presented in the associated publications.

## Validation scope

The reproducible MadGraph test (`validation/reproduce_photon_higgs.py`) checks nu gamma -> N h against an independent numerical Dirac trace at 18 kinematic/flavour points, including photon transversality and CB/CW interference. It does not certify every exported vertex, a full FeynArts/UFO comparison or loop counterterms. No new validation result is inferred from packaging.

Software citations: FeynRules 2.0, [arXiv:1310.1921](https://arxiv.org/abs/1310.1921); FeynArts, [hep-ph/0012260](https://arxiv.org/abs/hep-ph/0012260); FeynCalc, [arXiv:2312.14089](https://arxiv.org/abs/2312.14089); UFO, [arXiv:1108.2040](https://arxiv.org/abs/1108.2040); MadGraph5_aMC@NLO, [arXiv:1405.0301](https://arxiv.org/abs/1405.0301).

## Licence

The original contributions are provided under the MIT licence; see [LICENSE](LICENSE) for its scope. Notices in third-party support files are retained.

## Archived release

Version 1.0.0 is archived on Zenodo: [doi:10.5281/zenodo.23667622](https://doi.org/10.5281/zenodo.23667622). Please cite the archived model release and the associated physics publication.

## FeynCalc symbol conventions

In the analysis scripts, the weak dipole coefficient is named `CWDip` before `FCFAConvert`: a symbol named `CW` may otherwise be interpreted as the cosine of the weak mixing angle. This internal script name does not change the coefficient normalization or the UFO parameter-card entries described above.
