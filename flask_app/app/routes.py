from flask import Blueprint, render_template, request, redirect, url_for, flash
from werkzeug.utils import secure_filename
import numpy as np
import scipy.io
import io
from IterSolverLib.itersolvers.iter_solver_facade import IterSolverFacade

main = Blueprint('main', __name__)

ALLOWED_EXTENSIONS = {'mtx'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def read_mtx_file(file_storage):
    try:
        A = scipy.io.mmread(file_storage).tocsc()
        if not np.issubdtype(A.dtype, np.number):
                raise ValueError("The matrix contains non-numeric data")
        else:
            print(f"Matrix loaded successfully with shape {A.shape}")
        return A
    except Exception as e:
        raise ValueError(f"Error reading the matrix file: {str(e)}")

def check_input(file, tolerance, iteration):
    if file.filename == '':
        return "No file selected"
    if not allowed_file(file.filename):
        return "File type not allowed"
    try:
        tolerance_value = float(tolerance)
        iteration_value = int(iteration)
    except ValueError:
        return "Invalid tolerance or iteration value"
    return None

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/apply', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        flash("No file part")
        return redirect(request.url)

    file = request.files['file']
    tolerance_number = request.form.get('tolerance_number')
    tolerance_scientific = request.form.get('tolerance_scientific')
    tolerance = tolerance_number if tolerance_number else tolerance_scientific
    iteration = request.form.get('iteration')
    method = request.form.get('methodList')

    error = check_input(file, tolerance, iteration)
    if error:
        flash(error)
        return redirect(request.url)

    try:
        tolerance_value = float(tolerance)
        iteration_value = int(iteration)
        A = read_mtx_file(file)        
        b = A.dot(np.ones(A.shape[1]))
        
        solver = IterSolverFacade()
        solver.set_solver(method)
        solution = solver.solve(A, b, tolerance_value, iteration_value)
        
        print(f'File processed successfully with solution {solution}')
    except Exception as e:
        print(str(e))
        return redirect(request.url)

    return redirect(url_for('main.index'))
