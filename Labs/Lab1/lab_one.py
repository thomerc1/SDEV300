"""
Author: Eric Thomas
Date: Jan 2021
Description: Lab One
Requirements:
Using your Python programming environment, write a Python application that
supports voter registration. The application will launch and run from the
command line prompt. The application will prompt the user for their first
name, last name, AGE, country of citizenship, STATE of residence and zipcode.
To be a valid registration all fields must be entered. If they are at least
18 years old and a U.S citizen, they can move forward and be prompted for the
remaining questions and register to vote. If not, they should not be presented
with the additional questions. There should be some error checking logic on
the input STATEments to make sure the AGE numbers entered seem reasonable
(e.g. a person is probably not > 120 years) and STATEs should be 2 letter
representing only valid U.S. STATEs. The application should prompt the user
for the needed questions to complete the registration and re-prompt when data
is invalid giving the user the opportunity to retry. The output should
summarize the input data and congratulate the user if they are eligible to
vote and entered all of the data. The user should be given options to exit the
program at any time to cancel the registration process.
"""

import os
import states

def main():
    """ main method """
    #Dictionary to pass-by-reference to set functions
    reg_data = {
                "first_name": "",
                "last_name": "",
                "age": "",
                "us_citizen": "",
                "state": "",
                "zip_code": ""
                }
    #var to hold voter registration result at each step
    input_success = True
    ########################################################################
    #Traverse through each set function while verifying prior steps success
    #If a step is unsuccessful, it's required halt registration
    ########################################################################
    clear_screen()
    display_gui("head")
    input_success = set_first_name(reg_data, "first_name")
    if input_success:
        clear_screen()
        display_gui("head")
        input_success = set_last_name(reg_data, "last_name")
    if input_success:
        clear_screen()
        display_gui("head")
        input_success = set_age(reg_data, "age")
    if input_success:
        clear_screen()
        display_gui("head")
        input_success = verify_citizenship(reg_data, "us_citizen")
    if input_success:
        clear_screen()
        display_gui("head")
        input_success = set_state(reg_data, "state")
    if input_success:
        clear_screen()
        display_gui("head")
        input_success = set_zip(reg_data, "zip_code")
    ##########################################
    #         Display Final Messages
    ##########################################
    if input_success:
        print("\n****  Congratulations!  ****")
        print("You successfully registered!")
        print("Name:", reg_data["first_name"], reg_data["last_name"])
        print("Age:", reg_data["age"])
        print("U.S. Citizen:", reg_data["us_citizen"])
        print("State:", reg_data["state"])
        print("Zip code:", reg_data["zip_code"])
        print("****************************\n")
    else:
        print("\n[ALERT] You're registration was unsuccessful.")
        print("You either do not meet the registration requirements\n"
            + "or chose to exit the registration application.\n")
    display_gui("tail")
##############################################################################
# Set Functions - Return true on success or false upon error or sentinel input
##############################################################################
def set_first_name(reg_data, item_key):
    """ function to set user's first name """
    prompt = "Enter your first name: "
    fname_set = False
    while not fname_set:
        user_input = input(prompt).strip()
        #Eval sentinel
        if user_input == "-1":
            break
        #Check input requirements (alphabetic chars only)
        if user_input.isalpha():
            reg_data[item_key] = user_input
            fname_set = True
        else:
            print("[ERROR] Alphabetic input required (no spaces)...")
    return fname_set

def set_last_name(reg_data, item_key):
    """ function to set user's last name """
    prompt = "Enter your last name: "
    lname_set = False
    while not lname_set:
        user_input = input(prompt).strip()
        #Eval sentinel
        if user_input == "-1":
            break
        #Check input requirements (alphabetic chars only)
        if user_input.isalpha():
            reg_data[item_key] = user_input
            lname_set = True
        else:
            print("[ERROR] Alphabetic input required (no spaces)...")
    return lname_set

def set_age(reg_data, item_key):
    """ function to set user's age """
    prompt = "Enter your age: "
    temp_age = 0
    age_set = False
    while not age_set:
        user_input = input(prompt).strip()
        #Eval sentinel
        if user_input == "-1":
            break
        #Check input requirements
        if is_int(user_input):
            temp_age = int(user_input)
            #Verify appropriate AGE range to register and use this system
            if 18 <= temp_age <= 120:
                reg_data[item_key] = str(temp_age)
                age_set = True
            else:
                #Alert user they aren't qualified to register
                print("[ALERT] Must be 18 to 120 years old to register.")
                user_input = input("Enter '-1' to exit or [ENTER] key to "
                                  +"re-answer the question: ").strip()
                if user_input == "-1":
                    break
        else:
            print("[ERROR] Integer input required...")
    return age_set

def verify_citizenship(reg_data, item_key):
    """ function to set user's citizenship """
    prompt = "Are you a U.S. Citizen ('y' or 'n')? "
    citizenship_verified = False
    while not citizenship_verified:
        user_input = input(prompt).strip()
        #Eval sentinel
        if user_input == "-1":
            break
        #Check input requirements ('y' or 'n' chars)
        if user_input.lower() == 'y':
            reg_data[item_key] = "Yes"
            citizenship_verified = True
        elif user_input.lower() == 'n':
            #Alert user they aren't qualified to register
            print("[ALERT] Must be a US citizen to register.")
            user_input = input("Enter '-1' to exit or [ENTER] key to "
                              +"re-answer the question: ").strip()
            if user_input == "-1":
                break
        else:
            print("[ERROR] Enter 'y' or 'n'...")
    return citizenship_verified

def set_state(reg_data, item_key):
    """ function to set user's STATE """
    prompt = "Enter STATE of residence (2-letter code): "
    state_set = False
    while not state_set:
        user_input = input(prompt).strip()
        #Eval sentinel
        if user_input == "-1":
            break
        #Check input requirements (valid 2-digit state)
        if user_input.upper() in states.state_list:
            reg_data[item_key] = user_input.upper()
            state_set = True
        else:
            print("[ERROR] Enter a valid 2-letter state abbreviation")
    return state_set

def set_zip(reg_data, item_key):
    """ function to set user's zip """
    prompt = "Enter your 5-digit zipcode: "
    zip_set = False
    while not zip_set:
        user_input = input(prompt).strip()
        #Eval sentinel
        if user_input == "-1":
            break
        #Check input requirements (5-digit int)
        if (len(user_input) == 5) and (is_int(user_input)):
            reg_data[item_key] = user_input #no reason to convert to int
            zip_set = True
        else:
            print("[Error] Input must be limited to a 5-digit number")
    return zip_set

def is_int(str_val):
    """ Method to test that str val is numeric """
    is_type_int = False
    try:
        int(str_val)
        is_type_int = True
    except ValueError:
        is_type_int = False
    return is_type_int

def display_gui(option="head"):
    """ For use in displaying the gui """
    #vars to hold text for display at top of GUI
    banner = "************************************************************"
    heading = "VOTER REGISTRATION QUESTIONNAIRE"
    exit_instruction = "Enter -1 to exit"
    footer = "THANK YOU FOR USING THIS SERVICE"

    if option == "head":
        print(banner)
        print(heading)
        print(exit_instruction)

    elif option == "tail":
        print(footer)
        print(banner)

def clear_screen():
    """ function to clear the terminal """
    cmd = 'clear'
    if os.name == 'nt':
        cmd = 'cls'
    os.system(cmd)

if __name__ == ("__main__"):
    main()
