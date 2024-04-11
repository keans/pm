ReadMe
######

The python module `pm` provides a simple interface to a project manager
that allows the generation of Gantt charts as SVG from YAML files.

DISCLAIMER: this project is at early stage, thus has limited functionality
and still might have bugs.


Setup
=====

Install required modules:

.. code-block::

    poetry install


Usage
=====

Render Gantt diagram based on example YAML file:

.. code-block::

    poetry run python pm.py --debug gantt examples/example.yml --view day
    poetry run python pm.py --debug gantt examples/example.yml --view week
