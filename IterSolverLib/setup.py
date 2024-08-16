from setuptools import setup, find_packages

setup(
    name="IterSolverLib",
    version="0.1.0",
    setup_requires=['setuptools_scm'],
    packages=find_packages(),
    install_requires=[
        "numpy",
        "scipy",
    ],
    extras_require={
        "dev": [
            "pytest",
        ],
    },
    author="Matteo Severgnini",
    author_email="severgnini.matteo.00@gmail.com",
    description="Library for symmetrical and positive definite linear systems",
    long_description=open('README.md').read(),  # Aggiungi una descrizione lunga dal README
    long_description_content_type="text/markdown",  # Specifica il tipo di contenuto del long_description
    url="https://github.com/tetosever/MCS_project_1.git",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',  # Specifica la versione minima di Python
)
