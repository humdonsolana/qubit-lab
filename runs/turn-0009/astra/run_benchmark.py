"""Portable OpenQASM2: use qelib1.inc u3, not Qiskit's permissive u alias."""
import holstein_benchmark as h
from qiskit import transpile as original

def portable_transpile(*args,**kwargs):
 if kwargs.get('basis_gates')==['u','cx']:kwargs['basis_gates']=['u3','cx']
 return original(*args,**kwargs)
h.transpile=portable_transpile
h.main()
