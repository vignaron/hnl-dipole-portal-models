from pathlib import Path
import sys, json
root = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(root / 'ufo'))
import dipole_GI_UFO as model
hnl = [p for p in model.all_particles if abs(p.pdg_code) == 2000]
assert len(hnl) == 1, hnl
assert hnl[0].name == hnl[0].antiname, 'HNL must be Majorana'
vertices = [v for v in model.all_vertices if any(abs(p.pdg_code) == 2000 for p in v.particles)]
assert len(model.all_vertices) == 219 and len(vertices) == 144
assert any(any(p.pdg_code == 25 for p in v.particles) for v in vertices)
print(json.dumps({'import': 'passed', 'vertices': len(model.all_vertices), 'HNL_vertices': len(vertices), 'Majorana_HNL': hnl[0].name, 'scope': 'Import/inventory only; no new matrix-element or loop test'}, indent=2))
