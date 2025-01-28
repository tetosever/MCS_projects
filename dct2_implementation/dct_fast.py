from scipy.fftpack import dct, idct

def dct2_fast(image):
    """Compute 2D DCT using SciPy's optimized function."""
    return dct(dct(image.T, norm='ortho').T, norm='ortho')

def idct2_fast(image):
    """Compute 2D inverse DCT using SciPy's optimized function."""
    return idct(idct(image.T, norm='ortho').T, norm='ortho')