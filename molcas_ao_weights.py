#!/usr/bin/env python

def check_path(fp):
    import os
    if not os.path.exists(fp):
        raise FileNotFoundError("Could not find the file {}".format(fp))

def main(sew_file, orb_file, hdf_file, symmetry, index):
    import re
    import numpy as np
    import h5py
    print(' ')
    print('           M U L L I K E N  A N A L Y S I S')
    print('                          of ')
    print('    Molecular Orbital in terms of Atomic Orbital wt.%')
    print(' ')
    print('For questions/suggestions contact Gaurab Ganguly')
    print('                                  gaurabganguly1989@gmail.com')
    print(' ')
    print('Molecular Orbital of interest:')
    print('------------------------------')
    print('Symmetry label=', symmetry,', Index=', index)
    print(' ')
    print('Files from Molcas/OpenMolcas Calculation:')
    print('-----------------------------------------')
    print('Seward file   :', sew_file)
    print('Orbital file  :', orb_file)
    print('HDF5 file     :', hdf_file)
    print(' ')
    print(' ')
    count = []          # index of basis fn (all irreps combined)
    basisfn = []        # total number of basis fn (all irreps combined)
    irrep = []          # irreps of the point group
    sym_label = []      # indexing the irreps 1,2,3,...
    sym_bas = []        # number of basis fn in each irrep
    sym_block = []      # elements of AO overlap matrix in each irrep block
    coeff = []          # store the MO coefficients of the requested MO in a list
    check_path(sew_file)
    check_path(orb_file)
    check_path(hdf_file)
    #Reading basis information from the provided SEWARD file:
    with open(sew_file, 'r') as sfile:
        for line in sfile:
            if re.search(r'Basis Label        Type   Center', line):
                for line in sfile:
                    if re.search(r'Basis set specifications \:', line):
                        break
                    if re.search(r'\W\d', line):
                        count.append(int(line.split()[0]))
                        basisfn.append(line.split()[1] + "-" + (line.split()[2]))
        if len(count) == 0 and len(basisfn) == 0:
            raise ValueError("Could not find basis set table in seward output file {}".format(sew_file))
    with open(sew_file, 'r') as sfile:
        lines = sfile.readlines()
        try:
            point_group = [x for x in lines if 'Character Table' in x][0].split()[3]
            symmetry_species = [x for x in lines if 'Symmetry species' in x][0]
            basis_functions = [x for x in lines if 'Basis functions' in x][-1]
            #print("BAS", basis_functions)
        except IndexError:
            raise IndexError("Could not find 'Character Table', 'Symmetry species', or 'Basis functions' " \
                             +"search strings in seward output file {}".format(sew_file))
        num_of_irreps = len(re.findall(r'\d+', basis_functions))
        if num_of_irreps == 0:
            raise ValueError("Did not find any Irreps. in seward output file {}".format(sew_file))
        for i in range(num_of_irreps):
            sym_label.append(i+1)
            irrep.append(symmetry_species.split()[i+2])
            sym_bas.append(int(basis_functions.split()[i+2]))
            sym_block.append(int(basis_functions.split()[i+2])**2)
    # Reading orbitals from GssOrb/ScfOrb/RASOrb/PT2Orb/SONOrb or any orbitals file:
    search_string = r'\* ORBITAL{:>5d}{:>5d}'
    with open(orb_file, 'r') as ofile:
        for line in ofile:
            if re.search(search_string.format(symmetry, index), line):
                for line in ofile:
                    if re.search(search_string.format(symmetry, index+1), line):
                        break
                    if re.search(r'\s', line):
                        for item in line.strip().split():
                            coeff.append(float(item))
        if len(coeff) == 0 and re.search(search_string.format(symmetry, index), line):
            # found the search string
            raise ValueError("Did not find orbitals in orbital file {}".format(orb_file))
        elif re.search(search_string.format(symmetry, index), line) is not None:
            # did not find the search string
            raise RuntimeError("Something else went wrong.......Help me PLS. :(")
    # Reading AO overlap integrals from the provided '.h5' file:
    with h5py.File(hdf_file, 'r') as hdf:
        overlap = np.array(hdf.get('AO_OVERLAP_MATRIX'))
    print('                 POINT GROUP =', point_group)
    print('-------------------------------------------------------------')
    print('Symm. label      Irrep.       No. of MOs')
    print('-------------------------------------------------------------')
    template = ' {:>10d}      {:<10s}  {:>10d}'
    for i in range(num_of_irreps):
        print(template.format(i+1, symmetry_species.split()[i+2], int(basis_functions.split()[i+2])))
    print('-------------------------------------------------------------')
    start_bas = 0
    start_block = 0
    end_bas = 0
    end_block = 0
    try:
        if symmetry == 1:
            end_bas = start_bas + sym_bas[0]
            end_block = start_block + sym_block[0]
            bas = np.array(basisfn[start_bas:end_bas])
            block = np.reshape(overlap[start_block:end_block], (sym_bas[0], sym_bas[0]))
        else:
            for i in range(symmetry-1):
                start_bas += sym_bas[i]
                start_block += sym_block[i]
            for i in range(symmetry):
                end_bas += sym_bas[i]
                end_block += sym_block[i]
            bas = np.array(basisfn[start_bas:end_bas])
            block = np.reshape(overlap[start_block:end_block], (sym_bas[symmetry-1],
                                                                sym_bas[symmetry-1]))
    # TODO: find out what exception it raises that you would have to deal with.
    #       having a general Exception is not good to do.
    #       python has the great ability to handle different error cases separately and you can give the
    #       user valuable information as to what went wrong when you raise the appropriate error.
    except Exception:
        print("Error Exit:")
        print("Symmetry label", symmetry, "is not possible for", point_group, "point group!")
        print("Check the table and re run.")
    # Multiplying coeff*overlap*coeff (CSC) to get MO wt%
    if symmetry == 0 or index == 0:
        # TODO: here a raise ValueError would be more appropriate also it will terminate the program
        print("Error Exit:")
        print("Symmetry or Index can't be 0!")
        print("Check the Symmetry label for Irreps in the table and re run.")
    elif symmetry not in sym_label:
        pass
    elif index > sym_bas[symmetry-1]:
        # TODO: here a raise ValueError would be more appropriate also it will terminate the program
        raise ValueError("Error Exit: Index", index, "is beyond range for", irrep[symmetry-1], \
                        "Irrep! Check the table and re run.")
        #print("Error Exit:")
        #print("Index", index, "is beyond range for", irrep[symmetry-1], "Irrep!")
        #print("Check the table and re run.")
    elif symmetry in sym_label and index <= sym_bas[symmetry-1]:
        print('')
        print('Mulliken Analysis of:')
        template = "n-th ('n ={:>3}') MO in '{}' Symmetry (symm. label = '{}')."
        print(template.format(index, irrep[symmetry - 1], symmetry))
        print('All AO function with > 1.0% weight in the MO is printed.')
        print('-------------------------------------------------------------')
        print('AO-func.          wt.%  ')
        print('-------------------------------------------------------------')
        for i in range(len(coeff)):
            tmp = []
            for j in range(len(coeff)):
                tmp.append(coeff[i] * block[i][j] * coeff[j])
            if abs(sum(tmp))*100 > 1.0 : # user can change the thresold
                print('{:<10s} {:>10.1f}%'.format(bas[i], sum(tmp)*100))
        print('-------------------------------------------------------------')
        print('')
    else:
        # TODO: here a raise ValueError would be more appropriate also it will terminate the program
        raise ValueError("Error Exit: Symmetry label and Index is not possible! Check and re run.")
        #print("Error Exit: Symmetry label and Index is not possible! Check and re run.")

if __name__ == "__main__":
    import argparse, pathlib
    parser = argparse.ArgumentParser(description="This program calculates AO wt% in a given MO.")
    parser.add_argument('sew_file', type=pathlib.Path, metavar='1) file.out',
                        help="Gateway/Seward output file with print level = 3.")
    parser.add_argument('orb_file', type=pathlib.Path, metavar='2) file.SCF/RAS/SONOrb',
                        help="Orbital file with MO co-efficients.")
    parser.add_argument('hdf_file', type=pathlib.Path, metavar='3) file.h5',
                        help="HDF5 file for AO overlap matrix.")
    parser.add_argument('-s',  '--symmetry', type=int, metavar='MO_symmetry', required=True,
                        help="Symmetry/Irrep of the orbital of interest.")
    parser.add_argument('-i',  '--index',    type=int, metavar='MO_Index', required=True,
                        help="Orbital index in the particular Symmetry/Irrep.")
    args = parser.parse_args()
    main(args.sew_file, args.orb_file, args.hdf_file, args.symmetry, args.index)

