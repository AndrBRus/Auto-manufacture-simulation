import random # this module uses to generate probabilities of defects

# This module describes all the parts that are used in the manufacture of a car

# This class describes the parts required for the production of the car, 
# their main characteristics, as well as the main actions on these types of parts.
class parts_data(object):
    # class constructor
    def __init__(self):
        # This dict describes each type of part: 
        #   - initial number of parts in stock
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
    def check_pack(self, f_part_name, s_part_name):
        status = None # status of checking welding details
        p_undelivery = random.random() # random value of undelivery
        # if we have all details  
        if ((self.parts_dict[f_part_name][0] - self.parts_dict[f_part_name][2]) > self.parts_dict[f_part_name][1]) == True and ((self.parts_dict[s_part_name][0] - self.parts_dict[s_part_name][2]) > self.parts_dict[s_part_name][1]) == True:
            status = [True, 'OK']  # status is OK: all details at warehouse
        # if no second type parts
        elif ((self.parts_dict[f_part_name][0] - self.parts_dict[f_part_name][2]) > self.parts_dict[f_part_name][1]) == True and ((self.parts_dict[s_part_name][0] - self.parts_dict[s_part_name][2]) > self.parts_dict[s_part_name][1]) == False:
            # if random value of undelivery is less than probability of undelivery
            if p_undelivery < self.parts_dict[s_part_name][4]:
                status = [False, s_part_name] # status is KO: no second part type
            # else status is OK: all details at warehouse
            else:
                status = [True, 'OK']
                self.parts_dict[s_part_name][0] += self.parts_dict[s_part_name][6] # add details to warehouse
        # if no first type parts
        elif ((self.parts_dict[f_part_name][0] - self.parts_dict[f_part_name][2]) > self.parts_dict[f_part_name][1]) == False and ((self.parts_dict[s_part_name][0] - self.parts_dict[s_part_name][2]) > self.parts_dict[s_part_name][1]) == True:
            # if random value of undelivery is less than probability of undelivery
            if p_undelivery < self.parts_dict[f_part_name][4]:
                status = [False, f_part_name] # status is KO: no first type parts
            # else status is OK: all details at warehouse
            else:
                status = [True, 'OK']
                self.parts_dict[f_part_name][0] += self.parts_dict[f_part_name][6] # add details to warehouse
        # else no all details at warehouse
        else:
            # if random value of undelivery is less than probability of undelivery (first type parts)
            if p_undelivery < self.parts_dict[f_part_name][4] == True and p_undelivery < self.parts_dict[s_part_name][4] == False:
                status = [False, f_part_name] # status is KO: no first type parts
            # if random value of undelivery is less than probability of undelivery (second type parts)
            elif p_undelivery < self.parts_dict[f_part_name][4] == False and p_undelivery < self.parts_dict[s_part_name][4] == True:
                status = [False, s_part_name] # status is KO: no second type parts
             # if random value of undelivery is less than probability of undelivery (all details) 
            elif p_undelivery < self.parts_dict[f_part_name][4] == True and p_undelivery < self.parts_dict[s_part_name][4] == True:
                status = [False, f_part_name, s_part_name] # status is KO: no all types of parts
            # else all details at warehouse 
            else:
                status = [True, 'OK']
                self.parts_dict[f_part_name][0] += self.parts_dict[f_part_name][6] # add details to warehouse
                self.parts_dict[s_part_name][0] += self.parts_dict[s_part_name][6] # add details to warehouse    
        # return status of checking details
        return status
        
    # A function that fills a dict with spare parts data
    def get_data(self, part_name, list_data):
        self.parts_dict[part_name] = list_data