"""Check distributed hashes and recorded results; no new matrix-element run."""
from pathlib import Path
import hashlib, json, math
root = Path(__file__).resolve().parents[1]
manifest = json.loads((root / 'provenance.json').read_text())
for entry in manifest['files']:
    actual = hashlib.sha256((root / entry['file']).read_bytes()).hexdigest()
    if actual != entry['sha256']:
        raise RuntimeError('Hash mismatch: ' + entry['file'])
data = json.loads((root / 'validation/photon-higgs-test.json').read_text())
rows = data['rows']
if len(rows) != 18:
    raise RuntimeError('Unexpected number of recorded points')
for row in rows:
    values = row['m2_B_W_plus_minus_cancel_double']
    for actual, ratio in zip(values, [1, 0.25, 2.25, 0.25, 0, 4]):
        if not math.isclose(actual, ratio * values[0], rel_tol=1e-10, abs_tol=1e-15):
            raise RuntimeError('Recorded coefficient scaling mismatch')
    if not math.isclose(values[0], row['independent_Dirac_trace_m2_CB_only'], rel_tol=1e-10, abs_tol=1e-15):
        raise RuntimeError('Recorded trace mismatch')
    if abs(row['ward_m2']) > 1e-15:
        raise RuntimeError('Recorded Ward mismatch')
    if row['spin_average_denominator'] != 4:
        raise RuntimeError('Unexpected spin averaging')
if {r['nu_pdg'] for r in rows} != {12, 14, 16}:
    raise RuntimeError('Unexpected flavours')
print(json.dumps({'file_hashes_checked': len(manifest['files']), 'recorded_points_checked': len(rows), 'status': 'PASS; no new matrix-element or loop calculation'}, indent=2))
