"""Locate CHGNet/phonopy imaginary modes for the relaxed A M B4 C4 designs: which q, which atoms."""
import sys, json, numpy as np
from pymatgen.core import Structure
from pymatgen.io.phonopy import get_phonopy_structure
from phonopy import Phonopy
from chgnet.model import CHGNet
model = CHGNet.load()

def run(cif, sc=(2, 4, 2)):
    s = Structure.from_file(cif)
    ph = Phonopy(get_phonopy_structure(s), supercell_matrix=np.diag(sc), primitive_matrix=None)
    ph.generate_displacements(distance=0.01)
    forces = []
    for sc_ in ph.supercells_with_displacements:
        st = Structure(sc_.cell, sc_.symbols, sc_.scaled_positions)
        forces.append(np.array(model.predict_structure(st)["f"]))
    ph.forces = forces
    ph.produce_force_constants()
    ph.run_mesh([8, 8, 8], with_eigenvectors=True, is_mesh_symmetry=False)
    m = ph.get_mesh_dict()
    f = m["frequencies"]; q = m["qpoints"]
    idx = np.unravel_index(np.argmin(f), f.shape)
    ev = m["eigenvectors"][idx[0]][:, idx[1]].reshape(-1, 3)
    w = np.linalg.norm(ev, axis=1) ** 2
    out = {"cif": cif, "min_thz": float(f.min()), "q_min": q[idx[0]].tolist(),
           "n_imag_mesh": int((f < -0.1).sum()),
           "mode_weight_by_site": {f"{sp.symbol}{i}": round(float(w[i]), 3) for i, sp in enumerate(s.species)},
           "gamma_min_thz": float(f[np.all(np.abs(q) < 1e-6, axis=1)].min()) if np.any(np.all(np.abs(q) < 1e-6, axis=1)) else None}
    print(json.dumps(out, indent=1))
    return out

res = [run(c) for c in sys.argv[1:]]
json.dump(res, open("outputs/phonon_where.json", "w"), indent=1)
