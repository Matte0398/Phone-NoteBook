# Phone NoteBook

A Python command-line phone book that stores contacts in a local CSV file and records operations in a log file.

The script supports adding, searching, modifying, and removing contacts, with argument validation and an operation log.

## Requirements

- Python 3.6 or later (the script uses f-strings).
- Read and write access to the directory where you run the commands.

The application uses only the Python standard library. No packages need to be installed.

The examples below use `python`. Depending on your environment, use `python3` or the Windows Python launcher, `py`, instead.

## Quick start

Open a terminal in the project directory and add a fictional contact:

```bash
python MyPhoneNoteBook.py --add Rossi Alice 0000000001 "Demo contact"
```

Search for the contact:

```bash
python MyPhoneNoteBook.py --search Rossi Alice
```

Display the command-line help:

```bash
python MyPhoneNoteBook.py --help
```

Running the script without arguments prints a usage error and exits with status `2`. Use `--help` for the full syntax and argument order; it exits with status `0`. Neither command creates the CSV or log file.

## Usage

Supply exactly one operation per invocation. Arguments must follow the order shown below: **surname first, then name**. Enclose values containing spaces in quotes.

Leading and trailing whitespace is stripped from contact values. Surnames and names cannot be empty. Semicolons and line breaks are rejected in all contact fields because the storage format does not escape them. Invalid arguments are rejected before the CSV or log is created or changed.

### Add a contact

```text
python MyPhoneNoteBook.py -a SURNAME NAME PHONE_NUMBER [DESCRIPTION]
```

```bash
python MyPhoneNoteBook.py -a Rossi Alice 0000000001 "Demo contact"
python MyPhoneNoteBook.py --add Verdi Bob 0000000002
```

- Phone numbers must contain exactly 10 digits (`0-9`). Internal spaces, hyphens, and a leading `+` are not accepted. Leading zeros are preserved.
- The description is optional.
- Surnames and names are stored in uppercase; descriptions keep their original case.
- The script rejects an existing surname/name combination using exact, case-insensitive matching.
- After a successful addition, the CSV rows are sorted alphabetically.

### Search for a contact

```text
python MyPhoneNoteBook.py -s SURNAME NAME
```

```bash
python MyPhoneNoteBook.py --search Rossi Alice
```

Both surname and name are required. Matching is exact and case-insensitive within each field: searching for `Rossi` will not match `De Rossi`, and text in the description is not considered. The matching row is printed to the terminal. A missing contact returns status `1`.

### Remove a contact

```text
python MyPhoneNoteBook.py -r SURNAME [NAME]
```

```bash
python MyPhoneNoteBook.py --rem Rossi Alice
python MyPhoneNoteBook.py -r Rossi
```

If a surname matches multiple entries, supply the name as well. The script asks for confirmation: enter lowercase `y` to proceed; any other answer cancels the deletion.

Deleting the last remaining contact leaves an empty CSV file. Cancelling a deletion leaves the contacts unchanged and returns status `0`. A missing contact or an ambiguous surname returns status `1`.

### Modify a contact

The parser accepts `-m` or `--mod` with the following modes:

| Mode | Syntax                                               | Operation                |
| ---- | ---------------------------------------------------- | ------------------------ |
| `t`  | `-m t SURNAME NAME NEW_PHONE_NUMBER`                 | Update the phone number. |
| `c`  | `-m c SURNAME NAME NEW_DESCRIPTION`                  | Update the description.  |
| `b`  | `-m b SURNAME NAME NEW_PHONE_NUMBER NEW_DESCRIPTION` | Update both fields.      |

Examples:

```bash
python MyPhoneNoteBook.py -m t Rossi Alice 0000000003
python MyPhoneNoteBook.py -m c Rossi Alice "Updated description"
python MyPhoneNoteBook.py -m b Rossi Alice 0000000004 "New phone and description"
```

All three modes save the updated contact to the CSV. Mode `t` preserves the existing description, if any. Modes `c` and `b` can add a description to a contact that does not have one. Updated phone numbers must follow the same validation rules as new contacts.

Surname and name identify the contact using exact, case-insensitive matching; they are not renamed by these commands. A missing contact returns status `1` without changing existing contacts.

## Generated files

Files are stored in the **current working directory**, which may differ from the directory containing the script. Run commands from the same directory to use the same phone book. There are no command-line options for changing the filenames.

| File           | Purpose                       | Behavior                                                                                                                                               |
| -------------- | ----------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `NoteBook.csv` | Contact storage.              | Created if missing after arguments pass validation, including for searches. Rewritten on successful additions, modifications, and confirmed deletions. |
| `NoteBook.log` | Operation details and errors. | Created when the first log entry is written; subsequent entries are appended.                                                                          |

### CSV format

The file has no header. Fields are separated by a semicolon followed by a space:

```text
SURNAME; NAME; PHONE_NUMBER; DESCRIPTION
```

The description field is omitted when a contact is added without one. An explicitly supplied empty description is stored as an empty fourth field. For example:

```csv
ROSSI; ALICE; 0000000001; Demo contact
VERDI; BOB; 0000000002
```

When importing into a spreadsheet, choose `;` as the delimiter and treat phone numbers as text to preserve leading zeros. The script writes plain text without CSV quoting or escaping and rejects semicolons and line breaks in contact arguments. Blank lines are ignored when reading the file. Each successful write sorts the contact rows alphabetically.

### Log format

Logged operations include a timestamp, operation name, supplied contact details, and an outcome. Unexpected exceptions during file access or contact operations are recorded with the script arguments and a traceback when logging is available. Argument validation failures print an error to the terminal without writing a log entry. If the log cannot be written after an exception, a further error is printed to standard error.

Both generated files can contain personal information: the log may retain contact details even after a contact is removed from the CSV.
