import numpy as np
from scipy.fftpack import dct, idct

from image_compression.parameter_validator import ParameterValidator


class DCTProcessor:
    def __init__(self, block_size: int, frequency_threshold: int):
        ParameterValidator.validate_parameters(block_size, frequency_threshold)
        self.block_size = block_size
        self.frequency_threshold = frequency_threshold

    def apply_dct2(self, block: np.ndarray) -> np.ndarray:
        return dct(dct(block.T, norm='ortho').T, norm='ortho')

    def apply_idct2(self, block: np.ndarray) -> np.ndarray:
        return idct(idct(block.T, norm='ortho').T, norm='ortho')

    def process_block(self, block: np.ndarray) -> np.ndarray:
        if block.shape[0] != self.block_size or block.shape[1] != self.block_size:
            raise ValueError(f"Il blocco deve essere di dimensione {self.block_size}x{self.block_size}")

        dct_block = self.apply_dct2(block)
        for k in range(self.block_size):
            for l in range(self.block_size):
                if k + l >= self.frequency_threshold:
                    dct_block[k, l] = 0
        idct_block = self.apply_idct2(dct_block)
        return np.clip(np.rint(idct_block), 0, 255)
