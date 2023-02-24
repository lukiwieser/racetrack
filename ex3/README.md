# Exercise 3 - Racetrack

Learn how to drive on a simple racetrack by using reinforcement learning with monte carlo.

## Features

The main program [main.py](main.py) has the following features:

1) AI Static: train a model on one racetrack, and display 3 test runs as static images.
2) AI Interactive: trans a model on one racetrack, and watch live as the trained model plays a game.
3) User: Let the user play on one racetrack by applying inputs via the comandline

Additionally, there is the jupyter notebook [analyze_model.ipynb](analyze_model.ipynb) to create exploratorive statistics and plots.

## Usage

We used python 3.10 when developing this project.

First install the python dependencies with:

```console
pip install -r requirements.txt
```

Now simply run `main.py` or `analyze_model.ipynb`.

When running the main program certain aspects can be selected by setting the mode flag:

```console
python main.py -m ai_interactive
```


