# Intro
Il seguente progetto è un implementazione di metodi risolutivi iterativi per sistemi lineari. 
Sono presenti due cartelle principila:
* flask_app: una piccola webapp che è stata implementata con lo scopo di fornire un interfaccia grafica per la libraria implementata
* IterSolverLib: è la libreria dove sono stati effettivamente implementati i metodi risolutivi.

## IterSolverLib
The following library is intended to provide an implementation that performs the following iterative solvers, limited to the case of symmetric and positive definite matrices. The methods implemented are:
* Jacobi method;
* Gauß-Seidel;
* Gradient method;
* Conjugate gradient method.

### Vincoli esecuzione metodi risolutivi


## Using by Virtual Enviroment
A virtual environment to manage packages is a good practice to keep project dependencies isolated

### To create virtual enviroment run this code
```
python -m venv venv
```
### Per accedere utilizzare l'ambiente virtuale eseguire i seguenti comandi.
#### Windows
```
source .\venv\Scripts\activate
```
#### MacOS
```
source .venv/bin/activate
```
### Install all packages
To install all necessary packages in virtual enviroment run
```
pip install -r requirements.txt
```
