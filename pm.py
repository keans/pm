#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
from pathlib import Path

import svgwrite
import click

from draw.widgets.grid import GridWithBars, GridRow
from draw.widgets.gantt.gantt import Gantt

from models import Project


# prepare logger
log = logging.getLogger(__file__)


@click.group()
@click.option("--debug/--no-debug", default=False)
def cli(debug):
    if debug is True:
        # activate DEBUG output
        logging.basicConfig(level=logging.DEBUG)


@cli.command()
@click.argument("filename")
def gantt(filename):
    """
    create gantt chart from given project filename
    """
    # get project data from file
    log.debug(f"loading project file from '{filename}'...")
    p = Project.create_from(filename)

    # draw the gantt chart
    dwg = svgwrite.Drawing(size=("1900", "600"))

    # add default css for formatting
    # TODO: make configurable via parameter?!
    dwg.add_stylesheet("css/default.css", "default")

    #g = Gantt(100, 100, project=p)
    g = Gantt(100, 100, p)

    # draw gantt
    dwg.add(g.draw(dwg))

    # finally, save
    output_filename = f"{Path(filename).stem}.svg"
    log.debug(f"saving SVG to '{output_filename}'...")
    dwg.save(output_filename)


if __name__ == "__main__":
    cli()
