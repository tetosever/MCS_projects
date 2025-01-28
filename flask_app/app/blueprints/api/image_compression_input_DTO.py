class ImageCompressionInputDTO:
    def __init__(self, file, block_size, frequency_threshold):
        self.set_file(file)
        self.set_block_size(block_size)
        self.set_frequency_threshold(frequency_threshold)

    def get_file(self):
        return self.file

    def set_file(self, file):
        self.file = file

    def get_block_size(self):
        return self.block_size

    def set_block_size(self, block_size):
        self.block_size = block_size

    def get_frequency_threshold(self):
        return self.frequency_threshold

    def set_frequency_threshold(self, frequency_threshold):
        self.frequency_threshold = frequency_threshold

    def __repr__(self):
        return (f"ImageCompressionInputDTO(file={self.file.filename}, block_size={self.block_size}, "
                f"frequency_threshold={self.frequency_threshold})")