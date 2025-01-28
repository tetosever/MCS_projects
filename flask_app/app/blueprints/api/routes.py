import json
from PIL import Image
from flask import Blueprint, request, jsonify, send_file
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

    image_processed, image_processed_size = ImageCompressionService().process_image(image_processing_input)
    print("DEBUG - Dimensione immagine compressa:", image_processed_size, "KB")

    response = send_file(image_processed, mimetype='image/bmp')

    response.headers["X-Compressed-Size-KB"] = image_processed_size

    return response

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