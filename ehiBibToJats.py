### JATSetter
### EHI Bib to JATS
### Copyright (C) 2021
### Shaun Khoo (https://orcid.org/0000-0002-0972-3788), Episteme Health Inc.
### License: GPL v3+
###
### This script will take a .bib file and return JATS XML-formatted references.
### Preconditions: bib file
### Each field must be on its own line
### Reference IDs must be numbered sequentially, starting at 1 if the xref-linking script is to be used
### Each bib entry must terminate with the curly braces '}' on a separate line
### Only organisational authors should be contained within curly braces, e.g. {World Health Organization}
### Also supports some custom fields that are not commonly used:
### - PMIC, PMCID, OCLC, ISBN and ISSN for article identifiers
### - ArchiveURL for a web.archive.org URL (useful for citing websites that do not have PIDs and preservation plans)

from xml.etree.ElementTree import Element, SubElement, tostring
import xml.dom.minidom
import re, datetime, dateutil.parser

def convertbib(bibfilepath, outputfilepath):
    '''
    convertbib takes two arguments:
    bibfilepath, which must be a .bib file
    outputfilepath, which must be an .xml file

    convertbib will then read the data from the bib file and transfer it to arrays to represent
    the data within python.

    The data will then be iterated over and transferred to an XML element tree.

    The XML element tree will then be written to the outputfile.

    Preconditions: The .bib file must have only one reference attribute per line.
    Reference attributes must not break across lines.
    '''
    ### Start by opening the .bib file
    bibfile = open(bibfilepath, 'r', encoding='utf-8').readlines()

    ### Create the root XML element
    reflist = Element('ref-list')

    ### Set up lists for bibliographic fields
    RefID = list()
    Type = list()
    Authors = list()
    Editors = list()
    Translators = list()
    Edition = list()
    Title = list()
    Source = list()
    Series = list()
    Day = list()
    Month = list()
    Year = list()
    Volume = list()
    Issue = list()
    Pages = list()
    Publisher = list()
    PublisherLocation = list()
    DOI = list()
    PMID = list()
    PMCID = list()
    OCLC = list()
    ISBN = list()
    ISSN = list()
    ArchiveURL = list()
    URL = list()
    LastChecked = list()
    
    ### The datavars variable holds the names of all the data variables.
    ### It will be used to loop over the arrays at the end of each subject
    ### and even out any length differences
    datavars = list(['RefID',
    'Type',
    'Authors',
    'Editors',
    'Translators',
    'Edition',
    'Title',
    'Source',
    'Series',
    'Day',
    'Month',
    'Year',
    'Volume',
    'Issue',
    'Pages',
    'Publisher',
    'PublisherLocation',
    'DOI',
    'PMID',
    'PMCID',
    'OCLC',
    'ISBN',
    'ISSN',
    'ArchiveURL',
    'URL',
    'LastChecked'])

    ### Iterate over the bibfile and collect the bibliographic information
    for line in bibfile:
        # Begin by checking for the header
        # Is it a journal article?
        if '@article' in line.lower():
            Type.append('journal')
            # Get the RefID by splitting off the '{' and ','
            RefID.append(line.split('{')[1].split(',')[0])

        # Is it a preprint?
        if '@preprint' in line.lower():
            Type.append('preprint')
            # Get the RefID by splitting off the '{' and ','
            RefID.append(line.split('{')[1].split(',')[0])
            
        # Is it a book?
        elif '@book' in line.lower():
            Type.append('book')
            # Get the RefID by splitting off the '{' and ','
            RefID.append(line.split('{')[1].split(',')[0])

        # Is it a chapter?
        elif '@inbook' in line.lower() or '@incollection' in line.lower():
            Type.append('chapter')
            # Get the RefID by splitting off the '{' and ','
            RefID.append(line.split('{')[1].split(',')[0])

        # Is it a conference?
        # Use 'confproc' because that's what is used by eLife and SciElo.
        # 
        elif '@inproceedings' in line.lower() or '@conference' in line.lower():
            Type.append('confproc')
            # Get the RefID by splitting off the '{' and ','
            RefID.append(line.split('{')[1].split(',')[0])

        # Is it a webpage?
        elif '@webpage' in line.lower():
            Type.append('webpage')
            # Get the RefID by splitting off the '{' and ','
            RefID.append(line.split('{')[1].split(',')[0])

        # Is it misc?
        elif '@misc' in line.lower():
            Type.append('misc')
            # Get the RefID by splitting off the '{' and ','
            RefID.append(line.split('{')[1].split(',')[0])

        # If it is not the reference header, check whether it is data.
        elif '=' in line:
            key = line.split('=')[0].lower()
            data = line.split('=')[1]

            # Get the contents of the curly braces
            startindex = re.search('{', data).start() + 1
            closer = re.finditer('}', data)
            *_, last = closer
            endindex = last.start()
            data1 = detexify(data[startindex:endindex])

            # Identify what the data key is and append the data to the list
            if 'author' in key:
                 Authors.append(data1)

            elif 'editor' in key:
                Editors.append(data1)

            elif 'translator' in key:
                Translators.append(data1)

            elif 'edition' in key:
                Edition.append(data1)
                
            elif 'booktitle' in key:
                Source.append(data1)
                
            elif 'title' in key:
                if 'chapter' in Type[-1] or 'book' in Type[-1]:
                    Source.append(data1)
                else:                    
                    Title.append(data1)

            elif 'chapter' in key:
                Title.append(data1)

            elif 'journal' in key:
                Source.append(data1)

            elif 'series' in key:
                Series.append(data1)

            elif 'day' in key:
                Day.append(data1)

            elif 'month' in key:
                Month.append(data1)

            elif 'year' in key:
                Year.append(data1)

            elif 'volume' in key:
                Volume.append(data1)

            elif 'number' in key:
                Issue.append(data1)

            elif 'page' in key:
                Pages.append(data1)

            elif 'publisher' in key:
                Publisher.append(data1)

            elif 'address' in key:
                PublisherLocation.append(data1)

            elif 'doi' in key:
                DOI.append(data1)

            elif 'pmid' in key:
                PMID.append(data1)

            elif 'pmcid' in key:
                PMCID.append(data1)

            elif 'oclc' in key:
                OCLC.append(data1)

            elif 'isbn' in key:
                ISBN.append(data1)

            elif 'issn' in key:
                ISSN.append(data1)

            elif 'archiveurl' in key:
                ArchiveURL.append(data1)

            elif 'url' in key:
                URL.append(data1)

            elif 'lastchecked' in key:
                LastChecked.append(data1)

        # Go through all the data variables and fill in any empty ones
        elif '}' in line:
            for v in datavars:
                while len(eval(v)) < len(RefID):
                    eval(v).append(None)

    ### Start adding sub-elements
    for index, value in enumerate(RefID):
        ref = SubElement(reflist, 'ref')
        ref.set('id', 'ref' + value)
        label = SubElement(ref, 'label')
        label.text = str(index + 1)
        elementcitation = SubElement(ref, 'element-citation')
        elementcitation.set('publication-type', Type[index])

        # Edition and issue number
        if Edition[index] != None:
            edn = SubElement(elementcitation, 'edition')
            edn.text = Edition[index]

        if Issue[index] != None:
            iss = SubElement(elementcitation, 'issue')
            iss.text = Issue[index]

        # Page range. This will extract the first and last page if applicable.
        if Pages[index] != None:
            if '-' in Pages[index]:
                firstp = Pages[index].split('-')[0]
                lastp = Pages[index].split('-')[1]
                if len(lastp) < len(firstp):
                    tomerge = len(firstp) - len(lastp)
                    lastp = str(firstp[0:tomerge] + lastp)
                fpage = SubElement(elementcitation, 'fpage')
                fpage.text = firstp
                lpage = SubElement(elementcitation, 'lpage')
                lpage.text = lastp
                pagerange = SubElement(elementcitation, 'page-range')
                pagerange.text = Pages[index]
            else:
                pagerange = SubElement(elementcitation, 'page-range')
                pagerange.text = Pages[index]

        # Volume number
        if Volume[index] != None:
            vol = SubElement(elementcitation, 'volume')
            vol.text = Volume[index]

        # URL
        if URL[index] != None:
            uri = SubElement(elementcitation, 'uri')
            uri.text = URL[index]

        # Archive URL
        if ArchiveURL[index] != None:
            archivalurl = SubElement(elementcitation, 'uri')
            archivalurl.text = ArchiveURL[index]
            archivalurl.set('specific-use', 'archived')

        # Book publisher info
        if 'book' in Type[index] or 'chapter' in Type[index]:
            if PublisherLocation[index] != None:
                publocation = SubElement(elementcitation, 'publisher-loc')
                publocation.text = PublisherLocation[index]
            if Publisher[index] != None:
                pub = SubElement(elementcitation, 'publisher-name')
                pub.text = Publisher[index]

        # Date information
        if Year[index] != None:
            yr = SubElement(elementcitation, 'year')
            yr.text = Year[index]
            isodate = Year[index]
            if Month[index] != None and Day[index] != None:
                isodate = isodate + '-' + numericmonth(Month[index]) + '-' + numericday(Day[index])
            elif Month[index] != None:
                isodate = isodate + '-' + numericmonth(Month[index])
            yr.set('iso-8601-date', isodate)
                
        if Month[index] != None:
            mth = SubElement(elementcitation, 'month')
            mth.text = Month[index]

        if Day[index] != None:
            dy = SubElement(elementcitation, 'day')
            dy.text = Day[index]

        if LastChecked[index] != None:
            citedate = SubElement(elementcitation, 'date-in-citation')
            citedate.text = LastChecked[index]
            citedate.set('iso-8601-date', dateutil.parser.parse(LastChecked[index], fuzzy=True).date().isoformat())

        # Identifiers
        if DOI[index] != None:
            id_doi = SubElement(elementcitation, 'pub-id')
            id_doi.set('pub-id-type', 'doi')
            id_doi.text = DOI[index]

        if PMID[index] != None:
            id_pmid = SubElement(elementcitation, 'pub-id')
            id_pmid.set('pub-id-type', 'pmid')
            id_pmid.text = PMID[index]

        if PMCID[index] != None:
            id_pmcid = SubElement(elementcitation, 'pub-id')
            id_pmcid.set('pub-id-type', 'pmcid')
            id_pmcid.text = PMCID[index]

        # OCLC numbers are not a listed pub-id-type in JATS 1.2 Publishing (https://jats.nlm.nih.gov/publishing/tag-library/1.2/attribute/pub-id-type.html)
        # Therefore, use pub-id-type of 'other' and set the 'assigning-authority' to 'worldcat'
        if OCLC[index] != None:
            id_worldcat = SubElement(elementcitation, 'pub-id')
            id_worldcat.set('pub-id-type', 'other')
            id_worldcat.set('assigning-authority', 'worldcat')
            id_worldcat.text = OCLC[index]

        if ISBN[index] != None:
            id_isbn = SubElement(elementcitation, 'pub-id')
            id_isbn.set('pub-id-type', 'isbn')
            id_isbn.text = ISBN[index]

        # ISSNs are not a listed pub-id-type in JATS 1.2 Publishing (https://jats.nlm.nih.gov/publishing/tag-library/1.2/attribute/pub-id-type.html)
        # Therefore, use pub-id-type of 'other' and set the 'assigning-authority' to 'issn'
        if ISSN[index] != None:
            id_issn = SubElement(elementcitation, 'pub-id')
            id_issn.set('pub-id-type', 'other')
            id_issn.set('assigning-authority', 'issn')
            id_issn.text = ISSN[index]

        # Do the author list
        if Authors[index] != None:
            persongroup = SubElement(elementcitation, 'person-group')
            persongroup.set('person-group-type','author')
            names = re.compile("\s+and\s+").split(Authors[index])
            
            for ppl in names:
                if ',' in ppl:
                    name = SubElement(persongroup, 'name')
                    sur = re.compile(",\s*").split(ppl)[0]
                    given = re.compile(",\s*").split(ppl)[1]
                    surname = SubElement(name, 'surname')
                    surname.text = sur
                    givenname = SubElement(name, 'given-names')
                    givenname.text = given
                elif '{' in ppl:
                    collab = SubElement(persongroup, 'collab')
                    orgname = SubElement(collab, 'named-content')
                    orgname.set('content-type', 'name')
                    orgname.text = ppl[1:-1]
                elif 'organisation' in ppl.lower() or 'organization' in ppl.lower() or 'association' in ppl.lower() or 'council' in ppl.lower() or 'committee' in ppl.lower() or 'institute' in ppl.lower():
                    collab = SubElement(persongroup, 'collab')
                    orgname = SubElement(collab, 'named-content')
                    orgname.set('content-type', 'name')
                    orgname.text = ppl
                elif len(ppl.split(' ')) == 1:
                    name = SubElement(persongroup, 'string-name')
                    name.text = ppl
                elif len(ppl.split(' ' )) > 1:
                    name = SubElement(persongroup, 'name')
                    surname = SubElement(name, 'surname')
                    surname.text = ppl.split(' ')[-1]
                    givenname = SubElement(name, 'given-names')
                    givenname.text = ' '.join(ppl.split(' ')[0:-1])

        # Do the editors
        if Editors[index] != None:
            persongroup = SubElement(elementcitation, 'person-group')
            persongroup.set('person-group-type', 'editor')
            names = re.compile("\s+and\s+").split(Editors[index])
            
            for ppl in names:
                if ',' in ppl:
                    name = SubElement(persongroup, 'name')
                    sur = re.compile(",\s*").split(ppl)[0]
                    given = re.compile(",\s*").split(ppl)[1]
                    surname = SubElement(name, 'surname')
                    surname.text = sur
                    givenname = SubElement(name, 'given-names')
                    givenname.text = given
                elif '{' in ppl:
                    collab = SubElement(persongroup, 'collab')
                    orgname = SubElement(collab, 'named-content')
                    orgname.set('content-type', 'name')
                    orgname.text = ppl[1:-1]
                elif 'organisation' in ppl.lower() or 'organization' in ppl.lower() or 'association' in ppl.lower() or 'council' in ppl.lower() or 'committee' in ppl.lower():
                    collab = SubElement(persongroup, 'collab')
                    orgname = SubElement(collab, 'named-content')
                    orgname.set('content-type', 'name')
                    orgname.text = ppl
                elif len(ppl.split(' ')) == 1:
                    name = SubElement(persongroup, 'string-name')
                    name.text = ppl
                elif len(ppl.split(' ' )) > 1:
                    name = SubElement(persongroup, 'name')
                    surname = SubElement(name, 'surname')
                    surname.text = ppl.split(' ')[-1]
                    givenname = SubElement(name, 'given-names')
                    givenname.text = ' '.join(ppl.split(' ')[0:-1])

        # Do the translators
        if Translators[index] != None:
            persongroup = SubElement(elementcitation, 'person-group')
            persongroup.set('person-group-type', 'translator')
            names = re.compile("\s+and\s+").split(Translators[index])
            
            for ppl in names:
                if ',' in ppl:
                    name = SubElement(persongroup, 'name')
                    sur = re.compile(",\s*").split(ppl)[0]
                    given = re.compile(",\s*").split(ppl)[1]
                    surname = SubElement(name, 'surname')
                    surname.text = sur
                    givenname = SubElement(name, 'given-names')
                    givenname.text = given
                elif '{' in ppl:
                    collab = SubElement(persongroup, 'collab')
                    orgname = SubElement(collab, 'named-content')
                    orgname.set('content-type', 'name')
                    orgname.text = ppl[1:-1]
                elif 'organisation' in ppl.lower() or 'organization' in ppl.lower() or 'association' in ppl.lower() or 'council' in ppl.lower() or 'committee' in ppl.lower():
                    collab = SubElement(persongroup, 'collab')
                    orgname = SubElement(collab, 'named-content')
                    orgname.set('content-type', 'name')
                    orgname.text = ppl
                elif len(ppl.split(' ')) == 1:
                    name = SubElement(persongroup, 'string-name')
                    name.text = ppl
                elif len(ppl.split(' ' )) > 1:
                    name = SubElement(persongroup, 'name')
                    surname = SubElement(name, 'surname')
                    surname.text = ppl.split(' ')[-1]
                    givenname = SubElement(name, 'given-names')
                    givenname.text = ' '.join(ppl.split(' ')[0:-1])

        # Source information
        if 'paper' in Type[index] and Source[index] != None:
            confname = SubElement(elementcitation, 'conf-name')
            confname.text = Source[index]
            
            if PublisherLocation[index] != None:
                conflocation = SubElement(elementcitation, 'conf-loc')
                conflocation.text = PublisherLocation[index]
        elif Source[index] != None:
            src = SubElement(elementcitation, 'source')
            src.text = Source[index]

        if Series[index] != None:
            srs = SubElement(elementcitation, 'series')
            srs.text = Series[index]

        if 'chapter' in Type[index] and Title[index] != None:
            chaptertitle = SubElement(elementcitation, 'chapter-title')
            chaptertitle.text = Title[index]
        elif Title[index] != None:
            articletitle = SubElement(elementcitation, 'article-title')
            articletitle.text = Title[index]            
                    
    ### Format the XML string nicely so that it matches
    refliststring = xml.dom.minidom.parseString(tostring(reflist))
    reflistformatted = refliststring.toprettyxml(indent="  ")
    reflines = reflistformatted.splitlines()
    refliststring = ''
    for index, line in enumerate(reflines[1:]):
        reflines[index] = '  ' + line + '\n'
        refliststring = refliststring + reflines[index]

    ### Write the XML to a file
    outputfile = open(outputfilepath, 'w', encoding='utf-8')
    outputfile.write(refliststring)
    outputfile.close()

def numericmonth(month):
    if 'jan' in month.lower():
        return('01')
    elif 'feb' in month.lower():
        return('02')
    elif 'mar' in month.lower():
        return('03')
    elif 'apr' in month.lower():
        return('04')
    elif 'may' in month.lower():
        return('05')
    elif 'jun' in month.lower():
        return('06')
    elif 'jul' in month.lower():
        return('07')
    elif 'aug' in month.lower():
        return('08')
    elif 'sep' in month.lower():
        return('09')
    elif 'oct' in month.lower():
        return('10')
    elif 'nov' in month.lower():
        return('11')
    elif 'dec' in month.lower():
        return('12')
    elif len(month) < 2:
        return('0' + month)
    else:
        return(month)

def numericday(day):
    startday = day.split('-')
    if len(startday[0]) < 2:
        return('0' + startday[0])
    elif len(startday[0]) == 2:
        return(startday[0])

def detexify(string):
    #Define a dictionary of characters that need to be converted from LaTeX code
    detexifydict = {'\\&':'&', '\\%':'%', '\\$':'$', '\\#':'#', '\\_':'_',
               '\\{':'{', '\\}':'}', '\\textasciitilde{}':'~',
               '\\textasciicircum{}':'^',

               '\\textalpha{}':u'\u03B1', '\\textbeta{}':u'\u03B2',
               '\\textgamma{}':u'\u03B3', '\\textdelta{}':u'\u03B4',
               '\\textepsilon{}':u'\u03B5', '\\textzeta{}':u'\u03B6',
               '\\texteta{}':u'\u03B7', '\\texttheta{}':u'\u03B8',
               '\\textiota{}':u'\u03B9', '\\textkappa{}':u'\u03BA',
               '\\textlambda{}':u'\u03BB', '\\textmugreek{}':u'\u03BC',
               '\\textnu{}':u'\u03BD', '\\textxi{}':u'\u03BE',
               '\\textomikron{}':u'\u03BF', '\\textpi{}':u'\u03C0',
               '\\textrho{}':u'\u03C1', '\\textvarsigma{}':u'\u03C2',
               '\\textsigma{}':u'\u03C3', '\\texttau{}':u'\u03C4',
               '\\textupsilon{}':u'\u03C5', '\\textphi{}':u'\u03C6',
               '\\textchi{}':u'\u03C7', '\\textpsi{}':u'\u03C8',
               '\\textomega{}':u'\u03C9',
               
               '\\textAlpha{}':u'\u0391', '\\textBeta{}':u'\u0392',
               '\\textGamma{}':u'\u0393', '\\textDelta{}':u'\u0394',
               '\\textEpsilon{}':u'\u0395', '\\textZeta{}':u'\u0396',
               '\\textEta{}':u'\u0397', '\\textTheta{}':u'\u0398',
               '\\textIota{}':u'\u0399', '\\textKappa{}':u'\u039A',
               '\\textLambda{}':u'\u039B', '\\textMu{}':u'\u039C',
               '\\textNu{}':u'\u039D', '\\textXi{}':u'\u039E',
               '\\textOmikron{}':u'\u039F', '\\textPi{}':u'\u03A0',
               '\\textRho{}':u'\u03A1', '\\textSigma{}':u'\u03A3',
               '\\textTau{}':u'\u03A4', '\\textUpsilon{}':u'\u03A5',
               '\\textPhi{}':u'\u03A6', '\\textChi{}':u'\u03A7',
               '\\textPsi{}':u'\u03A8', '\\textOmega{}':u'\u03A9',
               '\\straighttheta{}':u'\u03F4',
        }

    # Go through and replace every character that needs replacing
    for key, value in detexifydict.items():
        string = string.replace(key, value)

    # Deal with the \ character last
    string = string.replace('\\\\', '\\')

    return(string)
