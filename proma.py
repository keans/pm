#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
from pathlib import Path

import svgwrite
import click

from proma.utils.timetable import (
    YEAR_MONTH_WEEK_FMT,
    YEAR_QUARTER_MONTH_WEEK_DAY_FMT,
)
from proma.draw.widgets.gantt.gantt import Gantt

from proma.models import Project


# prepare logger
log = logging.getLogger(__file__)


@click.group()
@click.option(
    "--debug/--no-debug",
    default=False,
)
def cli(debug: bool):
    if debug is True:
        # activate DEBUG output
        logging.basicConfig(level=logging.DEBUG)


@cli.command()
@click.argument("filename")
@click.option(
    "--view",
    type=click.Choice(["day", "week"]),
    show_default=True,
    default="day",
)
def gantt(filename: str, view: str):
    """
    create gantt chart from given project filename
    """
    # get project data from file
    log.debug(f"loading project file from '{filename}'...")
    project = Project.create_from(filename)

    # draw the gantt chart
    dwg = svgwrite.Drawing(size=("1900", "600"))

    # add default css for formatting
    # TODO: make configurable via parameter?!
    dwg.add_stylesheet("css/default.css", "default")

    # set format (hierarchy) for output
    formats = (
        YEAR_QUARTER_MONTH_WEEK_DAY_FMT
        if view == "day"
        else YEAR_MONTH_WEEK_FMT
    )

    # draw gantt
    gantt = Gantt(x=100, y=100, project=project, formats=formats)
    dwg.add(gantt.draw(dwg))

    # finally, save
    output_filename = f"{Path(filename).stem}.svg"
    log.debug(f"saving SVG to '{output_filename}'...")
    dwg.saveas(output_filename)


if __name__ == "__main__":
    cli()
