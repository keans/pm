ReadMe
######

The python module `pm` provides a simple interface to a project manager
that allows the generation of Gantt charts.


Setup
=====

Install required modules:

.. code-block::

    poetry install


Usage
=====

Render Gantt diagram based on example YAML file:

.. code-block::

    poetry run python pm.py --debug gantt examples/example.yml
