import click
import logging
import openpyxl as xl
import os
import yaml

from openpyxl import Workbook
from openpyxl.worksheet.worksheet import Worksheet
from openpyxl.utils import column_index_from_string

from x2gtfs.config import Configuration
from x2gtfs.x2gtfs import load_stop_metadata, load_calendar_metadata, load_agency_and_route_metadata, process_timetable_files
from x2gtfs.models import Stop, Calendar, CalendarDate, Agency, Route, Trip, StopTime
from x2gtfs.gtfs import Feed


@click.command
@click.argument('inputfilename', type=click.Path(exists=True))
@click.argument('outputfilename', type=click.Path())
def main(inputfilename, outputfilename):
    
    # load and apply configuration
    with open(inputfilename, 'r') as inputfile:
        config: dict = yaml.safe_load(inputfile)
        Configuration.apply_config(config)

    # define containers for results and meta data lookups
    stop_result_list: dict[str, Stop] = {}
    calendar_result_list: dict[str, Calendar] = {}
    calendar_exception_result_list: dict[str, list[CalendarDate]] = {}
    agency_result_list: dict[str, Agency] = {}
    route_result_list: dict[str, Route] = {}
    
    trip_result_list: list[Trip] = []
    stop_time_result_list: list[StopTime] = []

    # read meta data here if available
    logging.info("Loading stops metadata ...")
    stop_result_list = load_stop_metadata()

    # calendar data
    logging.info("Loading calendar metadata ...")
    calendar_result_list, calendar_exception_result_list = load_calendar_metadata()

    # route and agency data
    logging.info("Loading agency and route metadata ...")
    agency_result_list, route_result_list = load_agency_and_route_metadata()

    # run over timetable input files and process each one
    logging.info("Processing timetable input files ...")
    trip_result_list, stop_time_result_list = process_timetable_files(
        stop_result_list,
        calendar_result_list,
        calendar_exception_result_list,
        agency_result_list,
        route_result_list
    )

    # create GTFS output files
    feed = Feed()
    feed.add_data('stops.txt', list(stop_result_list.values()))

    if len(calendar_result_list) > 0:
        feed.add_data('calendar.txt', list(calendar_result_list.values()))
    if len(calendar_exception_result_list) > 0:
        feed.add_data('calendar_dates.txt', [cd for cdl in calendar_exception_result_list.values() for cd in cdl])

    feed.add_data('agency.txt', list(agency_result_list.values()))
    feed.add_data('routes.txt', list(route_result_list.values()))

    feed.add_data('trips.txt', trip_result_list)
    feed.add_data('stop_times.txt', stop_time_result_list)

    feed.write(outputfilename)


if __name__ == "__main__":

    # set logging default configuration
    logging.basicConfig(format="[%(levelname)s] %(asctime)s %(message)s", level=logging.INFO)

    # run main function
    main()