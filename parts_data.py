import random
import site # this module uses to generate probabilities of defects
from conveyor import conveyor # import conveyor class with info about conveyor at usine

# This module describes all the parts that are used in the manufacture of a car

# This class describes the parts required for the production of the car, 
# their main characteristics, as well as the main actions on these types of parts.
class parts_data(object):
    # class constructor
    def __init__(self):
        # This dict describes each type of part: 
        #   - initial number of parts in stock
        #   - maximum quantity details in stocks
        #   - minimum quantity in stock
        #   - the amount of material required for one car
        #   - stage of delivery to the conveyor
        #   - the probability of defective parts
        #   - waiting time for new delivery
        #   - number of parts for delivery
        # Dict containt raw materials and consumables for all stage of produciton
        self.parts_dict = {
            'wl_raw_materials': [],
            'wl_consumables': [],
            'cl_raw_materials': [],
            'cl_consumables': [],
            'as_raw_materials': [],
            'as_consumables': []
        }
        
    # this function checks the availability of two types of parts in stock
    def check_pack(self, f_part_name, s_part_name, work_time=None, check_time=None):
        print('Work time {}, check_time {}'.format(work_time, check_time))
        status = None # status of checking welding details
        p_undelivery = random.random() # random value of undelivery
        # if we have all details  
        if ((self.parts_dict[f_part_name][0] - self.parts_dict[f_part_name][3]) > self.parts_dict[f_part_name][2]) == True and ((self.parts_dict[s_part_name][0] - self.parts_dict[s_part_name][3]) > self.parts_dict[s_part_name][2]) == True:
            status = [True, 'OK']  # status is OK: all details at warehouse
        # if no second type parts
        elif ((self.parts_dict[f_part_name][0] - self.parts_dict[f_part_name][3]) > self.parts_dict[f_part_name][2]) == True and ((self.parts_dict[s_part_name][0] - self.parts_dict[s_part_name][3]) > self.parts_dict[s_part_name][2]) == False:
            # if random value of undelivery is less than probability of undelivery
            if p_undelivery < self.parts_dict[s_part_name][5]:
                status = [False, s_part_name] # status is KO: no second part type
            # else status is OK: all details at warehouse
            else:
                status = [True, 'OK']
                # if an interval strategy is used, 
                # then the check is performed only after a certain interval specified by the user
                if check_time != None and work_time % check_time == 0:
                    # change the replenished stock to the one that is necessary to fill the warehouse to the maximum
                    self.parts_dict[s_part_name][7] = self.parts_dict[s_part_name][1] - self.parts_dict[s_part_name][0]
                    self.parts_dict[s_part_name][0] += self.parts_dict[s_part_name][7] # add details to warehouse
                # in other strategies
                else:
                    # if replenishment does not exceed the maximum stock size
                    if self.parts_dict[s_part_name][0] + self.parts_dict[s_part_name][7] <= self.parts_dict[s_part_name][1]:
                        self.parts_dict[s_part_name][0] += self.parts_dict[s_part_name][7] # add details to warehouse
        # if no first type parts
        elif ((self.parts_dict[f_part_name][0] - self.parts_dict[f_part_name][3]) > self.parts_dict[f_part_name][2]) == False and ((self.parts_dict[s_part_name][0] - self.parts_dict[s_part_name][3]) > self.parts_dict[s_part_name][2]) == True:
            # if random value of undelivery is less than probability of undelivery
            if p_undelivery < self.parts_dict[f_part_name][5]:
                status = [False, f_part_name] # status is KO: no first type parts
            # else status is OK: all details at warehouse
            else:
                status = [True, 'OK']
                # if an interval strategy is used, 
                # then the check is performed only after a certain interval specified by the user
                if check_time != None and work_time % check_time == 0:
                    # change the replenished stock to the one that is necessary to fill the warehouse to the maximum
                    self.parts_dict[f_part_name][7] = self.parts_dict[f_part_name][1] - self.parts_dict[f_part_name][0]
                    self.parts_dict[f_part_name][0] += self.parts_dict[f_part_name][7] # add details to warehouse
                # in other strategies
                else:
                    # if replenishment does not exceed the maximum stock size
                    if self.parts_dict[f_part_name][0] + self.parts_dict[f_part_name][7] <= self.parts_dict[f_part_name][1]:
                        self.parts_dict[f_part_name][0] += self.parts_dict[f_part_name][7] # add details to warehouse
        # else no all details at warehouse
        else:
            # if random value of undelivery is less than probability of undelivery (first type parts)
            if p_undelivery < self.parts_dict[f_part_name][5] == True and p_undelivery < self.parts_dict[s_part_name][5] == False:
                status = [False, f_part_name] # status is KO: no first type parts
            # if random value of undelivery is less than probability of undelivery (second type parts)
            elif p_undelivery < self.parts_dict[f_part_name][5] == False and p_undelivery < self.parts_dict[s_part_name][5] == True:
                status = [False, s_part_name] # status is KO: no second type parts
             # if random value of undelivery is less than probability of undelivery (all details) 
            elif p_undelivery < self.parts_dict[f_part_name][5] == True and p_undelivery < self.parts_dict[s_part_name][5] == True:
                status = [False, f_part_name, s_part_name] # status is KO: no all types of parts
            # else all details at warehouse 
            else:
                status = [True, 'OK']
                # if an interval strategy is used, 
                # then the check is performed only after a certain interval specified by the user
                if check_time != None and work_time % check_time == 0:
                    # change the replenished stock to the one that is necessary to fill the warehouse to the maximum
                    self.parts_dict[f_part_name][7] = self.parts_dict[f_part_name][1] - self.parts_dict[f_part_name][0]
                    self.parts_dict[s_part_name][7] = self.parts_dict[s_part_name][1] - self.parts_dict[s_part_name][0]

                    self.parts_dict[f_part_name][0] += self.parts_dict[f_part_name][7] # add details to warehouse
                    self.parts_dict[s_part_name][0] += self.parts_dict[s_part_name][7] # add details to warehouse    
                # in other strategies
                else:
                    # if replenishment does not exceed the maximum stock size
                    if self.parts_dict[f_part_name][0] + self.parts_dict[f_part_name][7] <= self.parts_dict[f_part_name][1]:
                        self.parts_dict[f_part_name][0] += self.parts_dict[f_part_name][7] # add details to warehouse
                    # if replenishment does not exceed the maximum stock size
                    if self.parts_dict[s_part_name][0] + self.parts_dict[s_part_name][7] <= self.parts_dict[s_part_name][1]:
                        self.parts_dict[s_part_name][0] += self.parts_dict[s_part_name][7] # add details to warehouse    
        # return status of checking details
        return status

    # changes in the number of purchased parts to what was used today
    def check_used_day_details(self, conveyor):
        site_numb_cars = conveyor.numb_cars_site() # calculation of the number of cars at each stage
        # for each of the stages: "WL", "CL", "AS", - calculate the number of parts used, 
        # and change the quantity for purchase by the number of parts used per day
        # and then buy
        for key in site_numb_cars.keys():
            if key == 'WL':
                self.parts_dict['wl_raw_materials'][7] = (site_numb_cars[key] + site_numb_cars['RC'] + site_numb_cars['AS'] + site_numb_cars['CL']) * self.parts_dict['wl_raw_materials'][3]
                self.parts_dict['wl_raw_materials'][0] += self.parts_dict['wl_raw_materials'][7]
                self.parts_dict['wl_consumables'][7] = (site_numb_cars[key] + site_numb_cars['RC'] + site_numb_cars['AS'] + site_numb_cars['CL']) * self.parts_dict['wl_consumables'][3]
                self.parts_dict['wl_consumables'][0] += self.parts_dict['wl_consumables'][7]
            elif key == 'CL':
                self.parts_dict['cl_raw_materials'][7] = (site_numb_cars[key] + site_numb_cars['RC'] + site_numb_cars['AS']) * self.parts_dict['cl_raw_materials'][3]
                self.parts_dict['cl_consumables'][7] = (site_numb_cars[key] + site_numb_cars['RC'] + site_numb_cars['AS']) * self.parts_dict['cl_consumables'][3]
                self.parts_dict['cl_consumables'][0] += self.parts_dict['cl_consumables'][7]
            elif key == 'AS':
                self.parts_dict['as_raw_materials'][7] = (site_numb_cars[key] + site_numb_cars['RC']) * self.parts_dict['as_raw_materials'][3]
                self.parts_dict['as_raw_materials'][0] += self.parts_dict['as_raw_materials'][7]
                self.parts_dict['as_consumables'][7] = (site_numb_cars[key] + site_numb_cars['RC']) * self.parts_dict['as_consumables'][3]
                self.parts_dict['as_consumables'][0] += self.parts_dict['as_consumables'][7]

    # A function that fills a dict with spare parts data
    def get_data(self, part_name, list_data):
        self.parts_dict[part_name] = list_data