##################################################################################################################################
## Description: Script that manages an agenda where you can put some your information, modify them, remove them or search them
##
## Author: Matteo Z.
##################################################################################################################################

import os, sys, traceback
from datetime import datetime
from argparse import ArgumentParser

def print_usage():
	print("\nUsage:")
	print(f"  {os.path.basename(sys.argv[0])} [options] [params]\n")
	print("Options:\n")
	print(f"  -a|--add to add a new contact -> {os.path.basename(sys.argv[0])} -a surname name phone_number description(optional)\n")
	print("   -m|--mod to modify a contact\n")
	print(f"     t to modify a phone number -> {os.path.basename(sys.argv[0])} -m t surname name new_phone_number")
	print(f"     c to modify a description -> {os.path.basename(sys.argv[0])} -m c surname name new_description")
	print(f"     b to modify all the informations -> {os.path.basename(sys.argv[0])} -m b surname name new_phone_number new_description\n")
	print(f"  -r|--rem to remove a contact -> {os.path.basename(sys.argv[0])} -r surname (if there are more of one contact with this surname, you should put also the name)\n")
	print(f"  -s|--search to search a contact -> {os.path.basename(sys.argv[0])} -s surname name\n")
	sys.exit(1)


def create_empty_csvfile():
    if not os.path.isfile(csv_file):
        with open(csv_file, 'w') as f:
            pass


def write_to_logfile(msg):
    with open(log_file, 'a') as f:
        f.write(f"{msg}")


def read_csvfile():
    with open(csv_file, 'r') as f:
        csv_content = f.readlines()

    # print(f"CSV content: {csv_content}")
    return csv_content


def is_contact_exists(surname, name, csv_content):
    flag = 0
    line = ""

    for line in csv_content:
        line = line.strip()

        if f"{surname.upper()}; {name.upper()};" in line:
            flag = 1
            break

    return flag, line


def write_to_csvfile(msg):
    with open(csv_file, 'a') as f:
        f.write(f"{msg}\n")


def sort_csvfile():
    csv_content = read_csvfile()
    csv_content.sort()

    with open(csv_file, 'w') as f:
        for line in csv_content:
            f.write(line)


def end_logfile():
    print(f"Read the log file ({log_file}) if you want more info!")
    write_to_logfile("\n-------------------------------------\n")


def add_contact():
    if len(sys.argv) == 5 or len(sys.argv) == 6:
        surname = sys.argv[2]
        name = sys.argv[3]
        phone_number = sys.argv[4]
        # print(f"Surname: {surname} - Name: {name} - Phone number: {phone_number}")

        if phone_number.isnumeric() and len(phone_number) == 10:
            write_to_logfile(f"Date of execution: {datetime_str}\n\nOperation: {add_contact.__name__}\n\nArguments:\n\n")
            write_to_logfile(f"\tSurname: {surname}\n\tName: {name}\n\tPhone number: {phone_number}\n")

            if len(sys.argv) == 6:                # there is also the description
                description = sys.argv[5]
                write_to_logfile(f"\tDescription: {description}\n")

            csv_content = read_csvfile()
            flag, line = is_contact_exists(surname, name, csv_content)

            if flag:
                write_to_logfile(f"\nThe contact already exists in '{csv_file}' and it has not been added!\n")
                print(f"This contact ({surname} {name}) already exists!")
            else:
                if len(sys.argv) == 6:
                    write_to_csvfile(f"{surname.upper()}; {name.upper()}; {phone_number}; {description}")
                else:
                    write_to_csvfile(f"{surname.upper()}; {name.upper()}; {phone_number}")

                sort_csvfile()
                write_to_logfile(f"\nThe contact has been added in '{csv_file}'!\n")
                print(f"Contact ({surname} {name}) has been added in the csv file ({csv_file})!")

            end_logfile()
        else:
            print(f"The phone number's length ({sys.argv[4]}) must be of 10 numbers!")
    else:
        print("\nWarning!! You have done something wrong!")
        print_usage()


def modify_contact():
    if len(sys.argv) == 6 or len(sys.argv) == 7:
        surname = sys.argv[3]
        name = sys.argv[4]
        write_to_logfile(f"Date of execution: {datetime_str}\n\nOperation: {modify_contact.__name__}\n\nArguments:\n\n")
        write_to_logfile(f"\tSurname: {surname}\n\tName: {name}\n")

        if sys.argv[2] == "t":                 # modification of the telephone numberh
            phone_number = sys.argv[5]

            if phone_number.isnumeric() and len(phone_number) == 10:
                write_to_logfile(f"\tPhone number: {phone_number}\n")
                csv_content = read_csvfile()
                flag, line = is_contact_exists(surname, name, csv_content)

                if flag:
                    old_phone_number = line.split(";")[2].strip()
                    print(f"Old phone number: {old_phone_number}")
                    sys.exit(1)
                else:
                    write_to_logfile(f"\nThe contact has not been found in '{csv_file}'!\n")
                    print(f"This contact ({surname}) does not exists yet!")
            else:
                print(f"The phone number's length ({sys.argv[4]}) must be of 10 numbers!")
        elif sys.argv[2] == "c":               # modification of the description
            description = sys.argv[5]
            write_to_logfile(f"\tDescription: {description}\n")
            csv_content = read_csvfile()
            flag, line = is_contact_exists(surname, name, csv_content)

            if flag:
                old_description = line.split(";")[3].strip()
                print(f"Old description: {old_description}")
            else:
                write_to_logfile(f"\nThe contact has not been found in '{csv_file}'!\n")
                print(f"This contact ({surname}) does not exists yet!")
        elif sys.argv[2] == "b":               # modification of the telephone number and the description
            phone_number = sys.argv[5]
            description = sys.argv[5]
            write_to_logfile(f"\tPhone number: {phone_number}\n\tDescription: {description}\n")
            csv_content = read_csvfile()
            flag, line = is_contact_exists(surname, name, csv_content)

            if flag:
                old_phone_number = line.split(";")[2].strip()
                old_description = line.split(";")[3].strip()
            else:
                write_to_logfile(f"\nThe contact has not been found in '{csv_file}'!\n")
                print(f"This contact ({surname}) does not exists yet!")
        else:
            write_to_logfile(f"\nI don't understand what you want to modify, read the Usage to know how do you do!\n")
            print("\nWarning!! You have done something wrong!")
            print_usage()

        end_logfile()
    else:
        print("\nWarning!! You have done something wrong!")
        print_usage()


def count_surname(surname, csv_content):
    flag = 0
    line = ""

    for line in csv_content:
        line = line.strip()

        if f"{surname.upper()};" in line:
            flag += 1

    # print(f"Counter surname: {flag}")
    return flag


def new_csvfile(csv_content, args):
    new_csv_content = []
    # print(f"Argument list: {args}")

    for line in csv_content:
        line = line.strip()

        if len(args) == 1:
            if f"{args[0].upper()};" not in line:
                new_csv_content.append(line)
        else:
            if f"{args[0].upper()}; {args[1].upper()};" not in line:
                new_csv_content.append(line)

    if len(new_csv_content) > 0:
        with open(csv_file, 'w') as f:
            for item in new_csv_content:
                f.write(f"{item}\n")


def remove_contact(args):
    if len(sys.argv) == 3 or len(sys.argv) == 4:
        surname = sys.argv[2]

        write_to_logfile(f"Date of execution: {datetime_str}\n\nOperation: {remove_contact.__name__}\n\nArguments:\n\n")
        write_to_logfile(f"\tSurname: {surname}\n")

        if len(sys.argv) == 4:                # there is also the name
            name = sys.argv[3]
            write_to_logfile(f"\tName: {name}\n")

        csv_content = read_csvfile()

        if len(sys.argv) == 3:
            flag = count_surname(surname, csv_content)

            if flag > 1:
                write_to_logfile(f"\nThe contact with this surname has been found {flag} times '{csv_file}', you should put also the name!\n")
                print(f"This contact ({surname}) has been found {flag} times, please also enter a name!")
            elif flag == 0:
                write_to_logfile(f"\nThe contact has not been found in '{csv_file}'!\n")
                print(f"This contact ({surname}) does not exists yet!")
            else:
                answer = input("Do you really want delete this contact (y/n)? ")

                if answer == "y":
                    new_csvfile(csv_content, args.rem)
                    write_to_logfile(f"\nThe contact has been removed from '{csv_file}'!\n")
                    print(f"Contact ({surname}) has been removed from the csv file ({csv_file})!")
                else:
                    write_to_logfile(f"\nThe contact has not been removed from '{csv_file}'!\n")
                    print("You prefer not delete this contact!!\n")
        else:
            flag, line = is_contact_exists(surname, name, csv_content)

            if flag:
                answer = input("Do you really want delete this contact (y/n)? ")

                if answer == "y":
                    new_csvfile(csv_content, args.rem)
                    write_to_logfile(f"\nThe contact has been removed from '{csv_file}'!\n")
                    print(f"Contact ({surname} {name}) has been removed from the csv file ({csv_file})!")
                else:
                    write_to_logfile(f"\nThe contact has not been removed from '{csv_file}'!\n")
                    print("You prefer not delete this contact!!\n")
            else:
                write_to_logfile(f"\nThe contact has not been found in '{csv_file}'!\n")
                print(f"This contact ({surname} {name}) does not exists yet!")

        end_logfile()
    else:
        print("\nWarning!! You have done something wrong!")
        print_usage()


def search_contact():
    surname = sys.argv[2]
    name = sys.argv[3]

    write_to_logfile(f"Date of execution: {datetime_str}\n\nOperation: {search_contact.__name__}\n\nArguments:\n\n")
    write_to_logfile(f"\tSurname: {surname}\n\tName: {name}\n")
    csv_content = read_csvfile()

    flag, line = is_contact_exists(surname, name, csv_content)

    if flag:
        write_to_logfile(f"\nFound: {line}\n")
        print(f"Contact info: {line}")
    else:
        write_to_logfile(f"\nThe contact has not been found in '{csv_file}'!\n")
        print(f"This contact ({surname} {name}) does not exists yet!")

    end_logfile()


def main_program():
    parser = ArgumentParser(allow_abbrev=False)
    parser.add_argument("-a", "--add", nargs="+", help="to add a new contact")
    parser.add_argument("-m", "--mod", nargs="+", help="to modify a contact")
    parser.add_argument("-r", "--rem", nargs="+", help="to remove a contact")
    parser.add_argument("-s", "--search", nargs=2, help="to search a contact")
    args = parser.parse_args()

    if args.add:
        add_contact()
    elif args.mod:
        modify_contact()
    elif args.rem:
        remove_contact(args)
    elif args.search:
        search_contact()
               

# ------------------
# ------ MAIN ------
# ------------------

csv_file = "NoteBook.csv"
log_file = "NoteBook.log"
now = datetime.now()
datetime_str = now.strftime("%d/%m/%Y %H:%M:%S")

if len(sys.argv) > 1:
    try:
        create_empty_csvfile()
        main_program()
    except Exception as e:
        print("Error:", e)
        write_to_logfile(f"Error!!\nScript name: {sys.argv[0]}\nScript args: {sys.argv[1:]}\n\n{traceback.format_exc()}")
else:
    print_usage()
