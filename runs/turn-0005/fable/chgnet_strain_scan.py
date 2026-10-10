"""Structure-only CHGNet epitaxial-strain scan of idealized I4/mmm La3Ni2O7 (bilayer Ruddlesden-Popper,
24-atom conventional cell). In-plane a is clamped to substrate pseudocubic values taken from the Ko et al.
Nature 2025 Fig. 5a source data (3.7705, 3.7827, 3.792, 3.868 A) plus 3.83 A; internal coordinates relaxed at
five c values, c_min from a parabolic fit, then a final internal relaxation at c_min.
Reports c, c/a, apical and equatorial Ni-O bond lengths and the intra-bilayer Ni-Ni distance.
NO Tc inference is made from this. CHGNet 0.3.0 weights via chgnet 0.4.2, CPU.
Ran in /tmp/f5 (turn folder not shell-writable); log and JSON copied verbatim into outputs/."""
import numpy as np, json, time, warnings
warnings.filterwarnings("ignore")
import torch; torch.set_num_threads(2)
from pymatgen.core import Structure, Lattice
from chgnet.model import CHGNet, StructOptimizer

def build(a, c):
    # I4/mmm n=2 RP prototype positions (Sr3Ru2O7-like)
    sp=[]; fc=[]
    def add(s, x,y,z): sp.append(s); fc.append([x,y,z])
    zLa2=0.3185; zNi=0.0965; zO2=0.195; zO3=0.0965
    for sh in ([0,0,0],[0.5,0.5,0.5]):
        def A(s,x,y,z): add(s,(x+sh[0])%1,(y+sh[1])%1,(z+sh[2])%1)
        A('La',0,0,0.5)
        A('La',0,0,zLa2); A('La',0,0,-zLa2%1)
        A('Ni',0,0,zNi); A('Ni',0,0,-zNi%1)
        A('O',0,0,0)
        A('O',0,0,zO2); A('O',0,0,-zO2%1)
        A('O',0,0.5,zO3); A('O',0.5,0,zO3); A('O',0,0.5,-zO3%1); A('O',0.5,0,-zO3%1)
    return Structure(Lattice.tetragonal(a,c), sp, fc)

m=CHGNet.load(verbose=False); so=StructOptimizer(model=m)
def analyze(s2):
    ni=[i for i,x in enumerate(s2) if x.specie.symbol=='Ni']; bonds=[]
    for i in ni:
        for nb in s2.get_neighbors(s2[i],2.6):
            if nb.specie.symbol=='O': bonds.append((round(float(nb.nn_distance),4), abs(nb.coords[2]-s2[i].coords[2])>1.0))
    ap=sorted(set(b[0] for b in bonds if b[1])); eq=sorted(set(b[0] for b in bonds if not b[1]))
    nn=min(s2.get_distance(ni[0],j) for j in ni[1:])
    return dict(apical_NiO=ap,eq_NiO=eq,NiNi_interlayer=float(nn))

t0=time.time()
r=so.relax(build(3.83,20.5),fmax=0.05,steps=300,verbose=False,relax_cell=True)
sf=r['final_structure']
free=dict(a=sf.lattice.a,b=sf.lattice.b,c=sf.lattice.c,alpha=sf.lattice.alpha,E_per_atom=float(r['trajectory'].energies[-1])/len(sf),**analyze(sf))
print("free",free,time.time()-t0,flush=True)
a0=(free['a']*free['b'])**0.5
res=[]
for a in [3.7705,3.7827,3.792,3.83,3.868]:
    t0=time.time(); pts=[]
    for c in [20.0,20.3,20.6,20.9,21.2]:
        r=so.relax(build(a,c),fmax=0.05,steps=200,verbose=False,relax_cell=False)
        pts.append((c,float(r['trajectory'].energies[-1])/24,r['final_structure']))
    cs=np.array([p[0] for p in pts]); es=np.array([p[1] for p in pts])
    co=np.polyfit(cs,es,2); cmin=-co[1]/(2*co[0])
    r=so.relax(build(a,cmin),fmax=0.05,steps=200,verbose=False,relax_cell=False)
    s2=r['final_structure']
    d=dict(a=a,c_min=float(cmin),c_over_a=float(cmin/a),E_per_atom=float(r['trajectory'].energies[-1])/24,
           strain_pct_vs_free=100*(a/a0-1),E_vs_c=[(float(c),float(e)) for c,e,_ in pts],**analyze(s2))
    res.append(d); print(d,time.time()-t0,flush=True)
    s2.to(filename=f"La3Ni2O7_a{a}.cif")
json.dump(dict(free=free,scan=res,note="I4/mmm idealized La3Ni2O7 (24 atoms), CHGNet 0.3.0 weights via chgnet 0.4.2; in-plane a clamped, c from parabolic fit of internally-relaxed energies; structure only, no Tc inference"),open('chgnet_strain.json','w'),indent=1)
