from distutils.command.config import config
from parts_data import parts_data
import math # use for "sqrt" function

# This module contains functions for load data from console.

# name of parts for function "load_parts_data"
PARTS_DATA_NAME = ['wl_raw_materials', 'wl_consumables', 'cl_raw_materials', 'cl_consumables', 'as_raw_materials', 'as_consumables']
# data to be output to the console when using the function "load_parts_data"
INPUT_PARTS_PRINT = [
    'Initial stock quantity (blocks): ',
    'Maximum stock level (blocks): ',             
    'Minimum quantity in stock (blocks): ', 
    'Used quantity per car (blocks): ', 
    'Delivery stage to conveyor: ', 
    'Probability of delivery disruption: ',
    'Delivery time (hours): ', 
    'Number of units upon delivery (blocks): '
]

# this function loads data about parts
def load_parts_data(parts, config_data):
    read_data = list() # list for all data about parts
    # for every detail
    for iter_part_name in PARTS_DATA_NAME:
        print('\nEnter data for variable {}\n'.format(iter_part_name)) # output for which part we enter the value
        # if use the purchase strategy for used yesterday or use interval strategy
        if config_data.strategy == 'B' or config_data.strategy == 'I"':
            for iter_name in INPUT_PARTS_PRINT:
                if iter_name == INPUT_PARTS_PRINT[7]:
                    # purchase factor - indicates the percentage of the daily use of parts
                    if config_data.strategy == 'B':
                        purchase_factor = 1
                    else:
                        # status for check errors 
                        input_status = False 
                        # while error in answer try to input
                        while input_status == False:
                            # except ValueError for input (transformation from string to int)
                            try:
                                # enter each value, and add to the list
                                purchase_factor = int(input('Input the percentage of the daily use of parts'))
                                input_status = True # change the status
                            # except value error
                            except ValueError:
                                print('Incorrect value! Try again...')
                        
                    # write to list
                    read_data.append(int(config_data.max_car * read_data[3] * purchase_factor))
                    
                    continue # transition to the next stage
                # status for check errors 
                input_status = False 
                # while error in answer try to input
                while input_status == False:
                    try:    
                        read_data.append(float(input(iter_name)))
                        input_status = True # change the status
                    # except value error
                    except ValueError:
                        print('Incorrect value! Try again...')
        # if use user capacity strategy
        else:
            for iter_name in INPUT_PARTS_PRINT:
                # status for check errors 
                input_status = False 
                # while error in answer try to input
                while input_status == False:
                    # except ValueError for input (transformation from string to int)
                    try:
                        # enter each value, and add to the list
                        read_data.append(float(input(iter_name)))
                        input_status = True # change the status
                    # except value error
                    except ValueError:
                        print('Incorrect value! Try again...')
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
    'Strategy type (\'B\' - buy yesterday; \'I\' - inteval; \'U\' - user capacity): ',
    'Number of tests:  ',
    'Check interval for interval replenishment strategy (minutes): '
]

# this function loads configuration data
def load_config_data():
    read_data = list() # list for all data about parts
    # iterating through the entire list of class variables
    for iter_name in INPUT_CONFIG_PRINT:
        # if user input type of strategy
        if iter_name == INPUT_CONFIG_PRINT[13]:
            # status for check errors 
            input_status = False 
            # while error in answer try to input
            while input_status == False:
                try:
                    strategy = input(iter_name).upper()
                    # if input without error 
                    if strategy == 'I' or strategy == 'B' or strategy == 'U':
                        read_data.append(strategy) # write to list
                        input_status = True # change the status
                    # if input with error 
                    else:
                        raise ValueError # raise value error
                # except value error
                except ValueError: 
                    print('Incorrect value! Try again...') 
            continue # go to the next iteration (crutch :))
        elif iter_name == INPUT_CONFIG_PRINT[15]:
            if read_data[13] == 'I':
                # status for check errors 
                input_status = False 
                # while error in answer try to input
                while input_status == False:
                    try:
                        print('ONLY USE INTERVALS IN MULTIPLES OF 5 MINUTES')
                        check_time = int(input(iter_name)) # input time interval
                        # if the number is not a multiple of five, then we call Value error
                        if check_time % 5 != 0:
                            raise ValueError

                        read_data.append(check_time) # write to list
                        input_status = True # change the status
                    # except value error
                    except ValueError: 
                        print('Incorrect value! Try again...')
            else:
                pass
        # other config data
        elif iter_name != INPUT_CONFIG_PRINT[13] or iter_name != INPUT_CONFIG_PRINT[15]:
            # status for check errors 
            input_status = False 
            # while error in answer try to input
            while input_status == False:
                try:
                    read_data.append(float(input(iter_name))) # write to list
                    input_status = True # change the status
                # except value error
                except ValueError: 
                    print('Incorrect value! Try again...') 
    # return list with data
    return read_data

# This function, depending on the strategy, if necessary, calculates the desired values 
# and loads the data into the program
def load_parts_data_from_template(parts, config_data, type_strategy, temp_data):
    # if use "Purchase at yesterday's costs"
    if type_strategy == 'B' or type_strategy == 'I':
        # load all the data from "temp_data" + warehouse capacity (critical values) and initial delivery quantity
        for iter in range(0, len(temp_data)):
            # If we use the "purchase at yesterday's costs" strategy, then the initial quantity of purchased products will be equal to the 
            # maximum number of machines on the conveyor * per the number of blocks per machine.
            # For the interval strategy, the same value, but with a coefficient of 0.25, that is, a quarter of the full pipeline
            if type_strategy == 'B':
                replenishment_amount = int(config_data.max_car * temp_data[iter][1])
            else:
                replenishment_amount = int((config_data.max_car * 0.25) * temp_data[iter][1])
            parts.get_data(PARTS_DATA_NAME[iter], [temp_data[iter][0], int(config_data.max_car * temp_data[iter][1] * 1.5), int(config_data.max_car * temp_data[iter][1] * 0.5), *temp_data[iter][1:5], replenishment_amount])
    # if use "Custom inventory level"
    elif type_strategy == 'U':
        # load all data from "temp_data" into the model 
        # alternately using part names from "PARTS_DATA_NAME"
        for iter in range(0, len(temp_data)):
            parts.get_data(PARTS_DATA_NAME[iter], temp_data[iter])