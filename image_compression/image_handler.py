import numpy as np
from PIL import Image
from io import BytesIO
from image_compression.dct_processor import process_block

def split_into_blocks(image, block_size):
    """Split an image into non-overlapping blocks of size block_size x block_size."""
    h, w = image.shape
    blocks = []
    for i in range(0, h - block_size + 1, block_size):
        for j in range(0, w - block_size + 1, block_size):
            blocks.append((i, j, image[i:i+block_size, j:j+block_size]))
    return blocks

def reconstruct_image(blocks, image_shape, block_size):
    """Reconstruct an image from processed blocks."""
    h, w = image_shape
    new_image = np.zeros((h, w), dtype=np.uint8)
    for i, j, block in blocks:
        new_image[i:i+block_size, j:j+block_size] = block
    return new_image

def process_image(image_stream, block_size, frequency_threshold):
    """
    Full pipeline: Load, process blocks, and return the image as a byte stream.
    """
    # Load image from memory stream
    image = Image.open(image_stream).convert('L')  # Convert to grayscale
    image_array = np.array(image)

    # Process blocks
    blocks = split_into_blocks(image_array, block_size)
    processed_blocks = [
        (i, j, process_block(block, frequency_threshold))
        for i, j, block in blocks
    ]

    # Reconstruct image
    new_image_array = reconstruct_image(processed_blocks, image_array.shape, block_size)
    new_image = Image.fromarray(new_image_array.astype('uint8'))

    # Save image to memory buffer
    img_io = BytesIO()
    new_image.save(img_io, format='BMP')
    img_io.seek(0)

    return img_io  # Return the image stream
