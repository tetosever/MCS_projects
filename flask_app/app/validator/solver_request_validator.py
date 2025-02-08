from flask_app.app.blueprints.exceptions.exceptions import ValidationError
from flask_app.app.utils.mtx_utils import allowed_file

class SolverRequestValidator:
    def __init__(self, file, tolerance, iteration, method):
        self.file = file
        self.tolerance = tolerance
        self.iteration = iteration
        self.method = method
        self.errors = []

    def validate(self):
        self.file_validate(self.file)
        self.iteration_validate(self.iteration)
        self.tolerance_validate(self.tolerance)
        self.method_validate(self.method)

        if self.errors:
            raise ValidationError(self.errors)

    def file_validate(self, file):
        if not file or file.filename.strip() == '':
            self.errors.append("No file selected")
        elif not allowed_file(file.filename):
            self.errors.append("File type not allowed")

    def tolerance_validate(self, tolerance):
        if not tolerance:
            self.errors.append("Tolerance value is required")
            return
        try:
            float(tolerance)
        except ValueError:
            self.errors.append("Invalid tolerance value")

    def iteration_validate(self, iteration):
        if not iteration:
            self.errors.append("Iteration value is required")
            return
        try:
            int(iteration)
        except ValueError:
            self.errors.append("Invalid iteration value")

    def method_validate(self, method):
        valid_methods = {'jacobi', 'gauss_seidel', 'gradient', 'coniugate_gradient'}
        if method not in valid_methods:
            self.errors.append("Invalid method selected")
