from itertools import product
from math import prod
from delete_logs import delete_logs
import simpy # this module uses to simulate production process
from config_data import config_data # import config_data class with configuration data 
from parts_data import parts_data # import parts_data class with info about all parts
from car import car # import car class with info about car on conveyor
from conveyor import conveyor # import conveyor class with info about conveyor at usine
from manufacture import manufacture # import manufacture class with manufacture process at usine
from load_data import load_parts_data, load_config_data, load_parts_data_from_template # import from load_data module load functions
from delete_logs import delete_logs # import from delete_logs module function for delete all logs flies from logs folder

# It's main module, that prints menu and main actions

def start_command_line_app():

    action = None # variable for input user action ("-1" - stabdard value)
    parts = parts_data() # empty class for future use
    config = None # for next use in manufacture class
    
    while action != '0': # print menu until exit from program
        print('\nMAIN MENU')
        print('-' * 25)
        print('0. {}\n1. {}\n2. {}\n3. {}\n'.format('Exit', 'Load data', 'Modeling (once)', 'Full modeling'))
        
        try: # try to transofm to int
            action = input('Input action: ') # input action
        
        except ValueError: # if input not a number
                print('\nUnknown command!')
                pass # go to the next iteration

        if action == '0': # exit program
            print('\nExiting program...\n')
            break
        
        elif action == '1': # print "loading data" menu
            while action != None: # while no exit from menu
                print('\nLOADING DATA MENU')
                print('-' * 25)
                print('0. {}\n1. {}\n2. {}\n3. {}\n'.format('Return to main menu', 'Load config data', 'Load parts data', 'Template data'))

                action = input('Input action: ') # input additional action (for "loading data" menu)

                if action == '0': # if exit
                    action = None # standard value for action
                    pass # pass to the next iteration
                
                elif action == '1': # load config data
                    config = config_data(*load_config_data())
                    print('\nData loaded!')
                
                elif action == '2': # load parts data
                    try:
                        if config == None:
                            raise ValueError
                    except ValueError:
                        print('You must first enter the configuration data! Go to point one.')
                        continue
                    load_parts_data(parts, config)
                    print('\nData loaded!')
                
                elif action == '3': # test data
                    while action != None: # while no exit from menu
                        print('\nLOADING TEMPLATE MENU')
                        print('-' * 25)
                        print('0. {}\n1. {}\n2. {}\n3. {}\n'.format('Return to data loading menu', 'Template \"Custom inventory level\"', 'Template \"Interval strategy\"', 'Template \"Purchase at yesterday\'s costs\"'))
                        
                        action = input('Input action: ') # input additional action (for "loading data" menu)
                        
                        if action == '0': # if exit
                            action = None # standard value for action
                       
                        elif action == '1': # load user input template
                            # loading configuration data
                            config = config_data(0.0007, 0.000065, 5.5, 0.000026, 5, 7.25, 30, 6, 6, 2500, 0.165, 4.3, 0.7, 'U', 100)
                            # generated template with all data 
                            # (look "INPUT_PARTS_PRINT" list at "load_data.py")
                            temp_data = [
                                [1000, 5000, 500, 250, 1, 0.0025, 2.5, 300],
                                [500, 2500, 250, 100, 1, 0.0003, 3, 200],
                                [700, 7000, 300, 200, 2, 0.00045, 5.5, 400],
                                [550, 5500, 150, 50, 2, 0.000007, 10.5, 500],
                                [1500, 15000, 700, 500, 3, 0.000067, 3.5, 1400],
                                [600, 6000, 300, 100, 3, 0.0004, 7.5, 600]
                            ]
                            # loading data into the model
                            load_parts_data_from_template(parts, config, config.strategy, temp_data)
                            print('\nData loaded!') # write about the end of the operation
                        
                        elif action == '2': # load interval strategy template
                            # loading configuration data
                            config = config_data(0.0007, 0.000065, 5.5, 0.000026, 5, 7.25, 30, 6, 6, 2500, 0.165, 4.3, 0.7, 'I', 100, 15)
                            # generated template with data without max and minimum capacity of warehouse; last two columns: shipping price and storage price 
                            # (look "INPUT_PARTS_PRINT" list at "load_data.py")
                            temp_data = [
                                [1000, 25, 1, 0.0025, 2.5],
                                [500, 10, 1, 0.0003, 3],
                                [700, 20, 2, 0.00045, 5.5],
                                [550, 50, 2, 0.000007, 10.5],
                                [1500, 5, 3, 0.000067, 3.5],
                                [600, 1, 3, 0.0004, 7.5]
                            ]
                            # loading data into the model
                            load_parts_data_from_template(parts, config, config.strategy, temp_data)
                            print('\nData loaded!') # write about the end of the operation
                        
                        elif action == '3': # load "buy yesterday" template
                            # loading configuration data
                            config = config_data(0.0007, 0.000065, 5.5, 0.000026, 5, 7.25, 30, 6, 6, 2500, 0.165, 4.3, 0.7, 'B', 100)
                            # generated template with all data except delivery quantity
                            # (look "INPUT_PARTS_PRINT" list at "load_data.py")
                            temp_data = [
                                [1000, 250, 1, 0.0025, 2.5],
                                [500, 100, 1, 0.0003, 3],
                                [700, 200, 2, 0.00045, 5.5],
                                [550, 50, 2, 0.000007, 10.5],
                                [1500, 500, 3, 0.000067, 3.5],
                                [600, 100, 3, 0.0004, 7.5]
                            ]
                            # loading data into the model
                            load_parts_data_from_template(parts, config, config.strategy, temp_data)
                            print('\nData loaded!') # write about the end of the operation
                    
                    action = -1 # crutch to go only one menu up :)
                
                else: # if a different value is entered that is not listed in the menu
                    print('\nUnknown command!')

        elif action == '2': # if modeling production process 
            delete_logs() # delete all logs files before start modeling

            manufacture_env = simpy.Environment() # create env for manufacture timer 
            manufacture_process = manufacture(manufacture_env, conveyor(), parts, config, 'command_line')   # create a class 
            # start manufacture process
            manufacture_process.manufacture_process()
            # print revenue of product
            manufacture_process.car_revenue()
        
        elif action == '3':
            delete_logs() # delete all logs files before start modeling

            manufacture_env = simpy.Environment() # create env for manufacture timer
            
            production_data = list() # create empty list for data about all modeling processes
            # we carry out tests (the number of tests is specified by the user)
            for iter in range(0, config.numb_tests):
                manufacture_process = manufacture(manufacture_env, conveyor(), parts, config, 'command_line') # create a class (the class is re-created for each test for a new generation of random variables)
                manufacture_process.manufacture_process() # start manufacture process
                production_data.append(manufacture_process.car_revenue('full')) # add to list data about end result of the simulation

            # variables for average number of produced cars and average perfomance ratio
            average_ready_cars = 0
            average_perfomance_ratio = 0
            # sum all values in production_data list
            for iter in range(0, len(production_data)):
                average_ready_cars += production_data[iter][0]
                average_perfomance_ratio += production_data[iter][1]
            # find average values for this two variables
            average_perfomance_ratio /= len(production_data)
            # convert average number of produced cars to an integer, 
            # since only an integer number of cars can be produced
            average_ready_cars = int(average_ready_cars / len(production_data))
            # find number of expected cars for modeling test (the same for everyone)
            expected_cars = round((config.days_of_production * (config.change_time * 2) - (config.change_time * 2)) / (config.conveyor_length / (config.conveyor_speed * 1000)) * config.max_car)
            
            # print all data to command line
            print('Average values for {} days of {} test modeling processes'.format(config.days_of_production, config.numb_tests))
            print('Average number of produced cars: {}'.format(average_ready_cars))
            print('Expected number of cars for all tests: {}'.format(expected_cars))
            print('Average perfomance ration: {}'.format(average_perfomance_ratio))
            
        else: # if a different value is entered that is not listed in the menu
            print('\nUnknown command!')