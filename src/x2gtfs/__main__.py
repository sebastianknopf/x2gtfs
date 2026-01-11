import click
import logging
import openpyxl as xl
import os
import yaml

from openpyxl import Workbook

from x2gtfs.config import Configuration
from x2gtfs.iterator import iter_data_vertical, iter_data_horizontal


@click.command
@click.argument('inputfilename', type=click.Path(exists=True))
@click.argument('outputfilename', type=click.Path())
def main(inputfilename, outputfilename):
    with open(inputfilename, 'r') as inputfile:
        config: dict = yaml.safe_load(inputfile)
        Configuration.apply_config(config)

    for input_filename in os.listdir(Configuration.config.timetables.input_directory):
        if input_filename.endswith('.xlsx'):
            logging.info(f"Processing file: {input_filename}")
            wb: Workbook = xl.load_workbook(
                os.path.join(Configuration.config.timetables.input_directory, input_filename), 
                data_only=True
            )

            ws = wb.active

            if Configuration.config.timetables.layout_type == 'vertical':
                for cell in iter_data_vertical(ws, ws[Configuration.config.timetables.data_start_area]):
                    print(cell.coordinate, cell.value)
            else:
                for cell in iter_data_horizontal(ws, ws[Configuration.config.timetables.data_start_area]):
                    print(cell.coordinate, cell.value)


if __name__ == "__main__":

    # set logging default configuration
    logging.basicConfig(format="[%(levelname)s] %(asctime)s %(message)s", level=logging.INFO)

    # run main function
    main()