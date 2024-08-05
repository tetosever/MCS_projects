from setuptools import setup, find_packages

setup(
    name="mini_libreria_sistemi_lineari",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        "numpy",
    ],
    author="Il tuo nome",
    author_email="tuo.email@example.com",
    description="Mini libreria per sistemi lineari simmetrici e definiti positivi",
    url="https://github.com/tuo-username/mini_libreria_sistemi_lineari",
)