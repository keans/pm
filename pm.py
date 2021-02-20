#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
from pathlib import Path

import svgwrite
import click

from draw.gantt import Gantt

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
    dwg = svgwrite.Drawing(size=("1800", "600"))
    g = Gantt(100, 100, project=p)
    dwg.add(g.draw(dwg))

    # finally, save
    output_filename = f"{Path(filename).stem}.svg"
    log.debug(f"saving SVG to '{output_filename}'...")
    dwg.save(output_filename)


if __name__ == "__main__":
    cli()
