from flask_app.app.blueprints.exceptions.exceptions import ValidationError
from flask_app.app.utils.mtx_utils import allowed_file

class SolverRequestValidator:
    def __init__(self, request):
        self.request = request
        self.errors = []

    def validate(self):
        self.choose_file_validate()
        self.input_validate()

        if self.errors:
            raise ValidationError(self.errors)

    def choose_file_validate(self):
        if 'file' not in self.request.files:
            self.errors.append("No file part")

    def input_validate(self):
        file = self.request.files['file']
        tolerance_number = self.request.form.get('tolerance_number')
        tolerance_scientific = self.request.form.get('tolerance_scientific')
        tolerance = tolerance_number if tolerance_number else tolerance_scientific
        iteration = self.request.form.get('iteration')
        method = self.request.form.get('methodList')

        self.file_validate(file)
        self.iteration_validate(iteration)
        self.tolerance_validate(tolerance)
        self.method_validate(method)

    def file_validate(self, file):
        if not file or file.filename == '':
            self.errors.append("No file selected")
        elif not allowed_file(file.filename):
            self.errors.append("File type not allowed")

    def tolerance_validate(self, tolerance):
        try:
            float(tolerance)
        except ValueError:
            self.errors.append("Invalid tolerance value")

    def iteration_validate(self, iteration):
        try:
            int(iteration)
        except ValueError:
            self.errors.append("Invalid iteration value")

    def method_validate(self, method):
        if method not in ['jacobi', 'gauss_seidel', 'gradient', 'coniugate_gradient']:
            self.errors.append("Invalid method selected")