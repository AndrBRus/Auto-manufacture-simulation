# Simulation of the production process of a car factory 
**Auto-manufacture-simulation** repository describes a program that simulates the production cycle of an assembly line in an automobile factory.

At the moment, the program can simulate as a single process (performing one test) or simulation a certain number of times (specified by the user), including finding the average value for produced cars, the coefficient of performance.

Each program module describes a specific element of the program. At the moment, the following elements are included in separate modules:
* The main part of the program (program menu from where functions are called)
* Configuration data
* Description of the conveyor
* Description of the production process
* Description of parts required for production
* Function for deleting logs (in the future, logging will be separated into a separate module)
* Description of the car on the assembly line
* Functions for loading data from the console

To simplify the simulation, only a few types of parts were selected for a while:
* Welding raw materials
* Welding consumables
* Coloring raw materials
* Coloring consumables
* Assembly raw materials
* Assembly consumables

The main principle of the program is to simulate a conveyor based on configuration data, including the number of cars on the conveyor, and update data on all cars every time a new car enters the conveyor. Now the program checks the number of parts at each stage of production:
1. When entering a weld
2. When switching from welding to painting
3. When switching from painting to assembly

Also during these intervals, parts are checked for defects and the availability of spare parts in stock. If there are none, then a shortage of parts is simulated, and a new delivery is expected. After the car is ready, it rolls off the assembly line and is considered to be ready. Manufacturing defects are also taken into account. If it can be corrected, the car is removed from the conveyor and the defect is corrected, otherwise the body is recycled.

Please note that there is test data that is in the *"test_data.txt"* file. You can use in the first steps of learning this program for a better understanding of what is happening in it.

You can find the necessary libraries for the program to work in the *"requirements.txt"* file.

In the future, with the addition of new functions, this file will be supplemented.