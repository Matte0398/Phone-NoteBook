# Phone-NoteBook
A Python command-line application for managing a simple contact book.

## Features

- Add contacts
- Modify phone numbers
- Modify contact descriptions
- Remove contacts
- Search contacts

### USAGE
```bash
python MyPhoneNoteBook.py [options] [params]

  options and params:

     - To add a new contact -> '-a|--add [surname] [name] [phone_number] [description(optional)]'
     - To modify a contact:

         - To modify a phone number -> '-m|--mod t [surname] [name] [new_phone_number]'
         - To modify a description -> '-m|--mod c [surname] [name] [new_description]'
         - To modify all the informations -> '-m|--mod b [surname] [name] [new_phone_number] [new_description]'

     - To remove a contact (include the first name for duplicate surnames) -> -r|--rem -r [surname]
     - To search a contact -> '-s|--search -s surname [name]'
```

## Example

```bash
python MyPhoneNoteBook.py --add Rossi Mario 3331234567 "Work contact"
python MyPhoneNoteBook.py --search Rossi Mario
python MyPhoneNoteBook.py -m -c Rossi Mario "Project Manager"
