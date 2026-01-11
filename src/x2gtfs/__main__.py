import click
import logging
import openpyxl as xl
import os
import yaml

from openpyxl import Workbook
from openpyxl.worksheet.worksheet import Worksheet
from openpyxl.utils import column_index_from_string

from x2gtfs.config import Configuration
from x2gtfs.iterator import iter_data_vertical, iter_data_horizontal
from x2gtfs.models import Trip, StopTime
from x2gtfs.gtfs import Feed


@click.command
@click.argument('inputfilename', type=click.Path(exists=True))
@click.argument('outputfilename', type=click.Path())
def main(inputfilename, outputfilename):
    
    # load and apply configuration
    with open(inputfilename, 'r') as inputfile:
        config: dict = yaml.safe_load(inputfile)
        Configuration.apply_config(config)

    # define containers for results
    trip_result_list: list[Trip] = []
    stop_time_result_list: list[StopTime] = []

    # run over timetable input files and process each one
    for input_filename in os.listdir(Configuration.config.timetables.input_directory):
        if input_filename.endswith('.xlsx'):
            logging.info(f"Processing file: {input_filename}")
            wb: Workbook = xl.load_workbook(
                os.path.join(Configuration.config.timetables.input_directory, input_filename), 
                data_only=True
            )

            ws: Worksheet = wb.active

            current_trip_idx: int = -1
            current_stop_idx: str|None = None

            current_trip: Trip|None = None
            current_stop_time: StopTime|None = None

            if Configuration.config.timetables.layout_type == 'vertical':
                for cell in iter_data_vertical(ws, ws[Configuration.config.timetables.data_start_area]):
                    if cell.value == Configuration.config.timetables.run_through_char:
                        continue
                    
                    if not cell.column == current_trip_idx:
                        if current_trip is not None:
                            trip_result_list.append(current_trip)
                        
                        current_trip = Trip()
                        current_trip.trip_id = str(len(trip_result_list) + 1).zfill(6)
                        
                        route_idx: str = ws.cell(Configuration.config.timetables.route_identification_index, cell.column).value
                        service_idx: str = ws.cell(Configuration.config.timetables.service_identification_index, cell.column).value
                        shape_idx: str = ws.cell(Configuration.config.timetables.shape_identification_index, cell.column).value

                        current_trip.trip_short_name = ws.cell(Configuration.config.timetables.trip_short_name_index, cell.column).value
                        current_trip.trip_headsign = ws.cell(Configuration.config.timetables.trip_headsign_index, cell.column).value

                        current_trip_idx = cell.column
                        
                    stop_idx: str = ws.cell(cell.row, column_index_from_string(Configuration.config.timetables.stop_identification_index)).value
                    if not stop_idx == current_stop_idx:
                        current_stop_time = StopTime()
                        current_stop_time.trip_id = current_trip.trip_id
                        current_stop_time.stop_id = stop_idx
                        current_stop_time.stop_sequence = len([st for st in stop_time_result_list if st.trip_id == current_trip.trip_id]) + 1
                        current_stop_time.arrival_time = cell.value
                        current_stop_time.departure_time = cell.value

                        stop_time_result_list.append(current_stop_time)
                        current_stop_idx = stop_idx
                    else:
                        last_stop_time: StopTime = next(st for st in reversed(stop_time_result_list) if st.trip_id == current_trip.trip_id and st.stop_id == current_stop_idx)
                        last_stop_time.departure_time = cell.value

                if current_trip is not None:
                    trip_result_list.append(current_trip)

            else:
                for cell in iter_data_horizontal(ws, ws[Configuration.config.timetables.data_start_area]):
                    if cell.value == Configuration.config.timetables.run_through_char:
                        continue

                    print(cell.coordinate, cell.value)

    # create GTFS output files
    feed = Feed()
    #feed.add_data('agency.txt', [])
    #feed.add_data('stops.txt', [])
    #feed.add_data('routes.txt', [])
    feed.add_data('trips.txt', trip_result_list)
    feed.add_data('stop_times.txt', stop_time_result_list)

    feed.write(outputfilename)


if __name__ == "__main__":

    # set logging default configuration
    logging.basicConfig(format="[%(levelname)s] %(asctime)s %(message)s", level=logging.INFO)

    # run main function
    main()