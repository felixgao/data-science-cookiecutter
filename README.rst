Table of Contents
------------------

.. contents:: This article consists of the following sections.
    :depth: 1

Features
--------

Cookiecutter Docker Science provides the following features.

* **Improve reproducibility** of the results in machine learning projects with **Docker**
* Output optimal directories and file template for machine learning projects
* Provide `make` targets useful for data analysis (Jupyter notebook, test, lint, docker etc)

Introduction
------------

Many researchers and engineers do their machine learning or data mining experiments.
For such data engineering tasks, researchers apply various tools and system libraries which are constantly
updated, installing and updating them cause problems in local environments. Even when we work in hosting
environments such as EC2, we are not free from this problem. Some experiments succeeded in one
instance but failed in another one, since library versions of each EC2 instances could be different.

By contrast, we can creates the identical Docker container in which needed tools with the correct versions are already installed in one command without
changing system libraries in host machines. This aspect of Docker is important for reproducibility of experiments,
and keep the projects in continuous integration systems.

This project is a tiny template for machine learning projects developed in Docker environments.
In machine learning tasks, projects glow uniquely to fit target tasks, but in the initial state,
most directory structure and targets in `Makefile` are common.
Cookiecutter Docker Science generates initial directories which fits simple machine learning tasks.

Requirements
------------

* Python 3.6 or later
* `Cookiecutter 1.6 or later <https://cookiecutter.readthedocs.io/en/latest/installation.html>`_
* `Docker version 17 or later <https://docs.docker.com/install/#support>`_
* Jyputer Notebook locally installed
* AWS CLI locally installed
* pre-commit locally installed


Quick start
-----------

To generate project from the cookiecutter-doccker-science template, please run the following command.

``$cookiecutter gh:felixgao/data-science-cookiecutter``

Then the cookiecutter command ask for several questions on generated project as follows.

::

    $cookiecutter gh:felixgao/data-science-cookiecutter
    project_name [project_name]: food-image-classification
    project_slug [food_image_classification]:
    jupyter_host_port [8888]:
    description [Please Input a short description]: Classify food images into several categories
    Select data_source_type:
    1 - s3
    2 - url
    data_source [Please Input data source]: s3://research-data/food-images

Then you get the generated project directory, ``food-image-classification``.

Initial directories and files
-----------------------------

The following is the initial directory structure generated in the previous section.

::

    ├── Makefile                          <- Makefile contains many targets such as create docker container or
    │                                        get input files.
    ├── config                            <- This directory contains configuration files used in scripts
    │   │                                    or Jupyter Notebook.
    │   └── jupyter_config.py
    ├── data                              <- data directory contains the input resources.
    ├── docker                            <- docker directory contains Dockerfile.
    │   └── Dockerfile                    <- Dockerfile have the container settings. Users modify Dockerfile
    │                                        if additional library is needed for experiments.
    ├── model                             <- model directory store the model files created in the experiments.
    ├── my_data_science_project           <- cookie-cutter-docker-science creates the directory whose name is same
    │   │                                    as project name. In this directory users puts python files used in scripts
    │   │                                    or Jupyter Notebook.
    │   └── __init__.py
    ├── notebook                          <- This directory sotres the ipynb files saved in Jupyter Notebook.
    ├── tests                             <- This directory contains all the tests for my_data_science_project
    ├── Pipefile                          <- Libraries needed to run experiments. The library listed in this file
    │                                        are installed in the Docker container.
    └── scripts                           <- Users add the script files to generate model files or run evaluation.


Makefile targets
----------------

Cookiecutter Docker Science provides many Makefile targets to supports experiments in a Docker container. Users can run the target with `make [TARGET]` command.

For all supported targets please use the following command to get info

`make help`

Show target specific help
~~~~~~~~~~~~~~~~~~~~~~~~~

`help` target flushes the details of specified target. For example, to get the details of `clean` target.

:: 

    $make help TARGET=clean
    target: clean
    dependencies: clean-model clean-pyc clean-docker
    description: remove all artifacts

As we can see, the dependencies and description of the specified target (`clean`) are shown.

License
-------

Apache version 2.0

Contribution
-------------
