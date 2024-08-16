import numpy as np

class IterSolverValidator:
    @staticmethod
    def validate_max_iter(max_iter):
        if max_iter < 20000:
            raise ValueError("The maximum number of iterations must not be less than 20000")
        print("Maximum iterations validated.")

    @staticmethod
    def validate_numeric(A):
        if not np.issubdtype(A.dtype, np.number):
            raise ValueError("The matrix contains non-numeric data types.")
        print("Matrix is numeric.")

    @staticmethod
    def validate_finite(A):
        if not np.all(np.isfinite(A.toarray())):
            raise ValueError("The matrix contains non-finite values (NaN or Inf).")
        print("All matrix elements are finite.")

    @staticmethod
    def validate_symmetry(A):
        if not np.allclose(A.toarray(), A.T.toarray()):
            raise ValueError("The matrix must be symmetrical.")
        print("Matrix is symmetrical.")

    @staticmethod
    def is_positive_definite(A):
        try:
            np.linalg.cholesky(A.toarray())
            print("Matrix is positive definite.")
            return True
        except np.linalg.LinAlgError:
            raise ValueError("The matrix is not positive definite.")

    @staticmethod
    def validate_matrix(A):
        IterSolverValidator.validate_numeric(A)
        IterSolverValidator.validate_finite(A)
        IterSolverValidator.validate_symmetry(A)
        if not IterSolverValidator.is_positive_definite(A):
            raise ValueError("The matrix must be positive definite.")

    @staticmethod
    def validate(A, b, max_iter):
        IterSolverValidator.validate_max_iter(max_iter)
        IterSolverValidator.validate_matrix(A)
        if A.shape[0] != b.shape[0]:
            raise ValueError("The dimension of the vector b must be compatible with the matrix A")
        print("All validations passed.")
