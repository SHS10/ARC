#!/usr/bin/python

import os, sys
import json
import numpy as np
import re

### YOUR CODE HERE: write at least three functions which solve
### specific tasks by transforming the input x and returning the
### result. Name them according to the task ID as in the three
### examples below. Delete the three examples. The tasks you choose
### must be in the data/training directory, not data/evaluation.

### ID:14511263 
### Name: Hasan Syed
### URL: https://github.com/SHS10/ARC 

def solve_5bd6f4ac(x):
    # get shape data in different categories
    num_rows = x.shape[0]
    num_cols = x.shape[1]
    # perform integer division to get the right quarter of the array 
    # regardless of dimensions for extensibility to different dimensions.
    x = x[0:num_rows//3, 2*(num_cols//3):num_cols]
    return x

def solve_1a07d186(x):
#   step 1: find horizontal or verticle lines that contain none black continous lines.
    # If the lines are horizontal, the followuing will return index of rows in x 
    num_rows = x.shape[0]
    num_cols = x.shape[1]

    def solver(x):
        # get the coords for all non-zero entries
        non_z = np.where(x != 0)
        row = non_z[0]
        col = non_z[1]
        nz_cords = np.dstack((row,col))
        
        line_ind = list()
        line_vals = list()
        # get the index and val arrays for where the lines are
        # index here contains the row co-ord for the grid
        for index, vals in enumerate(x):
            if np.all(vals != 0):
                line_vals.append(vals)
                line_ind.append(index)
        
        # get one of the values from each of the lines for comparison
        one_val_grid = [elems[0] for elems in line_vals]


        points = list()
        points_idx = list()
        # where the individual occurences of the random points are
        for idx, vals in enumerate(x):
            if idx not in grid_ind:
                if np.all(vals == 0): pass
                else:
                    points_idx.append(idx)
                    points.append(vals)
        
        return x
    # find if there are values occurring repeatedly in the vertical
    col_vac_x = np.where(np.bitwise_or.reduce(x) != 0)

    # if the returned values is the same length as the number of columns than the grids are 
    # horizontal
    if len(col_val_x[0]) == num_rows:
        #  call internal solver func to perform rest of the necessary alg steps
        solver(x)
    else:
        x = x.transpose()
         #  call internal solver func to perform rest of the necessary alg steps
         solver(x)
         x = x.transpose()
         return x
    return x

def main():
    # Find all the functions defined in this file whose names are
    # like solve_abcd1234(), and run them.

    # regex to match solve_* functions and extract task IDs
    p = r"solve_([a-f0-9]{8})" 
    tasks_solvers = []
    # globals() gives a dict containing all global names (variables
    # and functions), as name: value pairs.
    for name in globals(): 
        m = re.match(p, name)
        if m:
            # if the name fits the pattern eg solve_abcd1234
            ID = m.group(1) # just the task ID
            solve_fn = globals()[name] # the fn itself
            tasks_solvers.append((ID, solve_fn))

    for ID, solve_fn in tasks_solvers:
        # for each task, read the data and call test()
        directory = os.path.join("..", "data", "training")
        json_filename = os.path.join(directory, ID + ".json")
        data = read_ARC_JSON(json_filename)
        test(ID, solve_fn, data)
    
def read_ARC_JSON(filepath):
    """Given a filepath, read in the ARC task data which is in JSON
    format. Extract the train/test input/output pairs of
    grids. Convert each grid to np.array and return train_input,
    train_output, test_input, test_output."""
    
    # Open the JSON file and load it 
    data = json.load(open(filepath))

    # Extract the train/test input/output grids. Each grid will be a
    # list of lists of ints. We convert to Numpy.
    train_input = [np.array(data['train'][i]['input']) for i in range(len(data['train']))]
    train_output = [np.array(data['train'][i]['output']) for i in range(len(data['train']))]
    test_input = [np.array(data['test'][i]['input']) for i in range(len(data['test']))]
    test_output = [np.array(data['test'][i]['output']) for i in range(len(data['test']))]

    return (train_input, train_output, test_input, test_output)


def test(taskID, solve, data):
    """Given a task ID, call the given solve() function on every
    example in the task data."""
    print(taskID)
    train_input, train_output, test_input, test_output = data
    print("Training grids")
    for x, y in zip(train_input, train_output):
        yhat = solve(x)
        show_result(x, y, yhat)
    print("Test grids")
    for x, y in zip(test_input, test_output):
        yhat = solve(x)
        show_result(x, y, yhat)

        
def show_result(x, y, yhat):
    print("Input")
    print(x)
    print("Correct output")
    print(y)
    print("Our output")
    print(yhat)
    print("Correct?")
    # if yhat has the right shape, then (y == yhat) is a bool array
    # and we test whether it is True everywhere. if yhat has the wrong
    # shape, then y == yhat is just a single bool.
    print(np.all(y == yhat))

if __name__ == "__main__": main()

