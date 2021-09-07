### JATSetter
### EHI Citation Linking
### Copyright (C) 2021
### Shaun Khoo (https://orcid.org/0000-0002-0972-3788), Episteme Health Inc.
### License: GPL v3+
###
### This script will take a JATS XML file containingre the body and a
### second JATS XML file containing the reference list.
### It will then do the crosslinking of in-text references that are made
### using numbered references in square brackets - e.g. [4,5,10-15]
### It will also crosslink references to "Figure #" or "Table #".
### Finally, this script will merge references from a second JATS XML
### file into the final output.

import re

figIDtracker = 0
tableIDtracker = 0

def referencetag(t):
    components = list(t.group())
    toreturn = list()
    stringindex = 0
    current = ''
    for value in components:
        try:
            temp = int(value)
            current = current + value
        except:
            if len(current) > 0:
                toreturn.append(current)
                current = ''
                toreturn.append(value)
            else:
                toreturn.append(value)
    for index, value in enumerate(toreturn):
        try:
            temp = int(value)
            toreturn[index] = '<xref ref-type="bibr" rid="ref' + value + '">' + value + '</xref>'
        except:
            pass
    retstring = ''
    for value in toreturn:
        retstring = retstring + value
    return(retstring)

def figuretag(t):
    figstring = t.group(0)
    components = list(t.group())
    figureID = ''
    for value in components:
        try:
            temp = int(value)
            figureID = figureID + value
        except:
            pass
    return('<xref ref-type="fig" rid="fig' + figureID + '">' + figstring + '</xref>')

def tabletag(t):
    tablestring = t.group(0)
    components = list(t.group())
    tableID = ''
    for value in components:
        try:
            temp = int(value)
            tableID = tableID + value
        except:
            pass
    return('<xref ref-type="table" rid="table' + tableID + '">' + tablestring + '</xref>')

def figIDfixer(t):
    global figIDtracker
    figIDtracker = figIDtracker + 1
    return('<fig id="fig' + str(figIDtracker) + '">')

def tableIDfixer(t):
    global tableIDtracker
    tableIDtracker = tableIDtracker + 1
    return('<table-wrap id="table' + str(tableIDtracker) + '">')

def xreflinking(inputxmlfile, refpath, outputxmlfile):
    global figIDtracker
    global tableIDtracker
    figIDtracker = 0
    tableIDtracker = 0

    jatsfile = open(inputxmlfile, 'r', encoding='utf-8').readlines()

#    re_references = re.compile("\[[\d+,*\-*a-z* *]+\]")
    re_references = re.compile("\[[\d+][\W+\d+]*\]")
    re_figure = re.compile("Figure \d+[\w\-]*")
    re_table = re.compile("Table \d+[\w\-]*")
    re_figID = re.compile('<fig id="[\w\-]+">')
    re_tableID = re.compile('<table-wrap id="[\w\-]+">')

    for index, value in enumerate(jatsfile):
        jatsfile[index] = re.sub(re_references, referencetag, value)

    for index, value in enumerate(jatsfile):
        if '<label>' not in value:
            jatsfile[index] = re.sub(re_figure, figuretag, value)

    for index, value in enumerate(jatsfile):
        if '<label>' not in value:
            jatsfile[index] = re.sub(re_table, tabletag, value)

    for index, value in enumerate(jatsfile):
        jatsfile[index] = re.sub(re_figID, figIDfixer, value)

    for index, value in enumerate(jatsfile):
        jatsfile[index] = re.sub(re_tableID, tableIDfixer, value)

    ## Get the reference list
    reflist = open(refpath, 'r', encoding='utf-8').read()
    reflist = '    ' + reflist[reflist.index("<ref-list>"):reflist.index("</ref-list>")] + '</ref-list>\n'

    ## Stick everything together
    outfile = open(outputxmlfile, 'w', encoding='utf-8')
    superstring = ''
    for i in jatsfile:
        if '</back>' in i:
            superstring = superstring + reflist + '  </back>\n'
        elif '<back />' in i:
            superstring = superstring + '  <back>\n' + reflist + '  </back>\n'
        else:
            superstring = superstring + i
    ## And write the file
    outfile.write(superstring)
    outfile.close()
