class _ConfigNamespace:
    def __init__(self, **entries):
        for key, value in entries.items():
            setattr(self, key, value)

    def dict(self):
        return self.__dict__
    
    def __repr__(self):
        return f"<Config {self.__dict__}>"


class Configuration:

    @classmethod
    def apply_config(cls, config: dict) -> None:

        # define required config keys
        required_config: list[tuple[str]] = [
            ('config', 'timetables', 'input_directory'),
            ('config', 'timetables', 'data_start_area'),
            ('config', 'timetables', 'stop_identification_index'),
            ('config', 'timetables', 'route_identification_index'),
            ('config', 'timetables', 'service_identification_index'),
            ('config', 'timetables', 'shape_identification_index'),
            ('config', 'timetables', 'trip_short_name_index'),
            ('config', 'timetables', 'trip_headsign_index')
        ]

        # define default config values
        # some of them are added as comment for documentation
        default_config = {
            'config': {
                'timetables': {
                    #'input_directory': None,
                    'layout_type': 'vertical',
                    'run_through_char': '$',
                    'time_format': '%H:%M:%S',
                    #'data_start_area': None,
                    #'stop_identification_index': None,
                    #'route_identification_index': None,
                    #'service_identification_index': None,
                    #'shape_identification_index': None,
                    #'trip_short_name_index': None,
                    #'trip_headsign_index': None
                }
            }
        }

        cls._validate_required(required_config, config)
        config = cls._merge_config(default_config, config)

        namespace = cls._dict_to_namespace(config)
        for key, value in namespace.__dict__.items():
            setattr(cls, key, value)
    
    @classmethod
    def _merge_config(cls, defaults: dict, actual: dict) -> dict:
        if isinstance(defaults, dict) and isinstance(actual, dict):
            return {
                k: cls._merge_config(
                    defaults[k] if k in defaults else {},
                    actual[k] if k in actual else {}
                )
                for k in set(defaults) | set(actual)
            }

        return actual if actual is not None else defaults
    
    @classmethod
    def _validate_required(cls, required: list[tuple[str]], config: dict):
        for path in required:
            current = config
            for key in path:
                if key not in current:
                    raise ValueError(f"Missing required config key: {'.'.join(path)}")
                
                current = current[key]

    @classmethod
    def _dict_to_namespace(cls, data: dict) -> _ConfigNamespace:
        if isinstance(data, dict):
            return _ConfigNamespace(
                **{k: cls._dict_to_namespace(v) for k, v in data.items()}
            )
        
        return data