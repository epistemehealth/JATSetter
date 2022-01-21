# JATSetter

A repository for a simple program for transforming between JATS XML and LaTeX.

## Functions

JATSetter provides the following conversion support functions:

1. Convert a reference list from .bib to JATS XML
2. Fetch metadata from the [Open Journal Systems](https://pkp.sfu.ca/ojs/) API and save it in a markdown file as TOML. The fetch metadata function takes input from a text file (see template-request.txt).
3. Combine one JATS XML file containing article frontmatter and body with a JATS XML file containing the reference list
4. Convert a JATS XML file into a .tex file (uses XSLT)
5. Convert a JATS XML reference list into a .bib file (uses XSLT)

## Workflow assumptions

JATSetter is written with the following workflow in mind:

1. Retrieve metadata from OJS so that it can be used to creative a markdown file to feed into Hugo. See [Health Science Journal](https://github.com/epistemehealth/health-science-journal), which ports the OJS Health Sciences theme to Hugo.
2. Enrich frontmatter in the markdown file before using it to generate the JATS XML frontmatter.
3. Depending on how the references are provided by the author, convert from .bib to JATS or from JATS to .bib.
4. Typeset the body of the article using [Texture](https://github.com/epistemehealth/texture), but without xref links in the body to the references or figures and tables.
5. Combine the JATS XML frontmatter + body with the reference list (this function also does xref links to references and figures and tables).
6. Convert the JATS XML to LaTeX for typesetting with [LaTeX](https://github.com/epistemehealth/article-production/tree/master/LaTeX). This will require some manual adjustment of LaTeX code to fine-tune tables and figures.

## Other notes

- Many organisations are using or trying to use [Pandoc](https://pandoc.org/) for document conversion. Whether or how to use Pandoc output is something to consider for future development.
- JATSetter will try to handle special characters and symbols properly when converting between LaTeX and JATS XML, but this is not 100%.
- JATSetter relies on XSLT 1.0 for transforming from JATS XML to other formats. Since it was developed for Neuroanatomy and Behaviour, the XSLT included is for this journal, but the python code is generic so any journal can adapt this software for their uses.

## License

JATSetter is free and open source software. Like the Open Journal Systems software that we rely on, JATSetter is licensed under GPL version 3.