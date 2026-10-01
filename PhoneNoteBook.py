####################################################################
## Description: Manage a local phone book stored in NoteBook.csv
##
## Author: Matteo Z.
####################################################################

import sys
import traceback
from argparse import ArgumentParser, RawDescriptionHelpFormatter
from datetime import datetime

csv_file = "NoteBook.csv"
log_file = "NoteBook.log"

def create_empty_csvfile():
    with open(csv_file, "a"):
        pass


def write_to_logfile(msg):
    with open(log_file, "a") as stream:
        stream.write(msg)


def read_csvfile():
    with open(csv_file, "r") as stream:
        return [line.rstrip("\r\n") for line in stream if line.strip()]


def write_contacts(contacts):
    # Always truncate the file, even when no contacts remain.
    with open(csv_file, "w") as stream:
        for line in sorted(contacts):
            stream.write(line + "\n")


def contact_matches(line, surname, name=None):
    fields = line.split(";", 3)
    return (
        len(fields) >= 3
        and fields[0].strip().upper() == surname.upper()
        and (name is None or fields[1].strip().upper() == name.upper())
    )


def start_log(operation, surname, name=None, phone_number=None, description=None):
    timestamp = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    message = (
        f"Date of execution: {timestamp}\n\nOperation: {operation}\n\nArguments:\n\n"
        f"\tSurname: {surname}\n"
    )
    for label, value in (("Name", name), ("Phone number", phone_number),
                         ("Description", description)):
        if value is not None:
            message += f"\t{label}: {value}\n"
    write_to_logfile(message)


def finish_operation(message, status=0):
    print(message)
    write_to_logfile(f"\n{message}\n\n-------------------------------------\n")
    print(f"Read the log file ({log_file}) if you want more info!")
    return status


def add_contact(values):
    surname, name, phone_number = values[:3]
    description = values[3] if len(values) == 4 else None
    start_log("add_contact", surname, name, phone_number, description)
    contacts = read_csvfile()
    if any(contact_matches(line, surname, name) for line in contacts):
        return finish_operation(f"This contact ({surname} {name}) already exists!", 1)

    fields = [surname.upper(), name.upper(), phone_number]
    if description is not None:
        fields.append(description)
    contacts.append("; ".join(fields))
    write_contacts(contacts)
    return finish_operation(
        f"Contact ({surname} {name}) has been added in the csv file ({csv_file})!"
    )


def modify_contact(values):
    mode, surname, name = values[:3]
    phone_number = values[3] if mode in ("t", "b") else None
    description = values[4] if mode == "b" else values[3] if mode == "c" else None
    start_log("modify_contact", surname, name, phone_number, description)
    contacts = read_csvfile()

    for index, line in enumerate(contacts):
        if contact_matches(line, surname, name):
            fields = [field.strip() for field in line.split(";", 3)]
            if phone_number is not None:
                fields[2] = phone_number
            if description is not None:
                fields = fields[:3] + [description]
            contacts[index] = "; ".join(fields)
            write_contacts(contacts)
            return finish_operation(
                f"Contact ({surname} {name}) has been updated in the csv file ({csv_file})!"
            )

    return finish_operation(f"This contact ({surname} {name}) does not exist yet!", 1)


def remove_contact(values):
    surname = values[0]
    name = values[1] if len(values) == 2 else None
    start_log("remove_contact", surname, name)
    contacts = read_csvfile()
    matches = [line for line in contacts if contact_matches(line, surname, name)]
    label = surname if name is None else f"{surname} {name}"
    if not matches:
        return finish_operation(f"This contact ({label}) does not exist yet!", 1)
    if len(matches) > 1 and name is None:
        return finish_operation(
            f"This surname ({surname}) has been found {len(matches)} times, "
            "please also enter a name!", 1
        )

    answer = input("Do you really want to delete this contact (y/n)? ")
    if answer != "y":
        return finish_operation("Deletion cancelled.")

    write_contacts([line for line in contacts if not contact_matches(line, surname, name)])
    return finish_operation(
        f"Contact ({label}) has been removed from the csv file ({csv_file})!"
    )


def search_contact(values):
    surname, name = values
    start_log("search_contact", surname, name)
    for line in read_csvfile():
        if contact_matches(line, surname, name):
            return finish_operation(f"Contact info: {line}")
    return finish_operation(f"This contact ({surname} {name}) does not exist yet!", 1)


def validate_values(parser, operation, values):
    expected = {"add": (3, 4), "rem": (1, 2), "search": (2,)}
    if operation == "mod":
        mode = values[0]
        if mode not in ("t", "c", "b"):
            parser.error("modification mode must be t, c, or b")
        required = 5 if mode == "b" else 4
        if len(values) != required:
            parser.error(f"--mod {mode} requires {required - 1} arguments after the mode")
    elif len(values) not in expected[operation]:
        counts = " or ".join(str(count) for count in expected[operation])
        parser.error(f"--{operation} requires {counts} arguments")

    # Preserve the existing, unquoted semicolon-separated file format.
    if any(any(char in value for char in ";\r\n") for value in values):
        parser.error("contact fields cannot contain semicolons or line breaks")
    values = [value.strip() for value in values]
    name_offset = 1 if operation == "mod" else 0
    name_count = 1 if operation == "rem" and len(values) == 1 else 2
    if any(not value for value in values[name_offset:name_offset + name_count]):
        parser.error("surname and name cannot be empty")

    phone_number = None
    if operation == "add":
        phone_number = values[2]
    elif operation == "mod" and values[0] in ("t", "b"):
        phone_number = values[3]
    if phone_number is not None and (
        len(phone_number) != 10 or any(char not in "0123456789" for char in phone_number)
    ):
        parser.error("the phone number must contain exactly 10 digits (0-9)")
    return values


def main_program(argv=None):
    parser = ArgumentParser(
        description="Manage contacts in NoteBook.csv in the current working directory.",
        allow_abbrev=False,
        formatter_class=RawDescriptionHelpFormatter,
        epilog="""Argument order:
  -a SURNAME NAME PHONE_NUMBER [DESCRIPTION]
  -m t SURNAME NAME NEW_PHONE_NUMBER
  -m c SURNAME NAME NEW_DESCRIPTION
  -m b SURNAME NAME NEW_PHONE_NUMBER NEW_DESCRIPTION
  -r SURNAME [NAME]
  -s SURNAME NAME

Quote values containing spaces. Phone numbers must contain exactly 10 digits.""",
    )
    operations = parser.add_mutually_exclusive_group(required=True)
    operations.add_argument("-a", "--add", nargs="+", help="add a new contact")
    operations.add_argument("-m", "--mod", nargs="+", help="modify a contact (t, c, or b)")
    operations.add_argument("-r", "--rem", nargs="+", help="remove a contact")
    operations.add_argument("-s", "--search", nargs=2, help="search for a contact")
    args = parser.parse_args(argv)
    handlers = {"add": add_contact, "mod": modify_contact,
                "rem": remove_contact, "search": search_contact}
    operation = next(key for key in handlers if getattr(args, key) is not None)
    values = validate_values(parser, operation, getattr(args, operation))

    try:
        create_empty_csvfile()
        return handlers[operation](values)
    except Exception as error:
        print(f"Error: {error}", file=sys.stderr)
        try:
            write_to_logfile(
                f"Error!!\nScript name: {sys.argv[0]}\n"
                f"Script args: {argv if argv is not None else sys.argv[1:]}\n\n"
                f"{traceback.format_exc()}\n-------------------------------------\n"
            )
        except OSError as log_error:
            print(f"Could not write the log file: {log_error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main_program())