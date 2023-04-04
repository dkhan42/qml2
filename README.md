QML: A Python Toolkit for Quantum Machine Learning
==================================================

|Build Status| |doi| |doi|

Fork of the QML library containing additional local kernels including local laplacian and local MBDF kernels.
Usage is entirely similar to the local kernels available in qmlcode : 

```
from qml.kernels import get_local_symmetric_kernel_laplacian, get_local_kernel_laplacian
K_train = get_local_symmetric_kernel_laplacian(X_train, Q_train, SIGMA)
K_test = get_local_kernel_laplacian(X_train, X_test, Q_train, Q_test, SIGMA)

from qml.kernels import get_local_symmetric_kernel_mbdf, get_local_kernel_mbdf
K_train = get_local_symmetric_kernel_mbdf(X_train, Q_train, SIGMA)
K_test = get_local_kernel_mbdf(X_train, X_test, Q_train, Q_test, SIGMA)
```

1) Citing QML:
--------------

Until the preprint is available from arXiv, please cite this GitHub
repository as:

::

    AS Christensen, LA Bratholm, S Amabilino, JC Kromann, FA Faber, B Huang, GR Glowacki, A Tkatchenko, K.R. Muller, OA von Lilienfeld (2018) "QML: A Python Toolkit for Quantum Machine Learning" https://github.com/qmlcode/qml

2) Get help:
------------

Documentation and installation instruction is found at:
http://www.qmlcode.org/

3) License:
-----------

QML is freely available under the terms of the MIT license.

.. |Build Status| image:: https://travis-ci.org/qmlcode/qml.svg?branch=master
   :target: https://travis-ci.org/qmlcode/qml
.. |doi| image:: https://badge.fury.io/py/qml.svg
   :target: https://badge.fury.io/py/qml
.. |doi| image:: https://zenodo.org/badge/89045103.svg
   :target: https://zenodo.org/badge/latestdoi/89045103
