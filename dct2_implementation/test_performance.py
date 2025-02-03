import time

import numpy as np
from matplotlib import pyplot as plt

from dct2_implementation.dct_fast import DCTFast
from dct2_implementation.dct_manual import DCTManual


class DCTPerformanceTester:
    def __init__(self):
        self.dct_manual = DCTManual()
        self.dct_fast = DCTFast()

    def plot_results(self, sizes, manual_times, fast_times):
        plt.figure(figsize=(10, 6))
        plt.plot(sizes, manual_times, 'o-', label="Manual DCT2")
        plt.plot(sizes, fast_times, 's-', label="Fast DCT2 (SciPy)")
        plt.xlabel("Dimensione (NxN)")
        plt.ylabel("Tempo di esecuzione (secondi)")
        plt.title("Confronto delle prestazioni tra Manual DCT2 e Fast DCT2")
        plt.legend()
        plt.grid(True)
        plt.show()

    def test_performance(self):
        sizes = [8, 16, 32, 64, 128, 256, 512]
        manual_times = []
        fast_times = []

        for size in sizes:
            image = np.random.rand(size, size) * 255

            start = time.time()
            self.dct_manual.dct2_manual(image)
            manual_time = time.time() - start
            manual_times.append(manual_time)
            print(f"Manual DCT2 for size {size} took {manual_time:.6f} seconds.")

            start = time.time()
            self.dct_fast.dct2_fast(image)
            fast_time = time.time() - start
            fast_times.append(fast_time)
            print(f"Fast DCT2 (SciPy) for size {size} took {fast_time:.6f} seconds.")

        self.plot_results(sizes, manual_times, fast_times)