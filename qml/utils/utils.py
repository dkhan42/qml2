# MIT License
#
# Copyright (c) 2018 Silvia Amabilino, Lars Andersen Bratholm
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


import numpy as np

def is_positive(x):
    return (not is_array_like(x) and is_numeric(x) and x > 0)

def is_positive_or_zero(x):
    return (not is_array_like(x) and is_numeric(x) and x >= 0)

def is_array_like(x):
    return isinstance(x, (tuple, list, np.ndarray))

def is_positive_integer(x):
    return (not is_array_like(x) and _is_integer(x) and x > 0)

def is_positive_integer_or_zero(x):
    return (not is_array_like(x) and _is_integer(x) and x >= 0)

def is_string(x):
    return isinstance(x, str)

def is_dict(x):
    return isinstance(x, dict)

def is_numeric(x):
    return isinstance(x, (float, int))

def is_numeric_array(x):
    if is_array_like(x) and np.asarray(x).size > 0:
        try:
            np.asarray(x, dtype=float)
            return True
        except (ValueError, TypeError):
            return False
    return False

def is_numeric_1d_array(x):
    return is_numeric_array(x) and is_1d_array(x)

# Accepts 2d arrays of shape (n,1) and (1,n) as well
def is_1d_array(x):
    return is_array_like(x) and (np.asarray(x).ndim == 1 or np.asarray(x).ndim == 2 and 1 in np.asarray(x).shape)

# Doesn't accept floats e.g. 1.0
def _is_integer(x):
    return isinstance(x, int)
    #return (is_numeric(x) and (float(x) == int(x)))

# will intentionally accept 0, 1 as well
def is_bool(x):
    return (x in (True, False))

def is_non_zero_integer(x):
    return (_is_integer(x) and x != 0)

def _is_positive_array(x):
    if is_numeric_array(x) and (np.asarray(x, dtype = float) > 0).all():
        return True
    return False

def _is_positive_or_zero_array(x):
    if is_numeric_array(x) and (np.asarray(x, dtype = float) >= 0).all():
        return True
    return False

def _is_integer_array(x):
    if is_numeric_array(x):
        if (np.asarray(x, dtype = float) == np.asarray(x, dtype = int)).all():
            return True
    return False

def is_positive_integer_1d_array(x):
    return is_positive_integer_array(x) and is_1d_array(x)

def is_positive_integer_array(x):
    return (_is_integer_array(x) and _is_positive_array(x))

def is_positive_integer_or_zero_array(x):
    return (_is_integer_array(x) and _is_positive_or_zero_array(x))

# ------------- ** Checking inputs ** --------------------------

def check_global_representation(x):
    """
    This function checks that the data passed through x corresponds to the descriptor in a numpy array of shape
    (n_samples, n_features) containing floats.

    :param x: array like
    :return: numpy array of floats of shape (n_samples, n_features)
    """

    if not is_array_like(x):
        raise InputError("x should be array like.")

    x = np.asarray(x)

    if len(x.shape) != 2:
        raise InputError("x should be an array with 2 dimensions. Got %s" % (len(x.shape)))

    return x

def check_local_representation(x):
    """
    This function checks that the data passed through x corresponds to the descriptor in a numpy array of shape
    (n_samples, n_atoms, n_features) containing floats.

    :param x: array like
    :return: numpy array of floats of shape (n_samples, n_atoms, n_features)
    """

    if not is_array_like(x):
        raise InputError("x should be array like.")

    x = np.asarray(x)

    if len(x.shape) != 3:
        raise InputError("x should be an array with 3 dimensions. Got %s" % (len(x.shape)))

    return x

def check_y(y):
    """
    This function checks that y is a one dimensional array of floats.

    :param y: array like
    :return: numpy array of shape (n_samples, 1)
    """
    if not is_array_like(y):
        raise InputError("y should be array like.")

    y = np.atleast_2d(y).T

    return y

def check_sizes(x, y=None, dy=None, classes=None):
    """
    This function checks that the different arrays have the correct number of dimensions.

    :param x: array of 3 dimensions
    :param y: array of 1 dimension
    :param dy: array of 3 dimensions
    :param classes: array of 2 dimensions
    :return: None
    """

    if dy is None and classes is None:

        if x.shape[0] != y.shape[0]:
            raise InputError("The descriptor and the properties should have the same first number of elements in the "
                             "first dimension. Got %s and %s" % (x.shape[0], y.shape[0]))

    elif y is None and dy is None:
        if classes is None:
            raise InputError("Only x is not none.")
        else:
            if x.shape[0] != classes.shape[0]:
                raise InputError("Different number of samples in the descriptor and the classes: %s and %s." % (x.shape[0], classes.shape[0]))
            if len(x.shape) == 3:
                if x.shape[1] != classes.shape[1]:
                    raise InputError("The number of atoms in the descriptor and in the classes is different: %s and %s." % (x.shape[1], classes.shape[1]))

    elif dy is None and classes is not None:

        if x.shape[0] != y.shape[0] or x.shape[0] != classes.shape[0]:
            raise InputError("All x, y and classes should have the first number of elements in the first dimension. Got "
                             "%s, %s and %s" % (x.shape[0], y.shape[0], classes.shape[0]))

        if len(x.shape) == 3:
            if x.shape[1] != classes.shape[1]:
                raise InputError("x and classes should have the same number of elements in the 2nd dimension. Got %s "
                                 "and %s" % (x.shape[1], classes.shape[1]))

    else:

        if x.shape[0] != y.shape[0] or x.shape[0] != dy.shape[0] or x.shape[0] != classes.shape[0]:
            raise InputError("All x, y, dy and classes should have the first number of elements in the first dimension. Got "
                             "%s, %s, %s and %s" % (x.shape[0], y.shape[0], dy.shape[0], classes.shape[0]))

        if x.shape[1] != dy.shape[1] or x.shape[1] != classes.shape[1]:
            raise InputError("x, dy and classes should have the same number of elements in the 2nd dimension. Got %s, %s "
                             "and %s" % (x.shape[1], dy.shape[1], classes.shape[1]))

def check_dy(dy):
    """
    This function checks that dy is a three dimensional array with the 3rd dimension equal to 3.

    :param dy: array like
    :return: numpy array of floats of shape (n_samples, n_atoms, 3)
    """

    if dy is None:
        approved_dy = dy
    else:
        if not is_array_like(dy):
            raise InputError("dy should be array like.")

        dy = np.asarray(dy)

        if len(dy.shape) != 3:
            raise InputError("dy should be an array with 3 dimensions. Got %s" % (len(dy.shape)))

        if dy.shape[-1] != 3:
            raise InputError("The last dimension of the array dy should be 3. Got %s" % (dy.shape[-1]))

        approved_dy = dy

    return approved_dy

def check_classes(classes):
    """
    This function checks that the classes is a numpy array of shape (n_samples, n_atoms) of ints
    :param classes: array like
    :return: numpy array of ints of shape (n_samples, n_atoms)
    """

    if classes is None:
        approved_classes = classes
    else:
        if not is_array_like(classes):
            raise InputError("classes should be array like.")

        if not is_positive_integer_or_zero_array(classes):
            raise InputError("classes should be an array of ints.")

        classes = np.asarray(classes)

        if len(classes.shape) != 2:
            raise InputError("classes should be an array with 2 dimensions. Got %s" % (len(classes.shape)))
        approved_classes = classes

    return approved_classes

# ------------ ** Utility functions ** ----------------

def get_unique(x):
    """
    Gets all unique elements in lists of lists
    """
    elements = list(set(item for l in x for item in l))
    return sorted(elements)

def get_pairs(x):
    """
    Get all unique pairs. E.g. x = [1,2,3] will return
    [[1, 1], [1, 2], [1, 3], [2, 2], [2, 3], [3, 3]]
    """
    pairs = []
    for i,v in enumerate(x):
        for w in x[i:]:
            pairs.append([v,w])
    return pairs


# Custom exception to raise when we intentinoally catch an error
# This way we can test that the right error was raised in test cases
class InputError(Exception):
    pass
    #def __init__(self, msg, loc):
    #    self.msg = msg
    #    self.loc = loc
    #def __str__(self):
    #    return repr(self.msg)

def ceil(a, b):
    """
    Returns a/b rounded up to nearest integer.

    """
    return -(-a//b)

def get_batch_size(batch_size, n_samples):

    if batch_size > n_samples:
        print("Warning: batch_size larger than sample size. It is going to be clipped")
        return min(n_samples, batch_size)

    # see if the batch size can be modified slightly to make sure the last batch is similar in size
    # to the rest of the batches
    # This is always less that the requested batch size, so no memory issues should arise

    better_batch_size = ceil(n_samples, ceil(n_samples, batch_size))
    return better_batch_size

