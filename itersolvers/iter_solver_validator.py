import numpy as np

class IterSolverValidator:
    @staticmethod
    def validate_max_iter(max_iter):
        if max_iter < 20000:
            raise ValueError("The maximum number of iterations must not be less than 20000")

    @staticmethod
    def validate_matrix(A):
        if not np.allclose(A, A.T):
            raise ValueError("The matrix must be symmetrical")
        
        if not IterSolverValidator.is_positive_definite(A):
            raise ValueError("The matrix must be defined as positive")

    @staticmethod
    def is_positive_definite(A):
        try:
            np.linalg.cholesky(A)
            return True
        except np.linalg.LinAlgError:
            return False

    @staticmethod
    def validate(A, b, max_iter):
        IterSolverValidator.validate_max_iter(max_iter)
        IterSolverValidator.validate_matrix(A)
        if A.shape[0] != b.shape[0]:
            raise ValueError("The dimension of the vector b must be compatible with the matrix A")
