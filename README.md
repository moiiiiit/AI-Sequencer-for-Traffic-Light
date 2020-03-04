# AI-Sequencer-for_Traffic-Lights

Imagine a single lane 4-way traffic intersection (N-S-E-W). There is a left turn lane and cars can go either straight or take a left. 
Time is discrete and in steps, each car takes exactly one step to cross the intersection.
The program takes in in an input file of the format "TIME ORIGIN DIRECTION"
The time parameter specifies the time step the car will arrive at the intersection. If there is already another car at the intersection, then this car will wait for the intersection. The origin parameter specifies which traffic light the car will watch (and there for which road and direction it comes to the intersection from). It will be a single letter either N,S,E, or W. The direction parameter specifies whether or not the car will turn left. The parameter will either be left or straight.
The program creates a sequence of traffic light configurations to let all the cars pass through and prints out either the state or significant time step changes.




HOW TO RUN:
In the code directory, run "python main.py *input_filename*"
ex: python main.py rushhour.txt
USES PYTHON V3.7




See problem details for the exact problem.

Please Suggest changes to the heuristic and methods to better handle the searching! I'm new to AI and will definitely learn from your input!
