import numpy as np
from flask import Blueprint, request, jsonify

from IterSolverLib.itersolvers import IterSolverFacade
from flask_app.app.blueprints.exceptions.exceptions import ValidationError
from flask_app.app.services.itersolver_service import IterSolverService
from flask_app.app.utils.mtx_utils import read_mtx_file
from flask_app.app.validator.solver_request_validator import SolverRequestValidator

api = Blueprint('api', __name__)

@api.route('/apply', methods=['POST'])
def upload_file():
    try:
        file = request.files.get('file')
        tolerance_number = request.form.get('tolerance_number')
        tolerance_scientific = request.form.get('tolerance_scientific')
        tolerance = float(tolerance_number if tolerance_number else tolerance_scientific)
        iteration = int(request.form.get('iteration'))
        method = request.form.get('methodList')

        solver_request_validator = SolverRequestValidator(file, tolerance, iteration, method)
        solver_request_validator.validate()

        itersolver_service = IterSolverService()
        result = itersolver_service.solve(file, tolerance, iteration, method)

        return jsonify({
            "message": "IterSolver successfully executed!",
            "solution": result["solution"],
            "execution_time": result["execution_time"],
            "iterations": result["iterations"],
            "images": result["images"]
        }), 200
    except Exception as exception:
        print(str(exception))
        raise