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







Write-up that I submitted with the project-

Properties: 
•	Fully observable: The environment is fully observable because we know how the intersection is, and it doesn’t change, and we also know exactly when a car arrives, where it arrives and where it wants to go.
•	Single agent: There’s multiple cars performing actions, but all these actions are only controlled by one signaling agent (traffic lights). 
•	Deterministic: Here, the what a car does is completely determined by the current state and what a car did in the current state. Hence, it’s a fully certain, fully observable, deterministic environment. 
•	Episodic: This task is episodic because a car receives a task and performs it, and then the next car does it one by one.
•	Static: The environment remains the same regardless of what any car does (assuming there’s no accidents)
•	Discrete: There is a discrete set of possible actions and percepts for a certain set of cars at an intersection. 
•	Known: There is no unknown factor, i.e. all outcomes are known for all actions.

Problem Formulation:
•	States: Each state has a list of cars in each lane, the traffic signal on each light, and the current time step.
•	Initial State: Specified by the file
•	Actions: Turn traffic light and left turn arrow Red, Green, Yellow at different point in times, leaving enough times for cars to smoothly go through the intersection without colliding.
•	Transition Model: The state resulting from changing a light will have a certain number of queued cars removed as they would have left the intersection.
•	Goal Test: Is there’s no cars left at the intersection
•	Path Cost: Amount of time each car waits.

•	What search strategy did you choose?
Modified Greedy Best First Search with a value pointing the algorithms towards the maximum change in state without changing the light (it’s better to have more cars leave the intersection every ‘step’). We will also use a Heuristic that’ll take into consideration the time a car has been waiting and the number of cars in each of the lanes, to change the lights in certain situations discussed below.

•	Why did you choose that particular search strategy? 
I chose this strategy because it uses a Heuristic and isn’t just a randomized strategy that will lead to the desirable result but by constantly changing the traffic lights or keeping cars waiting forever.

•	What other design decisions did you make?
This does however cause a problem of a small number of cars possibly infinitely waiting on one side of the intersection, and we will solve that by setting a time restriction. Hence, the best first search will use the heuristic specified above so see if a car has been waiting at the intersection for more than *global variable*maximumWaitingTime steps, in which case we’ll take the path in the state space that lets those cars cross the intersection first.
This global variable of maximum waiting time ‘SHOULD’ ideally change when it’s rushhour/uniform/burst.
There is also a situation where the light constantly changes for optimization, for which I have added another *global variable* minimumLightTime steps, so that the light won’t change for that many steps.

•	Why did you make the choices that you did? 
I made these decisions for making the crossing smooth and close to how it’d be desirable in a real-life situation. People don’t like to wait at intersections, so its important to optimize the movements but its also important to make sure that a small number of cars aren’t stuck for too long. 

•	Is your agent complete? Is it optimal? Why? 
This agent should handle the task well and optimally for the reasons mentioned above. i.e. because we’re using a heuristic to take a path to move cars quickly, but also taking care of cars that could disadvantage from the heuristic.

•	If you could change one thing about your design, what would it be?
Improve the heuristic from learning from data.
