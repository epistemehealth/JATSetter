<xsl:stylesheet version="3.0"
xmlns:xsl="http://www.w3.org/1999/XSL/Transform" xmlns:xlink="http://www.w3.org/1999/xlink">
<xsl:output method="text" omit-xml-declaration="yes" indent="no"/>

<!-- We are only interested in the reference list, whether or not there is an article here -->
<xsl:template match="/">
<xsl:apply-templates select="article/back/ref-list" />
</xsl:template>

<!-- Determine the type of reference and reference ID -->
<!-- Note: For references with IDs that start with "ref"
     The "ref" will be stripped so that it is just the number -->
<xsl:template match="article/back/ref-list">
<xsl:for-each select="ref">
<!-- Assign a variable to check if it is a preprint server -->
<xsl:variable name="jname" select="translate(element-citation/source, 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz')"/>
<xsl:variable name="ispreprint" select="$jname='arxiv' or
$jname='authorea preprints' or
$jname='beilstein archives' or
$jname='biorxiv' or
$jname='research square' or
$jname='preprints.org' or
$jname='medrxiv' or
$jname='chemrxiv' or
$jname='peerj preprints' or
$jname='ssrn' or
$jname='osf preprints' or
$jname='africarxiv' or
$jname='agrixiv' or
$jname='arabixiv' or
$jname='biohackrxiv' or
$jname='bodoarxiv' or
$jname='eartharxiv' or
$jname='ecoevorxiv' or
$jname='ecsarxiv' or
$jname='edarxiv' or
$jname='engrxiv' or
$jname='focus archive' or
$jname='frenxiv' or
$jname='ina-rxiv' or
$jname='indiarxiv' or
$jname='lawarxiv' or
$jname='lis scholarship archive' or
$jname='marxiv' or
$jname='mediarxiv' or
$jname='metarxiv' or
$jname='mindrxiv' or
$jname='nutrixiv' or
$jname='paleorxiv' or
$jname='psyarxiv' or 
$jname='socarxiv' or
$jname='sportxiv'"/>
@<xsl:choose>
<xsl:when test="$ispreprint or element-citation/@publication-type='preprint'">preprint</xsl:when>
<xsl:when test="element-citation/@publication-type='journal'">article</xsl:when>
<xsl:when test="element-citation/@publication-type='book'">book</xsl:when>
<xsl:when test="element-citation/@publication-type='chapter'">inbook</xsl:when>
<xsl:when test="element-citation/@publication-type='paper' and element-citation/source">inproceedings</xsl:when>
<xsl:when test="element-citation/@publication-type='paper'">conference</xsl:when>
<xsl:when test="element-citation/@publication-type='confproc' and element-citation/source">inproceedings</xsl:when>
<xsl:when test="element-citation/@publication-type='confproc'">conference</xsl:when>
<xsl:when test="element-citation/@publication-type='data'">article</xsl:when>
<xsl:when test="element-citation/@publication-type='webpage'">webpage</xsl:when>
</xsl:choose>{<xsl:choose>
<xsl:when test="starts-with(./@id, 'ref')"><xsl:value-of select="substring-after(./@id, 'ref')"/></xsl:when>
<xsl:otherwise><xsl:value-of select="./@id"/></xsl:otherwise>
</xsl:choose>,
<xsl:apply-templates><xsl:with-param name="ispreprint" select="$ispreprint" /></xsl:apply-templates>
</xsl:for-each>
</xsl:template>

<!-- Some basic formatting templates -->
<!-- Start by suppressing the printing of label tags -->
<xsl:template match="label"/>
<!-- Then convert superscript, subscript, bold, italic and underline to LaTeX -->
<xsl:template match="sup">$^{<xsl:apply-templates />}$</xsl:template>
<xsl:template match="sub">$_{<xsl:apply-templates />}$</xsl:template>
<xsl:template match="bold">\textbf{<xsl:apply-templates />}</xsl:template>
<xsl:template match="italic">\textit{<xsl:apply-templates />}</xsl:template>
<xsl:template match="underline">\underline{<xsl:apply-templates />}</xsl:template>

<!-- Template blocks to handle each major citation type -->
<!-- Begin with the most important one for journals and preprints -->
<!-- The value of $ispreprint is brought through to the template so it can be used to customise -->
<xsl:template match="element-citation[@publication-type='journal'] | element-citation[@publication-type='preprint']">
<xsl:param name="ispreprint"/>
<xsl:choose>

<!-- Output the fields for a preprint -->
<xsl:when test="$ispreprint or element-citation[@publication-type='preprint']">
<xsl:apply-templates select="person-group[@person-group-type='author']"/>
<xsl:apply-templates select="article-title"/>journal = {<xsl:value-of select="source"/>},
<xsl:apply-templates select="year"/>
<xsl:apply-templates select="volume"/>
<xsl:apply-templates select="issue"/>
<xsl:choose>
<xsl:when test="page-range">pages = {<xsl:value-of select="page-range"/>},
</xsl:when>
<xsl:when test="fpage">pages = {<xsl:value-of select="fpage"/><xsl:if test="lpage">-<xsl:value-of select="lpage"/></xsl:if>},
</xsl:when>
<xsl:when test="elocation-id">pages = {<xsl:value-of select="elocation-id"/>},
</xsl:when>
</xsl:choose>
<xsl:apply-templates select="date-in-citation"/>
<xsl:apply-templates select="pub-id"/>}
</xsl:when>
<!-- Output the fields for a journal article -->
<xsl:otherwise><xsl:apply-templates select="person-group[@person-group-type='author']"/>
<xsl:apply-templates select="article-title"/>journal = {<xsl:value-of select="source"/>},
<xsl:apply-templates select="year"/>
<xsl:apply-templates select="volume"/>
<xsl:apply-templates select="issue"/>
<xsl:choose>
<xsl:when test="page-range">pages = {<xsl:value-of select="page-range"/>},
</xsl:when>
<xsl:when test="fpage">pages = {<xsl:value-of select="fpage"/><xsl:if test="lpage">-<xsl:value-of select="lpage"/></xsl:if>},
</xsl:when>
<xsl:when test="elocation-id">pages = {<xsl:value-of select="elocation-id"/>},
</xsl:when>
</xsl:choose>
<xsl:apply-templates select="pub-id"/>
<xsl:text>}
</xsl:text>
</xsl:otherwise>

</xsl:choose>
</xsl:template>

<!-- Then do books-->
<xsl:template match="element-citation[@publication-type='book']">
<xsl:apply-templates select="person-group[@person-group-type='author']"/>
<xsl:apply-templates select="person-group[@person-group-type='editor']"/>
<xsl:apply-templates select="person-group[@person-group-type='translator']"/>title = {<xsl:value-of select="source"/>},
<xsl:apply-templates select="series"/>
<xsl:apply-templates select="volume"/>
<xsl:apply-templates select="year"/>
<xsl:apply-templates select="publisher-name"/>
<xsl:apply-templates select="publisher-loc"/>
<xsl:apply-templates select="pub-id"/>
<xsl:text>}
</xsl:text>
</xsl:template>
	 
<!-- Then do book chapters -->
<xsl:template match="element-citation[@publication-type='chapter']">
<xsl:apply-templates select="person-group[@person-group-type='author']"/>
<xsl:apply-templates select="person-group[@person-group-type='editor']"/>
<xsl:apply-templates select="person-group[@person-group-type='translator']"/>title = {<xsl:value-of select="source"/>},
<xsl:apply-templates select="chapter-title"/>
<xsl:apply-templates select="series"/>
<xsl:apply-templates select="volume"/>
<xsl:apply-templates select="year"/>
<xsl:choose>
<xsl:when test="page-range">pages = {<xsl:value-of select="page-range"/>},
</xsl:when>
<xsl:when test="fpage">pages = {<xsl:value-of select="fpage"/><xsl:if test="lpage">-<xsl:value-of select="lpage"/></xsl:if>},
</xsl:when>
<xsl:when test="elocation-id">pages = {<xsl:value-of select="elocation-id"/>},
</xsl:when>
</xsl:choose>
<xsl:apply-templates select="publisher-name"/>
<xsl:apply-templates select="publisher-loc"/>
<xsl:apply-templates select="pub-id"/>
<xsl:text>}
</xsl:text>
</xsl:template>

<!-- Now begin handling the more marginal cases of conference papers -->
<!-- JATSetter will use the publication-type of "paper" for conference papers
because this is the article type used in examples given by the JATS 1.2 Tag Library:
https://jats.nlm.nih.gov/publishing/tag-library/1.2/element/conf-name.html -->
<xsl:template match="element-citation[@publication-type='paper']">
<xsl:apply-templates select="person-group[@person-group-type='author']"/>
<xsl:apply-templates select="person-group[@person-group-type='editor']"/>
<xsl:apply-templates select="person-group[@person-group-type='translator']"/>
<xsl:if test="source">booktitle = {<xsl:value-of select="source"/>},
</xsl:if>
<xsl:apply-templates select="series"/>
<xsl:apply-templates select="volume"/>
<xsl:apply-templates select="year"/>
<xsl:apply-templates select="month"/>
<xsl:apply-templates select="day"/>
<xsl:apply-templates select="publisher-name"/>
<xsl:apply-templates select="publisher-loc"/>
<xsl:apply-templates select="pub-id"/>
<xsl:text>}
</xsl:text>
</xsl:template>

<!-- However, Texture uses publication-type of "confproc" for conferences
so this is supported here as well -->
<xsl:template match="element-citation[@publication-type='confproc']">
<xsl:apply-templates select="person-group[@person-group-type='author']"/>
<xsl:apply-templates select="person-group[@person-group-type='editor']"/>
<xsl:apply-templates select="person-group[@person-group-type='translator']"/>
<xsl:if test="source">booktitle = {<xsl:value-of select="source"/>},
</xsl:if>
<xsl:apply-templates select="series"/>
<xsl:apply-templates select="volume"/>
<xsl:apply-templates select="year"/>
<xsl:apply-templates select="month"/>
<xsl:apply-templates select="day"/>
<xsl:apply-templates select="conf-name"/>
<xsl:apply-templates select="conf-loc"/>
<xsl:apply-templates select="pub-id"/>
<xsl:text>}
</xsl:text>
</xsl:template>

<!-- Webpages are not often cited, but are included here -->
<!-- Note: Use a <uri> tag with a specific-use attribute of "archived" to link to web archive urls -->
<xsl:template match="element-citation[@publication-type='webpage']">
<xsl:apply-templates select="person-group[@person-group-type='author']"/>
<xsl:apply-templates select="article-title"/>
<xsl:apply-templates select="year"/>
<xsl:apply-templates select="month"/>
<xsl:apply-templates select="day"/>
<xsl:apply-templates select="date-in-citation"/>
<xsl:apply-templates select="publisher-name"/>
<xsl:apply-templates select="publisher-loc"/>
<xsl:apply-templates select="uri"/>
<xsl:apply-templates select="pub-id"/>
<xsl:text>}
</xsl:text>
</xsl:template>

<!-- Data citations-->
<xsl:template match="element-citation[@publication-type='data']">
<xsl:apply-templates select="person-group[@person-group-type='author']"/>
<xsl:apply-templates select="data-title"/>journal = {<xsl:value-of select="source"/>},
<xsl:apply-templates select="year"/>
<xsl:apply-templates select="date-in-citation"/>
<xsl:apply-templates select="pub-id"/>
<xsl:if test="contains(source, '.io')"><xsl:text>keepdots = {1},
</xsl:text></xsl:if>
<xsl:text>}
</xsl:text>
</xsl:template>


<!-- METADATA-FIELD TEMPLATES -->
<!-- Each of these templates corresponds to a specific metadata field and is called specifically
by the templates for citation types above -->
<xsl:template match="person-group[@person-group-type='author']">author = {<xsl:for-each select="./*"><xsl:if test="position() &gt; 1"> and </xsl:if><xsl:apply-templates select="." /></xsl:for-each>},
</xsl:template>

<xsl:template match="person-group[@person-group-type='editor']">editor = {<xsl:for-each select="./*"><xsl:if test="position() &gt; 1"> and </xsl:if><xsl:apply-templates select="." /></xsl:for-each>},
</xsl:template>

<xsl:template match="person-group[@person-group-type='translator']">translator = {<xsl:for-each select="./*"><xsl:if test="position() &gt; 1"> and </xsl:if><xsl:apply-templates select="." /></xsl:for-each>},
</xsl:template>

<xsl:template match="name"><xsl:choose>
<xsl:when test="surname and given-names"><xsl:apply-templates select="surname"/>, <xsl:apply-templates select="given-names"/></xsl:when>
<xsl:when test="surname"><xsl:apply-templates select="surname"/></xsl:when>
<xsl:when test="given-names">{<xsl:apply-templates select="given-names"/>}</xsl:when>
<xsl:when test="string-name">{<xsl:apply-templates select="string-name"/>}</xsl:when>
<xsl:when test="collab"><xsl:apply-templates select="collab"/></xsl:when>
</xsl:choose>
</xsl:template>

<xsl:template match="surname"><xsl:apply-templates /></xsl:template>
<xsl:template match="given-names"><xsl:apply-templates /></xsl:template>
<xsl:template match="collab">{<xsl:apply-templates />}</xsl:template>
<xsl:template match="named-content"><xsl:apply-templates /></xsl:template>
<xsl:template match="string-name">{<xsl:apply-templates />}</xsl:template>

<xsl:template match="year">year = {<xsl:value-of select="."/>},
</xsl:template>

<xsl:template match="month">month = {<xsl:value-of select="."/>},
</xsl:template>

<xsl:template match="day">day = {<xsl:value-of select="."/>},
</xsl:template>

<xsl:template match="date-in-citation">lastchecked = {<xsl:value-of select="."/>},
</xsl:template>

<xsl:template match="article-title">title = {<xsl:apply-templates />},
</xsl:template>

<xsl:template match="data-title">title = {<xsl:apply-templates />},
</xsl:template>

<xsl:template match="volume">volume = {<xsl:value-of select="."/>},
</xsl:template>

<xsl:template match="issue">number = {<xsl:value-of select="."/>},
</xsl:template>

<xsl:template match="series">series = {<xsl:value-of select="."/>},
</xsl:template>

<xsl:template match="chapter-title">chapter = {<xsl:value-of select="."/>},
</xsl:template>

<xsl:template match="uri"><xsl:choose>
<xsl:when test="./@specific-use='archived'">archiveurl = {<xsl:value-of select="."/>},
</xsl:when>
<xsl:otherwise>url = {<xsl:value-of select="."/>},
</xsl:otherwise>
</xsl:choose>
</xsl:template>

<xsl:template match="page-range"/>
<xsl:template match="fpage"/>
<xsl:template match="lpage"/>
<xsl:template match="elocation-id"/>

<xsl:template match="pub-id">
<xsl:choose>
<xsl:when test="./@pub-id-type='doi'">DOI = {<xsl:value-of select="."/>},
</xsl:when>
<xsl:when test="./@pub-id-type='pmid'">PMID = {<xsl:value-of select="."/>},
</xsl:when>
<xsl:when test="./@pub-id-type='pmcid'">PMCID = {<xsl:value-of select="."/>},
</xsl:when>
<xsl:when test="./@pub-id-type='isbn'">ISBN = {<xsl:value-of select="."/>},
</xsl:when>
<xsl:when test="./@pub-id-type='other' and ./@assigning-authority='worldcat'">OCLC = {<xsl:value-of select="."/>},
</xsl:when>
</xsl:choose>
</xsl:template>

<xsl:template match="publisher-name">publisher = {<xsl:apply-templates />},
</xsl:template>

<xsl:template match="publisher-loc">address = {<xsl:apply-templates />},
</xsl:template>

<xsl:template match="conf-name">publisher = {<xsl:apply-templates />},
</xsl:template>

<xsl:template match="conf-loc">address = {<xsl:apply-templates />},
</xsl:template>

</xsl:stylesheet>