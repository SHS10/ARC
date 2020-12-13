## Purpose of this repo:
Manually (using heuristics) solving some of the problems in Chollet's ARC - through matrix/vector based translations and transposes as part of a college assignment.
# Report: 
## Problems: 
 - Problem : **5bd6f4ac**
    #### General Description (Problem and solving it visually - intuition):
    We get the zoomed in grid, only containing the top right third of the original input grid. 
    ##### Algorithm (to  guide understandiing of the code)
    - First we get the dimensions of the input in width and height
    - Then we get the top 1/3 of rows from the input and the the last 2/3 of the columns
    - Reassign to x and return

    **status**: *fully solved* - all training examples and test case.


 - Problem : **1a07d186**
    #### General Description (Problem and solving it visually - intuition):
    We want detect the individual grids to either side of the matching colored vertical or horizontal lines whichever is nearest. Otherwise we can delete them. We then translate individual colors to the the nerarest side of the appropriate color matching line. 
    ##### Algorithm (to guide understanding of the code)
     - Find where the there are non-empty grids.
     - Convert to transpose (for ease of programming), only if the lines vertical - this helps simplify the below computation. 
     - Find the coordinates of the lines.
     - From the non-empty grids that are not on the rows check if any of them match the colors of the lines. Note positions.
     - Check which row the individual matching color occurs. 
     - If the line are rows infront of the matching invididual, translate the row value to the line-row-index-1, attach above/beside the line. The column does not need to changed as we only handle all cases as vertical. If the matching line is rows behind the original value translate the row index of the individual point to the lines row index - 1. And keep the column index the same.
     - Convert back the transpose back to the original shape and return as x.

    **status**: *fully solved* - all training examples and the test case. 


 - Problem : **6b9890af**
   #### General Description:
   We want to place the anomaly into the red box, and scale the anomaly relative to the red box and return this.
   ##### Algorithm (to guide understanding of the code)
      - Find the box from the space - we assume that it is always square and is always red (2): so getting the first row is enough.
      - Create the red square
      - Get the coordinates of the anomaly in the original product. Note the coordinates. 
      - Find the minimum value that occurs in the rows and cols respectively from the anomaly coordinates. 
      - Convert them to a range between 0-3 by getting the modulus of the indexes with minimum index value. (assumption here is that we will always be working with anomalies of dimension 3x3).
      - The scaling is calculated for the box by dividing the internal dimension of the box by 3. And the returning value is a added when specifying where to end a row and column. If division returns 1 i.e. the theres no upscaling. We set scaling to be 0. 
      - Split the internal area of the red block into thirds. 
      - For the row coordinates of the 0-3 encoded anamoly array we find the matching third of the split box. 
      - These are starting coordinates (apart from the starting point for rows which can be gotten from the intersection of the internal area). 
      - Fill the internal area of the box with the value of the anomaly.  

   **status**: *partially solved. Test case and training example 3 fully passing. Unknown error for the example 2. And unusual behavior for example 1. As a similar example has been tested and showed to work in the notebook. Please check github for link to the github where the notebook NB_6b9890af.ipynb can be found in src to illustrate an example similar to example 1*

## Reflections: 
  For all the problems that I have solved and attempted to solve. The commonality that I have found between all of the problems is that there is need to find some 
  kind of outlier or anomaly within the grid space. 
  For all the implementations aside from the non trivial ones, there is a need to keep track of all of these anomalies and perform complex and often confusing index based 
  manipulations. 
  In terms of the work done by Chollet, both tasks 1a07d186 and 6b9890af share the charateristic of Object cohesion, where we have to consider non-zero entries as objects 
  in the space. The lines in 1a07d186 and both the box and the anomaly and the scaling factor in 6b9890af. 
  Other than that the problems are largely unique. Since what are are trying to achieve in each of these very different.

   **Libraries Used and Tooling**: In terms of the library and tooling and features of the Python language used, I have written all of this code using the numpy and python.
   For finding the coordinates of anomlies the np.where and np.all and the np.any functions were sometimes useful. While Sometimes I have eshewed the use of numpy vectorization for the native python lists since it allowed me to follow the code flow more easily as it is often hard to visualise and understand what is happening in within loops. I have also used different numpy functions such as transpose and array_split where it was useful to do so.

<!-- Ownership watermark -->
<!-- Code and report by Name:Hasan Syed, Student ID: 14511263 -->

# The Abstraction and Reasoning Corpus (ARC)

This repository contains the ARC task data, as well as a browser-based interface for humans to try their hand at solving the tasks manually.

*"ARC can be seen as a general artificial intelligence benchmark, as a program synthesis benchmark, or as a psychometric intelligence test. It is targeted at both humans and artificially intelligent systems that aim at emulating a human-like form of general fluid intelligence."*

A complete description of the dataset, its goals, and its underlying logic, can be found in: [The Measure of Intelligence](https://arxiv.org/abs/1911.01547).

As a reminder, a test-taker is said to solve a task when, upon seeing the task for the first time, they are able to produce the correct output grid for *all* test inputs in the task (this includes picking the dimensions of the output grid). For each test input, the test-taker is allowed 3 trials (this holds for all test-takers, either humans or AI).


## Task file format

The `data` directory contains two subdirectories:

- `data/training`: contains the task files for training (400 tasks). Use these to prototype your algorithm or to train your algorithm to acquire ARC-relevant cognitive priors.
- `data/evaluation`: contains the task files for evaluation (400 tasks). Use these to evaluate your final algorithm. To ensure fair evaluation results, do not leak information from the evaluation set into your algorithm (e.g. by looking at the evaluation tasks yourself during development, or by repeatedly modifying an algorithm while using its evaluation score as feedback).

The tasks are stored in JSON format. Each task JSON file contains a dictionary with two fields:

- `"train"`: demonstration input/output pairs. It is a list of "pairs" (typically 3 pairs).
- `"test"`: test input/output pairs. It is a list of "pairs" (typically 1 pair).

A "pair" is a dictionary with two fields:

- `"input"`: the input "grid" for the pair.
- `"output"`: the output "grid" for the pair.

A "grid" is a rectangular matrix (list of lists) of integers between 0 and 9 (inclusive). The smallest possible grid size is 1x1 and the largest is 30x30.

When looking at a task, a test-taker has access to inputs & outputs of the demonstration pairs, plus the input(s) of the test pair(s). The goal is to construct the output grid(s) corresponding to the test input grid(s), using 3 trials for each test input. "Constructing the output grid" involves picking the height and width of the output grid, then filling each cell in the grid with a symbol (integer between 0 and 9, which are visualized as colors). Only *exact* solutions (all cells match the expected answer) can be said to be correct.


## Usage of the testing interface

The testing interface is located at `apps/testing_interface.html`. Open it in a web browser (Chrome recommended). It will prompt you to select a task JSON file.

After loading a task, you will enter the test space, which looks like this:

![test space](https://arc-benchmark.s3.amazonaws.com/figs/arc_test_space.png)

On the left, you will see the input/output pairs demonstrating the nature of the task. In the middle, you will see the current test input grid. On the right, you will see the controls you can use to construct the corresponding output grid.

You have access to the following tools:

### Grid controls

- Resize: input a grid size (e.g. "10x20" or "4x4") and click "Resize". This preserves existing grid content (in the top left corner).
- Copy from input: copy the input grid to the output grid. This is useful for tasks where the output consists of some modification of the input.
- Reset grid: fill the grid with 0s.

### Symbol controls

- Edit: select a color (symbol) from the color picking bar, then click on a cell to set its color.
- Select: click and drag on either the output grid or the input grid to select cells.
    - After selecting cells on the output grid, you can select a color from the color picking to set the color of the selected cells. This is useful to draw solid rectangles or lines.
    - After selecting cells on either the input grid or the output grid, you can press C to copy their content. After copying, you can select a cell on the output grid and press "V" to paste the copied content. You should select the cell in the top left corner of the zone you want to paste into.
- Floodfill: click on a cell from the output grid to color all connected cells to the selected color. "Connected cells" are contiguous cells with the same color.

### Answer validation

When your output grid is ready, click the green "Submit!" button to check your answer. We do not enforce the 3-trials rule.

After you've obtained the correct answer for the current test input grid, you can switch to the next test input grid for the task using the "Next test input" button (if there is any available; most tasks only have one test input).

When you're done with a task, use the "load task" button to open a new task.
