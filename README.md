# Tablet Qt

TabletQt is an intermediate graphics rendering layer intended to support the generation of model diagrams such as UML or SysML.

It establishes an intermediate layer between a model diagram tool and any particular graphics library.

Consequently, the model diagram tool is not affected by any change in the chosen graphics library as
long as all the required functionality is supported.

For example, the Flatland model diagram generator, also maintained on this site, was originally implemented on top of Tablet which was built on the Cairo graphics library.

I am moving it to TabletQt which offers the same functionality on top of the Qt GUI library using PyQt bindings.

In this readme file I will keep the focus on installation. For details about the interface, features, and other documentation, please see the wiki for this repository.

### Why you need this

You want to draw simple 2D to support model drawings such as UML or SysML

### Installation

Create or use a python 3.12+ environment.

% pip install tablet-qt

#### From your python script

Take a look at the etchasketch.py file to see an example script that imports and uses Tablet.

#### From the command line

This is not the intended usage scenario, but may be helpful for testing or exploration. Since scrall may generate
some diagnostic info you may want to create a fresh working directory and cd into it first. From there...

    % tablet

You should also see a file named `tabletqt.log`