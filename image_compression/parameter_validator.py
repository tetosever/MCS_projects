
class ParameterValidator:
    @staticmethod
    def validate_parameters(block_size, frequency_threshold):
        if not isinstance(block_size, int) or block_size <= 0:
            raise ValueError("Block size must be a positive integer.")

        if not isinstance(frequency_threshold, int) or not (0 <= frequency_threshold <= 2 * block_size - 2):
            raise ValueError(f"Frequency threshold must be an integer between 0 and {2 * block_size - 2} (inclusive).")

