import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import numpy as np
import pytest
from itersolvers.iter_solver_validator import IterSolverValidator

def test_validate_max_iter():
    IterSolverValidator.validate_max_iter(20000)
    
    with pytest.raises(ValueError, match="The maximum number of iterations must not be less than 20000"):
        IterSolverValidator.validate_max_iter(19999)

def test_validate_matrix_symmetric():
    A = np.array([[2, 1], [1, 2]])
    IterSolverValidator.validate_matrix(A)
    
    A = np.array([[2, 1], [3, 2]])
    with pytest.raises(ValueError, match="The matrix must be symmetrical"):
        IterSolverValidator.validate_matrix(A)

def test_validate_matrix_positive_definite():
    A = np.array([[2, -1], [-1, 2]])
    IterSolverValidator.validate_matrix(A)
    
    A = np.array([[1, 2], [2, 1]])
    with pytest.raises(ValueError, match="The matrix must be defined as positive"):
        IterSolverValidator.validate_matrix(A)

def test_validate_compatible_dimensions():
    A = np.array([[2, 1], [1, 2]])
    b = np.array([1, 2])
    IterSolverValidator.validate(A, b, 20000)
    
    b = np.array([1, 2, 3])
    with pytest.raises(ValueError, match="The dimension of the vector b must be compatible with the matrix A"):
        IterSolverValidator.validate(A, b, 20000)

def test_validate_all():
    A = np.array([[2, -1], [-1, 2]])
    b = np.array([1, 2])
    max_iter = 20000
    IterSolverValidator.validate(A, b, max_iter)
    
    with pytest.raises(ValueError, match="The maximum number of iterations must not be less than 20000"):
        IterSolverValidator.validate(A, b, 19999)
    
    A_non_sym = np.array([[2, 1], [3, 2]])
    with pytest.raises(ValueError, match="The matrix must be symmetrical"):
        IterSolverValidator.validate(A_non_sym, b, max_iter)
    
    A_non_pos_def = np.array([[1, 2], [2, 1]])
    with pytest.raises(ValueError, match="The matrix must be defined as positive"):
        IterSolverValidator.validate(A_non_pos_def, b, max_iter)
    
    b_non_compat = np.array([1, 2, 3])
    with pytest.raises(ValueError, match="The dimension of the vector b must be compatible with the matrix A"):
        IterSolverValidator.validate(A, b_non_compat, max_iter)

