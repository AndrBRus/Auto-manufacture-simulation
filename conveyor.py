# This module contains info about conveyor and actions on it.

# This class describes the conveyor,
# also all the functions that it can perform.
class conveyor(object):
    # class constructor 
    def __init__(self):
        self.work_status = True # status of conveyor work: True if conveyor is moving else False
        self.cars_on_conveyor = list() # list with cars on conveyor
        self.stop_time = 0 # time to delivery details
        self.stop_detail = list() # details that was stopping production
    
    # return status of conveyor work
    def status(self):
        return self.work_status
    
    # return status of number of cars now on conveyor
    def numb_cars(self):
        return len(self.cars_on_conveyor)
    
    def numb_cars_on_conveyor(self):
        numb_cars = 0
        for iter in range(0, len(self.cars_on_conveyor)):
            if self.cars_on_conveyor[iter].status != 'MD' or self.cars_on_conveyor[iter].status != 'DS':
                numb_cars += 1
        return numb_cars 
    
    # add car to conveyor
    def add_car(self, car):
        self.cars_on_conveyor.append(car)
    
    # add time to stop conveyor until delivery details
    def stop(self, part_details, part_name):
        # if more than one details need to delivery
        if type(part_name) == type(list()):
            time_delivery_list = list()
            for iter in part_name:
                time_delivery_list.append(part_details.parts_dict[iter][5] * 60)
                self.stop_detail.append(iter)
            # if stop time until delivery less that new time to delivery other detail
            if self.work_status == False and max(time_delivery_list) > self.stop_time:
                self.stop_time = max(time_delivery_list)  # edit stopping time
            # else if conveyor is moving
            elif self.work_status == True: 
                self.work_status = False # stop conveyor
                self.stop_time = max(time_delivery_list) # add stopping time
        # else one detail
        else:  
            # if stop time until delivery less that new time to delivery other detail
            if self.work_status == False and part_details.parts_dict[part_name][5] * 60 > self.stop_time:
                self.stop_time = part_details.parts_dict[part_name][5] * 60  # edit stopping time
            # else if conveyor is moving
            elif self.work_status == True:
                self.stop_time = part_details.parts_dict[part_name][5] * 60 # add time to stopping time
                self.work_status = False # stop moving 
            
            self.stop_detail.append(part_name) # add name to stopping detail 
    # this fucntion start conveyor and restores stocks of all details
    def start(self, parts_data):
        self.stop_time = 0  # reset stop time
        self.work_status = True  # conveyor is moving
        # if more than one detail in stopping list
        if type(self.stop_detail) == type(list()):
            # for each detail in stopping list
            for iter in self.stop_detail:
                parts_data.parts_dict[iter][0] += parts_data.parts_dict[iter][6]  # delivery parts to warehouse
            # cancellation of a stopping details list 
            self.stop_details = list()
        # if one detail in stopping list
        else:
            parts_data.parts_dict[self.stop_detail][0] += parts_data.parts_dict[self.stop_detail][6] # delivery parts to warehouse
    
    # this function is reduce stop time and starts conveyor if stop time is up
    def edit_stop_time(self, time_interval, parts_data):
        self.stop_time -= time_interval # reduce the stop time by time interval from "config_data" class
        # if stop time is up
        if self.stop_time <= 0:
            self.start(parts_data) # start conveyor
    
    # this function checks for finished machines or machines for disposal
    def ready_disposal_cars(self):
        # iterating through the whole list
        for iter in range(0, self.numb_cars()):
            # if there is a ready car or a car for recycling
            if self.cars_on_conveyor[iter].status == 'RC' or self.cars_on_conveyor[iter].status == 'DS':
                return True # then we return True
        return False # else return False