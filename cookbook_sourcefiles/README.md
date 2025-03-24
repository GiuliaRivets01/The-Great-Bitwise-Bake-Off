# Recipe Generator System

The Recipe Generator System is a Python-based application that uses a Genetic Algorithm 
to generate new recipes based on a provided dataset of existing recipes.

## System Requirements

Before compiling and running this program, ensure that you have the following requirements:

- **Python**: This program requires Python 3.6 +.\
You can download and install Python from [python.org](https://www.python.org/downloads/).

- **Dataset**: The system relies on a dataset of recipes in JSON format.\
Ensure that you have a valid dataset at the specified path (e.g., 'inspiration/Dessert_recipes.json').

## Installation

To generate your own cookbook, follow these steps:

1. Open your terminal or command prompt and navigate to the directory where the code is located.

2. Run the Python script:

    ```
    $ python main.py
    ```
   
3. The program will generate a collection of recipes and store them in a directory named "cookbook"


## Customization

- **Population Size**: You can customize the population size by modifying the population_size 
variable in the create_recipe function in main.py.

- **Number of Recipes**: Adjust the num_recipes variable in main.py to control the number 
of recipes generated and saved in the cookbook.