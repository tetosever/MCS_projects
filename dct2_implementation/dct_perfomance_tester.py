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

        self.test_dct_correctness()

        return self.plot_results(sizes, manual_times, fast_times)

    def test_dct_correctness(self):
        test_block = np.array([
            [231, 32, 233, 161, 24, 71, 140, 245],
            [247, 40, 248, 245, 124, 204, 36, 107],
            [234, 202, 245, 167, 9, 217, 239, 173],
            [193, 190, 100, 167, 43, 180, 8, 70],
            [11, 24, 210, 177, 81, 243, 8, 112],
            [97, 195, 203, 47, 125, 114, 165, 181],
            [193, 70, 174, 167, 41, 30, 127, 245],
            [87, 149, 57, 192, 65, 129, 178, 228]
        ])

        expected_dct2 = np.array([
            [1.11e+03, 4.40e+01, 7.59e+01, -1.38e+02, 3.50e+00, 1.22e+02, 1.95e+02, -1.01e+02],
            [7.71e+01, 1.14e+02, -2.18e+01, 4.13e+01, 8.77e+00, 9.90e+01, 1.38e+02, 1.09e+01],
            [4.48e+01, -6.27e+01, 1.11e+02, -7.63e+01, 1.24e+02, 9.55e+01, -3.98e+01, 5.85e+01],
            [-6.99e+01, -4.02e+01, -2.34e+01, -7.67e+01, 2.66e+01, -3.68e+01, 6.61e+01, 1.25e+02],
            [-1.09e+02, -4.33e+01, -5.55e+01, 8.17e+00, 3.02e+01, -2.86e+01, 2.44e+00, -9.41e+01],
            [-5.38e+00, 5.66e+01, 1.73e+02, -3.54e+01, 3.23e+01, 3.34e+01, -5.81e+01, 1.90e+01],
            [7.88e+01, -6.45e+01, 1.18e+02, -1.50e+01, -1.37e+02, -3.06e+01, -1.05e+02, 3.98e+01],
            [1.97e+01, -7.81e+01, 9.72e-01, -7.23e+01, -2.15e+01, 8.13e+01, 6.37e+01, 5.90e+00]
        ])

        dct_manual_result = self.dct_manual.dct2_manual(test_block)
        print("DCT-2 Manuale:")
        print(dct_manual_result)
        print("\n")

        dct_fast_result = self.dct_fast.dct2_fast(test_block)
        print("DCT-2 Fast:")
        print(dct_fast_result)
        print("\n")

        error_manual = np.abs(dct_manual_result - expected_dct2).mean()
        error_fast = np.abs(dct_fast_result - expected_dct2).mean()

        print(f"Errore medio (DCT Manuale): {error_manual:.4f}")
        print(f"Errore medio (DCT Veloce): {error_fast:.4f}")

        expected_dct1d = np.array([4.01e+02, 6.60e+00, 1.09e+02, -1.12e+02, 6.54e+01, 1.21e+02, 1.16e+02, 2.88e+01])

        dct_matrix_8 = self.dct_manual.precompute_dct_matrix(8)
        dct1d_manual_result = dct_matrix_8 @ test_block[0, :]
        print("DCT-1D Manuale sulla prima riga:")
        print(dct1d_manual_result)
        print("\n")

        error_1d_manual = np.abs(dct1d_manual_result - expected_dct1d).mean()
        print(f"Errore medio (DCT-1D Manuale sulla prima riga): {error_1d_manual:.4f}")

