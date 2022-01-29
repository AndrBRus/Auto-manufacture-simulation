# This module contains information about configuration data

# This class describes the configuration variables 
# needed to simulate the production process.
class config_data(object):
    # class constructor
    def __init__(self, p_manufacture_defect, resolve_manufacture_defect, time_to_resolve_manufacture_defect, p_detail_defect, days_of_production, change_time, u_time_interval, welding_time, coloring_time, conveyor_length, conveyor_speed, car_length, distance_cars, numb_tests=1):
        self.change_time = change_time # time of one change at produciton
        self.u_time_interval = u_time_interval # user time interval (the interval in which the data in the file will be logged)
        self.p_manufacture_defect = p_manufacture_defect    # the likelihood of a manufacturing defect (common to all phases of production)
        self.p_detail_defect = p_detail_defect # the likelihoog of a detail defect (common to all details)
        self.welding_time = welding_time   # time it takes for the car to welding
        self.coloring_time = coloring_time  # time it takes for the car to paint
        self.car_length = car_length # length of car
        self.distance_between_cars = distance_cars # distance between two cars at conveyor
        self.conveyor_speed = conveyor_speed    # speed of conveyor
        self.conveyor_length = conveyor_length  # length of all conveyor
        self.days_of_production = days_of_production # days of prodcution cars 
        self.assembly_time = (self.conveyor_length / (self.conveyor_speed * 1000)) - self.welding_time - self.coloring_time # time to assembly car
        self.max_car = round(self.conveyor_length / (self.car_length + self.distance_between_cars * 2)) # max number of cars on conveyor
        self.resolve_manufacture_defect = resolve_manufacture_defect # the likelihoog of a detail defect correction (common to all details)
        self.time_to_resolve_manufacture_defect = time_to_resolve_manufacture_defect # time of a detail defect correction (common to all details)
        self.interval_add_conveyor = (self.car_length + self.distance_between_cars * 2) / ((self.conveyor_speed * 1000) / 60) # the interval of the appearance of the machine on the conveyor
        self.time_interval = (self.car_length + self.distance_between_cars * 2) / ((self.conveyor_speed * 1000) / 60)  # period of time in which the production check will be carried out
        self.numb_tests = int(numb_tests) # number of trials (number of repetitions over the selected interval)