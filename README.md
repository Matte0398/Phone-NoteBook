# Phone-NoteBook

A Python command-line application for managing a simple contact book.

## Features

- Add contacts
- Modify phone numbers
- Modify contact descriptions
- Remove contacts
- Search contacts

### USAGE

``` python
python MyPhoneNoteBook.py [options] [params]
```

#### Options and params:

To add a new contact:

``` python
python MyPhoneNoteBook.py -a|--add [surname] [name] [phone_number] [description(optional)]
```

To modify a contact's phone number:

``` python
python MyPhoneNoteBook.py -m|--mod t [surname] [name] [new_phone_number]
```

To modify a contact's description:

``` python
python MyPhoneNoteBook.py -m|--mod c [surname] [name] [new_description]
```

To modify all the informations (the phone number and the description):

``` python
python MyPhoneNoteBook.py -m|--mod b [surname] [name] [new_phone_number] [new_description]
```

To remove a contact (you must include the first name for duplicate surnames):

``` python
python MyPhoneNoteBook.py -r|--rem [surname]
```

To search a contact:

``` python
python MyPhoneNoteBook.py -s|--search surname [name]
```

## Example

``` python
python MyPhoneNoteBook.py --add Rossi Mario 3331234567 "Work contact"
python MyPhoneNoteBook.py --search Rossi Mario
python MyPhoneNoteBook.py -m -c Rossi Mario "Project Manager"
