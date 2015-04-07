#--------------------------------------------------------
# Python script to add header of comments for Doxygen
# it is specially adapted to the SELALIB library.
# It is not suppose to write the documentation but to
# make the process easier...
# To execute : python make_doxygen_doc.py <name_of_the_file>
# Author: Laura S. Mendoza
#--------------------------------------------------------
from sys import argv
import os

def ignore_word(word):
    flag = False
    if (word == ""):
        flag = True
    if (word == "&"):
        flag = True
    if (word == "!"):
        flag = True
    return flag

# file that write the documentation for the functions
# it writes all parameters in between the brackets as IN parameters
# and writes the corresponding comment with the name of the agrument 
def write_doc_for_functions(f, line, last_line, f_new, splitted_line, i):
    if (len(last_line) == 0)|(last_line[:2]!='!>'): # prevents double writing doc
        flag_end_of_arguments = 0
        function_string = \
            "!-------------------------------------------------------------------\n" + \
            "!> @brief <BRIEF_DESCRIPTION>\n" + \
            "!> @details <DETAILED_DESCRIPTION>\n" # header
        f_new.write(function_string)
        #.............. writing arguments:
        i=i+1 # index on word being read, normally we are at function name
        print "     ...Adding doc for function :", splitted_line[i]
        while(flag_end_of_arguments == 0): # flag that notifies if ")" was reached
            i = i+1 #we want to read the next word
            while ((i <= len(splitted_line)-1) and ignore_word(splitted_line[i])):
                # while line is not over and the word is a "feeler" word
                # we continue reading
                i=i+1
            if (i == len(splitted_line)) :
                # if we reached the end of the line but not the end of the document
                # list, we read the next line
                next_line = f.next()
                line = line + next_line # we keep the line to write it at the EOF
                splitted_line = next_line.split()
                i=0
                while (ignore_word(splitted_line[i])):
                    i = i+1
            # we finally got the right index for the argument
            argument = splitted_line[i]
            if(argument[-1] == ")"):
                # if it is the last argument we take the ')' out
                # and activate flag
                argument = argument[:-1]
                flag_end_of_arguments = 1
            if (not ignore_word(argument)):
                function_argument = "!> @param[IN] "+ argument+" <DESCRIPTION>\n"
                f_new.write(function_argument)
    f_new.write(line)

script, filename = argv

print " ================================================="
print "  Adding Doxygen documentation to file %r." % filename
print " ================================================="

print "Opening the file..."
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
        write_doc_for_functions(f, line, last_line, f_new, splitted_line, i)
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

print "Headers of documentation written. Don't forget to fill in the documentation yourself."
f.close()
f_new.close()

#TODO: put it back:
#os.rename(filename+'.tmp', filename)
                    
