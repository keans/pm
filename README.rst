ReadMe
######

The python module `proma` provides a simple interface to a project manager
that allows the generation of Gantt charts as SVG from YAML files.

DISCLAIMER: this project is at early stage, thus has limited functionality
and still might have bugs.


Setup
=====

Install the `proma` module:

.. code-block::

    poetry add proma


For development
---------------

Install required modules:

.. code-block::

    poetry install


Usage
=====

Render Gantt diagram based on example YAML file:

.. code-block::

    poetry run proma --debug gantt examples/example.yml --view day
    poetry run proma --debug gantt examples/example.yml --view week

Please note that css file must be inplace (css/default.css) to correctly see
the rendered output.
