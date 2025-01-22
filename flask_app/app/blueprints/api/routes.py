import numpy as np
from flask import Blueprint, request, jsonify

from IterSolverLib.itersolvers import IterSolverFacade
from flask_app.app.blueprints.exceptions.exceptions import ValidationError
from flask_app.app.utils.mtx_utils import read_mtx_file
from flask_app.app.validator.solver_request_validator import SolverRequestValidator

api = Blueprint('api', __name__)

@api.route('/apply', methods=['POST'])
def upload_file():
    try:
        solver_request_validator = SolverRequestValidator(request)
        solver_request_validator.validate()

        file = request.files['file']
        tolerance_number = request.form.get('tolerance_number')
        tolerance_scientific = request.form.get('tolerance_scientific')
        tolerance = tolerance_number if tolerance_number else tolerance_scientific
        iteration = request.form.get('iteration')
        method = request.form.get('methodList')

        tolerance_value = float(tolerance)
        iteration_value = int(iteration)
        A = read_mtx_file(file)
        b = A.dot(np.ones(A.shape[1]))

        solver = IterSolverFacade()
        solver.set_solver(method)
        solution = solver.solve(A, b, tolerance_value, iteration_value)

        print(f'File processed successfully with solution {solution}')
    except ValidationError as validation_error:
        raise
    except Exception as exception:
        print(str(exception))
        raise

    return jsonify({"message": "IterSolver successfully executed!"}), 200