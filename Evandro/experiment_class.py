from dataclasses import dataclass


@dataclass
class SynchronizedExperiment:
    experiment_name: str
    inlet_pressure: float
    inlet_flow: float
    inlet_temperature: float
    adsorbent_mass: float
    bed_length: float
    bed_diameter: float
    time_column: []
    temperature_column: []
    flow_column: []
    y_column: []
    temperature_unit: str
    pressure_unit: str
    flow_unit: str
    poly_flow: []
    poly_temperature: []
    poly_y: []
    f_out_column: []
    c_out_column: []


    def __init__(self,
                 experiment_name: str,
                 inlet_pressure: float,
                 inlet_flow: float,
                 inlet_temperature: float,
                 adsorbent_mass: float,
                 bed_length: float,
                 bed_diameter: float,
                 time_column: [],
                 temperature_column: [],
                 flow_column: [],
                 y_column: [],
                 temperature_unit: str,
                 pressure_unit: str,
                 flow_unit: str,
                 poly_flow: [],
                 poly_temperature: [],
                 poly_y: [],
                 f_out_column: [],
                 c_out_column: []):
        self.experiment_name = experiment_name
        self.inlet_pressure = inlet_pressure
        self.inlet_flow = inlet_flow
        self.inlet_temperature = inlet_temperature
        self.adsorbent_mass = adsorbent_mass
        self.bed_length = bed_length
        self.bed_diameter = bed_diameter
        self.time_column = time_column
        self.temperature_column = temperature_column
        self.flow_column = flow_column
        self.y_column = y_column
        self.temperature_unit = temperature_unit
        self.pressure_unit = pressure_unit
        self.flow_unit = flow_unit
        self.poly_flow = poly_flow
        self.poly_temperature = poly_temperature
        self.poly_y = poly_y
        self.f_out_column = f_out_column
        self.c_out_column = c_out_column


@dataclass
class NotSynchronizedExperiment:
    experiment_name: str
    inlet_pressure: float
    inlet_flow: float
    inlet_temperature: float
    adsorbent_mass: float
    bed_length: float
    bed_diameter: float
    time_temperature_column: []
    time_flow_column: []
    time_y_column: []
    temperature_column: []
    flow_column: []
    y_column: []
    temperature_unit: str
    pressure_unit: str
    flow_unit: str

    def __init__(self,
                 experiment_name: str,
                 inlet_pressure: float,
                 inlet_flow: float,
                 inlet_temperature: float,
                 adsorbent_mass: float,
                 bed_length: float,
                 bed_diameter: float,
                 time_y_column: [],
                 time_temperature_column: [],
                 time_flow_column: [],
                 temperature_column: [],
                 flow_column: [],
                 y_column: [],
                 temperature_unit: str,
                 pressure_unit: str,
                 flow_unit: str,):
        self.experiment_name = experiment_name
        self.inlet_pressure = inlet_pressure
        self.inlet_flow = inlet_flow
        self.inlet_temperature = inlet_temperature
        self.adsorbent_mass = adsorbent_mass
        self.bed_length = bed_length
        self.bed_diameter = bed_diameter
        self.time_y_column = time_y_column
        self.time_temperature_column = time_temperature_column
        self.time_flow_column = time_flow_column
        self.temperature_column = temperature_column
        self.flow_column = flow_column
        self.y_column = y_column
        self.temperature_unit = temperature_unit
        self.pressure_unit = pressure_unit
        self.flow_unit = flow_unit


