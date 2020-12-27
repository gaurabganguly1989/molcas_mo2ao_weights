# Molcas MO2AO

The script `molcas_ao_weights.py` can be used to get AO wt% in a
chosen MO. The MO can be read from **ScfOrb/RasOrb/Pt2Orb/SonOrb**. 
The code works for any given point group symmetry and any given 
MO (occupied or virtual). 

Usage of the Script can be found by running the following command:
 
```
python molcas_ao_weights.py -h
```

Examples are provided in the Example folder of the base directory.

Example:
========
Molecule: UF6. Calculations are done in three different point groups 
D2h, Ci, and C1 (NoSym). The metal-ceneterd (with high 5f character) 
orbitals are analyzed from DFT (PBE) calculation using .ScfOrb file. 
AO composition wt.% are found to be invarient to the symmetry point 
group used in the calculation. 

Look for Sym-{*}-Index-{*}.out files in the `sub-folders` under `Example` folder:

Wt.% to match from the `molcas_ao_weights.py` run, among different 
point group symmetries. $a_{2u}$ and $t_{1u}$ (in $O_h$) orbitals are analyzed.
They show same AO wt% given below:

|                                                   | UF6(D2h)           | UF6(Ci)            |    UF6(C1)          |            
|---------------------------------------------------|--------------------|--------------------|---------------------|
| $a_{2u} (99.8% U-5f0)                             | Sym-5-Index-02.out | Sym-2-Index-38.out | Sym-1-Index-74.out  |
| $t_{1u}:(74% U-5$f_0$, 2% U-6$f_0$, 23% F-2$p_z$) | Sym-7-Index-14.out | Sym-2-Index-43.out | Sym-1-Index-79.out  |





