#--------------------------------------------------------
# Python script to add header of comments for Doxygen
# it is specially adapted to the SELALIB library.
# It is not suppose to write the documentation but to
# make the process easier...
# To execute : python make_doxygen_doc.py <name_of_the_file>
# Author : Laura S. Mendoza
#--------------------------------------------------------
from sys import argv
import os

script, filename = argv

print(" =================================================")
print("  Adding Doxygen documentation to file ", filename)
print(" =================================================")

print("Opening the file...")
f = open(filename, 'r')

#Creating a temporary file which will be the modified file
f_new = open(filename+".tmp", 'w')

# Variable to keep last line info:
last_line=""

for line in f:
    # Getting the first word, which is usually the keyword
    if (len(line.strip()) == 0):     # Testing if line is empty
        first_word = ""
    else:
        i = 0
        first_word = ""
        splitted_line = line.split()
        while (splitted_line[i] == ""):
            i = i+1
        first_word = splitted_line[i]

    # We analyze the first word.........
    # CASE : module
    if (first_word == 'module') :
        if (len(last_line) == 0)|(last_line[:2]!='!>'):
            module_string = "!> @ingroup <DIRECTORY_NAME>\n" + \
                            "!> @author <MODULE_AUTHOR_NAME_AND_AFFILIATION>\n" + \
                            "!> @brief <BRIEF_DESCRIPTION>\n" + \
                            "!> @details <DETAILED_DESCRIPTION>\n"
            f_new.write(module_string)
        f_new.write(line)
    # CASE : function
    elif(first_word == 'function'):
        if (len(last_line) == 0)|(last_line[:2]!='!>'):
            function_string = \
                "!---------------------------------------------------------------------------\n" + \
                "!> @brief <BRIEF_DESCRIPTION>\n" + \
                "!> @details <DETAILED_DESCRIPTION>\n" + \
                "!> @param[<IN or OUT or INOUT>] <PARAM1> <DESCRIPTION>\n" +\
                "!> @param[<IN or OUT or INOUT>] <PARAM2> <DESCRIPTION>\n"
            f_new.write(function_string)
        f_new.write(line)
    # CASE : subroutine
    elif(first_word == 'subroutine'):
        if (len(last_line) == 0)|(last_line[:2]!='!>'):
            function_string = \
                "!---------------------------------------------------------------------------\n" + \
                "!> @brief <BRIEF_DESCRIPTION>\n" + \
                "!> @details <DETAILED_DESCRIPTION>\n" + \
                "!> @param[<IN or OUT or INOUT>] <PARAM1> <DESCRIPTION>\n" +\
                "!> @param[<IN or OUT or INOUT>] <PARAM2> <DESCRIPTION>\n"
            f_new.write(function_string)
        f_new.write(line)
    else :
        f_new.write(line)

    # Updating last line only if non empty
    if (len(line.strip()) != 0):     # Testing if line is empty
        last_line = first_word

print("Headers of documentation written." +\
      " Don't forget to fill in the documentation yourself.")
f.close()
f_new.close()

os.rename(filename+'.tmp', filename)
