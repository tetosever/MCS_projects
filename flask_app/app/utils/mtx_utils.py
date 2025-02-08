import numpy as np
import scipy.io
import io

ALLOWED_EXTENSIONS = {'mtx'}
MATRIX_MARKET_HEADER = "%%MatrixMarket matrix coordinate real general\n"

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def ensure_mtx_header(file_storage):
    file_storage.seek(0)
    first_line = file_storage.readline().decode("utf-8").strip()

    if first_line.startswith("%%MatrixMarket"):
        file_storage.seek(0)
        print("MatrixMarket header already present")
        return file_storage

    file_storage.seek(0)
    buffer = io.BytesIO()
    buffer.write(MATRIX_MARKET_HEADER.encode("utf-8"))
    buffer.write(file_storage.read())
    buffer.seek(0)
    print("MatrixMarket header added")

    return buffer

def read_mtx_file(file_storage):
    try:
        corrected_file = ensure_mtx_header(file_storage)
        A = scipy.io.mmread(corrected_file).tocsc()

        if not np.issubdtype(A.dtype, np.number):
            raise ValueError("The matrix contains non-numeric data")

        print(f"Matrix loaded successfully with shape {A.shape}")
        return A
    except Exception as e:
        raise ValueError(f"Error reading the matrix file: {str(e)}")
