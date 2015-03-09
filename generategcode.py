
letters_dict = {' ': 'space',',': 'comma',"'":"single_quote",'"':'double_quote','.':'period','(':'open_round_bracket',
  ')':'close_round_bracket',':':'colon','-':'hyphen',' ':'space'}


import sys
import os
import re

page_width = 18
page_height = 29
# page_height is the number of lines..
letters_gcode_directory = 'NewLetters'


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
  if len(sys.argv) != 2:
    print "Usage: python generategcode.py [in file]"
    return

  infile = sys.argv[1]
  if not os.path.exists(infile):
    print "Filename %s does not exist." %infile
    return
  letter_lengths = get_letter_lengths()
  # print letter_lengths
  # inobj = open(infile,'r')
  file_contents = ""
  cur_x = 0
  cur_y = 0
  wotrd_length = 0
  with open(infile,'r') as inobj:
    for line in inobj:

      cur_x=0
      words=line.split()
      for word in words:
        word_length=0
        for letter in word:
          if letter in letters_dict:
            letter = letters_dict[letter]
          cur_x+=letter_lengths[letter][0]
          word_length+=letter_lengths[letter][0]
        if cur_x>page_width:
          cur_x=word_length
          file_contents+='\n'
        cur_x+=letter_lengths['space'][0]
        file_contents+=word+' '
      file_contents+='\n'

  pages=[]
  cur_x=0
  output_line_num=0
  # for compiling the gcode file
  output_gcode_lines = []
  line_num=0
  for file_lines in file_contents.split('\n'):
    print file_lines
    line_num+=1
    if line_num>28:
      line_num=0
      print '----------------------------'


  for letter in file_contents:
    if letter == '\n':
      cur_x=0
      output_gcode_lines.append("\n\nG00 X0 Y-0.818\nG00 Z0\nG10 P0 L20 X0 Y0 Z0\n\n")
      output_line_num+=1
      if output_line_num>28:
        output_line_num=0
        pages.append(output_gcode_lines)
        output_gcode_lines=[]
      continue
    # print letter
    if letter in letters_dict:
      letter = letters_dict[letter]
    # print letter,
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
  page_num=1
  for page in pages:
    outfile=infile[:-4]+'_'+str(page_num)+'.ngc'
    page_num+=1
    outobj = open(outfile,'wa')
    for output_gcode_line in page:
      outobj.write(output_gcode_line)
      outobj.write('\n')











if __name__ == '__main__':
  main()