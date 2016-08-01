#Machine Learning Nano Degree Repo

This is a general repository for Udacity's MLND program.  Each directory represents a different machine learning project.  All of these projects rely on the Python data ecosystem & Jupyter notebooks.  For best results download the Anaconda Python distribution and create a conda environment.

## Download Anaconda

Follow the instructions at the following link: https://www.continuum.io/downloads

FYI: if you don't want the full Anaconda distribution, download Miniconda.  Miniconda does not include all the libraries that the full Anaconda distribution does.  Download Miniconda at the following link: http://conda.pydata.org/miniconda.html

These projects were built on top of Python 2.7 (unfortunately)

## Create an Environment

After Anaconda or Miniconda have been installed it is best to create a virtual environment to interact with any of the projects.  This can be done by using the conda environment manager (docs linked below.)

`conda create --name mlnd --file requirements.txt`

A basic requirements file is included.  Note that the rsi project has a separate requirements file.  To activate the environment use the following command:

`source activate mlnd`

conda docs: http://conda.pydata.org/docs/using/envs.html
