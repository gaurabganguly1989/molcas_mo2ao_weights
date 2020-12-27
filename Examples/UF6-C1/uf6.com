 
*********************** SEWARD ***************************
&SEWARD  &END
RICD

Basis set
U.ANO-RCC-VDZ
U            0.000000   0.000000   0.000000     angstrom
End of basis

Basis set
F.ANO-RCC-VDZ
F1           0.000000   0.000000   2.090557     angstrom
F2           0.000000   2.090557   0.000000     angstrom
F3           2.090557   0.000000   0.000000     angstrom
F4           0.000000   0.000000  -2.090557     angstrom
F5           0.000000  -2.090557   0.000000     angstrom
F6          -2.090557   0.000000   0.000000     angstrom
End of basis
Angmom
0.0 0.0 0.0
AMFI
End of input
********************************************************

******************* DFT JOB ***************************
>> COPY ${Project}.GssOrb INPORB

&SCF &END
 Spin=1
 KSDFT=PBE
 Charge=0
 LumOrb
End of input

>> COPY ${Project}.ScfOrb $HomeDir/${Project}.ScfOrb
********************************************************

********************* PLOT ***************************
>> COPY $HomeDir/$Project.ScfOrb INPORB

&GRID_IT &END
 Sparse
 all
End of input

>> COPY $Project.lus $HomeDir/${Project}-scf.lus
*******************************************************



