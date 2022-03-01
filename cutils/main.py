import click
import csv
import json
from loguru import logger
from pathlib import Path
from typing import Callable, Tuple


logger.remove()
logger.add(
    "cli.log", format="{time} {level} {message}", level="DEBUG", rotation="500 MB"
)


def json_to_csv(input_path, output_path):
    with open(input_path, "r", encoding="utf-8") as data_file, open(
        output_path, "w", encoding="utf-8"
    ) as csvfile:
        fieldnames = None
        for row in data_file:
            data = json.loads(row)
            if fieldnames is None:
                fieldnames = list(data.keys())
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()
            writer.writerow(data)


FILE_CONVERTERS: [Tuple[str, str], Callable[Path, Path]] = {
    ("json", "csv"): json_to_csv,
}


@click.group()
def cli():
    pass


@cli.command()
@click.option("-f", "--from-format", type=str, required=True)
@click.option("-t", "--to-format", type=str, required=True)
@click.argument("input_", type=str)
@click.argument("output", type=str)
def convert(from_format: str, to_format: str, input_: str, output: str):
    """Convert `file` from `from_format` format to `to_format` format"""
    input_path = Path(input_)
    output_path = Path(output)
    converter = FILE_CONVERTERS[(from_format, to_format)]
    converter(input_path, output_path)
