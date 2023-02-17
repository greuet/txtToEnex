#!/usr/bin/env python3
import os, sys, pathlib, argparse
from argparse import RawTextHelpFormatter

# parse arguments
parser = argparse.ArgumentParser (
    prog = 'txtToEnex',
    description = 'Convert a list of items in a .txt file to enex format, to be imported in Apple Notes.\nThe .txt file must have the following format:\n'
    + '  # 1st note title\n'
    + '  A section title\n'
    + '  - First item\n'
    + '  - Second item\n\n'
    + '  Another section title\n'
    + '  - First item\n'
    + '  - Second item\n'
    + '  - Third item\n\n'
    + '  # 2nd note title\n'
    + '  ...\n\n'
    + 'By default, items are put in a checklist. Using --bullets option put them in a bulleted list instead.',
    formatter_class = RawTextHelpFormatter)
parser.add_argument ('input', type = argparse.FileType ('r'),
                     help = '<input file>')
parser.add_argument ('output', type = pathlib.Path, nargs = '?',
                     help = '<output file>')
parser.add_argument ('--bullets', action = 'store_true', help = 'outputs bulleted lists instead of checklists')

args = parser.parse_args()
infile = args.input
# if no output file given, append .enex to input file name as default
outfile_path = args.output
if (outfile_path == None):
    outfile_path = pathlib.Path (infile.name + '.enex')

bullets = args.bullets
checklist = not bullets

# file exists ? ask if overwrite : create it
if (os.path.isfile (outfile_path)):
    print ('Output file ' + outfile_path.as_posix() + ' already exists. Overwrite ? [y/N]')
    res = input ()
    if ((res == 'y') or (res == 'Y')):
        0
    else:
        print ('Exiting')
        exit (1)

print  ('Writing output in ' + outfile_path.as_posix() + '...', end = '')
outfile = open (outfile_path, 'w')

# flags for opened markups
div_open = 0
note_open = 0
ul_open = 0

print ('<?xml version="1.0" encoding="UTF-8"?>', file=outfile)
print ('<!DOCTYPE note-export>', file=outfile)
print ('<note-export>', file=outfile)

for line in infile:
    if (line[0] == '#'):
        if (note_open == 0):
            note_open = 1
            titre = line.rstrip()[2:]
            print ('  <Note>', file=outfile)
            print ('    <Title>' + titre + '</Title>', file=outfile)
            print ('    <Content>', file=outfile)
            print ('      <![CDATA[<?xml version="1.0" encoding="UTF-8"?>', file=outfile)
            print ('      <!DOCTYPE en-note SYSTEM \'http://xml.evernote.com/pub/enml2.dtd\'>', file=outfile)
            print ('      <en-note>', file=outfile)
        else:
            titre = line.rstrip()[2:]
            div_open = 0

            if (bullets):
                if (ul_open):
                    ul_open = 0
                    print ('          </ul>', file=outfile)

            print ('        </div>', file=outfile)
            print ('      </en-note>]]>', file=outfile)
            print ('    </Content>', file=outfile)
            print ('  </Note>', file=outfile)
            print ('', file=outfile)
            print ('  <Note>', file=outfile)
            print ('    <Title>' + titre + '</Title>', file=outfile)
            print ('    <Content>', file=outfile)
            print ('      <![CDATA[<?xml version="1.0" encoding="UTF-8"?>', file=outfile)
            print ('      <!DOCTYPE en-note SYSTEM \'http://xml.evernote.com/pub/enml2.dtd\'>', file=outfile)
            print ('      <en-note>', file=outfile)

    elif (line[0] == '-'):
        item = line.rstrip()[2:]
        if (bullets):
            if (ul_open == 0):
                ul_open = 1
                print ('          <ul>', file=outfile)
            print ('            <li>' + item + '</li>', file=outfile)
        elif (checklist):
            print ('          <div><en-todo/>' + item + '</div>', file=outfile)

    else:
        if (div_open == 0):
            div_open = 1
            head = line.rstrip()
            print ('        <div>', file=outfile)
            print ('          <span style="font-size: 17pt; font-weight: bold;">' + head + '</span>', file=outfile)
        elif (line[0] != '' and line[0] != os.linesep):
            if (bullets):
                ul_open = 0
                print ('          </ul>', file=outfile)
            print ('        </div>', file=outfile)
            print ('', file=outfile)
            print ('        <br/>', file=outfile)
            print ('', file=outfile)
            head = line.rstrip()
            print ('        <div>', file=outfile)
            print ('          <span style="font-size: 17pt; font-weight: bold;">' + head + '</span>', file=outfile)

# end of file
if (bullets):
    if (ul_open):
        print ('          </ul>', file=outfile)
print ('        </div>', file=outfile)
print ('      </en-note>]]>', file=outfile)
print ('    </Content>', file=outfile)
print ('  </Note>', file=outfile)
print ('</note-export>', file=outfile)

infile.close ()
outfile.close ()

print (' done!')
exit (0)
