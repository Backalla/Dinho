# Can write in next line now
# But cannot go to next line if line ending is encountered.. Do it..

letters_dict = {' ': 'space',',': 'comma',"'":"single_quote",'"':'double_quote','.':'period'}


import sys
import os
import re

page_width = 18
page_height = 29
# page_height is the number of lines..
letters_gcode_directory = 'my'


def get_letter_lengths():
  letter_lengths = {}
  all_files = [x for x in os.listdir(letters_gcode_directory) if x[-3:]=='ngc']
  for all_file in all_files:
    gcode_file_obj = open(os.path.join(letters_gcode_directory,all_file),'r')
    line = gcode_file_obj.readline()
    letter=all_file[:-4]
    line = gcode_file_obj.readline()
    # print line
    match = re.search(r'\d+\.\d*',line)
    width = float(match.group())
    line = gcode_file_obj.readline()
    match = re.search(r'\d+\.\d*',line)
    height = float(match.group())
    letter_lengths[letter] = (width,height)
  return letter_lengths

def main():
  if len(sys.argv) != 3:
    print "Usage: python generategcode.py [in file] [out file]"
    return

  infile = sys.argv[1]
  outfile = sys.argv[2]
  if not os.path.exists(infile):
    print "Filename %s does not exist." %infile
    return

  letter_lengths = get_letter_lengths()
  # print letter_lengths
  outobj = open(outfile,'wa')
  # inobj = open(infile,'r')
  file_contents = ""
  cur_x = 0
  cur_y = 0
  word_length = 0
  with open(infile,'r') as inobj:
    for line in inobj:
      cur_x=0
      words=line.split()
      for word in words:
        word_length=0
        for letter in word:
          cur_x+=letter_lengths[letter][0]
          word_length+=letter_lengths[letter][0]
        if cur_x>page_width:
          cur_x=word_length
          file_contents+='\n'
        cur_x+=letter_lengths['space'][0]
        file_contents+=word+' '
      file_contents+='\n'  


  cur_x=0
  # for compiling the gcode file
  output_gcode_lines = []
  print file_contents
  for letter in file_contents:
    if letter==' ':
      letter = 'space'
    if letter == '\n':
      cur_x=0
      output_gcode_lines.append("\n\nG00 X0 Y-0.818\nG00 Z0\nG10 P0 L20 X0 Y0 Z0\n\n")
      continue
    # print letter
    letter_obj = open(os.path.join(letters_gcode_directory,letter)+'.ngc','r')
    letter_gcode = letter_obj.read()
    match = re.search(r'%(.*)%',letter_gcode,re.DOTALL)
    letter_gcode = match.group(1)
    letter_gcode_lines = [x for x in letter_gcode.split('\n') if x!='']
    for letter_gcode_line in letter_gcode_lines:
      if 'X' in letter_gcode_line:
        letter_gcode_line_parts = letter_gcode_line.split()
        x_dist = float(letter_gcode_line_parts[letter_gcode_line_parts.index('X')+1])
        x_dist+=cur_x;
        letter_gcode_line_parts[letter_gcode_line_parts.index('X')+1]=str(x_dist)
        output_gcode_lines.append(' '.join(letter_gcode_line_parts))
        continue
      output_gcode_lines.append(letter_gcode_line)
    cur_x += letter_lengths[letter][0]
    output_gcode_lines.append('\n\n')
  for output_gcode_line in output_gcode_lines:
    outobj.write(output_gcode_line)
    outobj.write('\n')











if __name__ == '__main__':
  main()