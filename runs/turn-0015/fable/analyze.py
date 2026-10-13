"""Descriptors of relaxed structures: a, c, anion height above Fe plane, Fe-X-Fe angle, FeX-layer spacing, nearest X-cation distances."""
import sys, json, numpy as np
from pymatgen.core import Structure

def descriptors(path):
    s = Structure.from_file(path)
    out = {"file": path, "formula": s.composition.reduced_formula, "a": s.lattice.a, "b": s.lattice.b, "c": s.lattice.c,
           "alpha,beta,gamma": [round(x, 2) for x in s.lattice.angles]}
    fe = [i for i, x in enumerate(s) if x.specie.symbol == "Fe"]
    X = [i for i, x in enumerate(s) if x.specie.symbol in ("Se", "As", "Te", "S")]
    c = s.lattice.c
    zfe0 = s[fe[0]].coords[2]
    def dz(z):
        d = abs(z - zfe0) % c
        return min(d, c - d)
    h = np.mean([dz(s[i].coords[2]) for i in X])
    out["anion_height_A"] = round(float(h), 3)
    # Fe-X bond and Fe-X-Fe angle (nearest Fe neighbours of X)
    d_fex = []
    angs = []
    for i in X:
        nn = s.get_neighbors(s[i], 3.0)
        fes = [n for n in nn if n.specie.symbol == "Fe"]
        d_fex += [n.nn_distance for n in fes]
        for p in range(len(fes)):
            for q in range(p + 1, len(fes)):
                v1 = fes[p].coords - s[i].coords; v2 = fes[q].coords - s[i].coords
                ang = np.degrees(np.arccos(np.dot(v1, v2) / np.linalg.norm(v1) / np.linalg.norm(v2)))
                angs.append(ang)
    out["d_FeX_A"] = round(float(np.mean(d_fex)), 3) if d_fex else None
    angs = sorted(angs)
    out["FeXFe_angles_deg"] = [round(float(a), 1) for a in (angs[:2] + angs[-2:])] if angs else None
    # Fe-Fe in plane
    dfefe = []
    for i in fe:
        nn = s.get_neighbors(s[i], 3.2)
        dfefe += [n.nn_distance for n in nn if n.specie.symbol == "Fe"]
    out["d_FeFe_A"] = round(float(np.min(dfefe)), 3) if dfefe else None
    # X to nearest non-Fe cation (apical) distances
    for i in X[:1]:
        nn = s.get_neighbors(s[i], 4.0)
        others = sorted([(n.nn_distance, n.specie.symbol) for n in nn if n.specie.symbol not in ("Fe",)])
        out["X_apical_contacts"] = [(round(d, 3), e) for d, e in others[:4]]
    out["FeX_layer_spacing_A"] = round(float(s.lattice.c), 3)
    return out

if __name__ == "__main__":
    res = [descriptors(p) for p in sys.argv[1:]]
    print(json.dumps(res, indent=1))
