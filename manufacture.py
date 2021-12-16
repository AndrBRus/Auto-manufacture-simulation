from types import NoneType
import simpy # this module uses to simulate production process
import random # this module uses to generate probabilities of defects
import contextlib
from config_data import config_data # import config_data class with configuration data 
from parts_data import parts_data # import parts_data class with info about all parts
from car import car # import car class with info about car on conveyor
from conveyor import conveyor # import conveyor class with info about conveyor at usine
import os # use for search path to file
import sys # use to system definitions

# This module describes the process of car production.

# This class includes the main parts of production: a list of vehicles on a conveyor, 
# warehouse credentials, conveyor data, configuration data.
# Also, this class describes the production process itself.
class manufacture(object):
    # class constructor
    def __init__(self, env, conveyor, parts_data, config_data):
        self.env = env # this env uses to simulate production process (simpy module)
        self.conveyor = conveyor # exemplar of "conveyor" class
        self.parts_data = parts_data # exemplar of "parts_data" class
        self.config_data = config_data # exemplar of "config_data" class
        self.ready_cars = 0 # ready cars to sell
        self.time_days_production = -1 # number of days of production
        self.time_production = 0 # total production time

    # this function describes one production cycle
    def manufacture_interval(self):
        # change time (+ time interval from "config_data" class)
        self.env.timeout(self.config_data.time_interval)
        # if first day (for the first pass of the loop (manufacture_process function))
        if self.time_production == -1:
            self.time__days_production = 1 # edit days of production for 
        self.time_days_production += self.config_data.time_interval # add time to total production time
        self.time_production += self.config_data.time_interval # all time conveyor work (reset at the end of the day)
        # if conveyor is moving 
        if self.conveyor.status():
            # if less than three cars on conveyor
            if self.conveyor.numb_cars_on_conveyor() <= round(self.config_data.conveyor_length / (self.config_data.car_length + 2 * self.config_data.distance_between_cars)):    
                self.conveyor.add_car(car())
            # for every car at conveyor check finished vehicles and vehicles for recycling
            while self.conveyor.ready_disposal_cars():
                for iter in range(0, self.conveyor.numb_cars()):
                    # if ready car
                    if self.conveyor.cars_on_conveyor[iter].status == 'RC':
                        self.conveyor.cars_on_conveyor.pop(iter) # delete car from conveyor list
                        self.ready_cars += 1 # add one car to ready cars
                        break
                    # if car disposal
                    elif self.conveyor.cars_on_conveyor[iter].status == 'DS':
                        self.conveyor.cars_on_conveyor.pop(iter) # remove car from conveyor list
                        break
            # for every car at conveyor edit data
            for iter in range(0, self.conveyor.numb_cars()):
                # if conveyor is stop, break until conveyor start moving
                if self.conveyor.status() == False:
                    break
                # edit data for every car
                self.conveyor.cars_on_conveyor[iter].edit_data(self.parts_data, self.config_data, self.conveyor)      
        # if conveyor is stop
        else:
            self.conveyor.edit_stop_time(self.config_data.time_interval, self.parts_data) # reduce the stop time by time interval from "config_data" class

    # This function describes the production process 
    # for a selected interval specified in the "config_data" class.
    def manufacture_process(self):
       # search path to folder of program
        path =  str(os.path.dirname(os.path.abspath('manufacture.py')))
        # if Linux or MAC OS system
        if sys.platform == 'darwin' or sys.platform == 'linux':
            path += '/'
        # if Windows system
        elif sys.platform == 'win32':
            path += '\\'
         # create a file into which production data will be logged for subsequent analysis
        with open(path + 'logs.txt', 'w+') as file:
            with contextlib.redirect_stdout(file): # redirect the output to a log file
                # for all interval
                while (self.time_days_production / (self.config_data.change_time * 2 * 60)) < self.config_data.days_of_production:
                    # for every day
                    while self.time_production < (self.config_data.change_time * 2 * 60):
                        iter_time = 0 # iteration variable
                        # iterate over the interval of the car climbing onto the conveyor
                        # the user will see the data only for the interval that he entered
                        while iter_time < self.config_data.u_time_interval:
                            self.manufacture_interval() # go through the day at intervals
                            iter_time += self.config_data.interval_add_conveyor
                        print('\nNumber of cars on conveyor: {}\n'.format(self.conveyor.numb_cars_on_conveyor()))   # print number of cars on conveyor
                        print('Conveyor status: {}\n'.format(self.conveyor.status()))
                        # print every time interval parst data    
                        for iter_key in self.parts_data.parts_dict.keys():
                            print('{}: {}'.format(iter_key, self.parts_data.parts_dict[iter_key]))
                        print('\n')
                        for iter in range(0, self.conveyor.numb_cars()):
                            self.conveyor.cars_on_conveyor[iter].print_data() # and print this data   
                        # save to file data about paassed days and released cars for every day
                    print('\nAt this moment, passed {} days, released {} cars'.format(round(self.time_days_production / (self.config_data.change_time * 2 * 60)), self.ready_cars)) 
                    self.time_production = 0 # reset at the end of the day timer of work conveyor
                    print() # testing
    
    # This function displays the number of cars produced, the expected number of cars and the performance ratio (cars built / expected number of cars)
    def car_revenue(self):
        # number of expected cars that usine need to product
        expected_cars = round((self.config_data.days_of_production * (self.config_data.change_time * 2) - (self.config_data.change_time * 2)) / (self.config_data.conveyor_length / (self.config_data.conveyor_speed * 1000)) * self.config_data.max_car)
        print('\nCars produced: {}, expected to produce: {}, performance ratio: {}'.format(self.ready_cars, expected_cars, (self.ready_cars / expected_cars)))