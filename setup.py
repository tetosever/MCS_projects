from setuptools import setup, find_packages

setup(
    name="IterSolverLib",
    use_scm_version=True,
    setup_requires=['setuptools_scm'],
    packages=find_packages(),
    install_requires=[
        "numpy",
        "setuptools",
        "setuptools_scm",
        "scipy"
    ],
    extras_require={
        "dev": [
            "pytest",
        ],
    },
    author="Matteo Severgnini",
    author_email="severgnini.matteo.00@gmail.com",
    description="Library for symmetrical and positive definite linear systems",
    url="https://github.com/tetosever/IterSolverLib.git",
)