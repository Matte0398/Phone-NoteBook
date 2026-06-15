# Phone-NoteBook
A Python Script that manages an agenda where you can put some your information, modify them, remove them or search them

### USAGE
```python MyPhoneNoteBook.py [options] [params]```

### Options and params

- To add a new contact: `-a|--add [surname] [name] [phone_number] [description(optional)]`
- To modify a contact: <br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; - To modify a phone number: `-m|--mod t [surname] [name] [new_phone_number]` <br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; - To modify a description: `-m|--mod c [surname] [name] [new_description]` <br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; - To modify all the informations -> `-m|--mod b [surname] [name] [new_phone_number] [new_description]`
- To remove a contact (include the first name for duplicate surnames): `-r|--rem -r [surname]`
- To search a contact: `-s|--search -s surname [name]`
