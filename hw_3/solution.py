from numpy.random import randint, seed
from matrix import Matrix, Matrix_np
from inspect import cleandoc
import unittest


seed(0)
m1 = randint(0, 10, (10, 10))
m2 = randint(0, 10, (10, 10))
m3 = randint(0, 10, (11, 10))
dir = 'artifacts/'


class TestMatrix(unittest.TestCase):
    def test_add(self):
        my_m = Matrix(m1) + Matrix(m2)
        np_m = Matrix_np(m1) + Matrix_np(m2)
        self.assertRaises(ValueError, Matrix.__add__, m1, m3)
        m = m1 + m2
        for i in range(10):
            for j in range(10):
                self.assertEqual(m[i][j], my_m[i, j])
                self.assertEqual(m[i][j], np_m[i, j])
        my_m.write('matrix+.txt', dir)
        np_m.write('matrix_np+.txt', dir)

    def test_mul(self):
        my_m = Matrix(m1) * Matrix(m2)
        np_m = Matrix_np(m1) * Matrix_np(m2)
        self.assertRaises(ValueError, Matrix.__mul__, m1, m3)
        self.assertRaises(ValueError, Matrix.__mul__, m3, m1)
        m = m1 * m2
        for i in range(10):
            for j in range(10):
                self.assertEqual(m[i][j], my_m[i, j])
                self.assertEqual(m[i][j], np_m[i, j])
        my_m.write('matrix*.txt', dir)
        np_m.write('matrix_np*.txt', dir)

    def test_matmul(self):
        my_m = Matrix(m1) @ Matrix(m2)
        np_m = Matrix_np(m1) @ Matrix_np(m2)
        self.assertRaises(ValueError, Matrix.__matmul__, m1, m3)
        try:
            m3 @ m1
        except ValueError:
            raise AssertionError('Those matrices should be able to matmul')
        m = m1 @ m2
        for i in range(10):
            for j in range(10):
                self.assertEqual(m[i][j], my_m[i, j])
                self.assertEqual(m[i][j], np_m[i, j])
        my_m.write('matrix@.txt', dir)
        np_m.write('matrix_np@.txt', dir)

    def test_cachedResult(self):
        data = [[[1, 1]], [[1], [1]], [[1, 0]], [[1], [1]]]
        A, B, C, D = (Matrix(mat) for mat in data)
        self.assertTrue(hash(A) == hash(C))
        self.assertTrue((A != C))
        self.assertTrue((B == D))
        real_C, real_D = Matrix_np(data[2]), Matrix_np(data[3])
        self.assertTrue(A @ B != real_C @ real_D)
        for mat, name in zip(
            [A, B, C, D, A @ B, real_C @ real_D],
            ['A', 'B', 'C', 'D', 'AB', 'CD']
        ):
            mat.write(f'{name}.txt', dir)
        with open(f'{dir}hash.txt', 'w') as fout:
            fout.write(cleandoc(
                rf"""
                hash of AB: {hash(A @ B)}
                hash of CD: {hash(real_C @ real_D)}
                """
            ))


if __name__ == '__main__':
    unittest.main()
