import numpy as np


def precompute_dct_matrix(N):
    """Precompute the DCT transformation matrix."""
    factor = np.pi / (2 * N)
    dct_matrix = np.zeros((N, N))

    for k in range(N):
        for n in range(N):
            dct_matrix[k, n] = np.cos((2 * n + 1) * k * factor)

    # Apply normalization factors
    dct_matrix *= np.sqrt(2 / N)
    dct_matrix[0, :] *= np.sqrt(1 / 2)

    return dct_matrix

def dct2_manual(image):
    """Compute 2D DCT using precomputed DCT matrix."""
    N, M = image.shape
    dct_matrix_N = precompute_dct_matrix(N)
    dct_matrix_M = precompute_dct_matrix(M)

    # Compute DCT for rows and then for columns
    dct_rows = dct_matrix_N @ image @ dct_matrix_M.T
    return dct_rows

def idct2_manual(image):
    """Compute 2D inverse DCT using precomputed matrices."""
    N, M = image.shape
    dct_matrix_N = precompute_dct_matrix(N)
    dct_matrix_M = precompute_dct_matrix(M)

    # Compute inverse DCT for rows and then for columns
    idct_rows = dct_matrix_N.T @ image @ dct_matrix_M
    return idct_rows
