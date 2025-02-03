import numpy as np

class ImageBlockManager:
    def __init__(self, block_size: int):
        self.block_size = block_size

    def split_into_blocks(self, image_array: np.ndarray) -> list:
        h, w = image_array.shape
        blocks = []
        for i in range(0, h - self.block_size + 1, self.block_size):
            for j in range(0, w - self.block_size + 1, self.block_size):
                block = image_array[i:i+self.block_size, j:j+self.block_size]
                blocks.append((i, j, block))
        return blocks

    def reconstruct_image(self, blocks: list, image_shape: tuple) -> np.ndarray:
        h, w = image_shape
        new_image = np.zeros((h, w), dtype=np.uint8)
        for i, j, block in blocks:
            new_image[i:i+self.block_size, j:j+self.block_size] = block
        return new_image
