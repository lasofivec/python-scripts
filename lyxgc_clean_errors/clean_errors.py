#--------------------------------------------------------
# To execute : python clean_errors.py <name_of_the_file>
# Author: Laura S. Mendoza
#--------------------------------------------------------
from sys import argv
import os

script, filename = argv

print " ================================================="
print "  Parsing lyx-gc error file %r." % filename
print " ================================================="

#-------------------------------------------------
print "Opening the file..."
f = open(filename, 'r')
#-------------------------------------------------

#Creating a temporary file which will be the modified file
f_new = open(filename+".tmp", 'w')

# Flags useful for deleting lines
# we could use only one (dontwrite) but I feel that having a Flag makes the code clearer
write_line = True
dontwrite = 0

# Flags for checking dictionnary part (last section of file)
in_dict = False

# List of all "mathematical" words that are not in the lyx-gc dictionnary
# but are indeed correct
math_words = ['advection',\
              'BSL',
              'Cadarache',
              'CEA',
              'Eulerian',
              'GKW',
              'INRIA',
              'IPP',
              'ITER',
              'ITG',
              'IgA',
              'Jacobian',
              'Lagrangian',
              'NURBS',
              'Semi',
              'Vlasov',
              'anisotropy',
              'annulus',
              'borealis',
              'collisional', 'collisionless',
              'discretization', 'discretized', 'discretize',
              'equilibria',
              'hellicaly',
              'linearized',
              'multi',
              'plasmas',
              'poloidal', 'toroidal',
              'positivity',
              'tokamak']

# List of some authors that might come up
some_authors = ['Abiteboul',\
                'Besse',
                'Brizard',
                'Cheng',
                'Grandgirard',
                'Hahm',
                'Knorr',
                'Ratnani',
                'Sonnendrucker'
                'Sarazin']
                


# Parsing file -------------------------------------------------------------
for line in f:
    if (len(line.strip()) != 0):     # Testing if line is not empty
        i = 0
        first_word = ""
        splitted_line = line.split()
        while (splitted_line[i] == ""):
            i = i+1
        first_word = splitted_line[i]

        # Lyx-gc general corrector:
        if first_word == '*' and len(splitted_line) > 6:
            keyword1 = splitted_line[i+3]
            keyword2 = splitted_line[i+4]
            keyword3 = splitted_line[i+5]
            keyword4 = splitted_line[i+6]
            
            if (keyword1 == 'Captial')\
               and (keyword2 == 'without') and (keyword4 == 'fullstop;'):
                write_line = False
                dontwrite = 3
            elif keyword1 == 'Saace' and keyword2 == 'before' and keyword3 == '\label;':
                write_line = False
                dontwrite = 3

        # LanguageTool warnings:
        if len(splitted_line) > 6 and splitted_line[i+5] == 'Rule':

            if splitted_line[i+7] == 'CURRENCY[1]':
                write_line=False
                dontwrite = 5

        # Checking if we have reached the dictionnary part:
        if len(splitted_line) > 3 and first_word == "----" and splitted_line[i+1] == 'Spelling':
            in_dict = True

        if in_dict :

            # all dictionnary words are followed by ':', so we take it out
            first_word = first_word[:-1]
            if first_word in some_authors or first_word in math_words :
                write_line = False
                dontwrite = 1
        
        
    if write_line and dontwrite == 0:
        f_new.write(line)
    elif dontwrite > 0 :
        dontwrite = dontwrite - 1
        if dontwrite == 0:
            write_line = True


print "Succes: File cleaned!"
f.close()
f_new.close()

os.rename(filename+'.tmp', filename)
                    
