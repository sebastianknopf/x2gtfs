from dataclasses import dataclass
from typing import Optional

@dataclass
class Agency:
    agency_name: str = ""
    agency_url: str = ""
    agency_timezone: str = ""
    agency_id: Optional[str] = None
    agency_lang: Optional[str] = None
    agency_phone: Optional[str] = None
    agency_fare_url: Optional[str] = None

@dataclass
class Route:
    route_id: str = ""
    route_type: int = 3  # Default: Bus (3)
    agency_id: Optional[str] = None
    route_short_name: Optional[str] = None
    route_long_name: Optional[str] = None
    route_desc: Optional[str] = None
    route_url: Optional[str] = None
    route_color: Optional[str] = None
    route_text_color: Optional[str] = None

@dataclass
class Stop:
    stop_id: str = ""
    stop_name: str = ""
    stop_lat: float = 0.0
    stop_lon: float = 0.0
    stop_code: Optional[str] = None
    stop_desc: Optional[str] = None
    zone_id: Optional[str] = None
    stop_url: Optional[str] = None
    location_type: int = 0  # 0 = Stop, 1 = Station
    parent_station: Optional[str] = None
    wheelchair_boarding: Optional[int] = None

@dataclass
class Trip:
    trip_id: str = ""
    route_id: str = ""
    service_id: str = ""
    trip_headsign: Optional[str] = None
    trip_short_name: Optional[str] = None
    direction_id: Optional[int] = None
    block_id: Optional[str] = None
    shape_id: Optional[str] = None
    wheelchair_accessible: Optional[int] = None
    bikes_allowed: Optional[int] = None

@dataclass
class StopTime:
    trip_id: str = ""
    arrival_time: str = "00:00:00"  # HH:MM:SS
    departure_time: str = "00:00:00"  # HH:MM:SS
    stop_id: str = ""
    stop_sequence: int = 0
    stop_headsign: Optional[str] = None
    pickup_type: Optional[int] = None
    drop_off_type: Optional[int] = None
    shape_dist_traveled: Optional[float] = None
    timepoint: Optional[int] = None

@dataclass
class ShapePoint:
    shape_id: str = ""
    shape_pt_lat: float = 0.0
    shape_pt_lon: float = 0.0
    shape_pt_sequence: int = 0
    shape_dist_traveled: Optional[float] = None
