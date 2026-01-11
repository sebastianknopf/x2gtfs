import click
import logging
import yaml

from x2gtfs.config import Configuration


@click.command
@click.argument('inputfilename', type=click.Path(exists=True))
@click.argument('outputfilename', type=click.Path())
def main(inputfilename, outputfilename):
    logging.info("test")
    logging.info(f"Input file: {inputfilename}")
    logging.info(f"Output file: {outputfilename}")

    with open(inputfilename, 'r') as inputfile:
        config: dict = yaml.safe_load(inputfile)
        Configuration.apply_config(config)

    logging.info(f"Configuration Test: {Configuration.config.timetables.input_directory}")


if __name__ == "__main__":

    # set logging default configuration
    logging.basicConfig(format="[%(levelname)s] %(asctime)s %(message)s", level=logging.INFO)

    # run main function
    main()