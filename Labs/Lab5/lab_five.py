"""
__filename__ = "lab_five.py"
__coursename__ = "SDEV 300 6380 - Building Secure Web Applications (2198)"
__author__ = "Eric Thomas"
__copyright__ = "None"
__credits__ = ["Eric Thomas"]
__license__ = "GPL"
__version__ = "1.0.0"
__maintainer__ = "Eric Thomas"
__email__ = "ethomas48@student.umgc.edu"
__status__ = "Test"

Discussion: This exercise (80 points) allows a user to load one of two CSV
files and then perform histogram analysis and plots for select variables on the
datasets. The first dataset represents the population change for specific dates
for U.S. regions. The second dataset represents Housing data over an extended
period of time describing home age, number of bedrooms and other variables. The
first row provides a column name for each dataset. The following columns should
be used to perform analysis.
"""

import sys
import os
import traceback
import logging
from logging.config import fileConfig
import pandas as pd
import matplotlib.pyplot as plt
import ui_common as uicom

LOG_CONFIG = "{}/log_config.ini".format(os.getcwd())
print(LOG_CONFIG)
fileConfig(LOG_CONFIG)


def main():
    """
    main method
    :return: Main returns 0 upon no issue and -1 upon issue
    """

    # Create a menu-driven command-line app
    # vars to hold text for display at top of GUI
    banner = "*" * 60
    heading = "Welcome to the Python Data Analysis App"

    # Filenames
    pop_f_name = "PopChange.csv"  # Population Data
    housing_f_name = "Housing.csv"  # Housing Data

    ret_code = 0

    while True:
        uicom.clear_screen()
        print(banner)
        print(heading)

        print("Select the file you want to analyze: ")
        print("\t1. Population Data")
        print("\t2. Housing Data")
        print("\t3. Exit the program")

        user_input = input("Enter a selection: ").strip()

        # USER INPUT OPTIONS
        if user_input == '1':  # Population Data
            print("You have selected Population Data")
            try:
                pop_file = open(pop_f_name, 'r')
                population_data_frame = pd.read_csv(pop_file)
                analyze_population_data(population_data_frame)
            except (FileNotFoundError, Exception):
                print("AN ERROR OCCURRED...")
                logging.error(traceback.format_exc())
                input("Hit <ENTER> to continue...")
            finally:
                pop_file.close()

        elif user_input == '2':  # Housing Data
            print("You have selected Housing Data")
            try:
                housing_file = open(housing_f_name, 'r')
                housing_data_frame = pd.read_csv(housing_file)
                analyze_housing_data(housing_data_frame)
            except (FileNotFoundError, Exception):
                print("AN ERROR OCCURRED...")
                logging.error(traceback.format_exc())
                input("Hit <ENTER> to continue...")
            finally:
                housing_file.close()

        elif user_input == '3':  # Exit upon user request
            break
        else:
            print("Make a selection of 1 - 3...")
            input("Hit <ENTER> to continue...")

    sys.exit(0)


def analyze_population_data(population_data_frame):
    """
    Takes a panda dataframe and display data as dictated by the user. It can
    display a histogram and "describe()" data for each of column specified.
    :param population_data_frame:
    :return:
    """

    pop_df = population_data_frame

    valid_operation_selected = False

    col = -1

    while not valid_operation_selected:
        print("Select the Column you want to analyze: ")
        print("a.", pop_df.columns[4])
        print("b.", pop_df.columns[5])
        print("c.", pop_df.columns[6])
        print("d. Go Back")
        user_input = input().strip().lower()

        if user_input.lower() == 'a':
            valid_operation_selected = True
            col = 4
        elif user_input.lower() == 'b':
            valid_operation_selected = True
            col = 5
        elif user_input.lower() == 'c':
            valid_operation_selected = True
            col = 6
        elif user_input.lower() == 'd':
            valid_operation_selected = True
        else:
            print("[ERROR] Invalid selection...")

    if col != -1:
        print("You selected {}".format(pop_df.columns[col].title()))
        print("The statistics for this column are: ")
        print(pop_df.describe()[pop_df.columns[col]].apply(lambda val:
                                                           format(val, '.3f')))
        print("The histogram for this column is now displayed...")
        pop_df.hist(column=pop_df.columns[col])
        plt.show()
        input("Hit <ENTER> to continue...")


def analyze_housing_data(housing_data_frame):
    """
    Takes a panda dataframe and display data as dictated by the user. It can
    display a histogram and "describe()" data for each of column specified.
    :param population_data_frame:
    :return:
    """

    housing_df = housing_data_frame

    valid_operation_selected = False

    col = -1  # Init for control below

    while not valid_operation_selected:
        print("Select the Column you want to analyze: ")
        print("a.", housing_df.columns[0].title())
        print("b.", housing_df.columns[1].title())
        print("c.", housing_df.columns[2].title())
        print("d.", housing_df.columns[4].title())
        print("e.", housing_df.columns[6].title())
        print("f. Go Back")
        user_input = input().strip().lower()

        if user_input.lower() == 'a':
            valid_operation_selected = True
            col = 0
        elif user_input.lower() == 'b':
            valid_operation_selected = True
            col = 1
        elif user_input.lower() == 'c':
            valid_operation_selected = True
            col = 2
        elif user_input.lower() == 'd':
            valid_operation_selected = True
            col = 4
        elif user_input.lower() == 'e':
            valid_operation_selected = True
            col = 6
        elif user_input.lower() == 'f':
            valid_operation_selected = True
        else:
            print("[ERROR] Invalid selection...")

    if col != -1:
        print("You selected {}".format(housing_df.columns[col].title()))
        print("The statistics for this column are: ")
        print(housing_df.describe()[housing_df.columns[col]])
        print("The histogram for this column is now displayed...")
        housing_df.hist(column=housing_df.columns[col])
        plt.show()
        input("Hit <ENTER> to continue...")


if __name__ == ("__main__"):
    main()
