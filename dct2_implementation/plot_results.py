import matplotlib.pyplot as plt

def plot_results(sizes, manual_times, fast_times):
    """Plot the performance comparison between manual and fast DCT2."""
    plt.figure()
    plt.semilogy(sizes, manual_times, label='Manual DCT2')
    plt.semilogy(sizes, fast_times, label='Fast DCT2 (SciPy)')
    plt.xlabel('Matrix Size N')
    plt.ylabel('Execution Time (s)')
    plt.title('Performance Comparison of DCT2 Implementations')
    plt.legend()
    plt.grid()
    plt.show()