#!/usr/bin/env python3
"""Compatibility guard for missing publisher cells; executes checked-in analysis.
The Figure 1c A11 column contains temperature but no resistivity values. It is
excluded explicitly, never imputed. This runner also simplifies the bin expression.
"""
from pathlib import Path
code=Path(__file__).with_name('analyze_nickelate_data.py').read_text()
code=code.replace("x['bin']=np.round(x.T.values[0]/width).astype(int) if False else np.round(x['T']/width).astype(int)","x['bin']=np.round(x['T']/width).astype(int)")
code=code.replace("label=str(d.iloc[0,col+1]); rawcurve=curve(d,col)","label=str(d.iloc[0,col+1]); rawcurve=curve(d,col)\n            if len(rawcurve)==0:\n                print('MISSING SOURCE COLUMN:',sheet,label)\n                continue")
exec(compile(code,'analyze_nickelate_data.py','exec'))
