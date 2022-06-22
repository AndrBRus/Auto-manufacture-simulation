import random # this module uses to generate probabilities of defects

# This module contains information about the machine on the conveyor

# This class describes the car that manufactere product.
# The selection of vehicles for recycling and finished vehicles will be held in the "manufacture" class at function "manufacture_interval".
class car(object):
    # class constructor
    def __init__(self):
        self.status = None  # stage at conveyor: 'WL', 'CL', 'AS', 'MD', 'DS', 'RC' (described below)
        self.on_conveyor = True # the status of the machine being on the conveyor
        self.time_defect = 0 # time to correct defect
        self.time_on_conveyor = 0   # time on conveyor before release
        self.last_status = None # last status if car now at 'MD' status 

    # This function edits class data according to pipeline advance timeю
    # The status of the car may be as follows:  
    #   - WL - welding
    #   - CL - coloring
    #   - AS - assembly
    #   - MD - manufacture defect
    #   - DS - disposal body
    #   - RC - ready car
    # work_time - pipeline operation time, check_time - check interval to interval strategy
    def edit_data(self, parts_data, config_data, conveyor, work_time, check_time):
        manufacture_detail_defect = random.random() # generate random variable for detail defect at conveyor
        manufacture_defect = random.random() # generate random variable for manufacture defect at conveyor
        resolve_manufacture_defect = random.random() # generate random variable for is it possible to correct a manufacturing defect

        # if car at conveyor
        if self.on_conveyor:
            # if the car has just entered the conveyor
            if self.time_on_conveyor == 0:
                # if appeared detail defect 
                if manufacture_detail_defect < config_data.p_detail_defect:
                    # iterate twice to deduct for two parts
                    for iter in range(0, 2):
                        # check if production have details at warehouse
                        wl_second_check = parts_data.check_pack('wl_raw_materials', 'wl_consumables', work_time, check_time)
                        # if production have details at warehouse
                        if wl_second_check[0]:
                            self.time_on_conveyor += config_data.time_interval  # add time on conveyor
                            self.status = 'WL'  # set status
                            parts_data.parts_dict['wl_raw_materials'][0] -= parts_data.parts_dict['wl_raw_materials'][3] # spend materials for a defective part and for the one that was used in production
                            parts_data.parts_dict['wl_consumables'][0] -= parts_data.parts_dict['wl_consumables'][3] # spend materials for a defective part and for the one that was used in production
                        # if no details at warehouse
                        else:
                            conveyor.stop(parts_data, wl_second_check[1])   # stop conveyor
                else:
                    # check if production have details at warehouse
                    wl_second_check = parts_data.check_pack('wl_raw_materials', 'wl_consumables', work_time, check_time)
                    # if production have details at warehouse
                    if wl_second_check[0]:
                        self.time_on_conveyor += config_data.time_interval  # add time on conveyor
                        self.status = 'WL'  # set status
                        parts_data.parts_dict['wl_raw_materials'][0] -= parts_data.parts_dict['wl_raw_materials'][3] # spend materials for a part and for that was used in production
                        parts_data.parts_dict['wl_consumables'][0] -= parts_data.parts_dict['wl_consumables'][3] # spend materials for a part that was used in production
                    # if no details at warehouse
                    else:
                        conveyor.stop(parts_data, wl_second_check[1])   # stop conveyor
            # if the car if the car goes from one stage to another        
            elif ((self.time_on_conveyor < (config_data.welding_time * 60)) and ((self.time_on_conveyor  + config_data.time_interval) >= (config_data.welding_time * 60))) or ((self.time_on_conveyor < ((config_data.welding_time + config_data.coloring_time) * 60)) and ((self.time_on_conveyor  + config_data.time_interval) >= ((config_data.welding_time + config_data.coloring_time) * 60))):
                # if appeared manufacture defectx
                if manufacture_defect < config_data.p_manufacture_defect:
                    # if production can't correct this defect
                    if resolve_manufacture_defect < config_data.resolve_manufacture_defect:
                        # send the car for recycling
                        self.status = 'DS'
                        self.on_conveyor = False # change status "on conveyor" to not at conveyor 
                    # if production can correct defect
                    else:
                        self.last_status = self.status  # save last status of car on conveyor
                        self.status = 'MD'  # change status to "manufacture defect"
                        self.time_defect = config_data.time_to_resolve_manufacture_defect * 60  # add time to correct defect
                        self.on_conveyor = False # change status "on conveyor" to not at conveyor
                # if car haven't manufacture defect
                else:
                    # if car at welding
                    if self.status == 'WL':
                        # check detailt from coloring to defect, and if it have
                        if manufacture_detail_defect < config_data.p_detail_defect:
                            # iter two 
                            # iterate twice to deduct for two parts
                            for iter in range(0, 2):
                                cl_check = parts_data.check_pack('cl_raw_materials', 'cl_consumables', work_time, check_time)  # check details at warehouse
                                # if details at warehouse
                                if cl_check[0]:
                                    self.time_on_conveyor += config_data.time_interval  # add time to time on conveyor of car
                                    self.status = 'CL'  # change car to coloring stage
                                    parts_data.parts_dict['cl_raw_materials'][0] -= parts_data.parts_dict['cl_raw_materials'][3] # spend materials for a defective part and for the one that was used in production
                                    parts_data.parts_dict['cl_consumables'][0] -= parts_data.parts_dict['cl_consumables'][3] # spend materials for a defective part and for the one that was used in production
                                # if details aren't at warehouse
                                else:
                                    conveyor.stop(parts_data, cl_check[1]) # stop conveyor
                        # if no defect parts at coloring 
                        else:
                            # check if production have details at warehouse
                            cl_check = parts_data.check_pack('cl_raw_materials', 'cl_consumables', work_time, check_time)
                            # if production have details at warehouse
                            if cl_check[0]:
                                self.time_on_conveyor += config_data.time_interval  # add time on conveyor
                                self.status = 'CL'  # set status
                                parts_data.parts_dict['cl_raw_materials'][0] -= parts_data.parts_dict['cl_raw_materials'][3] # spend materials for a part and for that was used in production
                                parts_data.parts_dict['cl_consumables'][0] -= parts_data.parts_dict['cl_consumables'][3] # spend materials for a part that was used in production
                            # if no details at warehouse
                            else:
                                conveyor.stop(parts_data, cl_check[1])   # stop conveyor
                    # if cat at coloring
                    elif self.status == 'CL':
                        # check detailt from assembly to defect, and if it have
                        if manufacture_detail_defect < config_data.p_detail_defect:
                            # iterate twice to deduct for two parts
                            for iter in range(0, 2):
                                as_check = parts_data.check_pack('as_raw_materials', 'as_consumables', work_time, check_time) # check details at warehouse
                                # if details at warehouse
                                if as_check[0]:
                                    self.time_on_conveyor += config_data.time_interval  # add time to time on conveyor of car
                                    self.status = 'AS' # change car to assembly stage
                                    parts_data.parts_dict['as_raw_materials'][0] -= parts_data.parts_dict['as_raw_materials'][3] # spend materials for a defective part and for the one that was used in production
                                    parts_data.parts_dict['as_consumables'][0] -= parts_data.parts_dict['as_consumables'][3] # spend materials for a defective part and for the one that was used in production
                                # if details aren't at warehouse
                                else:
                                    conveyor.stop(parts_data, as_check[1]) # stop conveyor
                        # if no defect parts at assembly 
                        else:
                            # check if production have details at warehouse
                            as_check = parts_data.check_pack('as_raw_materials', 'as_consumables', work_time, check_time)
                            # if production have details at warehouse
                            if as_check[0]:
                                self.time_on_conveyor += config_data.time_interval  # add time on conveyor
                                self.status = 'AS'  # set status
                                parts_data.parts_dict['as_raw_materials'][0] -= parts_data.parts_dict['as_raw_materials'][3] # spend materials for a part and for that was used in production
                                parts_data.parts_dict['as_consumables'][0] -= parts_data.parts_dict['as_consumables'][3] # spend materials for a part that was used in production
                            # if no details at warehouse
                            else:
                                conveyor.stop(parts_data, as_check[1])   # stop conveyor
            # if car doesn't change stage and now at conveyor
            elif self.time_on_conveyor < ((config_data.welding_time + config_data.coloring_time + config_data.assembly_time) * 60):
                self.time_on_conveyor += config_data.time_interval  # add time to time on conveyor of car
            # if car ready
            elif self.status == 'AS' and self.time_on_conveyor >= ((config_data.welding_time + config_data.coloring_time + config_data.assembly_time) * 60):
                self.status = 'RC'  # change status to 
                self.on_conveyor = False # remove the car from the conveyor
        # if car not at conveyor
        else:
            # if time to correct defect more than 0
            if self.time_defect > 0:
                self.time_defect -= config_data.time_interval   # subtract from the time to correct defect interval of manufacture
            # else if defect corrected
            else:
                self.status = self.last_status # return last status from conveyor
                self.on_conveyor = True # return to conveyor
                self.last_status = None # reset last status to None

    # print data about car at conveyor    
    def print_data(self):
        # print status of stage, time on conveyor and status if car at conveyor, or not
        print('Car at {} stage, time on conveyor {}, conveyor status: {}'.format(self.status, "%.2f" % ((self.time_on_conveyor) / 60), self.on_conveyor))