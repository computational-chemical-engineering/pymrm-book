# Getting Started with PyMRM

## Overview

PyMRM is a Python package for modeling multiphase reactors, developed as part of the Multiphase Reactor Modeling course at Eindhoven University of Technology. It provides tools for modeling diffusion, convection, reaction, and mass transfer, with a user-friendly interface and extensive documentation.

This book is designed to help you get started with PyMRM, explore its features, and develop your own models.

## Installation

To use PyMRM locally, install Python 3.10 or newer and create an isolated environment before installing the package.

### Windows

Choose one of the following environment options:

1. **Conda (Anaconda or Miniconda)**:
   Install [Anaconda](https://www.anaconda.com/products/distribution) or [Miniconda](https://www.anaconda.com/docs/getting-started/miniconda/main), then create and activate an environment:
   ```sh
   conda create -n pymrm_env python=3.12
   conda activate pymrm_env
   ```
2. **`venv` (standard Python)**:
   Install Python from [python.org](https://www.python.org/downloads/windows/), then create and activate a virtual environment:
   ```sh
   py -3.12 -m venv .venv
   .venv\Scripts\activate
   ```
   In Windows PowerShell, if script execution is blocked, run:
   ```powershell
   Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned
   ```

After activating either environment, install PyMRM:

```sh
python -m pip install --upgrade pip
pip install pymrm
```

### Linux and macOS

The same steps apply, but activation for `venv` is usually:

```sh
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install pymrm
```

### Verify the installation

```python
import pymrm
print("PyMRM version:", pymrm.__version__)
```

For detailed instructions, refer to the [Installation Guide](../../pymrm/docs/installation.md).

## Using Google Colab

If you prefer not to install PyMRM locally, you can use [Google Colab](https://colab.research.google.com/). Colab allows you to run Jupyter notebooks in the cloud without any setup. To get started:

1. Open [Google Colab](https://colab.research.google.com/).
2. Navigate to the **GitHub** tab under **File → Open Notebook**.
3. Enter the repository URL:  
   [https://github.com/multiscale-modelling-multiphase-flows/pymrm](https://github.com/multiscale-modelling-multiphase-flows/pymrm).
4. Select a notebook from the [examples folder](https://github.com/multiscale-modelling-multiphase-flows/pymrm/tree/main/examples), such as [counter_diffusion_reaction.ipynb](https://github.com/multiscale-modelling-multiphase-flows/pymrm/blob/main/examples/counter_diffusion_reaction.ipynb).
5. Add the following code cell to install PyMRM:
   ```python
   !pip install pymrm
   ```

## Content of the Book

This book contains the following sections to help you master PyMRM:

- **Tutorials**: Step-by-step guides to learn the basics of PyMRM (coming soon).
- **Examples**: A collection of advanced use cases, such as modeling diffusion, convection, and reaction processes.
- **Exercises**: Practice problems to deepen your understanding of PyMRM's features.
- **API Documentation**: A comprehensive reference for all functions and classes in PyMRM.

Start with the tutorials to build a strong foundation, then explore the examples and exercises to enhance your skills. For further details, consult the [API documentation](../api/api.rst).
