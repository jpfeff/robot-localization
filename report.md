# Joshua Pfefferkorn
## Programming Assignment #6
## COSC 76, Fall 2021

## **Description**

**General Problem Modeling and Algorithms**

For this problem, the state was represented as a matrix of the same size as the maze, each position holding a normalized probability value that the robot was on that space. For each time step in the robot's path, the filtering algorithm, implemented with matrix multiplication using the `numpy` library, was used to incorporate data from the transition and sensor models, described below.

**Transition Model**

The transition model was implemented as a matrix of size (maze height)^2 x (maze width)^2. For the particular 4x4 test maze, the transition matrix was 16x16. Each index i,j in the transition model represented the probability that the robot moved from state i (a one-dimensional position in the state matrix) to another state j. To compute the next state using the transition model, the state matrix was reshaped to the proper multiplication dimensions (1x16 in my test case) and multiplied by the transpose of the transition model.

**Sensor Model**

The sensor models were implemented as matrices of size maze height x maze width, one model for each color. The sensor model's values represented the probability robot was on any given space given the sensor reading, accounting for imperfect sensing abilities. To incorporate this data into the probability distribution, the state matrix's values were multiplied by their corresponding value in the color's sensor model.

## Evaluation

My implemented algorithms worked as aniticipated. The program was able to compute a reasonable probability distrubution (verified visually) for each move, accounting well for incorrect sensor readings and bumps into walls. Spots containing barriers remained at 0.0 probability throughout computation. Below is a brief 7-move sequence in which the robot computes a 0.67 of being in the spot it is in, correcting for an early incorrect sensor reading.

```
Move: 0 / 7 

Probability Distribution:

[[0.         0.01       0.22       0.        ]
 [0.22       0.22       0.01       0.01333333]
 [0.         0.01       0.22       0.01333333]
 [0.04       0.01       0.01333333 0.        ]] 

Actual Maze:

#..#
....
#...
A..#

Sensor Color: b
Actual Color: y 

----------------------------------------------------

Move: 1 / 7 

Probability Distribution:

[[0.         0.31000739 0.00751533 0.        ]
 [0.02066716 0.00587135 0.34789719 0.0015309 ]
 [0.         0.23767234 0.00109599 0.01029879]
 [0.00939416 0.03788979 0.01015961 0.        ]] 

Actual Maze:

#..#
....
#...
.A.#

Sensor Color: g
Actual Color: g 

----------------------------------------------------

Move: 2 / 7 

Probability Distribution:

[[0.         0.0211756  0.0435712  0.        ]
 [0.00260658 0.04499623 0.00078642 0.6909363 ]
 [0.         0.01387486 0.02976169 0.02482666]
 [0.01857671 0.01449298 0.09439477 0.        ]] 

Actual Maze:

#..#
....
#...
..A#

Sensor Color: r
Actual Color: r 

----------------------------------------------------

Move: 3 / 7 

Probability Distribution:

[[0.         0.01207458 0.15862784 0.        ]
 [0.17283903 0.06979137 0.06678017 0.10511873]
 [0.         0.00850988 0.24305451 0.10936944]
 [0.02183115 0.01166325 0.02034005 0.        ]] 

Actual Maze:

#..#
....
#.A.
...#

Sensor Color: b
Actual Color: b 

----------------------------------------------------

Move: 4 / 7 

Probability Distribution:

[[0.         0.22201362 0.00996517 0.        ]
 [0.01527178 0.00818894 0.39921418 0.01573666]
 [0.         0.23057172 0.0064516  0.02559902]
 [0.00843289 0.04316522 0.01538919 0.        ]] 

Actual Maze:

#..#
....
#A..
...#

Sensor Color: g
Actual Color: g 

----------------------------------------------------

Move: 5 / 7 

Probability Distribution:

[[0.         0.00574672 0.33226919 0.        ]
 [0.0185251  0.34232923 0.00072398 0.01405527]
 [0.         0.00517521 0.26482896 0.0015246 ]
 [0.00740782 0.00533998 0.00207395 0.        ]] 

Actual Maze:

#..#
....
#.A.
...#

Sensor Color: b
Actual Color: b 

----------------------------------------------------

Move: 6 / 7 

Probability Distribution:

[[0.00000000e+00 3.48014510e-02 1.73274401e-02 0.00000000e+00]
 [2.76879781e-02 1.15749491e-03 3.65798668e-02 2.44635581e-02]
 [0.00000000e+00 2.36967186e-02 3.64375798e-04 4.20747126e-01]
 [3.91250120e-03 7.67172702e-04 4.08494316e-01 0.00000000e+00]] 

Actual Maze:

#..#
....
#..A
...#

Sensor Color: r
Actual Color: r 

----------------------------------------------------

Move: 7 / 7 

Probability Distribution:

[[0.         0.00243876 0.08931845 0.        ]
 [0.04356559 0.09270734 0.00148672 0.02940011]
 [0.         0.00089197 0.67172375 0.02719015]
 [0.00128505 0.01499568 0.02499644 0.        ]] 

Actual Maze:

#..#
....
#.A.
...#

Sensor Color: b
Actual Color: b 
```
