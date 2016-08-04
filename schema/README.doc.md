# OpenSwitch Schema documentation

In order to produce HTML documentation from the OpenSwitch schema, the
following software must be available on the system:

* Cmake (tested with Cmake 3.0.2)
* Python >= 2.7.9
* Sphinx (tested with Sphinx v1.4.4).
* Sphinx ReadTheDocs theme (RTD theme).
* A Java Runtime Environment (tested with OpenJDK 1.7.0_95).

Usually Cmake, Python and Java are already installed in a development
environment. This leaves Sphinx and RTD theme to be installed.

## Install Sphinx and RTD theme

```
$ pip install sphinx
$ pip install sphinx_rtd_theme
```

## Create HTML documentation
Create a directory to store the documentation, for example `build`, and execute
`cmake` and `make` in that directory:
```
$ mkdir build
$ cd build
$ cmake ..
$ make
```
The documentation will be available under `build/docs`, the main page is
`build/docs/index.html`.
