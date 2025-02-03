from io import BytesIO
from PIL import Image
import numpy as np

from image_compression.dct_processor import DCTProcessor
from image_compression.image_block_manager import ImageBlockManager


class ImageProcessor:
    def __init__(self, block_size: int, frequency_threshold: int):
        self.dct_processor = DCTProcessor(block_size, frequency_threshold)
        self.block_manager = ImageBlockManager(block_size)

    def process_image(self, image_stream) -> BytesIO:
        image = Image.open(image_stream).convert('L')
        image_array = np.array(image)

        blocks = self.block_manager.split_into_blocks(image_array)

        processed_blocks = [
            (i, j, self.dct_processor.process_block(block))
            for i, j, block in blocks
        ]

        new_image_array = self.block_manager.reconstruct_image(processed_blocks, image_array.shape)
        new_image = Image.fromarray(new_image_array.astype(np.uint8))

        img_io = BytesIO()
        new_image.save(img_io, format='BMP')
        img_io.seek(0)
        return img_io