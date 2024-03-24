from matrix.util import handleEqualShape, handleMatMulShape
from numpy.lib.mixins import NDArrayOperatorsMixin
from dataclasses import dataclass


class MatrixMixin:

    cache = {}

    def __init__(self, mat):
        if mat is None:
            raise ValueError('matrix is not provided')
        self._data = mat

    def __getitem__(self, key):
        i, j = key
        return self._data[i][j]

    @property
    def shape(self):
        return (len(self._data), len(self._data[0]))

    def __setitem__(self, key, value):
        i, j = key
        self._data[i][j] = value

    def __str__(self):
        n, m = self.shape
        return '\n'.join(
            ' '.join(str(self[i, j]) for j in range(m)) for i in range(n)
        )

    def write(self, filename, dir):
        with open(dir + filename, 'w') as fout:
            fout.write(str(self))

    def __hash__(self):
        return int(self[0, 0])

    def handleCacheKey(self, key):
        if key not in self.cache:
            self.cache[key] = CachedResult()

    def __eq__(self, other):
        try:
            handleEqualShape(self, other)
        except ValueError:
            return False
        n, m = self.shape
        for i in range(n):
            for j in range(m):
                if self[i, j] != other[i, j]:
                    return False
        return True


class Matrix(MatrixMixin):
    def __add__(self, other):
        handleEqualShape(self, other)
        key = (hash(self), hash(other))
        self.handleCacheKey(key)
        if self.cache[key].add is None:
            n, m = self.shape
            self.cache[key].add = Matrix(
                [
                    [self[i, j] + other[i, j] for j in range(m)]
                    for i in range(n)
                ]
            )
        return self.cache[key].add

    def __mul__(self, other):
        handleEqualShape(self, other)
        key = (hash(self), hash(other))
        self.handleCacheKey(key)
        if self.cache[key].mul is None:
            n, m = self.shape
            self.cache[key].mul = Matrix(
                [
                    [self[i, j] * other[i, j] for j in range(m)]
                    for i in range(n)
                ]
            )
        return self.cache[key].mul

    def __matmul__(self, other):
        handleMatMulShape(self, other)
        key = (hash(self), hash(other))
        self.handleCacheKey(key)
        if self.cache[key].matmul is None:
            n, k, m = *self.shape, other.shape[1]
            self.cache[key].matmul = Matrix(
                [
                    [
                        sum(self[i, _] * other[_, j] for _ in range(k))
                        for j in range(m)
                    ]
                    for i in range(n)
                ]
            )
        return self.cache[key].matmul


@dataclass
class CachedResult:
    add: Matrix = None
    mul: Matrix = None
    matmul: Matrix = None


class Matrix_np(MatrixMixin, NDArrayOperatorsMixin):
    def __array_ufunc__(self, ufunc, method, *inputs, **kwargs):
        out = kwargs.get('out', ())
        # Defer to the implementation of the ufunc
        # on unwrapped values.
        inputs = tuple(
            x._data if isinstance(x, Matrix_np) else x for x in inputs
        )
        if out:
            kwargs['out'] = tuple(
                x._data if isinstance(x, Matrix_np) else x for x in out
            )
        result = getattr(ufunc, method)(*inputs, **kwargs)

        if type(result) is tuple:
            # multiple return values
            return tuple(type(self)(x) for x in result)
        elif method == 'at':
            # no return value
            return None
        else:
            # one return value
            return type(self)(result)
