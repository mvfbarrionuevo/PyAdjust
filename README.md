# PyMOL Plugin - PyAdjust

Simple plugin for [PyMOL](https://pymol.org) which can be used for adjusting atomic positions at a XY plane within a periodic boundary system.

## Requirements

PyMOL 2.x

## Usage

[Download ZIP](https://github.com/mvfbarrionuevo/pyadjust/archive/master.zip)
and install with PyMOL's plugin manager
(Plugin > Plugin Manger > Install New Plugin > Install from local file).

Alternatively, you can clone this repo into a directory which is in PyMOL's plugin search path
(Plugin > Plugin Manger > Settings > Plugin override search path).

## Plugin files

* [\_\_init\_\_.py](__init__.py): Entry point, provides the `__init_plugin__` function which adds an entry to PyMOL's plugin menu.
* [pyadjust.ui](pyadjust.ui): Graphical user interface file, created with [Qt Designer](http://doc.qt.io/qt-5/qtdesigner-manual.html)

## Created by

[Manoel Victor Frutuoso Barrionuevo](manoelvfb@live.ca)

## License

[GPL-3-Clause](LICENSE)

## Citing

