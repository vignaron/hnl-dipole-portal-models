"""Recompute nu gamma -> N h with the supplied UFO and an independent Dirac trace. Requires NumPy and MadGraph5_aMC; not loop validation. Do not run with python -O."""
from pathlib import Path
import sys,json,math,copy
import numpy as np
import argparse, tempfile, shutil, hashlib
parser=argparse.ArgumentParser(description=__doc__)
parser.add_argument('--mg5', required=True, type=Path, help='MadGraph5_aMC installation directory (tested: 3.5.3)')
parser.add_argument('--output', type=Path, default=None)
args=parser.parse_args()
if not __debug__:
 parser.error("Do not run with -O: numerical assertions must remain enabled")
root=Path(__file__).resolve().parents[1]
mg5=args.mg5.expanduser().resolve()
if not (mg5/'madgraph').is_dir():
 parser.error('--mg5 must point to a MadGraph5_aMC installation')
sys.path.insert(0,str(mg5))
from models import import_ufo
from madgraph.core import base_objects,diagram_generation,helas_objects
from madgraph.various import process_checks
# MG may cache model files: work in a disposable copy, leaving the release intact.
temp_model=tempfile.TemporaryDirectory(prefix='hnl-contact-check-')
ufo_source=root/'ufo/dipole_GI_UFO'
ufo_copy=Path(temp_model.name)/'dipole_gi_contact_check'
shutil.copytree(ufo_source,ufo_copy,ignore=shutil.ignore_patterns('__pycache__','*.pyc','*.pkl'))
model=import_ufo.import_model(str(ufo_copy))
mw,mz,mh=80.3692,91.1875,125.2
alpha_inverse=128.94676405807147
e=math.sqrt(4*math.pi/alpha_inverse)
v=2*mw*math.sqrt(1-mw*mw/(mz*mz))/e
base={'aEWM1':alpha_inverse,'Gf':1/(math.sqrt(2)*v*v),'MZ':mz,'MH':mh,'MvN':200.,'WZ':0.}
def setparams(ev,b,w):
 values=base|{'CB':b*1e-6,'CW':w*1e-6}
 for param in ev.full_model['parameters'][('external',)]:
  name=param.name.removeprefix('mdl_')
  if name in values:param.value=values[name]
  if param.lhablock.upper()=='HNLDIPOLE':param.value={1:b*1e-6,2:w*1e-6}[param.lhacode[0]]
 ev.full_model.set_parameters_and_couplings()
# Independent Dirac-matrix trace for the photon contact from d_gamma/v.
I2=np.eye(2); O=np.zeros((2,2)); paulis=[np.array([[0,1],[1,0]]),np.array([[0,-1j],[1j,0]]),np.diag([1,-1])]
gamma=[np.block([[I2,O],[O,-I2]])]+[np.block([[O,a],[-a,O]]) for a in paulis]
g5=1j*gamma[0]@gamma[1]@gamma[2]@gamma[3]; PR=(np.eye(4)+g5)/2
metric=[1,-1,-1,-1]
def slash(p):return sum(metric[j]*p[j]*gamma[j] for j in range(4))
def trace_m2(p):
 q=slash(p[1]); total=0j
 for mu in range(4):
  g=(q@gamma[mu]-gamma[mu]@q)@PR
  bar=gamma[0]@g.conj().T@gamma[0]
  total+=-metric[mu]*np.trace((slash(p[2])+200*np.eye(4))@g@slash(p[0])@bar)
 return float(total.real)*(e*1e-6/math.sqrt(2))**2/4
rows=[]
for pdg in [12,14,16]:
 legs=base_objects.LegList([base_objects.Leg({'id':pid,'state':j>=2,'number':j+1}) for j,pid in enumerate([pdg,22,2000,25])])
 proc=base_objects.Process({'legs':legs,'model':model}); amp=diagram_generation.Amplitude(proc); me=helas_objects.HelasMatrixElement(amp)
 assert len(amp.get('diagrams'))==1
 ev=process_checks.MatrixElementEvaluator(model,reuse=False)
 for energy in [400.,600.]:
  s=energy**2; mn=200.; lam=(1-(mn+mh)**2/s)*(1-(mn-mh)**2/s); k=energy*math.sqrt(lam)/2;en=(s+mn*mn-mh*mh)/(2*energy)
  for x in [-.6,.2,.8]:
   px=k*math.sqrt(1-x*x);pz=k*x
   p=[[energy/2,0.,0.,energy/2],[energy/2,0.,0.,-energy/2],[en,px,0.,pz],[energy-en,-px,0.,-pz]]
   vals=[]
   for b,w in [(1,0),(0,1),(1,1),(1,-1),(1,-2),(2,0)]:
    setparams(ev,b,w); vals.append(ev.evaluate_matrix_element(copy.deepcopy(me),p=p)[0])
   for got,ratio in zip(vals,[1,.25,2.25,.25,0,4]):assert abs(got/vals[0]-ratio)<1e-10,(pdg,got,ratio)
   reference=trace_m2(p)
   assert abs(reference/vals[0]-1)<1e-10,(reference,vals[0])
   setparams(ev,1,0);ward=ev.evaluate_matrix_element(copy.deepcopy(me),p=p,gauge_check=True)[0]
   assert abs(ward/vals[0])<1e-10
   rows.append({'nu_pdg':pdg,'energy_GeV':energy,'cos_theta':x,'m2_B_W_plus_minus_cancel_double':vals,'independent_Dirac_trace_m2_CB_only':reference,'ward_m2':ward,'spin_average_denominator':me.get_denominator_factor()})
for j in range(6):
 for k in [6,12]:assert abs(rows[j+k]['m2_B_W_plus_minus_cancel_double'][0]/rows[j]['m2_B_W_plus_minus_cancel_double'][0]-1)<1e-10
out={'process':'nu gamma -> N h','source_UFO':'ufo/dipole_GI_UFO','mass_N_GeV':200,'coefficient_units':'TeV^-2, converted to GeV^-2','checks':{'independent_absolute_Dirac_trace':True,'single_contact_diagram':True,'photon_Ward':True,'flavor_universality':True,'CB_CW_interference_ratio':True,'photon_blind_direction_CB_plus_CW_over_2_zero':True,'quadratic_scaling':True},'scope':'Tree photon Higgs dipole contact only. Does not certify full charged sector, FeynArts equality, loop sign or finite matching.','rows':rows}
out['inputs']={'MW_GeV':mw,'MZ_GeV':mz,'MH_GeV':mh,'alphaMZ_inverse':alpha_inverse}
out['source_sha256']={f.name:hashlib.sha256(f.read_bytes()).hexdigest() for f in sorted(ufo_source.glob('*.py'))}
reference=json.loads((root/'validation/photon-higgs-test.json').read_text())
if len(reference['rows']) != len(rows):
 raise RuntimeError('Reference point count differs')
max_relative=0.
for actual, saved in zip(rows, reference['rows']):
 if any(actual[k] != saved[k] for k in ['nu_pdg','energy_GeV','cos_theta','spin_average_denominator']):
  raise RuntimeError('Reference kinematics or spin convention differ')
 for x,y in zip(actual['m2_B_W_plus_minus_cancel_double'],saved['m2_B_W_plus_minus_cancel_double']):
  if not math.isclose(x,y,rel_tol=1e-10,abs_tol=1e-15):
   raise RuntimeError('Fresh amplitude differs from recorded benchmark')
  if y: max_relative=max(max_relative,abs(x/y-1))
out['recorded_benchmark_max_relative_difference']=max_relative
output=args.output or root/'generated/photon-higgs-reproduced.json'
output.parent.mkdir(parents=True,exist_ok=True)
output.write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({'checks':out['checks'],'points':len(rows),'max_relative_difference_from_record':max_relative,'output':str(output)},indent=2))
temp_model.cleanup()
