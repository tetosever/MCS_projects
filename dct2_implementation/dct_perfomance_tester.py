import io
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
        plt.xlabel("Dimensione (N x N)")
        plt.ylabel("Tempo di esecuzione (secondi)")
        plt.yscale("log")
        plt.title("Confronto prestazionale: Manual DCT2 vs Fast DCT2")
        plt.legend()
        plt.grid(True)

        # Salva il grafico in un buffer
        buf = io.BytesIO()
        plt.savefig(buf, format='png')
        buf.seek(0)
        plt.close()

        return buf

    def test_performance(self):
        sizes = [8, 16, 32, 64, 128, 256, 512, 1024, 2048]
        manual_times = []
        fast_times = []

        for size in sizes:
            image = np.random.rand(size, size) * 255

            start = time.time()
            self.dct_manual.dct2_manual(image)
            manual_times.append(time.time() - start)

            start = time.time()
            self.dct_fast.dct2_fast(image)
            fast_times.append(time.time() - start)

            print(f"Size {size}x{size}: Manual DCT2 = {manual_times[-1]:.6f}s, Fast DCT2 = {fast_times[-1]:.6f}s")

        return self.plot_results(sizes, manual_times, fast_times)