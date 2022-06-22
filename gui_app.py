from statistics import mean
import tkinter
import tkinter.messagebox
from load_data import  INPUT_CONFIG_PRINT, INPUT_PARTS_PRINT, PARTS_DATA_NAME
from math import prod
from delete_logs import delete_logs
import simpy # this module uses to simulate production process
from config_data import config_data # import config_data class with configuration data 
from parts_data import parts_data # import parts_data class with info about all parts
from car import car # import car class with info about car on conveyor
from conveyor import conveyor # import conveyor class with info about conveyor at usine
from manufacture import manufacture # import manufacture class with manufacture process at usine
from delete_logs import delete_logs # import from delete_logs module function for delete all logs flies from logs folder
import numpy
import seaborn
import matplotlib
import matplotlib.backends
import matplotlib.backends.backend_tkagg

FULL_PARTS_DATA_NAME = ['Welding raw materials', 'Welding consumables', 'Coloring raw materials', 'Coloring consumables', 'Assembly raw materials', 'Coloring consumables']

class manufacture_data(): 
    def __init__(self):
        self.config = None
        self.parts = parts_data()
    
    def add_config_data(self, values):
        self.config = config_data(*values)

    def add_parts_data(self, part_name, part_data):
        self.parts.get_data(part_name, part_data)

    def strategy_type(self):
        return self.config.strategy

    def config_max_cars(self):
        return self.config.max_car

    def config_status(self):
        if self.config == None:
            return False
        else:
            return True

    def parts_data(self):
        return self.parts

    def config_data(self):
        return self.config

    def numb_tests(self):
        return self.config.numb_tests

    def expected_cars(self):
        expected_cars = round((self.config.days_of_production * (self.config.change_time * 2) - (self.config.change_time * 2)) / (self.config.conveyor_length / (self.config.conveyor_speed * 1000)) * self.config.max_car)
        return expected_cars

DATA_MANUFACTURE_PROCESS = manufacture_data()



class main_menu_gui(tkinter.Tk):
    def __init__(self):
        super().__init__()
        self.title('AUTOMANUFACTURE SIMULATION')
        self.geometry('400x350+550+350')

        main_menu_label = tkinter.Label(self, text='MAIN MENU', font='Helvetica 20 bold', justify=tkinter.CENTER)
        main_menu_label.place(relx=.5, rely=.12, anchor='c')

        load_data_btn = tkinter.Button(self, text='Load data', padx='20', pady='8', font='Helvetica 15', command=self.open_load_menu_gui)
        load_data_btn.pack()
        load_data_btn.place(width=350, height=50, relx=.5, rely=.3, anchor='c', bordermode=tkinter.OUTSIDE)

        modeling_once_btn = tkinter.Button(self, text='Modeling (once)', padx='20', pady='8', font='Helvetica 15', command=self.start_modeling_once)
        modeling_once_btn.pack()
        modeling_once_btn.place(width=350, height=50, relx=.5, rely=.5, anchor='c', bordermode=tkinter.OUTSIDE)

        full_modeling_btn = tkinter.Button(self, text='Full modeling', padx='20', pady='8', font='Helvetica 15', command=self.start_full_modeling)
        full_modeling_btn.pack()
        full_modeling_btn.place(width=350, height=50, relx=.5, rely=.7, anchor='c', bordermode=tkinter.OUTSIDE)

        copyright_label = tkinter.Label(self, text='© Andrey Vladimirov, 2022', font='Helvetica')
        copyright_label.place(relx=.005, rely=.99, anchor='sw')


    def open_load_menu_gui(self):
        load_menu = load_menu_gui()
        self.destroy()
        load_menu.grab_set()

    def start_modeling_once(self):
        tkinter.messagebox.showinfo('SIMULATION WORKING', 'The simulation model is running.\nWait for the model completion window to appear with the results.\nYou can find a more detailed description of how the model works in the log folder.')
        
        delete_logs() # delete all logs files before start modeling

        manufacture_env = simpy.Environment() # create env for manufacture timer 
        manufacture_process = manufacture(manufacture_env, conveyor(), DATA_MANUFACTURE_PROCESS.parts_data(), DATA_MANUFACTURE_PROCESS.config_data(), 'gui')   # create a class 
        # start manufacture process
        manufacture_process.manufacture_process()
        
        result = manufacture_process.car_revenue()

        tkinter.messagebox.showinfo('SIMULATION RESULT', 'Total cars produced: {}.\nExpected number of cars: {}.\nProductivity factor: {:.4f}.\nYou can find a more detailed description of how the model works in the log folder.'.format(result[0], result[1], result[2]))


    def start_full_modeling(self):
        delete_logs() # delete all logs files before start modeling
        
        tkinter.messagebox.showinfo('SIMULATION WORKING', 'The simulation model is running.\nWait for the model completion window to appear with the results.\nYou can find a more detailed description of how the model works in the log folder.')
        
        manufacture_env = simpy.Environment() # create env for manufacture timer
            
        production_data = list() # create empty list for data about all modeling processes
        # we carry out tests (the number of tests is specified by the user)
        for iter in range(0, DATA_MANUFACTURE_PROCESS.numb_tests()):
            manufacture_process = manufacture(manufacture_env, conveyor(), DATA_MANUFACTURE_PROCESS.parts_data(), DATA_MANUFACTURE_PROCESS.config_data(), 'gui') # create a class (the class is re-created for each test for a new generation of random variables)
            manufacture_process.manufacture_process() # start manufacture process
            production_data.append(manufacture_process.car_revenue('full')) # add to list data about end result of the simulation

        # variables for average number of produced cars and average perfomance ratio
        average_ready_cars = 0
        average_perfomance_ratio = 0
        # sum all values in production_data list
        for iter in range(0, len(production_data)):
            average_perfomance_ratio += production_data[iter][1]
        # find average values for this two variables
        average_perfomance_ratio /= len(production_data)
        # find number of expected cars for modeling test (the same for everyone)
        expected_cars = DATA_MANUFACTURE_PROCESS.expected_cars()

        production_cars_all_days = list()
        for iter in range(0, len(production_data)):
            production_cars_all_days.append(production_data[iter][0])

        mean_value_cars = numpy.mean(production_cars_all_days) 

        unique_elements, count_unique_elemenets = numpy.unique(production_cars_all_days, return_counts=True)
        prob_unique_elements = count_unique_elemenets / len(production_data)

        prob_more_mean_value = 0
        for iter in range(0, len(prob_unique_elements)):
            if unique_elements[iter] > mean_value_cars:
                prob_more_mean_value += prob_unique_elements[iter]

        result_plot = result_plot_gui(unique_elements, prob_unique_elements)

        tkinter.messagebox.showinfo('SIMULATION RESULT', 'Mean value of cars produced: {:.0f}.\nProbability of overcoming {:.0f} cars: {:.2f}.\nExpected number of cars: {}.\nAverage productivity factor: {:.4f}.\nYou can find a more detailed description of how the model works in the log folder.'.format(mean_value_cars, mean_value_cars, prob_more_mean_value, expected_cars, average_perfomance_ratio))

class result_plot_gui(tkinter.Tk):
    def __init__(self, unique_elements, prob_unique_elements):
        super().__init__()
        self.title('SIMULATION PLOT RESULT')
        self.geometry('600x500+550+350')

        figure = matplotlib.figure.Figure(figsize=(6, 4), dpi=100)
        figure_canvas = matplotlib.backends.backend_tkagg.FigureCanvasTkAgg(figure, self)
        matplotlib.backends.backend_tkagg.NavigationToolbar2Tk(figure_canvas, self)
        axes = figure.add_subplot()
        axes.bar(unique_elements, prob_unique_elements)
        axes.set_title('Distribution of produced cars')
        axes.set_ylabel('Probability')
        figure_canvas.get_tk_widget().pack(side=tkinter.TOP, fill=tkinter.BOTH, expand=1)
        mean_cars_value = 1
        expected_cars = 1
        prob_more_mean_value = 1
        average_perfomance_ratio = 1
        mean_cars_label = tkinter.Label(self, text='Mean value of produced cars: {}'.format(mean_cars_value), font='Helvetica 15')
        expected_cars_label = tkinter.Label(self, text='Expected number of produced cars: {}'.format(expected_cars), font='Helvetica 15')
        average_numb_cars_label = tkinter.Label(self, text='Probability of overcoming {} cars: {}'.format(mean_cars_value, prob_more_mean_value), font='Helvetica 15')
        average_perfomance_label = tkinter.Label(self, text='Average perfomance ration: {}'.format(average_perfomance_ratio), font='Helvetica 15')
        

class load_menu_gui(tkinter.Tk):
    def __init__(self):
        super().__init__()
        self.title('AUTOMANUFACTURE SIMULATION')
        self.geometry('400x350+550+350')

        load_menu_label = tkinter.Label(self, text='LOADING DATA MENU', font='Helvetica 20 bold', justify=tkinter.CENTER)
        load_menu_label.place(relx=.5, rely=.07, anchor='c')

        load_config_data_btn = tkinter.Button(self, text='Loading config data', padx='20', pady='8', font='Helvetica 15', command=self.open_load_config_menu_gui)
        load_config_data_btn.pack()
        load_config_data_btn.place(width=350, height=50, relx=.5, rely=.2, anchor='c', bordermode=tkinter.OUTSIDE)

        load_parts_data_btn = tkinter.Button(self, text='Loading parts data', padx='20', pady='8', font='Helvetica 15', command=self.open_load_parts_menu_gui)
        load_parts_data_btn.pack()
        load_parts_data_btn.place(width=350, height=50, relx=.5, rely=.4, anchor='c', bordermode=tkinter.OUTSIDE)

        templates_btn = tkinter.Button(self, text='Template data', padx='20', pady='8', font='Helvetica 15', command=self.templates_menu_gui)
        templates_btn.pack()
        templates_btn.place(width=350, height=50, relx=.5, rely=.6, anchor='c', bordermode=tkinter.OUTSIDE)

        main_menu_btn = tkinter.Button(self, text='Go to Main Menu', padx='20', pady='8', font='Helvetica 15', command=self.open_main_menu_gui)
        main_menu_btn.pack()
        main_menu_btn.place(width=350, height=50, relx=.5, rely=.8, anchor='c', bordermode=tkinter.OUTSIDE)

        copyright_label = tkinter.Label(self, text='© Andrey Vladimirov, 2022', font='Helvetica')
        copyright_label.place(relx=.005, rely=.99, anchor='sw')

    def open_main_menu_gui(self):
        main_menu = main_menu_gui()
        self.destroy()
        main_menu.grab_set()

    def open_load_config_menu_gui(self):
        load_config_data_menu = load_config_data_menu_gui()
        self.destroy()
        load_config_data_menu.grab_set()

    def open_load_parts_menu_gui(self):
        
        if DATA_MANUFACTURE_PROCESS.config_status() == False:
            tkinter.messagebox.showerror('ERROR MESSAGE', 'First input config data!')
            return None

        load_parts_data_menu = load_parts_data_menu_gui()
        self.destroy()
        load_parts_data_menu.grab_set()

    def templates_menu_gui(self):
        load_parts_data_menu = templates_menu_gui()
        self.destroy()
        load_parts_data_menu.grab_set()

class load_config_data_menu_gui(tkinter.Tk):
    def __init__(self):
        super().__init__()
        self.title('AUTOMANUFACTURE SIMULATION')
        self.geometry('900x700+550+350')

        row = 0
        self.input_data = list()
        for iter in range(0, len(INPUT_CONFIG_PRINT)):
            self.input_data.append(tkinter.StringVar())
        for iter in range(0, len(INPUT_CONFIG_PRINT)):
            create_label = tkinter.Label(self, text=INPUT_CONFIG_PRINT[iter], font='Helvetica 15')
            create_label.grid(row=row, column=0, padx=5, pady=5, sticky='w')
            entry_create_label = tkinter.Entry(self, textvariable=self.input_data[iter], font='Helvetica 15')
            entry_create_label.grid(row=row, column=1, padx=5, pady=5, sticky='e')
            create_label.place()
            entry_create_label.place()
            row += 1

        add_config_data_btn = tkinter.Button(text='Add config data', font='Helvetica 12', command=self.add_config_data)
        add_config_data_btn.grid(row=row, column=1, padx=5, pady=7, sticky='w')
        back_btn = tkinter.Button(text='Back', font='Helvetica 12', command=self.open_load_data_menu_gui)
        back_btn.grid(row=row, column=1, padx=5, pady=7, sticky='e')
        add_config_data_btn.place()
        back_btn.place()

    def open_load_data_menu_gui(self):
        load_menu = load_menu_gui()
        self.destroy()
        load_menu.grab_set()

    def add_config_data(self):
        result_input_data = list()
        try:
            for iter in range(0, len(self.input_data)):
                if iter == 13:
                    if str(self.input_data[13].get()).upper() in ['B', 'I', 'U']:
                        result_input_data.append(str(self.input_data[iter].get()))
                    else:
                        raise ValueError
                elif iter == 4 or iter == 14:
                    result_input_data.append(int(self.input_data[iter].get()))
                elif iter == 15:
                    if self.input_data[13].get() == 'I':
                        if float(self.input_data[15].get()) % 5 == 0:
                            result_input_data.append(iter(self.input_data[iter].get()))
                        else:
                            raise ValueError
                    else:
                        pass
                else:
                    result_input_data.append(float(self.input_data[iter].get()))
        except ValueError:
            tkinter.messagebox.showerror('ERROR MESSAGE', 'Error at value: "{}"'.format(INPUT_CONFIG_PRINT[iter]))
        
        DATA_MANUFACTURE_PROCESS.add_config_data(result_input_data)

        tkinter.messagebox.showinfo('ADD DATA RESULT', 'Config data added to program!')
        
        load_menu = load_menu_gui()
        self.destroy()
        load_menu.grab_set()
        
class load_parts_data_menu_gui(tkinter.Tk):
    def __init__(self):
        super().__init__()
        self.title('AUTOMANUFACTURE SIMULATION')
        self.geometry('1200x650+550+350')

        self.input_data = list()

        for iter_parts in range(0, len(PARTS_DATA_NAME)):
            self.input_data.append(list())
            for iter_data in range(0, len(INPUT_PARTS_PRINT)):
               self. input_data[iter_parts].append(tkinter.StringVar())


        row = 0
        column = 0

        for iter_part_name in range(0, len(FULL_PARTS_DATA_NAME)):
            part_name_label = tkinter.Label(self, text=FULL_PARTS_DATA_NAME[iter_part_name], font='Helvetica 15')
            part_name_label.grid(row=row, column=column, padx=5, pady=5)
            part_name_label.place()
            
            row += 1

            for iter_data_name in range(0, len(INPUT_PARTS_PRINT)):
                data_label = tkinter.Label(self, text=INPUT_PARTS_PRINT[iter_data_name], font='Helvetica 10')
                data_label.grid(row=row, column=column, padx=5, pady=5, sticky='w')
                entry_data_label = tkinter.Entry(self, textvariable=self.input_data[iter_part_name][iter_data_name], font='Helvetica 10')
                if iter_data_name == 7 and DATA_MANUFACTURE_PROCESS.strategy_type() == 'B':
                    entry_data_label.config(state='disable')
                else:
                    entry_data_label.config(state='normal')
                entry_data_label.grid(row=row, column=column+1, padx=5, pady=5, sticky='e')
                
                data_label.place()
                entry_data_label.place()

                row += 1

            if iter_part_name == 1 or iter_part_name == 3:
                column += 2
                row = 0

        add_parts_data_btn = tkinter.Button(text='Add parts data', font='Helvetica 12', command=self.add_parts_data)
        add_parts_data_btn.grid(row=row, column=0, padx=5, pady=7, sticky='es')
        back_btn = tkinter.Button(text='Back', font='Helvetica 12', command=self.open_load_data_menu_gui)
        back_btn.grid(row=row, column=column+1, padx=5, pady=7, sticky='ws')
        add_parts_data_btn.place()
        back_btn.place()
    
    def open_load_data_menu_gui(self):
        load_menu = load_menu_gui()
        self.destroy()
        load_menu.grab_set()

    def add_parts_data(self):
        result_input_data = list()

        for iter_part in range(0, len(self.input_data)):
            result_input_data.append(list())

        try:
            for iter_part in range(0, len(self.input_data)):
                for iter_data in range(0, len(INPUT_PARTS_PRINT)):
                    if iter_data == 7 and DATA_MANUFACTURE_PROCESS.strategy_type() == 'B':
                        result_input_data[iter_part].append(int(self.input_data[iter_part][iter_data-4].get()) * DATA_MANUFACTURE_PROCESS.config_max_cars())
                        continue
                    if iter_data == 5 or iter_data == 6:
                        result_input_data[iter_part].append(float(self.input_data[iter_part][iter_data].get()))
                    else:
                        result_input_data[iter_part].append(int(self.input_data[iter_part][iter_data].get()))
        except ValueError:
            tkinter.messagebox.showerror('ERROR MESSAGE', 'Error at value "{}" at part "{}"'.format(INPUT_PARTS_PRINT[iter_data], FULL_PARTS_DATA_NAME[iter_part]))
            
        for iter_part in range(0, len(FULL_PARTS_DATA_NAME)):
            DATA_MANUFACTURE_PROCESS.add_parts_data(PARTS_DATA_NAME[iter_part], result_input_data[iter_part])
    
        tkinter.messagebox.showinfo('ADD DATA RESULT', 'Parts data added to program!')
        
        load_menu = load_menu_gui()
        self.destroy()
        load_menu.grab_set()   
           
class templates_menu_gui(tkinter.Tk):
    def __init__(self):
        super().__init__()
        self.title('AUTOMANUFACTURE SIMULATION')
        self.geometry('510x400+550+350')

        loading_templates_label = tkinter.Label(self, text='TEMPLATES MENU', font='Helvetica 20 bold', justify=tkinter.CENTER)
        loading_templates_label.place(relx=.5, rely=.07, anchor='c')

        load_user_input_template_btn = tkinter.Button(self, text='Loading custom inventory level template (Ss strategy)', padx='20', pady='8', font='Helvetica 15', command=self.load_user_input_template)
        load_user_input_template_btn.pack()
        load_user_input_template_btn.place(width=490, height=50, relx=.5, rely=.2, anchor='c', bordermode=tkinter.OUTSIDE)

        load_interval_template_btn = tkinter.Button(self, text='Loading interval strategy template', padx='20', pady='8', font='Helvetica 15', command=self.load_interval_template)
        load_interval_template_btn.pack()
        load_interval_template_btn.place(width=490, height=50, relx=.5, rely=.4, anchor='c', bordermode=tkinter.OUTSIDE)

        load_buy_yesterday_template_btn = tkinter.Button(self, text='Loading Purchase at yesterday\'s costs template', padx='20', pady='8', font='Helvetica 15', command=self.load_buy_yesterday_template)
        load_buy_yesterday_template_btn.pack()
        load_buy_yesterday_template_btn.place(width=490, height=50, relx=.5, rely=.6, anchor='c', bordermode=tkinter.OUTSIDE)

        main_menu_btn = tkinter.Button(self, text='Go to Loading Data Menu', padx='20', pady='8', font='Helvetica 15', command=self.open_load_data_menu_gui)
        main_menu_btn.pack()
        main_menu_btn.place(width=490, height=50, relx=.5, rely=.8, anchor='c', bordermode=tkinter.OUTSIDE)

        copyright_label = tkinter.Label(self, text='© Andrey Vladimirov, 2022', font='Helvetica')
        copyright_label.place(relx=.005, rely=.99, anchor='sw')

    def open_load_data_menu_gui(self):
        load_menu = load_menu_gui()
        self.destroy()
        load_menu.grab_set()

    def load_user_input_template(self):
        DATA_MANUFACTURE_PROCESS.add_config_data([0.0007, 0.000065, 5.5, 0.000026, 5, 7.25, 30, 6, 6, 2500, 0.165, 4.3, 0.7, 'U', 100])
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

        # load all data from "temp_data" into the model 
        # alternately using part names from "PARTS_DATA_NAME"
        for iter in range(0, len(temp_data)):
            DATA_MANUFACTURE_PROCESS.add_parts_data(PARTS_DATA_NAME[iter], temp_data[iter])

        tkinter.messagebox.showinfo('ADD DATA RESULT', 'Template data added to program!')
        
        main_menu = main_menu_gui()
        self.destroy()
        main_menu.grab_set()   
        
    def load_interval_template(self):
        # loading configuration data
        DATA_MANUFACTURE_PROCESS.add_config_data([0.0007, 0.000065, 5.5, 0.000026, 5, 7.25, 30, 6, 6, 2500, 0.165, 4.3, 0.7, 'I', 100, 15])
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

        for iter in range(0, len(temp_data)):
            replenishment_amount = int((DATA_MANUFACTURE_PROCESS.config_max_cars() * 0.25) * temp_data[iter][1])
            DATA_MANUFACTURE_PROCESS.add_parts_data(PARTS_DATA_NAME[iter], [temp_data[iter][0], int(DATA_MANUFACTURE_PROCESS.config_max_cars() * temp_data[iter][1] * 1.5), int(DATA_MANUFACTURE_PROCESS.config_max_cars() * temp_data[iter][1] * 0.5), *temp_data[iter][1:5], replenishment_amount])

        tkinter.messagebox.showinfo('ADD DATA RESULT', 'Template data added to program!')
        
        main_menu = main_menu_gui()
        self.destroy()
        main_menu.grab_set()   
    
    def load_buy_yesterday_template(self):
        # loading configuration data
        DATA_MANUFACTURE_PROCESS.add_config_data([0.0007, 0.000065, 5.5, 0.000026, 5, 7.25, 30, 6, 6, 2500, 0.165, 4.3, 0.7, 'B', 100])
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
        
        for iter in range(0, len(temp_data)):
            replenishment_amount = int(DATA_MANUFACTURE_PROCESS.config_max_cars() * temp_data[iter][1])
            DATA_MANUFACTURE_PROCESS.add_parts_data(PARTS_DATA_NAME[iter], [temp_data[iter][0], int(DATA_MANUFACTURE_PROCESS.config_max_cars() * temp_data[iter][1] * 1.5), int(DATA_MANUFACTURE_PROCESS.config_max_cars() * temp_data[iter][1] * 0.5), *temp_data[iter][1:5], replenishment_amount])

        tkinter.messagebox.showinfo('ADD DATA RESULT', 'Template data added to program!')
        
        main_menu = main_menu_gui()
        self.destroy()
        main_menu.grab_set()   
                    
def start_gui_app():
    app =  main_menu_gui()
    app.mainloop()