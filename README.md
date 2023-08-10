# Exercise 3 - Racetrack

Learn how to drive on a simple racetrack by using reinforcement learning with monte carlo.

## Features

The main program [main.py](main.py) has the following features:

1) AI Static: Train a model on one racetrack, and display 3 test runs as static images.
2) AI Interactive: Train a model on one racetrack, and watch live as the trained model plays a game.
3) User: Let the user play on one racetrack by applying inputs via the command line.

Additionally, there is the jupyter notebook [model_analysis.ipynb](model_analysis.ipynb) to create exploratory statistics and plots.

## Usage

We used python 3.10 when developing this project.

First install the python dependencies with:

```console
pip install -r requirements.txt
```

Now simply run `main.py` or `model_analysis.ipynb`.

When running the main program certain aspects can be selected by setting the mode flag:

```console
python main.py -m ai_interactive
```

## Further Information

The racetrack is internally represented by a 2 dimensional numpy array. 
The elements of this array are integers, and specify the type of the cell:
- 0 = OFF_TRACK
- 1 = ON_TRACK
- 2 = START
- 3 = END/FINISH
