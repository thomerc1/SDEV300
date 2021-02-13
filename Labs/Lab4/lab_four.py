"""
__filename__ = "lab_four.py"
__coursename__ = "SDEV 300 6380 - Building Secure Web Applications (2198)"
__author__ = "Eric Thomas"
__copyright__ = "None"
__credits__ = ["Eric Thomas"]
__license__ = "GPL"
__version__ = "1.0.0"
__maintainer__ = "Eric Thomas"
__email__ = "ethomas48@student.umgc.edu"
__status__ = "Test"
"""

import re
import numpy as np
import ui_common as uicom

#####################
# GLOBAL CONSTANT(S)
#####################
SENTINEL = "-1"
MATRIX_SIZE = 9


def main():
    """
    main method
    :return: Main returns 0 on exit
    """

    # Create a menu-driven command-line app
    # vars to hold text for display at top of GUI
    banner = '*' * 60
    heading = "{:^60s}\n".format("Welcome to the Lab 4 Matrix Game")
    footer = "\n{:^60s}".format("Thank you for playing")

    while True:
        uicom.clear_screen()
        print(banner)
        print(heading)

        print("Do you want to play the Matrix Game? ")
        user_input = input("Enter 'Y' for Yes and 'N' for No: ").strip()
        if user_input.lower() == 'y':
            print("\n[ALERT] Enter -1 at anytime to go back...\n")
            proceed = True
            if not get_phone_number():
                proceed = False
            if proceed and (not get_zip()):
                proceed = False
            if proceed:
                play_matrix_game()
        elif user_input.lower() == 'n':
            break
        else:
            print("[ERROR] Invalid entry...")
            input("Hit <ENTER> to continue...")

    print(footer)
    print(banner)
    return 0


def play_matrix_game():
    """
    Function that manages the matrice part of the game
    :return: implicit
    """

    proceed = True

    # Get matrix one
    matrix_one = get_matrix()

    # If matrix of proper size, display it to user
    if matrix_one.size == MATRIX_SIZE:
        print("Your first 3x3 matrix is: ")
        display_numpy_matrix(matrix_one)
    else:
        proceed = False

    # Get matrix two
    if proceed:
        matrix_two = get_matrix()

        # If matrix of proper size, display it to user
        if matrix_two.size == MATRIX_SIZE:
            print("Your second 3x3 matrix is: ")
            display_numpy_matrix(matrix_two)

        else:
            proceed = False

    # Operate on the matrices
    if proceed:
        operate_on_matrices(matrix_one, matrix_two)

    return 0


def operate_on_matrices(matrix_one, matrix_two):
    """
    Function to operate on matrices passed as parameters
    :return: implicit
    """
    # Flag for valid user selection
    valid_operation_selected = False

    # Initialized vars
    output_matrix = np.array([])
    input_confirmation = ""

    while not valid_operation_selected:
        print("Select a matrix operation from the list below"
              "(-1 to go back): ")
        print("a. Addition")
        print("b. Subtraction")
        print("c. Matrix Multiplication")
        print("d. Element by element multiplication")
        user_input = input().strip()

        if user_input.lower() == 'a':
            valid_operation_selected = True
            output_matrix = matrix_one + matrix_two
            input_confirmation = "You selected Addition. The results are: "
        elif user_input.lower() == 'b':
            valid_operation_selected = True
            output_matrix = matrix_one - matrix_two
            input_confirmation = "You selected Subtraction. The results are: "
        elif user_input.lower() == 'c':
            valid_operation_selected = True
            output_matrix = np.matmul(matrix_one, matrix_two)
            input_confirmation = ("You selected Matrix Multiplication.",
                                  "The results are: ")
        elif user_input.lower() == 'd':
            valid_operation_selected = True
            output_matrix = matrix_one * matrix_two
            input_confirmation = ("You selected element by element"
                                  "multiplication. The results are: ")
        elif user_input == SENTINEL:
            break
        else:
            print("[ERROR] Invalid selection...")
            input("Hit <ENTER> to continue...")

    # Display operation results if user entered input properly
    if valid_operation_selected:
        print(input_confirmation)
        display_numpy_matrix(output_matrix)
        print("The row and column mean values of the results are: ")
        print("Rows: ", ["{:0.2f}".format(x) for x in
                         output_matrix.mean(axis=1)])
        print("Columns: ", ["{:0.2f}".format(x) for x in
                            output_matrix.mean(axis=0)])
        input("Hit <ENTER> to continue...")
        print("The transpose is: ")
        display_numpy_matrix(output_matrix.T)


def get_matrix():
    """
    Obtains and validates user input to add rows of a ndarray to achieve a
    3x3 matrix
    :return: 3x3 ndarray if properly formatted user input, else an empty array
    """

    # Regex pattern
    row_pattern = r'-?\d+ -?\d+ -?\d+'

    matrix = np.array([], dtype=int)

    while matrix.size < MATRIX_SIZE:
        solicitation = "Enter one row of integers for a 3x3 matrix (X X X): "
        user_input = input(solicitation).strip()
        if re.fullmatch(row_pattern, user_input):

            # Build list of ints from input
            row = [int(item) for item in user_input.split()]

            # Append list of ints to ndarray
            matrix = np.append(matrix, row)

        elif user_input == SENTINEL:
            break
        else:
            print("[ERROR] Improperly formatted matrix row...")

    if matrix.size == 9:
        # Resize the matrix in place
        matrix.resize(3, 3)
    else:
        matrix = np.array([], dtype=int)

    return matrix


def display_numpy_matrix(matrix):
    """
    function to display a 3x3 ndarray row by row
    :param matrix: 3x3 numpy ndarray
    :return: implicit
    """
    for row in matrix:
        for item in row:
            print(item, end='   ')
        print()

    input("Hit <ENTER> to continue...")


def get_phone_number():
    """
    Obtains user input for a phone number and checks the format with regex.
    :return: returns the properly formatted phone number or an empty string
    """

    # Regex pattern
    phone_number_pattern = r'\d{3}-\d{3}-\d{4}'

    ret_val = ''

    while not ret_val:
        user_input = input("Enter your phone number(XXX-XXX-XXXX): ").strip()

        result = re.fullmatch(phone_number_pattern, user_input)
        if result:
            ret_val = result.group()
        elif user_input == SENTINEL:
            break
        else:
            print("[ERROR] Your phone number format is incorrect...")

    return ret_val


def get_zip():
    """
    Obtains user input for a zipcode and checks the format with regex.
    :return: returns the properly formatted zipcode or an empty string
    """
    # Regex pattern
    zip_code_pattern = r'\d{5}-\d{4}'

    ret_val = ''

    while not ret_val:
        user_input = input("Enter your zip code+4 (XXXXX-XXXX): ").strip()

        result = re.fullmatch(zip_code_pattern, user_input)
        if result:
            ret_val = result.group()
        elif user_input == SENTINEL:
            break
        else:
            print("[ERROR] Your zip code format is incorrect...")

    return ret_val


if __name__ == ("__main__"):
    main()
