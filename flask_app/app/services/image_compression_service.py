from io import BytesIO
from PIL import Image
import numpy as np
from image_compression.image_handler import process_image

class ImageCompressionService:
    """
    Service class responsible for handling image compression logic.
    """

    def process_image(self, image_processing_input):
        """
        Process an image in-memory and return the compressed image as a byte stream.
        """
        # Process the image using DCT2
        image_processed = process_image(image_processing_input.get_file().stream,
                                        image_processing_input.get_block_size(),
                                        image_processing_input.get_frequency_threshold())

        processed_image_size = round(image_processed.tell() / 1024, 2)

        return image_processed, processed_image_size
