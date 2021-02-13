"""
__filename__ = "lab_three.py"
__coursename__ = "SDEV 300 6380 - Building Secure Web Applications (2198)"
__author__ = "Eric Thomas"
__copyright__ = "None"
__credits__ = ["Eric Thomas"]
__license__ = "GPL"
__version__ = "1.0.0"
__maintainer__ = "Eric Thomas"
__email__ = "ethomas48@student.umgc.edu"
__status__ = "Test"

Dependencies:
pip3 install Image -U
pip3 install requests -U
pip3 install matplotlib
sudo apt-get install imagemagick
"""

import sys
import requests
import matplotlib.pyplot as plt
from PIL import Image
import state_dict as states
import ui_common as uicom

#####################
# GLOBAL CONSTANT(S)
#####################
SENTINEL = "-1"


def main():
    """
    main method
    :return: Main returns 0 on exit
    """

    # Create a menu-driven command-line app
    # vars to hold text for display at top of GUI
    banner = "*" * 60
    heading = "Welcome to the Lab 3 User Application"

    while True:
        uicom.clear_screen()
        print(banner)
        print(heading)

        print("How can I help you? ")
        print("\t1. Display all U.S. states and information")
        print("\t2. Search for a specific state")
        print("\t3. Compare the top 5 most populated states")
        print("\t4. Update a states population")
        print("\t5. Exit")

        user_input = input("Enter a selection: ").strip()

        # USER INPUT OPTIONS
        if user_input == '1':  # Display all US states
            for state in states.states:
                display_state(state)
            input("Hit <ENTER> to continue...")
        elif user_input == '2':  # Display a user defined US state
            valid_us_state = get_us_state_input()
            if valid_us_state:
                display_state(valid_us_state)
            input("Hit <ENTER> to continue...")
        elif user_input == '3':  # Display bar chart of highest populated
            show_top_populated()
            input("Hit <ENTER> to continue...")
        elif user_input == '4':
            valid_us_state = get_us_state_input()
            if valid_us_state:
                updated_population = get_population_input()
                if updated_population:
                    set_population(valid_us_state, updated_population)
            input("Hit <ENTER> to continue...")
        elif user_input == '5':  # Exit upon user request
            sys.exit(0)
        else:
            print("Make a selection of 1 - 5...")
            input("Hit <ENTER> to continue...")


def display_state(state):
    """
    Displays US State information of the state passed as a param
    :param state:
    :return:
    """

    print("*" * 60)
    print("State:", state)
    print("Capital:", states.states[state]["Capital"])
    print("Flower:", states.states[state]["Flower"])
    url_pic = states.states[state]["URL"]
    response = requests.get(url_pic, stream=True)
    img = Image.open(response.raw)
    img.show()


def show_top_populated():
    """
    Function sorts the states dict based on population from most to least
    and then creates a bar chart to display the top 5 most populated states
    :return:
    """

    # Get a sorted list of states ordered by population (most to least)
    pop_sort = sorted(states.states.keys(),
                      key=lambda key_:
                      int(states.states[key_]['Population']),
                      reverse=True)

    # Remove all be the first five (most populated) states in list
    pop_sort = pop_sort[:5]
    populations = []

    print("*" * 60)
    print("The five (5) top populated US States are:")

    # Build populations list
    for state in pop_sort:
        print("\t{}: {:,}".format(state,
                                  int(states.states[state]['Population'])))
        populations.append(int(states.states[state]['Population']))

    # Plot states population
    plt.bar(pop_sort, populations)
    plt.gca().yaxis.get_major_formatter().set_scientific(False)
    plt.xlabel("States", fontsize=14)
    plt.ylabel("Population", fontsize=14)
    plt.subplots_adjust(left=0.2)
    plt.title("Most Populated US States")
    plt.show()


def get_us_state_input():
    """
    Solicits for user input for US State. If user input includes only spaces
    and alphabetic chars, function will remove extra spaces, capitalize the
    first char of each char set (as categorized by a space separator), and test
    for the existence of the phrase in the state_dict keys.

    :return: Returns a properly formatted US State if parsable from user input.
    Empty string returned if sentinel entered or invalid user input.
    """

    us_state = ''

    while not us_state:

        # Get user input
        user_input = input("Please enter a US State (-1 to go back): ").strip()

        if user_input == SENTINEL:  # go back on user request
            break

        # Validate input
        normalized_alpha_input = ''

        # Normalize to capitalized first letter and single spaced phrase / word
        # if user input only spaces and alpha chars
        if user_input.replace(' ', '').isalpha():
            words = user_input.split()

            for word in words:
                normalized_alpha_input += word.capitalize() + " "

            normalized_alpha_input = normalized_alpha_input.strip()

        if normalized_alpha_input in states.states.keys():
            us_state = normalized_alpha_input

    return us_state


def get_population_input():
    """
    Function to validate US state population as positive integer represented as
    as string.

    :return: String representation of positive integer for US State population
    if valid input entered by user. Empty string returned if sentinel entered
    or invalid user input.
    """
    updated_state_population = ''

    while not updated_state_population:

        # Get user input
        user_input = input("Please enter a US State population (positive"
                           + " integer. '-1' to go back): ").strip()

        if user_input == SENTINEL:  # go back on user request
            break

        # Validate input
        if uicom.is_int(user_input):
            if int(user_input) >= 0:
                updated_state_population = user_input

    return updated_state_population


def set_population(us_state, population):
    """
    Function that sets updates the value of the dictionary in state_dict.py

    :param us_state: Expected to be a properly formatted str (Capitalized first
    letter of each word) and a valid US State existing in state_dict.py
    :param population: Expected to a string representation of a positive
    integer

    :return: None
    """

    if us_state in states.states.keys():  # Likely a redundant check
        states.states[us_state]['Population'] = population
        print("Population of %s set to %s" % (us_state, population))
    else:
        print("[ERROR] - State does not exist in dictionary...")


if __name__ == ("__main__"):
    main()
