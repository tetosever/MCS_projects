import numpy as np
import scipy

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

#TODO: aggiungere in automatico l'inserimento della stringa per la lettura del file .mtx
