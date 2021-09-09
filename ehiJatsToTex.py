### JATSetter
### EHI JATS to TeX
### Copyright (C) 2021
### Shaun Khoo (https://orcid.org/0000-0002-0972-3788), Episteme Health Inc.
### License: GPL v3+
###
### The EHI JATS to TeX contains a couple of functions for converting
### JATS XML to BibTeX files using XSLT.
### transformJatsToTex will use XSLT to transform an XML file to LaTeX or BibTeX
### texify will convert special characters into LaTeX code

from lxml import etree

def texify(text):
    #Define a dictionary of characters that need to be converted to LaTeX code
    texdict = {'&amp;':'\\&','&':'\\&', '%':'\\%', '$':'\\$', '#':'\\#', '_':'\\_',
               '{':'\\{', '}':'\\}', '~':'\\textasciitilde{}',
               '^':'\\textasciicircum{}',

               u'\u03B1':'\\textalpha{}', u'\u03B2':'\\textbeta{}',
               u'\u03B3':'\\textgamma{}', u'\u03B4':'\\textdelta{}',
               u'\u03B5':'\\textepsilon{}', u'\u03B6':'\\textzeta{}',
               u'\u03B7':'\\texteta{}', u'\u03B8':'\\texttheta{}',
               u'\u03B9':'\\textiota{}', u'\u03BA':'\\textkappa{}',
               u'\u03BB':'\\textlambda{}', u'\u03BC':'\\textmugreek{}',
               u'\u03BD':'\\textnu{}', u'\u03BE':'\\textxi{}',
               u'\u03BF':'\\textomikron{}', u'\u03C0':'\\textpi{}',
               u'\u03C1':'\\textrho{}', u'\u03C2':'\\textvarsigma{}',
               u'\u03C3':'\\textsigma{}', u'\u03C4':'\\texttau{}',
               u'\u03C5':'\\textupsilon{}', u'\u03C6':'\\textphi{}',
               u'\u03C7':'\\textchi{}', u'\u03C8':'\\textpsi{}',
               u'\u03C9':'\\textomega{}',
               
               u'\u0391':'\\textAlpha{}', u'\u0392':'\\textBeta{}',
               u'\u0393':'\\textGamma{}', u'\u0394':'\\textDelta{}',
               u'\u0395':'\\textEpsilon{}', u'\u0396':'\\textZeta{}',
               u'\u0397':'\\textEta{}', u'\u0398':'\\textTheta{}',
               u'\u0399':'\\textIota{}', u'\u039A':'\\textKappa{}',
               u'\u039B':'\\textLambda{}', u'\u039C':'\\textMu{}',
               u'\u039D':'\\textNu{}', u'\u039E':'\\textXi{}',
               u'\u039F':'\\textOmikron{}', u'\u03A0':'\\textPi{}',
               u'\u03A1':'\\textRho{}', u'\u03A3':'\\textSigma{}',
               u'\u03A4':'\\textTau{}', u'\u03A5':'\\textUpsilon{}',
               u'\u03A6':'\\textPhi{}', u'\u03A7':'\\textChi{}',
               u'\u03A8':'\\textPsi{}', u'\u03A9':'\\textOmega{}',
               u'\u03F4':'\\straighttheta{}',
        }

    # Deal with the \ character first so that we don't double up
    # on it later!
    text = text.replace('\\', '\\\\')

    # Now go through and replace every character that needs replacing
    for key, value in texdict.items():
        text = text.replace(key, value)
    return(text)

def transformJatsToTex(xmlpath, xslpath, outpath):
    # Open the XSLT file and use it for the transform function
    xsltfile = open(xslpath, mode='r', encoding='utf-8').read()
    xslt_root = etree.XML(xsltfile)
    transform = etree.XSLT(xslt_root)

    # Open the XML file
    xmlfile = open(xmlpath, mode='rb').read()
    parser = etree.XMLParser(remove_blank_text=True)
    xmldoc = etree.XML(xmlfile, parser)

    # Parse the text elements and texify them
    for elem in xmldoc.iter():
        if elem.text != None:
            elem.text = texify(elem.text)
        if elem.tail != None:
            elem.tail = texify(elem.tail)

    # Transform the XML document using the XSLT stylesheet        
    transformed = transform(xmldoc)

    # Output and save the .bib file
    outputstring = str(transformed)
    outputfile = open(outpath, mode='w', encoding='utf-8')
    outputfile.write(outputstring)
    outputfile.close()
