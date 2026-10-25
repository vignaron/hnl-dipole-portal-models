# Usage and provenance

## Scope and tested environment

The model contains one Majorana HNL (PDG 2000), real dipole coefficients universal across three lepton flavours, and the Higgs/Goldstone and non-Abelian interactions implied by the electroweak-invariant operators. It is not a three-HNL flavour-aligned export. See the README for the limited equivalence of diagonal pole observables.

The original working environment used Mathematica 14.0 on macOS ARM, FeynRules 2.3.49, FeynCalc 10.2.1 with patched FeynArts 3.12, and MadGraph5_aMC@NLO 3.5.3. These are provenance statements, not a promise of compatibility with every other version. The FeynRules release metadata version 0.1.0-dev labels this model candidate, not the FeynRules package or the inherited SM version.

## Use the distributed UFO

Copy `ufo/dipole_GI_UFO` into the `models` directory of MadGraph, then enter:

```text
import model dipole_GI_UFO
```

Edit the generated parameter card by block and index:

| Quantity | LHA block | Index | Example |
|---|---|---|---|
| C_B | HNLDIPOLE | 1 | 1.0e-6 GeV^-2 |
| C_W | HNLDIPOLE | 2 | 0.0 GeV^-2 |
| M_N | MASS | 2000 | 200.0 GeV |
| Gamma_N | DECAY | 2000 | choose consistently with the process and couplings |

One TeV^-2 equals 1e-6 GeV^-2. Use block indices to avoid confusion between the dipole `CW` and the weak-angle parameter `cw` in case-insensitive tools. The input width is not automatically a validated prediction; the export was made with AddDecays -> False. Do not use an arbitrary width for a resonant production/decay study.

## FeynRules regeneration

Use a fresh Mathematica kernel without FeynCalc/FeynArts loaded. The source already includes the SM: do not load SM.fr a second time. Adapt only the two paths below to your installation:

```mathematica
frInstallation = "/absolute/path/to/feynrules-current";
releaseDirectory = "/absolute/path/to/hnl-dipole-portal-models";
Get[FileNameJoin[{frInstallation, "FeynRules.m"}]];
LoadModel[FileNameJoin[{releaseDirectory, "feynrules", "BSM_GI_UFO.fr"}]];
FeynmanGauge = False;
lagExpanded = ExpandIndices[LBSM, FlavorExpand -> True];
outputDirectory = FileNameJoin[{releaseDirectory, "generated", "dipole_GI_UFO"}];
If[DirectoryQ[outputDirectory], Print["Choose a new output directory."]; Abort[]];
If[!DirectoryQ[DirectoryName[outputDirectory]],
 CreateDirectory[DirectoryName[outputDirectory], CreateIntermediateDirectories -> True]];
WriteUFO[lagExpanded, FlavorExpand -> True, AddDecays -> False,
 Output -> outputDirectory];
```

This reproduces the export settings used in the original script, with a separate destination to protect the distributed files. It has not been rerun for this release candidate. FeynRules 2.3.49 can produce Python-2-style output; the supplied UFO is the Python-3-adapted snapshot used in the numerical check. A fresh export must be checked for Python compatibility and numerical agreement before replacing it. The author/date/comment-only edit does not require regenerating the existing physics exports.

## FeynArts/FeynCalc snapshot

The `.mod` and `.gen` pair in `feynarts-feyncalc` is the FeynCalc-patched pair actually used for the loop calculation. Copy the pair to the Models directory of the FeynArts installation used by FeynCalc, without overwriting an existing installation without a backup. Load it with model name `dipole_GI_FA` in a fresh FeynCalc session.

This snapshot and the UFO have separately recorded provenance. A byte-identical joint regeneration from the distributed FeynRules source has not been demonstrated. In particular, the generic Lorentz structures and patching must be preserved; a new default FeynArts export is not automatically the same model pair. No loop counterterm model is provided by this package.

## Checks and their limits

From the repository root:

```text
python3 -B validation/check_ufo.py
python3 -B validation/check_release.py
```

The first checks import, the Majorana declaration and the inventory (219 total vertices, 144 containing N). The second checks file hashes and the internal consistency of the recorded numerical benchmark. Neither regenerates matrix elements nor recomputes loop matching.

To recompute the tree contact test with NumPy and MadGraph installed:

```text
python3 -B validation/reproduce_photon_higgs.py --mg5 /absolute/path/to/MG5_aMC
```

This script imports the distributed UFO through MadGraph, generates the matrix element anew, and compares it to an independent numerical Dirac trace and the recorded benchmark. It uses a temporary model copy to avoid modifying the release. The output is written to `generated/photon-higgs-reproduced.json`. It checks 18 points, three neutrino flavours, six coefficient choices, photon transversality, and the spin average. On 25 October 2026 all checks passed with MG5_aMC 3.5.3; the maximum relative difference from the recorded nonzero values was zero in the tested environment. This is a fresh tree-level check of the photon-Higgs contact, not a loop or full-model validation. Do not invoke Python with `-O`, which disables assertions.

`validation/photon-higgs-test.json` records an earlier independent check of nu gamma -> N h at 18 flavour/kinematic points: a Dirac-trace comparison, the photon Ward identity, coefficient interference and scaling. At M_N=200 GeV, sqrt(s)=400 GeV, cos(theta)=-0.6, C_B=1 TeV^-2 and C_W=0, the recorded squared amplitude is 0.0010089498699128049, versus 0.0010089498699128044 from the independent trace. The spin average denominator is 4; this must be accounted for when comparing to a beam with only the physical active-neutrino helicity. This validates the photon-Higgs contact subset, not every vertex or the loop analysis.

## Credits and redistribution status

The dipole extension is by Natascia Vignaroli, Universita' del Salento. The incorporated SM implementation is credited to N. Christensen, C. Duhr and B. Fuks (SM model version 1.4.7). UFO support files retain their individual author notices, including C. Duhr for function_library.py and O. Mattelaer for write_param_card.py. Generated-export metadata may still describe the inherited SM; it is preserved as historical provenance.

The local files inspected do not supply an explicit redistribution licence covering all inherited components. This candidate therefore does not assign a blanket licence to those components. Before public release, clarify their applicable terms and select the licence for original contributions. This is a release-documentation issue, not a change to the physics or validation results.

Official resources: https://feynrules.irmp.ucl.ac.be/ and https://feynrules.irmp.ucl.ac.be/wiki/StandardModel .
