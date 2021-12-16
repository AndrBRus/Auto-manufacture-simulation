import simpy # this module uses to simulate production process
from config_data import config_data # import config_data class with configuration data 
from parts_data import parts_data # import parts_data class with info about all parts
from car import car # import car class with info about car on conveyor
from conveyor import conveyor # import conveyor class with info about conveyor at usine
from manufacture import manufacture # import manufacture class with manufacture process at usine
from load_data import load_parts_data, load_config_data # import from load_data module load functions 

# It's main module, that prints menu and main actions

if __name__ == '__main__':

    action = None # variable for input user action ("-1" - stabdard value)
    parts = parts_data() # empty class for future use
    config = None # for next use in manufacture class
    
    while action != '0': # print menu until exit from program
        print('\nMAIN MENU\n')
        print('0. {}\n1. {}\n2. {}\n'.format('Exit', 'Load data', 'Modeling'))
        
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
                print('\nLOADING DATA MENU\n')
                print('0. {}\n1. {}\n2. {}\n3. {}\n'.format('Return to main menu', 'Load parts data', 'Load config data', 'Test data'))

                action = input('Input action: ') # input additional action (for "loading data" menu)

                if action == '0': # if exit
                    action = None # standard value for action
                    pass # pass to the next iteration
                elif action == '1': # load parts data
                    load_parts_data(parts)
                elif action == '2': # load config data
                    config = config_data(*load_config_data())
                elif action == '3': # test data 
                    config = config_data(0.0007, 0.000065, 5.5, 0.000026, 5, 7.25, 30, 6, 6, 2500, 0.165, 4.3, 0.7)
                    parts.get_data('wl_raw_materials', [1000, 500, 250, 1, 0.0025, 2.5, 300])
                    parts.get_data('wl_consumables', [500, 250, 100, 1, 0.0003, 3, 200])
                    parts.get_data('cl_raw_materials', [700, 300, 200, 2, 0.00045, 5.5, 400])
                    parts.get_data('cl_consumables', [550, 150, 50, 2, 0.000007, 10.5, 500])
                    parts.get_data('as_raw_materials', [1500, 700, 500, 3, 0.000067, 3.5, 1400])
                    parts.get_data('as_consumables', [600, 300, 100, 3, 0.0004, 7.5, 600])
                    print('\nData loaded!')
                else: # if a different value is entered that is not listed in the menu
                    print('\nUnknown command!')

        elif action == '2': # if modeling production process 
            manufacture_env = simpy.Environment() # create env for manufacture timer 
            manufacture_process = manufacture(manufacture_env, conveyor(), parts, config)   # create a class 
            # start manufacture process
            manufacture_process.manufacture_process()
            # print revenue of product
            manufacture_process.car_revenue()
        else: # if a different value is entered that is not listed in the menu
            print('\nUnknown command!')