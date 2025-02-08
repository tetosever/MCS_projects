class ImageCompressionValidator:
    def __init__(self, file, block_size, frequency_threshold):
        self.file = file
        self.block_size = block_size
        self.frequency_threshold = frequency_threshold
        self.errors = []

    def validate(self):
        self.validate_file(self.file)
        self.validate_parameters(self.block_size, self.frequency_threshold)

        if self.errors:
            raise ValueError(self.errors)

    def validate_file(self,file):
        if file is None:
            self.errors.append("No image file provided.")
        elif file.filename == '':
            self.errors.append("No selected file.")
        elif not file.filename.lower().endswith('.bmp'):
            self.errors.append("Only .bmp files are supported.")

    def validate_parameters(self, block_size, frequency_threshold):
        """ Validate block_size and frequency_threshold parameters. """
        if not isinstance(block_size, int) or block_size <= 0:
            self.errors.append("Block size must be a positive integer.")
        if not isinstance(frequency_threshold, int) or frequency_threshold < 0 or frequency_threshold >= 2 * block_size - 1:
            self.errors.append("Frequency threshold must be between 0 and (2F-2).")