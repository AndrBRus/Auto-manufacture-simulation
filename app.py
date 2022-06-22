from command_line_app import start_command_line_app
from gui_app import start_gui_app
import argparse

if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Parsing command line arguments for start command line mode or gui mode')
    parser.add_argument('--cmd', action='store_true', default=False, help='Start app at command line mode')
    parser.add_argument('--gui', action='store_true', default=False, help='start app at gui mode')
    args = parser.parse_args()

    if args.cmd == True and args.gui == False:
        start_command_line_app()
    elif (args.gui == True and args.cmd == False) or (args.cmd == False and args.gui == False): 
        start_gui_app()
    else:
        print('Too many command line arguments!\nEnter one argument')