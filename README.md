# txtToEnex
Python script to convert a list of items in a .txt file to Enex format, that can be imported in Apple Notes.
The .txt file must have the following format:

```
# Title for 1st note
A section
- an item
- another item
- and a last one

The second section
- which have
- several
- items
- too

# 2nd note title
And again, a section
- with
- some
- items
```

## Usage
```
usage: txtToEnex [-h] [--bullets] input [output]

positional arguments:
  input       <input file>
  output      <output file>

options:
  -h, --help  show this help message and exit
  --bullets   outputs bulleted lists instead of checklists
```

## Screenshots
Enex files can be imported to Apple Note. The following screenshots show the result on iPhone SE 2.
![imported notes](/example/screenshots/imported_notes.png?raw=true "Two notes were imported")
![first note checklist](/example/screenshots/first_note_checklist.png?raw=true "First note, checklist format (default)")
![second note checklist](/example/screenshots/second_note_checklist.png?raw=true "Second note, checklist format (default)")
![first note bullets](/example/screenshots/first_note_bullets.png?raw=true "First note, bullets format (using --bullets option)")

