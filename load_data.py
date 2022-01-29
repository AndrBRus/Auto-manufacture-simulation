from parts_data import parts_data 
# This module contains functions for load data from console.

# name of parts for function "load_parts_data"
PARTS_DATA_NAME = ['wl_raw_materials', 'wl_consumables', 'cl_raw_materials', 'cl_consumables', 'as_raw_materials', 'as_consumables']
# data to be output to the console when using the function "load_parts_data"
INPUT_PARTS_PRINT = [
    'Initial stock quantity (blocks): ',                 
    'Minimum quantity in stock (blocks): ', 
    'Used quantity per car (blocks): ', 
    'Delivery stage to conveyor: ', 
    'Probability of delivery disruption: ',
    'Delivery time (hours): ', 
    'Number of units upon delivery (blocks): '
]

# this function loads data about parts
def load_parts_data(parts):
    read_data = list() # list for all data about parts
    # for every detail
    for iter_part_name in PARTS_DATA_NAME:
        print('\nEnter data for variable {}\n'.format(iter_part_name)) # output for which part we enter the value
        # enter each value, and add to the list
        for iter_name in INPUT_PARTS_PRINT:
            read_data.append(float(input(iter_name)))
        
        parts.get_data(iter_part_name, read_data) # adding value to parts dict
        
# data to be output to the console when using the function "load_config_data"
INPUT_CONFIG_PRINT = [
    'Probability of manufacture defect: ',
    'Probability of fixing a manufacturing defect: ',
    'Time to fixing a manufacture defect (hours): ', 
    'Probability of details defect: ',
    'Days of production: ',
    'Change time (hours): ',
    'Time interval (minutes): ',
    'Time at welding (hours): ',
    'Time at coloring (hours): ',
    'Conveyor length (meters): ',
    'Conveyor speed (meters/h): ',
    'Car length (meters): ',
    'Distance between cars (meters): ',
    'Number of tests:  '
]

# this function loads configuration data
def load_config_data():
    read_data = list() # list for all data about parts
    # iterating through the entire list of class variables
    for iter_name in INPUT_CONFIG_PRINT:
        read_data.append(float(input(iter_name))) # write to list
    # return list with data
    return read_data