QML: A Python Toolkit for Quantum Machine Learning
==================================================

Fork of the QML library (https://github.com/qmlcode/qml) containing additional local kernels including local laplacian and local MBDF kernels.
Can be installed as :
```
python setup.py install
```

Usage is entirely similar to the local kernels available in qmlcode : 

```
from qml.kernels import get_local_symmetric_kernel_laplacian, get_local_kernel_laplacian
K_train = get_local_symmetric_kernel_laplacian(X_train, Q_train, SIGMA)
K_test = get_local_kernel_laplacian(X_train, X_test, Q_train, Q_test, SIGMA)

from qml.kernels import get_local_symmetric_kernel_mbdf, get_local_kernel_mbdf
K_train = get_local_symmetric_kernel_mbdf(X_train, Q_train, SIGMA)
K_test = get_local_kernel_mbdf(X_train, X_test, Q_train, Q_test, SIGMA)
```
