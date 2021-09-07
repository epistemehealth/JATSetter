### This is part of JATSetter
### Copyright (C) 2021 Shaun Khoo, Episteme Health Inc.
### License: GPL v3+

import requests
import json

from tkinter import *

def getFromAPI(APIToken, journalurl, locale, submissionid, outputfile):

    ## Make the first request to retrieve the paper ID
    makerequest = journalurl + '/api/v1/submissions/' + str(submissionid) + '?apiToken=' + APIToken
    metadata = requests.get(makerequest)

    ## Transform the JSON response into a python dictionary
    jsondata = json.dumps(metadata.json())
    jsondata = json.loads(jsondata)

    ## Get the publication ID so we can retrieve the article metadata
    pubid = jsondata["publications"][0]["id"]

    ## Get the submission date
    submissiondate = jsondata["dateSubmitted"]

    ## Make the request for the article metadata
    makerequest2 = journalurl + '/api/v1/submissions/' + str(submissionid) + '/publications/' + str(pubid) + '?apiToken=' + APIToken
    metadata = requests.get(makerequest2)

    ## Transform the JSON reponse into a python dictionary
    jsondata = json.dumps(metadata.json())
    jsondata = json.loads(jsondata)

    ## Start extracting article metadata
    canonicalurl = jsondata["_href"]
    issueid = jsondata["issueId"]
    sectionid = jsondata["sectionId"]
    title = jsondata["title"][locale]
    publishdate = jsondata["datePublished"]
    doi = jsondata["pub-id::doi"]
    abstract = jsondata["abstract"][locale][3:-4]
    copyrightholder = jsondata["copyrightHolder"][locale]
    copyrightyear = jsondata["copyrightYear"]
    licenseurl = jsondata["licenseUrl"]
    pages = jsondata["pages"]
    
    keywords = list()
    for i in jsondata["keywords"][locale]:
        keywords.append(i)

    disciplines = list()
    for i in jsondata["disciplines"][locale]:
        disciplines.append(i)

    affiliations = list()
    for i in jsondata["authors"]:
        if i["affiliation"][locale] not in affiliations:
            affiliations.append(i["affiliation"][locale])
    
    authorlist = list()
    authorlist.append('authors = [\n')
    
    for i in jsondata["authors"]:
        affils = ''
        authstring = '{'
        if len(i["familyName"][locale]) > 0:
            authstring = authstring + 'surname = "' + i["familyName"][locale] + '", '
        if len(i["givenName"][locale]) > 0:
            authstring = authstring + 'given_name = "' + i["givenName"][locale] + '", '
        authstring = authstring + 'affiliations = [""], '
        authstring = authstring + 'funding = [""], '
        if len(i["orcid"]) > 0:
            authstring = authstring + 'ORCID = "' + i["orcid"][-19:] + '", '
##        if len(i["email"]) > 0:
##            authstring = authstring + 'email = "' + i["email"] + '", '
        if i["id"] == jsondata["primaryContactId"]:
            authstring = authstring = 'corresp = "' + i["email"] + '", '
        else:
            authstring = authstring + 'corresp = "no", '
        authstring = authstring + 'equalcontrib = "no", '
        authstring = authstring + 'deceased = "no"},\n'
        authorlist.append('  ' + authstring)

    authorlist.append(']')

    reflist = list()
    for i in jsondata["citations"]:
        reflist.append(i)

    galleytypes = list()
    galleyfilenames = list()
    galleyids = list()
    ## Try to get galley information
    for i in jsondata["galleys"]:
        galleytypes.append(i["label"])
        galleyfilenames.append(i["file"]["name"][locale])
        galleyids.append(i["id"])        

    ### Get the volume number and article type if available
    makerequest3 = journalurl + '/api/v1/issues/' + str(issueid) + '?apiToken=' + APIToken
    issuemetadata = requests.get(makerequest3)
    issuedata = json.dumps(issuemetadata.json())
    issuedata = json.loads(issuedata)

    ## Extract issue metadata
    volume = issuedata["volume"]
    issuenumber = issuedata["number"]
    ## Try to get the section name
    sectionname = ''
    sectionweight = ''
    for i in issuedata["sections"]:
        if sectionid == i["id"]:
            sectionname = i["title"][locale]
            sectionweight = i["seq"]
    
    ### Begin building the TOML Markdown file
    ## Begin the TOML header
    toml = '+++\n'

    ## Canonical URL
    toml = toml + '## Provide a canonical URL if mirroring an OJS instance\n'
    toml = toml + 'canonicalurl = "' + canonicalurl + '"\n\n'

    ## Article Title
    toml = toml + 'title = "' + title + '"\n\n'
    toml = toml + '## Provide the article type and the ordering of its type in the contents page\n'

    ## Article Type
    toml = toml + 'articleType = "' + str(sectionname) + '"\n'
    toml = toml + 'articleType_weight = "' + str(sectionweight) + '"\n\n'

    ## Author Details
    ## Note that authors are not linked here with their affiliations and funding because
    ## OJS does not record multiple affiliations or output funding information via the API
    toml = toml + '## Provide author details\n'
    for i in authorlist:
        toml = toml + i

    ## Affiliations
    toml = toml + '\n\n'
    toml = toml + 'affiliations = [\n'
    for i in affiliations:
        toml = toml + '  {ISNI = "", ROR = "", name = "' + i + '"},\n'

    ## Funding
    toml = toml + ']\n\n'
    toml = toml + 'funding = [\n  {fundref = "", ROR = "", funder = "", awardtype = "", receipient = 1},\n]\n\n'

    ## Article History
    ## Note that OJS API does not record revision request date and resubmission dates, so only template information is output here
    toml = toml + 'history = [{event = "submission", date = "' + submissiondate[:10] + '"},\n'
    toml = toml + '  {event = "revisionrequest", date = ""},\n  {event = "revisionreceived", date = ""},\n  {event = "accept", date = ""},\n]\n\n'
    toml = toml + 'date = "' + publishdate + '"\n\n'

    ## Article Identifiers
    toml = toml + '## Article identifiers\n'
    if 'e' in pages:
        toml = toml + 'articleID = "' + '"\n'
    toml = toml + 'DOI = "' + doi + '"\n'
    toml = toml + 'volume = "' + str(volume) + '"\n'
    if issuenumber != None:
        toml = toml + 'issue = "' + str(issuenumber) + '"\n'
    toml = toml + 'firstpage = "' + str(pages).split('-')[0] + '"\n'
    if len(str(pages).split('-')) > 1:
        toml = toml + 'lastpage = "' + str(pages).split('-')[1] + '"\n'

    ## Galley information
    toml = toml + '\n## Galley information\n'
    for i in range(0,len(galleyids)):
        if 'pdf' in galleytypes[i].lower():
            toml = toml + 'PDF = "' + galleyfilenames[i] + '"\n'
            toml = toml + 'PDFcanonical = "' + canonicalurl + '/' + str(galleyids[i]) + '"\n'
        elif 'xml' in galleytypes[i].lower():
            toml = toml + 'XML = "' + galleyfilenames[i] + '"\n'
            toml = toml + 'XMLcanonical = "' + canonicalurl + '/' + str(galleyids[i]) + '"\n'
        elif 'html' in galleytypes[i].lower():
            toml = toml + 'HTML = "' + galleyfilenames[i] + '"\n'
            toml = toml + 'HTMLcanonical = "' + canonicalurl + '/' + str(galleyids[i]) + '"\n'
        elif 'epub' in galleytypes[i].lower():
            toml = toml + 'EPUB = "' + galleyfilenames[i] + '"\n'
            toml = toml + 'EPUBcanonical = "' + canonicalurl + '/' + str(galleyids[i]) + '"\n'

    ## Output types for Hugo
    toml = toml + '\noutputs - ["html", '
    for i in galleytypes:
        if 'pdf' in i.lower():
            toml = toml + '"galleyPDF", '
        elif 'xml' in i.lower():
            toml = toml + '"galleyXML", '
        elif 'html' in i.lower():
            toml = toml + '"galleyHTML", '
    toml = toml + ']\n\n'

    ## Keywords
    toml = toml + 'keywords = [\n'
    for i in keywords:
        toml = toml + '  "' + i + '",\n'
    toml = toml + ']\n\n'

    ## License information
    toml = toml + 'license = "' + licenseurl + '"\n\n'

    ## Article abstract
    toml = toml + 'abstract = "' + abstract + '"\n\n'

    ## Relations
    ## Since OJS does not record or output relations via the API, this is template information only
    toml = toml + 'relations = [\n'
    toml = toml + '#  {linktype = "", contenttype = "", sourcetype = "repository", objectidtype = "doi", objectid = "", link = "https://", source = "", datatitle = ""},\n'
    toml = toml + ']\n\n'

    ## Resources
    ## Since OJS does not record or output resource via the API, this is template information only
    toml = toml + 'resources = [\n'
    toml = toml + '#  {resourceidtype = "rrid", vocab = "Research Resource Identifier", resourcename = "", resourceid = "" },\n'
    toml = toml + ']\n\n'

    ## References
    toml = toml + 'references = [\n'
    for i in reflist:
        toml = toml + '"' + i + '",\n'
    toml = toml + ']\n\n'

    ## Close off the TOML headers
    toml = toml + '+++\n'

    ## Save the output file
    outfile = open(outputfile, 'w', encoding='utf-8')
    outfile.write(toml)
    outfile.close()
