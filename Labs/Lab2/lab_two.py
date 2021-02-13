"""
Author: Eric thomas
Date: Jan 2021
Description: exercise produces a command line menu-driven python application
providing users with the ability to perform several math and security related
functions.

Questions:
1. Dictionary of dictionaries for min value, max value, etc.
2. Auto remove whitespace
"""

import datetime
import math
import sys
import string
import secrets
import ui_common as uicom

#####################
# GLOBAL CONSTANT(S)
#####################
SENTINEL = "-1"

def main():
    """ main method """

    pw_attribs = {
                  "pw_length"         : 0,
                  "min_uppercase"     : 0,
                  "min_lowercase"     : 0,
                  "min_digits"        : 0,
                  "min_special_chars" : 0
                 }

    percent_attribs = {
                       "numerator"   : 0,
                       "denominator" : 1,
                       "precision"   : 0
                      }

    cylinder_attribs = {
                        "radius" : 0,
                        "height" : 0
                       }

    triangle_attribs = {
                        "line_ac" : 0,
                        "line_cb" : 0,
                        "angle_c" : 0
                       }

    #Create a menu-driven command-line app
    #vars to hold text for display at top of GUI
    banner = "*" * 60
    heading = "Welcome to the Lab 2 User Application"

    while True:
        uicom.clear_screen()
        print(banner)
        print(heading)

        print("How can I help you? ")
        print("\ta. Generate a Secure Password")
        print("\tb. Calculate and format a percentage")
        print("\tc. Calculate days until July 4, 2025")
        print("\td. Calculate the leg of a triangle")
        print("\te. Calculate the volume of a circular cylinder")
        print("\tf. Exit")

        user_input = input ("Enter a selection: ").strip()

        #USER INPUT OPTIONS
        if user_input == 'a':
            if set_pw_attributes(pw_attribs):
                generate_secure_password(pw_attribs)
        elif user_input == 'b':
            if set_percent_attributes(percent_attribs):
                calculate_percentage(percent_attribs)
        elif user_input == 'c':
            date_delta()
        elif user_input == 'd':
            if set_triangle_attributes(triangle_attribs):
                calculate_triangle_leg_length(triangle_attribs)
        elif user_input == 'e':
            if set_cylinder_attributes(cylinder_attribs):
                calculate_cylinder_area(cylinder_attribs)
        elif user_input == 'f':
            sys.exit(0)
        else:
            print ("Make a selection of a - f...")
            input("Hit <ENTER> to continue...")

def set_pw_attributes(pw_attribs):
    """Generate secure password. Prompt the user for the length of the
    password to be created, as well as the complexity (i.e. Use of UpperCase,
    Use of Lower Case, Use of Numbers, Use of special characters)."""

    #bool to hold status of setting an attrib value
    attrib_set = False

    #sentinel flag
    sentinel_input = False

    #To hold count of pw attribute contraints to verify length is not exceeded
    attrib_total = 0

    solicitations = [
                     "Enter the password length: ",
                     "Enter minimum uppercase chars: ",
                     "Enter minimum lowercase chars: ",
                     "Enter minimum digits: ",
                     "Enter minimum special chars: "
                    ]

    print("\nYou chose to generate a secure password...")
    print("Enter '-1' to go back\n")

    for attrib, solicit in zip(pw_attribs, solicitations):
        #set flag on each iteration
        attrib_set = False

        while ((not sentinel_input) and (not attrib_set)):
            user_input = input(solicit).strip()

            if user_input == SENTINEL:
                sentinel_input = True

            #if input not sentinel, evaluate the input and set attrib_set flag
            #to true if values pass all checks
            if not sentinel_input:
                if (uicom.is_int(user_input)
                    and int(user_input) >= 0):
                    #Sum all attribs except pw length
                    if attrib != "pw_length":
                        attrib_total += int(user_input)
                    #verify attribs sum (excluding pw_length) are
                    #less than pw_length
                    if attrib_total <= pw_attribs['pw_length']:
                        pw_attribs[attrib] = int(user_input)
                        attrib_set = True
                    else:
                        print("\n[ERROR] Your constraints exceed the total"
                             +" password length of %d" %
                               pw_attribs["pw_length"])
                        input("Hit <ENTER> to continue...")
                        break
                else:
                    print("[ERROR] Enter an integer value of 0 or greater...")

        if sentinel_input or not attrib_set:
            break

    return attrib_set #will be false if not all attribs set

def generate_secure_password(pw_attribs):
    """ Generate a secure password based on attributes passed to function """
    banner = "*" * 60
    pw_rqmts_met = False
    char_list = string.ascii_letters + string.digits + string.punctuation
    password = ""

    #Generate the password by randomly selecting from the char list
    #until all requirements are met
    while not pw_rqmts_met:
        password = "".join(secrets.choice(char_list)
                           for i in range(pw_attribs["pw_length"]))

        #Verify requirements are met and remove the first char if not
        if ((len(password) == pw_attribs["pw_length"])
            and (sum(c.isupper() for c in password)
                >= pw_attribs["min_uppercase"])
            and (sum(c.islower() for c in password)
                >= pw_attribs["min_lowercase"])
            and (sum(c.isdigit() for c in password)
                >= pw_attribs["min_digits"])
            and (sum(c in string.punctuation for c in password)
                >= pw_attribs["min_special_chars"])):
            pw_rqmts_met = True
        else:
            password = password[1:]
            break

    #Display result
    print("\n%s" % (banner))
    print ("Your password is: %s" % password)
    print("%s\n" % (banner))
    input ("Hit <Enter> to continue...")

def set_percent_attributes(percent_attribs):
    """ get / validate user input to set attribs passed to function """
    #bool to hold status of setting an attrib value
    attrib_set = False

    #sentinel flag
    sentinel_input = False

    solicitations = [
                     "Enter a positive integer numerator: ",
                     "Enter a positive integer denominator: ",
                     "Enter a positive integer float precision: "
                    ]

    print("You chose to calculate and format a percentage...")
    print("Enter '-1' to go back\n")

    #cycle through all the attributes and solicit the user for values
    for attrib, solicit in zip(percent_attribs, solicitations):
        #set flag on each iteration
        attrib_set = False

        min_attrib_val = (0 if attrib != "numerator" else 1)

        while ((not sentinel_input) and (not attrib_set)):
            user_input = input(solicit).strip()

            if user_input == SENTINEL:
                sentinel_input = True

            #if input not sentinel, evaluate the input and set attrib_set flag
            #to true if values pass all checks
            if not sentinel_input:
                #verify input is an integer grater than min alllowable value
                if (uicom.is_int(user_input)
                    and int(user_input) >= min_attrib_val):
                    percent_attribs[attrib] = int(user_input)
                    attrib_set = True
                else:
                    print("[ERROR] Enter an integer value greater than"
                         +" %d..." % (min_attrib_val))

        if sentinel_input:
            break #break before setting any more attributes

    return attrib_set #will be left false if not all attribs set

def calculate_percentage(percent_attribs):
    """
    Generates and returns a string representation of a percentage based on
    attribs passed to function
    """

    percentage = round((percent_attribs["numerator"] / percent_attribs["denominator"]),
                        percent_attribs["precision"])
    percentage = percentage * 100

    #Display result
    banner = "*" * 60
    print("\n%s" % (banner))
    print("The percentage is %.*f" %
         (percent_attribs["precision"], percentage))
    print("%s\n" % (banner))
    input ("Hit <Enter> to continue...")

def date_delta():
    """ Return the number of days from today until 2025-07-04 """

    today = datetime.date.today()
    future = datetime.date.fromisoformat("2025-07-04")
    print(future)
    delta_days = future - today


    #Display result
    banner = "*" * 60
    print("\n%s" % (banner))
    print(delta_days.days, "days until July 4th, 2025...")
    print("%s\n" % (banner))
    input ("Hit <Enter> to continue...")

def set_triangle_attributes(triangle_attribs):
    """ get / validate user input to set attribs passed to function """

    print("You chose to calculate the leg of a triangle...")
    print("Enter '-1' to go back\n")

    #bool to hold status of setting an attrib value
    attrib_set = False

    #sentinel flag
    sentinel_input = False

    solicitations = [
                     "Enter a positive integer for line a<->c length: ",
                     "Enter a positive integer for line c<->b length: ",
                     "Enter a positive integer for angle C in the triangle"
                    +" (in degrees): "
                    ]

    #cycle through all the attributes and solicit the user for values
    for attrib, solicit in zip(triangle_attribs, solicitations):
        #set flag on each iteration
        attrib_set = False

        while ((not sentinel_input) and (not attrib_set)):
            user_input = input(solicit).strip()

            if user_input == SENTINEL:
                sentinel_input = True

            #if input not sentinel, evaluate the input and set attrib_set flag
            #to true if values pass all checks
            if not sentinel_input:
                #verify input is an integer grater than min alllowable value
                if (uicom.is_int(user_input)
                    and int(user_input) >= 0):
                    triangle_attribs[attrib] = int(user_input)
                    attrib_set = True
                else:
                    print("[ERROR] Positive integer value required...")

        if sentinel_input:
            break #break before setting any more attributes

    return attrib_set

def calculate_triangle_leg_length(triangle_attrib):
    """
    Calculates the leg of a triangle per triangle attributes using
    the Law of Cosines
    """

    #Convert all values to floats
    line_a = float(triangle_attrib["line_cb"])
    line_b = float(triangle_attrib["line_ac"])
    #convert degrees to radians
    angle_radians = float(triangle_attrib["angle_c"]) * (math.pi / 180)

    #Find lenght of line_c with Law of Cosines
    line_c = math.sqrt((line_a ** 2)
                      +(line_b ** 2)
                      -(2 * line_a * line_b * math.cos(angle_radians)))

    #Display result
    banner = "*" * 60
    print("\n%s" % (banner))
    print ("The length of leg c is: %.3f" % line_c)
    print("%s\n" % (banner))
    input ("Hit <Enter> to continue...")

def set_cylinder_attributes(cylinder_attribs):
    """ get / validate user input to set attribs passed to function """

    print("You chose to calculate the area of a cylinder...")
    print("Enter '-1' to go back\n")

    #bool to hold status of setting an attrib value
    attrib_set = False

    #sentinel flag
    sentinel_input = False

    solicitations = [
                     "Enter a positive integer radius: ",
                     "Enter a positive integer height: "
                    ]

    #cycle through all the attributes and solicit the user for values
    for attrib, solicit in zip(cylinder_attribs, solicitations):
        #set flag on each iteration
        attrib_set = False

        while ((not sentinel_input) and (not attrib_set)):
            user_input = input(solicit).strip()

            if user_input == SENTINEL:
                sentinel_input = True

            #if input not sentinel, evaluate the input and set attrib_set flag
            #to true if values pass all checks
            if not sentinel_input:
                #verify input is an integer grater than min alllowable value
                if (uicom.is_int(user_input)
                    and int(user_input) >= 0):
                    cylinder_attribs[attrib] = int(user_input)
                    attrib_set = True
                else:
                    print("[ERROR] Positive integer value required...")

        if sentinel_input:
            break #break before setting any more attributes

    return attrib_set

def calculate_cylinder_area(cylinder_attribs):
    """ calculate volume of cylinder per cylinder attributes """
    volume = (math.pi * (float(cylinder_attribs["radius"]) ** 2)
             * float(cylinder_attribs["height"]))

    #Display result
    banner = "*" * 60
    print("\n%s" % (banner))
    print ("The volume of the cylinder is: %.3f" % volume)
    print("%s\n" % (banner))
    input ("Hit <Enter> to continue...")

if __name__ == ("__main__"):
    main()
