import time
import numpy as np
from dct_manual import dct2_manual
from dct_fast import dct2_fast
from plot_results import plot_results

def test_performance():
    """Compare execution times of manual vs fast DCT2."""
    sizes = [8, 16, 32, 64, 128, 256, 512]
    manual_times = []
    fast_times = []

    for size in sizes:
        image = np.random.rand(size, size) * 255

        start = time.time()
        dct2_manual(image)
        manual_times.append(time.time() - start)
        print(f"Manual DCT2 for size {size} took {manual_times[-1]:.6f} seconds.")

        start = time.time()
        dct2_fast(image)
        fast_times.append(time.time() - start)
        print(f"Fast DCT2 (SciPy) for size {size} took {fast_times[-1]:.6f} seconds.")

    plot_results(sizes, manual_times, fast_times)