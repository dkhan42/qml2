# MIT License
#
# Copyright (c) 2017 Anders Steen Christensen
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

from __future__ import print_function

import os
import sys
import time
import numpy as np
import qml

from qml.math import cho_solve
from qml.arad import generate_arad_representation

from qml.arad import get_local_kernels_arad
from qml.arad import get_local_symmetric_kernels_arad

from qml.arad import get_global_kernels_arad
from qml.arad import get_global_symmetric_kernels_arad

from qml.arad import get_atomic_kernels_arad
from qml.arad import get_atomic_symmetric_kernels_arad

def get_energies(filename):
    """ Returns a dictionary with heats of formation for each xyz-file.
    """

    f = open(filename, "r")
    lines = f.readlines()
    f.close()

    energies = dict()

    for line in lines:
        tokens = line.split()

        xyz_name = tokens[0]
        hof = float(tokens[1])

        energies[xyz_name] = hof

    return energies

def test_arad():
    test_dir = os.path.dirname(os.path.realpath(__file__))

    # Parse file containing PBE0/def2-TZVP heats of formation and xyz filenames
    data = get_energies(test_dir + "/data/hof_qm7.txt")

    # Generate a list of qml.data.Compound() objects
    mols = []

    for xyz_file in sorted(data.keys())[:10]:

        # Initialize the qml.data.Compound() objects
        mol = qml.Compound(xyz=test_dir + "/qm7/" + xyz_file)

        # Associate a property (heat of formation) with the object
        mol.properties = data[xyz_file]

        # This is a Molecular Coulomb matrix sorted by row norm

        mol.representation = generate_arad_representation(mol.coordinates,
                mol.nuclear_charges)
        
        mols.append(mol)

    sigmas = [25.0]

    X1 = np.array([mol.representation for mol in mols])

    K_local_asymm = get_local_kernels_arad(X1, X1, sigmas)
    K_local_symm = get_local_symmetric_kernels_arad(X1, sigmas)

    assert np.allclose(K_local_symm, K_local_asymm), "Symmetry error in local kernels"
    assert np.invert(np.all(np.isnan(K_local_asymm))), "ERROR: ARAD local symmetric kernel contains NaN"

    K_global_asymm = get_global_kernels_arad(X1, X1, sigmas)
    K_global_symm = get_global_symmetric_kernels_arad(X1, sigmas)

    assert np.allclose(K_global_symm, K_global_asymm), "Symmetry error in global kernels"
    assert np.invert(np.all(np.isnan(K_global_asymm))), "ERROR: ARAD global symmetric kernel contains NaN"

    molid = 5
    X1 = generate_arad_representation(mols[molid].coordinates,
                mols[molid].nuclear_charges, size = mols[molid].natoms)
    XA = X1[:mols[molid].natoms]

    K_atomic_asymm = get_atomic_kernels_arad(XA, XA, sigmas)
    K_atomic_symm = get_atomic_symmetric_kernels_arad(XA, sigmas)

    assert np.allclose(K_atomic_symm, K_atomic_asymm), "Symmetry error in atomic kernels"
    assert np.invert(np.all(np.isnan(K_atomic_asymm))), "ERROR: ARAD atomic symmetric kernel contains NaN"
    
    K_atomic_asymm = get_atomic_kernels_arad(XA, XA, sigmas)

if __name__ == "__main__":

    test_arad()
