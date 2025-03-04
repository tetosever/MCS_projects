import base64
import io
import json

from PIL import Image
from flask import Blueprint, request, jsonify, send_file

from dct2_implementation.dct_perfomance_tester import DCTPerformanceTester
from flask_app.app.blueprints.api.image_compression_input_DTO import ImageCompressionInputDTO
from flask_app.app.blueprints.api.itersolver_input_DTO import IterSolverInputDTO
from flask_app.app.services.image_compression_service import ImageCompressionService
from flask_app.app.services.itersolver_service import IterSolverService
from flask_app.app.validator.image_compression_validator import ImageCompressionValidator
from flask_app.app.validator.solver_request_validator import SolverRequestValidator

api = Blueprint('api', __name__)

@api.route('/apply', methods=['POST'])
def upload_files():
    try:
        solver_inputs = parse_solver_inputs()

        for solver_input in solver_inputs:
            solver_request_validator = SolverRequestValidator(solver_input.file,
                                                              solver_input.tolerance,
                                                              solver_input.max_iterations,
                                                              solver_input.method)
            solver_request_validator.validate()

        itersolver_service = IterSolverService()
        results = itersolver_service.solve(solver_inputs)

        return jsonify({
            "message": "IterSolver eseguiti con successo!",
            "results": [result.to_json() for result in results],
            "images": itersolver_service.generate_plots(results)
        }), 200
    except Exception as exception:
        print("DEBUG - Errore:", str(exception))
        raise exception

@api.route('/process_image', methods=['POST'])
def process_image():
    image_processing_input = parse_image_processing_input()

    image_processed = ImageCompressionService().process_image(image_processing_input)

    print("DEBUG - Dimensione immagine originale:", round(get_file_size(image_processing_input.get_file()) / 1024, 2), "KB")
    print("DEBUG - Dimensione immagine processata:", round(get_file_size(image_processed) / 1024, 2), "KB")

    response = send_file(image_processed, mimetype='image/bmp')

    return response

@api.route('/test_dct2', methods=['GET'])
def test_dct2():
    performance_tester = DCTPerformanceTester()
    img_stream = performance_tester.test_performance()
    img_stream.seek(0)

    base64_image = base64.b64encode(img_stream.read()).decode('utf-8')

    return jsonify({'manualImplementationDCT': base64_image})

def parse_solver_inputs():
    data_list = json.loads(request.form.get("data"))
    files_dict = {key: request.files[key] for key in request.files if request.files[key].filename != "empty.txt"}

    print("DEBUG - Ricevuti file:", files_dict.keys())
    print("DEBUG - Ricevuti dati:", data_list)

    if len(data_list) != len(files_dict):
        raise ValueError("Numero di file e parametri non corrispondenti")

    solver_inputs = []
    for data in data_list:
        index = data["index"]
        file_key = f"file-{index}"

        if file_key not in files_dict:
            raise ValueError(f"File mancante per il form {index}")

        file = files_dict[file_key]
        solver_inputs.append(IterSolverInputDTO(
            index=index,
            file=file,
            tolerance=data["tolerance"],
            max_iterations=data["max_iterations"],
            method=data["method"]
        ))

    return sorted(solver_inputs, key=lambda itersolver_input_dto: itersolver_input_dto.index)

def parse_image_processing_input():
    image_processing_input = ImageCompressionInputDTO(request.files.get('image'),
                                                      int(request.form['block_size']),
                                                      int(request.form['frequency_threshold']))

    ImageCompressionValidator(image_processing_input.get_file(),
                              image_processing_input.get_block_size(),
                              image_processing_input.get_frequency_threshold()).validate()

    print("DEBUG - Ricevuti file:", image_processing_input.__repr__() + "\n")

    return image_processing_input

def get_file_size(img):
    """Calcola la dimensione dell'immagine in memoria senza salvarla su disco."""

    # Se l'oggetto è un `BytesIO`, resettare il cursore
    if isinstance(img, io.BytesIO):
        img.seek(0)
        size = len(img.getvalue())  # Metodo corretto per `BytesIO`
    else:
        # Se è un file standard, aprilo normalmente
        original_image = Image.open(img)
        print(f"DEBUG - Modalità colore originale: {original_image.mode}")

        # Converti in scala di grigi
        grayscale_image = original_image.convert("L")
        print(f"DEBUG - Modalità colore dopo conversione: {grayscale_image.mode}")

        # Salva l'immagine in un buffer
        img_io = io.BytesIO()
        grayscale_image.save(img_io, format="BMP")

        size = len(img_io.getvalue())  # Metodo corretto per ottenere la dimensione

    return size