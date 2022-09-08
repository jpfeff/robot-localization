# Written by Joshua Pfefferkorn
# Dartmouth CS76, Fall 2021
# November 16, 2021

import numpy as np
from Maze import Maze
import random
import time

class HiddenMarkovModel:
    def __init__(self, maze, start_loc, num_moves):
        self.maze = maze
        # updated in `self.generate_maze_colors()` to hold the number of floor spaces in the maze
        self.num_floors = None
        # number of moves
        self.num_moves = num_moves
        # holds move possibilities
        self.moves = ['up','down','left', 'right']
        # sequence of moves
        self.path = self.generate_random_path(self.num_moves)
        # holds the color possibilities
        self.colors = ['r','g','b','y']
        # assigns random colors to the maze
        self.maze_colors = self.generate_maze_colors()
        # generates an initial probability distribution
        self.start_state = self.get_start_state()
        # the robot's starting coordinates
        self.start_loc = start_loc
        # sequence of robot locations
        self.locations = []
        # sequence of actual colors
        self.actual_colors = []
        # sequence of sensed colors
        self.sensed_colors = []
        # holds the number of each color in the maze
        self.num_each_color = self.generate_num_colors()
        # get the sensor model for each color
        self.r_model = self.generate_sensor_model('r')
        self.g_model = self.generate_sensor_model('g')
        self.b_model = self.generate_sensor_model('b')
        self.y_model = self.generate_sensor_model('y')
        # transition model
        self.transition_model = self.generate_transition_model()


    # generates a probability distrubution (assigns a uniform probability to each floor space on the maze)
    def get_start_state(self):
        # creates a matrix of zeros
        start_state = np.zeros((self.maze.width, self.maze.height))
        # loop over maze
        for x in range(self.maze.width):
            for y in range(self.maze.height):
                # if the space is a floor
                if self.maze.is_floor(x,y):
                    # assigns a uniform probability to each floor space
                    start_state[x,y] = 1/self.num_floors
        return start_state

    # assigns a random color to each floor space in the maze
    def generate_maze_colors(self):
        maze_colors = {}
        # loop over maze
        for x in range(self.maze.width):
            for y in range(self.maze.height):
                # if the space is a floor
                if self.maze.is_floor(x,y):
                    # assign a random color to the space
                    color = self.colors[random.randint(0,3)]
                    maze_colors[(x,y)] = color
        # store the number of floor spaces for use in `get_start_state()`
        self.num_floors = len(maze_colors)
        return maze_colors
    
    # generates a sensor model for the given color
    def generate_sensor_model(self, color):
        # initialize matrix of 0s the same dimensions as the maze
        sensor_model = np.zeros((self.maze.width, self.maze.height))
        # loop over maze
        for x in range(self.maze.width):
            for y in range(self.maze.height):
                # if the space is a floor
                if self.maze.is_floor(x,y):
                    # compute the probability that we are on the space when our sensor reading is correct
                    if self.maze_colors[(x,y)] == color:
                        prob = 0.88/self.num_each_color[color]
                        sensor_model[x,y] = prob
                    # compute the probability that we are on the space when our sensor reading is incorrect
                    else:
                        new_color = self.maze_colors[(x,y)]
                        prob = 0.04/self.num_each_color[new_color]
                        sensor_model[x,y] = prob
        return sensor_model

    # generates a matrix in which index i,j represents the probability of moving from state i to state j
    def generate_transition_model(self):
        transition_model = np.zeros((self.maze.width**2, self.maze.height**2))
        # loop over maze
        for x in range(self.maze.width):
            for y in range(self.maze.height):
                # get the one dimensional index of the position (i.e., the position in the array if the maze was flattened)
                index1 = self.get_one_d_index(x,y)

                # if the space is a floor
                if self.maze.is_floor(x,y):
                    valid_moves, num_moves = self.valid_moves(x,y)
                    # if there is a wall in one of the spaces around the robot
                    if not num_moves == 4:
                        # include its current location in the list of valid moves (if the robot hits the wall it stays in place)
                        valid_moves.append((x,y))
                        num_moves += 1
                    # for each move
                    for move in valid_moves:
                        # get the 1-D index of the new position
                        index2 = self.get_one_d_index(move[0],move[1])
                        # insert the probability of the move into [old position, new position]
                        transition_model[index1, index2] += 1/num_moves

        # transpose the model for later multiplication
        return transition_model.T

    # gets the index of the position in the maze as a number 0 through [maze width * maze height - 1]
    def get_one_d_index(self,x,y):
        return self.maze.width*x + y

    # finds floor spaces around the robot
    def valid_moves(self, x, y):
        # empty list of legal moves
        valid_moves = []
        # all possible moves (up, down, right, and left)
        neighbors = [(x+1,y),(x-1,y),(x,y+1),(x,y-1)]
        # loops over neighbors, appends to legal moves if it is a floor space
        for neighbor in neighbors:
            if self.maze.is_floor(neighbor[0], neighbor[1]):
                valid_moves.append(neighbor)
        return valid_moves, len(valid_moves)

    # iterates over the robots path, creating a list of locations, actual colors, sensed colors
    def get_colors_and_locations(self):
        current_location = self.start_loc
        
        # add the initial location to the list of locations
        self.locations.append(current_location)

        # store the actual color of the initial space as well as the imperfect sensed color
        self.actual_colors.append(self.maze_colors[current_location])
        self.sensed_colors.append(self.get_sensor_color(current_location))

        # iterate over path
        for move in self.path:
            # create x and y according to the direction of the move
            if move == 'up':
                x = current_location[0]
                y = current_location[1]+1
            elif move == 'down':
                x = current_location[0]
                y = current_location[1]-1
            elif move == 'right':
                x = current_location[0]+1
                y = current_location[1]
            elif move == 'left':
                x = current_location[0]-1
                y = current_location[1]

            # if the new space is a floor
            if self.maze.is_floor(x,y):
                # update the current location and the robot's location in the maze
                current_location = (x,y)

                self.locations.append(current_location)
                # store the actual color of the space as well as the imperfect sensed color
                self.actual_colors.append(self.maze_colors[current_location])
                self.sensed_colors.append(self.get_sensor_color(current_location))
            # if the space is not a floor and the robot did not move, add the color of the previous location
            else:
                self.locations.append(current_location)
                self.actual_colors.append(self.maze_colors[current_location])
                self.sensed_colors.append(self.get_sensor_color(current_location))

    # gets the imperfect sensor color of a space on the maze
    def get_sensor_color(self,location):
        # get the actual color
        actual_color = self.maze_colors[location]

        # generate a random number between 0 and 1
        rand = random.uniform(0, 1)

        # if the number is within the 0.12 chance of the sensor getting an incorrect reading
        if rand >= 0.88:
            # copy the list of colors and remove the actual one
            other_colors = self.colors.copy()
            other_colors.remove(actual_color)
            # randomly choose one of the other colors
            return other_colors[random.randint(0,2)]
        
        # otherwize return the true color
        return actual_color
    
    # greates a dictionary of counters for each color used for generating sensor models
    def generate_num_colors(self):
        # initialize dictionary to hold 0 for each color
        colors = {'r':0,'g':0,'b':0,'y':0}
        # loop over the maze colors, incrementing the value of a color when found
        for color in self.maze_colors.values():
            colors[color] += 1
        
        return colors
    
    # returns a sequence of probability distributions using the transition and sensor models with the state
    def get_probability_sequence(self):
        probability_sequence = []
        state = self.start_state

        # iterate over the sequence of colors picked up by the robot's sensor
        for color in self.sensed_colors:
            # reshape the state to a 1x[maze width * maze height] for multiplication with the transition model
            state = np.reshape(state,(1,self.maze.width * self.maze.height))
            # multiply by transposed transition model
            state = np.matmul(state, self.transition_model)
            # reshape the state back to the maze dimensions
            state = np.reshape(state,(self.maze.width,self.maze.height))


            # incorporate sensor model data from the correct color
            if color == 'r':
                # not typical matrix multiplication, simply multiplies each value with its corresponding value in the second matrix
                state = np.multiply(state, self.r_model)
            elif color == 'g':
                state = np.multiply(state, self.g_model)
            elif color == 'b':
                state = np.multiply(state, self.b_model)
            elif color == 'y':
                state = np.multiply(state, self.y_model)
            
            # normalize the probability distribution to avoid very small probabilities
            state = self.normalize(state)
            # rotate the state so that the printed matrix is the same orientation as the maze
            probability_sequence.append(np.rot90(state))
        return probability_sequence

    # normalizes a matrix
    def normalize(self, matrix):
        sum = 0
        # sums all values in the matrix
        for x in range(matrix.shape[0]):
            for y in range(matrix.shape[1]):
                sum += matrix[x,y]
        # replaces each value with itself/sum
        for x in range(matrix.shape[0]):
            for y in range(matrix.shape[1]):
                matrix[x,y] /= sum
        return matrix
    
    # generates a random sequence of moves
    def generate_random_path(self,num_moves):
        path = []
        # for the given length
        for x in range(num_moves):
            # choose a random direction
            rand = random.randint(0,3)
            path.append(self.moves[rand])
        return path

    # calls necessary algorithm functions and sequentially prints results
    def driver(self):
        # gets lists of locations, actual colors, and sensed colors
        self.get_colors_and_locations()
        # creates probability distribution for each time step
        probability_sequence = self.get_probability_sequence()

        # iterate over time steps, printing relevant data
        for time_step in range(len(probability_sequence)):
            print("Move:", time_step, "/", len(probability_sequence)-1, "\n")

            print("Probability Distribution:\n")
            print(probability_sequence[time_step],"\n")

            print("Actual Maze:\n")
            self.maze.robotloc = [self.locations[time_step][0], self.locations[time_step][1]]
            print(self.maze)

            print("Sensor Color:", self.sensed_colors[time_step])
            print("Actual Color:", self.actual_colors[time_step], "\n")

            print("----------------------------------------------------\n")
            
            # slight delay for visual purposes
            time.sleep(1)

# some testing code (can change starting location, path length, seed, etc.)
if __name__ == "__main__":
    random.seed(0)
    test_maze = Maze("maze1.maz")
    hmm = HiddenMarkovModel(test_maze,(0,0),7)
    hmm.driver()