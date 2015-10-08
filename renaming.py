#--------------------------------------------------------
# Python script that takes a string, normally the name
# of a SeLaLib module, and gives a new string that
# respects the library conventions, typically in the
# form "sll_m_<module_name>".
# To execute : renaming.py (shows some examples)
# or import it and call "renaming(<string>)"
# Author: Laura S. Mendoza
#--------------------------------------------------------

def keywords():
    """ Returns an array of keywords, for the moment only SeLaLib's module
    keywords. In the future it could take a parameter in order to change
    the types of keywords (ie. simulations, functions, subroutines, ...) """

    list_key = []
    list_key+= ["sll"]
    list_key+= ["module"]
    list_key+= ["mod"]

    return list_key


def convention():
    """ Returns a string, for the moment common string to SeLaLib's modules
    In the future it could take a parameter in order to adapt it to other
    types (ie. simulations, functions, subroutines, ...) """

    return "sll_m"


def renaming(original_name):
    """ Changes a string to make it respects SeLaLib naming convention

    Args :
       original_name (str) : original module name. """

    list_key   = keywords()
    splitted   = original_name.split("_")
    modulename = convention()

    for word in splitted :
        if not word in list_key :
            modulename += "_"
            modulename += word

    return modulename


def main():
    print "sll_module_modname      -->    " + renaming("sll_module_modname")
    print "modname                 -->    " + renaming("modname")
    print "modname_module          -->    " + renaming("modname_module")
    print "specific_modname_1d_mod -->    " + renaming("specific_modname_1d_mod")



if __name__ == "__main__":
        main()
