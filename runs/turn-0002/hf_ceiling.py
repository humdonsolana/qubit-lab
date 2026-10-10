"""
Heavy-fermion Tc ceiling from the Sommerfeld coefficient.

Idea (standard, e.g. Sarrao & Thompson, J. Phys. Soc. Jpn. 76, 051013 (2007);
Bauer et al. PRL 93, 147005 (2004) for Pu-115): in heavy-fermion superconductors
Tc scales with the Kondo-lattice coherence scale T*, and T* is inversely
proportional to the quasiparticle mass measured by the normal-state Sommerfeld
coefficient gamma.  We test this on a hand-compiled table of ambient-pressure
heavy-fermion / f-electron superconductors and ask what gamma would be needed
for Tc = 300 K if the same ratio Tc/T* held.

Effective Fermi temperature from gamma for one f-electron per formula unit
(free-quasiparticle formula): gamma = (pi^2/2) R / T*  ->  T* = pi^2 R / (2 gamma).

All values are literature values quoted to the precision usually tabulated in
reviews (Pfleiderer, Rev. Mod. Phys. 81, 1551 (2009); Sarrao & Thompson 2007;
Aoki et al. J. Phys. Soc. Jpn. 88, 022001 (2019) for UTe2; Khim et al. Science
373, 1012 (2021) for CeRh2As2; Aoki et al. JPSJ 76, 063701 (2007) for NpPd5Al2).
They are approximate (gamma of a superconductor is itself ambiguous: we use the
normal-state value just above Tc where available).
"""
import numpy as np, pandas as pd, json
R = 8.314  # J/(mol K)

# name, Tc (K), gamma (mJ mol^-1 K^-2), note
data = [
    ("CeCu2Si2",  0.6,  1000, "Steglich 1979; gamma ~1 J/molK2"),
    ("CeCoIn5",   2.3,   290, "Petrovic 2001; gamma(T->Tc) ~290"),
    ("CeIrIn5",   0.4,   720, "Petrovic 2001"),
    ("Ce2PdIn8",  0.68,  550, "Kaczorowski 2009"),
    ("CePt3Si",   0.75,  390, "Bauer 2004 (noncentrosymmetric)"),
    ("CeRh2As2",  0.26, 1000, "Khim 2021"),
    ("UPt3",      0.55,  420, "Stewart 1984"),
    ("UBe13",     0.9,  1100, "Ott 1983"),
    ("URu2Si2",   1.5,   65,  "Palstra 1985; gamma below hidden order"),
    ("UPd2Al3",   2.0,   150, "Geibel 1991"),
    ("UNi2Al3",   1.0,   120, "Geibel 1991"),
    ("UTe2",      1.6,   120, "Ran 2019 (Tc 1.6-2.1 K)"),
    ("UCoGe",     0.6,   57,  "Huy 2007 (FM superconductor)"),
    ("URhGe",     0.25,  160, "Aoki 2001"),
    ("NpPd5Al2",  4.9,   200, "Aoki 2007"),
    ("PuCoIn5",   2.5,   200, "Bauer 2012"),
    ("PuRhGa5",   8.7,   70,  "Wastin 2003"),
    ("PuCoGa5",  18.5,   77,  "Sarrao 2002"),
]
df = pd.DataFrame(data, columns=["compound","Tc_K","gamma_mJ","note"])
df["Tstar_K"] = np.pi**2 * R / (2 * df.gamma_mJ * 1e-3)
df["Tc_over_Tstar"] = df.Tc_K / df.Tstar_K
df["Tc_x_gamma"] = df.Tc_K * df.gamma_mJ

# log-log fit Tc = A * gamma^b
b, logA = np.polyfit(np.log10(df.gamma_mJ), np.log10(df.Tc_K), 1)
pred = 10**logA * df.gamma_mJ**b
resid = np.log10(df.Tc_K) - np.log10(pred)
r2 = 1 - np.sum(resid**2)/np.sum((np.log10(df.Tc_K)-np.log10(df.Tc_K).mean())**2)

ratio_max = df.Tc_over_Tstar.max()
ratio_med = df.Tc_over_Tstar.median()
out = {
    "n_compounds": len(df),
    "loglog_fit": {"exponent_b": b, "prefactor_A": 10**logA, "R2_log": r2,
                    "comment": "Tc = A*gamma^b; b near -1 means Tc*gamma ~ const"},
    "Tc_over_Tstar": {"min": df.Tc_over_Tstar.min(), "median": ratio_med, "max": ratio_max,
                       "max_compound": df.loc[df.Tc_over_Tstar.idxmax(),"compound"]},
    # gamma needed for Tc=300 K if the best observed ratio held
    "gamma_needed_for_300K_at_max_ratio_mJ": np.pi**2*R/(2*(300/ratio_max))*1e3,
    "gamma_needed_for_300K_at_median_ratio_mJ": np.pi**2*R/(2*(300/ratio_med))*1e3,
    # ceiling Tc for a material still 'heavy' (gamma >= 50 mJ/molK2) at best ratio
    "Tc_ceiling_gamma50_at_max_ratio_K": ratio_max*np.pi**2*R/(2*0.05),
    "Tc_ceiling_gamma100_at_max_ratio_K": ratio_max*np.pi**2*R/(2*0.10),
    # what Tc does the fit predict for gamma typical of mixed-valent Ce/Yb 115-like metals
    "fit_Tc_at_gamma_50": 10**logA*50**b,
    "fit_Tc_at_gamma_30": 10**logA*30**b,
}
pd.set_option("display.width",200)
print(df.round(4).to_string(index=False))
print(json.dumps(out, indent=2, default=float))
df.to_csv("outputs/hf_table.csv", index=False)
json.dump(out, open("outputs/hf_ceiling.json","w"), indent=2, default=float)

try:
    import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
    fig,ax=plt.subplots(figsize=(5,4))
    ax.loglog(df.gamma_mJ, df.Tc_K, "o")
    for _,r in df.iterrows(): ax.annotate(r.compound,(r.gamma_mJ,r.Tc_K),fontsize=6)
    g=np.logspace(0.5,3.2,50); ax.loglog(g,10**logA*g**b,"--",label=f"fit b={b:.2f}")
    ax.loglog(g, ratio_max*np.pi**2*R/(2*g*1e-3),":",label=f"Tc={ratio_max:.3f} T*")
    ax.axhline(300,color="r",lw=0.5); ax.set_xlabel("gamma (mJ/mol K^2)"); ax.set_ylabel("Tc (K)")
    ax.legend(fontsize=7); fig.tight_layout(); fig.savefig("outputs/hf_ceiling.png",dpi=130)
except Exception as e: print("plot skipped",e)
