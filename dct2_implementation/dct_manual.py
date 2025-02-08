import numpy as np


class DCTManual:
    def __init__(self):
        pass

    def precompute_dct_matrix(self, N):
        factor = np.pi / (2 * N)
        dct_matrix = np.zeros((N, N))

        for k in range(N):
            for n in range(N):
                dct_matrix[k, n] = np.cos((2 * n + 1) * k * factor)

        dct_matrix *= np.sqrt(2 / N)
        dct_matrix[0, :] *= np.sqrt(1 / 2)

        return dct_matrix

    def dct2_manual(self, image):
        N, M = image.shape
        dct_matrix_N = self.precompute_dct_matrix(N)
        dct_matrix_M = self.precompute_dct_matrix(M)

        return dct_matrix_N @ image @ dct_matrix_M.T

    def idct2_manual(self, image):
        N, M = image.shape
        dct_matrix_N = self.precompute_dct_matrix(N)
        dct_matrix_M = self.precompute_dct_matrix(M)

        return dct_matrix_N.T @ image @ dct_matrix_M
