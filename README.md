# Random Walk with Restart (RWR) project

Random Walk with Restart project is my mathematics master 2 project of a RWR modelisation in python and PDF report.

## Requirements

Use the package manager [pip](https://pip.pypa.io/en/stable/) or 
[conda](https://docs.conda.io/projects/conda/en/latest/user-guide/index.html) to install foobar.

```bash
pip install matplotlib
pip install networkx
pip install random
pip install numpy
pip install os
pip install shutil
pip install tkinter
pip install PIL
```

## How to run the program ? 

#### Set up your parameters :

1. Transition probability matrix
2. Restart probability
3. Number of iterations
4. Seed node

#### And run !

## Example

```python
matrix = np.matrix([[0, 0.6, 0.2, 0.2],
                      [0.6, 0, 0.3, 0.1],
                      [0.2, 0.6, 0, 0.2],
                      [0.1, 0.6, 0.3, 0]])
restart_probability = 0.25
iterations = 1000
seed = 0
```
