import numpy as np
from PIL import Image
from io import BytesIO
from image_compression.dct_processor import process_block

'''
def pad_image(image, block_size):
    """Aggiunge padding ai bordi per rendere l'immagine divisibile per block_size."""
    h, w = image.shape
    new_h = ((h + block_size - 1) // block_size) * block_size
    new_w = ((w + block_size - 1) // block_size) * block_size

    # Aggiunge padding replicando i bordi
    padded_image = np.pad(image,
                          ((0, new_h - h), (0, new_w - w)),
                          mode='edge')

    return padded_image, (h, w)  # Ritorna anche la dimensione originale


def split_into_blocks(image, block_size):
    """Divide un'immagine in blocchi non sovrapposti di dimensione block_size x block_size."""
    h, w = image.shape
    blocks = []
    for i in range(0, h, block_size):
        for j in range(0, w, block_size):
            blocks.append((i, j, image[i:i + block_size, j:j + block_size]))
    return blocks

def reconstruct_image(blocks, image_shape, block_size):
    """Ricostruisce l'immagine dai blocchi processati."""
    h, w = image_shape
    new_image = np.zeros((h, w), dtype=np.uint8)

    for i, j, block in blocks:
        new_image[i:i+block_size, j:j+block_size] = block

    return new_image

def remove_padding(image, original_size):
    """Rimuove il padding per ripristinare la dimensione originale."""
    h, w = original_size
    return image[:h, :w]

def process_image(image_stream, block_size, frequency_threshold):
    """
    Pipeline completa:
    - Carica l'immagine
    - Aggiunge il padding
    - Divide in blocchi ed elabora con la DCT
    - Ricostruisce l'immagine
    - Rimuove il padding e salva il risultato
    """
    # Carica l'immagine e converte in scala di grigi
    image = Image.open(image_stream).convert('L')
    image_array = np.array(image)

    # Aggiungi il padding
    padded_image, original_size = pad_image(image_array, block_size)

    # Processa i blocchi
    blocks = split_into_blocks(padded_image, block_size)
    processed_blocks = [(i, j, process_block(block, frequency_threshold)) for i, j, block in blocks]

    # Ricostruisce l'immagine dai blocchi
    new_image_array = reconstruct_image(processed_blocks, padded_image.shape, block_size)

    # Rimuove il padding per riportare l'immagine alla dimensione originale
    new_image_array = remove_padding(new_image_array, original_size)

    # Salva il risultato in BMP
    new_image = Image.fromarray(new_image_array.astype('uint8'))
    img_io = BytesIO()
    new_image.save(img_io, format='BMP')
    img_io.seek(0)

    return img_io  # Ritorna l'immagine come stream di byte
'''

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