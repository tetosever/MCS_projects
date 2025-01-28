import numpy as np
from scipy.fftpack import dct, idct

def apply_dct2(block):
    """Apply 2D Discrete Cosine Transform to a block."""
    return dct(dct(block.T, norm='ortho').T, norm='ortho')

def apply_idct2(block):
    """Apply Inverse 2D Discrete Cosine Transform to a block."""
    return idct(idct(block.T, norm='ortho').T, norm='ortho')

def process_block(block, frequency_threshold):
    """
    Process a single block:
    - Apply DCT2.
    - Remove frequencies where k + l >= threshold.
    - Apply IDCT2.
    """
    dct_block = apply_dct2(block)
    size = block.shape[0]
    for k in range(size):
        for l in range(size):
            if k + l >= frequency_threshold:
                dct_block[k, l] = 0
    idct_block = apply_idct2(dct_block)
    return np.clip(np.rint(idct_block), 0, 255)  # Normalize values
