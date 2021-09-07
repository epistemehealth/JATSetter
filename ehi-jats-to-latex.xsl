<xsl:stylesheet version="3.0"
xmlns:xsl="http://www.w3.org/1999/XSL/Transform" xmlns:xlink="http://www.w3.org/1999/xlink">
<xsl:output method="text" omit-xml-declaration="yes" indent="no"/>
<xsl:template match="article"><!-- 
Start by templating out the standard LaTeX headers for manuscript files -->
\documentclass[a4paper,num-refs]{ehi-journals}

\journal{neurobehav}
\usepackage{graphicx}
\usepackage{siunitx}
\usepackage{academicons}
\usepackage{hyperxmp}
\usepackage{textgreek}
\definecolor{orcidlogocol}{HTML}{A6CE39}
\newcommand{\orcid}[1]{\href{https://orcid.org/#1}{\textcolor[HTML]{A6CE39}{\aiOrcid}}}
\newcommand{\ror}[1]{\href{https://ror.org/#1}{\includegraphics[width=0.3cm]{ror}}}

<!-- Template the Title -->
\title{<xsl:value-of select="front/article-meta/title-group/article-title"/>}

<!-- Before templating the authors, count how many footnotes there are-->
<xsl:variable name="totalfn" select="count(front/article-meta/author-notes/fn)"/>

<!-- Now template the authors, with footnotes first and corresponding author footnotes at the end-->
<xsl:for-each select="front/article-meta/contrib-group/contrib">
\author[<xsl:for-each select="xref[@ref-type='aff']"><xsl:if test="position() &gt; 1">,</xsl:if><xsl:value-of select="substring-after(./@rid,'affiliation')"/></xsl:for-each><xsl:choose>
<xsl:when test="xref/@ref-type='author-notes'"><xsl:if test="xref/@ref-type='aff'">,</xsl:if>\authfn{<xsl:for-each select="xref[@ref-type='author-notes']"><xsl:if test="position() &gt; 1">,</xsl:if><xsl:value-of select="substring-after(./@rid,'fn')"/></xsl:for-each><xsl:if test="xref/@ref-type='corresp'">,<xsl:value-of select="substring-after(xref[@ref-type='corresp']/@rid,'cor') + $totalfn"/></xsl:if>}</xsl:when><xsl:when test="xref/@ref-type='corresp'"><xsl:if test="xref/@ref-type='aff'">,</xsl:if>\authfn{<xsl:value-of select="substring-after(xref[@ref-type='corresp']/@rid,'cor') + $totalfn"/>}</xsl:when></xsl:choose>]{<xsl:value-of select="name/string-name"/><xsl:value-of select="name/given-names"/><xsl:if test="name/given-names and name/surname">&#160;</xsl:if><xsl:value-of select="name/surname"/><xsl:apply-templates select="contrib-id[@contrib-id-type='orcid']"/>}</xsl:for-each>
&#160;
<!-- Get the author affiliations -->
<xsl:for-each select="front/article-meta/aff">
\affil[<xsl:value-of select="substring-after(./@id,'affiliation')"/>]{<xsl:value-of select="institution-wrap/institution"/><xsl:if test="institution-wrap/institution-id/@institution-id-type='ROR'">\ror{<xsl:value-of select="institution-wrap/institution-id[@institution-id-type='ROR']"/>}</xsl:if>}
</xsl:for-each>
&#160;
<!-- Add author notes -->	
<xsl:for-each select="front/article-meta/author-notes">
<xsl:for-each select="fn">\authnote{\authfn{<xsl:value-of select="substring-after(./@id,'fn')"/>}<xsl:value-of select="."/>}
</xsl:for-each>
<xsl:for-each select="corresp">\authnote{\authfn{<xsl:value-of select="substring-after(./@id,'cor') + $totalfn"/>}<xsl:value-of select="email"/>}
</xsl:for-each>
</xsl:for-each>
&#160;
\papercat{<xsl:choose><xsl:when test="./@article-type='research-article'">Research Article</xsl:when><xsl:when test="./@article-type='review-article'">Review</xsl:when><xsl:when test="./@article-type='editorial'">Editorial</xsl:when><xsl:when test="./@article-type='professional-perspectives'">Professional Perspectives</xsl:when><xsl:when test="./@article-type='brief-communication'">Brief Communication</xsl:when><xsl:when test="./@article-type='data-brief'">Data Brief</xsl:when><xsl:when test="./@article-type='addendum'">Addendum</xsl:when><xsl:when test="./@article-type='correction'">Correction</xsl:when><xsl:when test="./@article-type='retraction'">Retraction</xsl:when></xsl:choose>}

\runningauthor{<xsl:choose>
<xsl:when test="count(front/article-meta/contrib-group/contrib) = 1"><xsl:choose>
<xsl:when test="front/article-meta/contrib-group/contrib/name/surname"><xsl:value-of select="front/article-meta/contrib-group/contrib/name/surname" /></xsl:when>
<xsl:when test="front/article-meta/contrib-group/contrib/name/string-name"><xsl:value-of select="front/article-meta/contrib-group/contrib/name/string-name" /></xsl:when>
<xsl:when test="front/article-meta/contrib-group/contrib/collab"><xsl:value-of select="front/article-meta/contrib-group/contrib/collab" /></xsl:when>
</xsl:choose></xsl:when>
<xsl:when test="count(front/article-meta/contrib-group/contrib) = 2">
<xsl:choose>
<xsl:when test="front/article-meta/contrib-group/contrib[1]/name/surname"><xsl:value-of select="front/article-meta/contrib-group/contrib[1]/name/surname" /></xsl:when>
<xsl:when test="front/article-meta/contrib-group/contrib[1]/name/string-name"><xsl:value-of select="front/article-meta/contrib-group/contrib[1]/name/string-name" /></xsl:when>
<xsl:when test="front/article-meta/contrib-group/contrib[1]/collab"><xsl:value-of select="front/article-meta/contrib-group/contrib[1]/collab" /></xsl:when>
</xsl:choose>&#160;\&amp;&#160;<xsl:choose>
<xsl:when test="front/article-meta/contrib-group/contrib[2]/name/surname"><xsl:value-of select="front/article-meta/contrib-group/contrib[2]/name/surname" /></xsl:when>
<xsl:when test="front/article-meta/contrib-group/contrib[2]/name/string-name"><xsl:value-of select="front/article-meta/contrib-group/contrib[2]/name/string-name" /></xsl:when>
<xsl:when test="front/article-meta/contrib-group/contrib[2]/collab"><xsl:value-of select="front/article-meta/contrib-group/contrib[2]/collab" /></xsl:when>
</xsl:choose>
</xsl:when>
<xsl:otherwise><xsl:choose>
<xsl:when test="front/article-meta/contrib-group/contrib[1]/name/surname"><xsl:value-of select="front/article-meta/contrib-group/contrib[1]/name/surname" /></xsl:when>
<xsl:when test="front/article-meta/contrib-group/contrib[1]/name/string-name"><xsl:value-of select="front/article-meta/contrib-group/contrib[1]/name/string-name" /></xsl:when>
<xsl:when test="front/article-meta/contrib-group/contrib[1]/collab"><xsl:value-of select="front/article-meta/contrib-group/contrib[1]/collab" /></xsl:when>
</xsl:choose>&#160;et al.</xsl:otherwise>
</xsl:choose>}

\jarticlenum{<xsl:value-of select="front/article-meta/elocation-id"/>}

\crossmarkdate{<xsl:value-of select="front/article-meta/pub-date/@iso-8601-date"/>}

\jdoi{<xsl:value-of select="front/article-meta/article-id[@pub-id-type='doi']"/>}

\begin{document}

<!-- Finish the frontmatter, including the keywords and abstract -->
\begin{frontmatter}
\maketitle
\begin{abstract}
<xsl:apply-templates select="front/article-meta/abstract/p"/>
\end{abstract}
\begin{keywords}
<xsl:for-each select="front/article-meta/kwd-group/kwd"><xsl:if test="position() &gt; 1">; </xsl:if><xsl:value-of select="."/></xsl:for-each>
\end{keywords}
\end{frontmatter}
<!-- Establish the bibliography, since references will be cited individually based on the XML text -->
\nocite{<xsl:for-each select="back/ref-list/ref"><xsl:if test="position() &gt; 1">,</xsl:if><xsl:value-of select="substring-after(./@id,'ref')"/></xsl:for-each>}

<xsl:apply-templates select="body"/>

\bibliography{paper-refs}

\section{Copyright and License}
<xsl:choose>
<xsl:when test="contains(front/article-meta/permissions/license/@xlink:href,'creativecommons.org/licenses/by/4.0')">Copyright \textcopyright\space<xsl:value-of select="front/article-meta/permissions/copyright-year"/>. <xsl:for-each select="front/article-meta/contrib-group/contrib"><xsl:if test="position() &gt; 1">, </xsl:if><xsl:value-of select="name/string-name"/><xsl:value-of select="name/given-names"/><xsl:if test="name/given-names and name/surname">&#160;</xsl:if><xsl:value-of select="name/surname"/></xsl:for-each>. Except where otherwise noted, the content of this article is licensed under a \href{https://creativecommons.org/licenses/by/4.0/}{Creative Commons Attribution 4.0 International License}. You are free to reuse or adapt this article for any purpose, provided appropriate acknowledgement is provided. For additional permissions, please contact the corresponding author.

\hypersetup{
pdfmetalang={en},
pdfauthor={<xsl:for-each select="front/article-meta/contrib-group/contrib"><xsl:if test="position() &gt; 1">, </xsl:if><xsl:value-of select="name/string-name"/><xsl:value-of select="name/given-names"/><xsl:if test="name/given-names and name/surname">&#160;</xsl:if><xsl:value-of select="name/surname"/></xsl:for-each>},
pdfsubject={<xsl:for-each select="front/article-meta/article-categories/subj-group/subject"><xsl:if test="position() &gt; 1">, </xsl:if><xsl:value-of select="."/></xsl:for-each>},
pdfkeywords={<xsl:for-each select="front/article-meta/kwd-group/kwd"><xsl:if test="position() &gt; 1">, </xsl:if><xsl:value-of select="."/></xsl:for-each>},
pdfpublication={<xsl:value-of select="front/journal-meta/journal-title-group/journal-title"/>},
pdfpublisher={<xsl:value-of select="front/journal-meta/publisher/publisher-name"/>},
pdfpubtype={journal},
pdfeissn={<xsl:value-of select="front/journal-meta/issn[@publication-format='electronic']"/>},
pdfdoi={<xsl:value-of select="front/article-meta/article-id[@pub-id-type='doi']"/>},
pdfvolumenum={<xsl:value-of select="front/article-meta/volume"/>},<xsl:if test="front/article-meta/issue">
pdfissuenum={<xsl:value-of select="front/article-meta/issue"/>},</xsl:if>
pdfdate={<xsl:value-of select="front/article-meta/pub-date/@iso-8601-date"/>},
pdfcopyright={Copyright (C) <xsl:value-of select="front/article-meta/permissions/copyright-year"/>. <xsl:for-each select="front/article-meta/contrib-group/contrib"><xsl:if test="position() &gt; 1">, </xsl:if><xsl:value-of select="name/string-name"/><xsl:value-of select="name/given-names"/><xsl:if test="name/given-names and name/surname">&#160;</xsl:if><xsl:value-of select="name/surname"/></xsl:for-each>. Except where otherwise noted, the content of this article is licensed under Creative Commons Attribution License, which permits unrestricted use, distribution, and reproduction in any medium, provided the original author and source are credited.},
pdflicenseurl={https://creativecommons.org/licenses/by/4.0/},
}

</xsl:when>
<xsl:when test="contains(front/article-meta/permissions/license/@xlink:href,'creativecommons.org/licenses/by-nc/4.0')">Copyright \textcopyright\space\<xsl:value-of select="front/article-meta/permissions/copyright-year"/>. <xsl:for-each select="front/article-meta/contrib-group/contrib"><xsl:if test="position() &gt; 1">, </xsl:if><xsl:value-of select="name/string-name"/><xsl:value-of select="name/given-names"/><xsl:if test="name/given-names and name/surname">&#160;</xsl:if><xsl:value-of select="name/surname"/></xsl:for-each>. Except where otherwise noted, the content of this article is licensed under a \href{https://creativecommons.org/licenses/by-nc/4.0/}{Creative Commons Attribution-NonCommercial 4.0 International License}. In addition to this license, reuse of a reasonable portion of the work for \emph{fair dealing} purposes under Australian copyright law, such as medical research, education, scholarship, or not-for-profit or charitable purposes, is also permitted. For additional permissions, please contact the corresponding author.

\hypersetup{
pdfmetalang={en},
pdfauthor={<xsl:for-each select="front/article-meta/contrib-group/contrib"><xsl:if test="position() &gt; 1">, </xsl:if><xsl:value-of select="name/string-name"/><xsl:value-of select="name/given-names"/><xsl:if test="name/given-names and name/surname">&#160;</xsl:if><xsl:value-of select="name/surname"/></xsl:for-each>},
pdfsubject={<xsl:for-each select="front/article-meta/article-categories/subj-group/subject"><xsl:if test="position() &gt; 1">, </xsl:if><xsl:value-of select="."/></xsl:for-each>},
pdfkeywords={<xsl:for-each select="front/article-meta/kwd-group/kwd"><xsl:if test="position() &gt; 1">, </xsl:if><xsl:value-of select="."/></xsl:for-each>},
pdfpublication={<xsl:value-of select="front/journal-meta/journal-title-group/journal-title"/>},
pdfpublisher={<xsl:value-of select="front/journal-meta/publisher/publisher-name"/>},
pdfpubtype={journal},
pdfeissn={<xsl:value-of select="front/journal-meta/issn[@publication-format='electronic']"/>},
pdfdoi={<xsl:value-of select="front/article-meta/article-id[@pub-id-type='doi']"/>},
pdfvolumenum={<xsl:value-of select="front/article-meta/volume"/>},<xsl:if test="front/article-meta/issue">
pdfissuenum={<xsl:value-of select="front/article-meta/issue"/>},</xsl:if>
pdfdate={<xsl:value-of select="front/article-meta/pub-date/@iso-8601-date"/>},
pdfcopyright={Copyright (C) <xsl:value-of select="front/article-meta/permissions/copyright-year"/>. <xsl:for-each select="front/article-meta/contrib-group/contrib"><xsl:if test="position() &gt; 1">, </xsl:if><xsl:value-of select="name/string-name"/><xsl:value-of select="name/given-names"/><xsl:if test="name/given-names and name/surname">&#160;</xsl:if><xsl:value-of select="name/surname"/></xsl:for-each>.Except where otherwise noted, the content of this article is licensed under a Creative Commons Attribution-NonCommercial 4.0 International License. In addition to this license, reuse of a reasonable portion of the work for fair dealing purposes under Australian copyright law, such as medical research, education, scholarship, or not-for-profit or charitable purposes, is also permitted. For additional permissions, please contact the corresponding author.},
pdflicenseurl={https://creativecommons.org/licenses/by-nc/4.0/},
}
</xsl:when>
</xsl:choose>
\end{document}
</xsl:template>

<!-- Templates for specific tags -->
<xsl:template match="front/article-meta/abstract/p"><xsl:apply-templates /></xsl:template>

<xsl:template match="body">
<xsl:apply-templates />
</xsl:template>

<xsl:template match="sec">
<xsl:if test="contains(title,'Declaration') and ../../back/ack"><xsl:apply-templates select="../../back/ack" /></xsl:if>
<xsl:apply-templates />
</xsl:template>

<xsl:template match="sec/sec">
<xsl:apply-templates />
</xsl:template>

<xsl:template match="sec/sec/sec">
<xsl:apply-templates />
</xsl:template>

<xsl:template match="p">
<xsl:apply-templates />
&#160;
</xsl:template>

<xsl:template match="xref[@ref-type='bibr']"><xsl:choose><xsl:when test=". = substring-after(./@rid,'ref')">\citealp{<xsl:value-of select="."/>}</xsl:when><xsl:otherwise>\defcitealias{<xsl:value-of select="substring-after(./@rid, 'ref')"/>}{<xsl:value-of select="."/>}\citetalias{<xsl:value-of select="substring-after(./@rid,'ref')"/>}</xsl:otherwise></xsl:choose></xsl:template>
<xsl:template match="xref[@ref-type='table']">\hyperref[<xsl:value-of select="./@rid"/>]{<xsl:value-of select="."/>}</xsl:template>
<xsl:template match="xref[@ref-type='fig']">\hyperref[<xsl:value-of select="./@rid"/>]{<xsl:value-of select="."/>}</xsl:template>
<xsl:template match="italic">\emph{<xsl:value-of select="."/>}</xsl:template>

<xsl:template match="title">
<xsl:choose>
<xsl:when test="count(ancestor::sec) = 1">\section{<xsl:apply-templates />}
</xsl:when>
<xsl:when test="count(ancestor::sec) = 2">\subsection{<xsl:apply-templates />}
</xsl:when>
<xsl:otherwise>\subsubsection{<xsl:apply-templates />}
</xsl:otherwise>
</xsl:choose>
</xsl:template>

<xsl:template match="sup">$^{<xsl:apply-templates />}$</xsl:template>
<xsl:template match="sub">$_{<xsl:apply-templates />}$</xsl:template>
<xsl:template match="bold">\textbf{<xsl:apply-templates />}</xsl:template>
<xsl:template match="italic">\textit{<xsl:apply-templates />}</xsl:template>
<xsl:template match="underline">\underline{<xsl:apply-templates />}</xsl:template>

<xsl:template match="caption/p"><xsl:apply-templates /></xsl:template>


<xsl:template match="table-wrap">

\begin{table*}[bt!]
\caption{<xsl:value-of select="caption/title"/>}\label{<xsl:value-of select="./@id"/>}
\begin{tabularx}{\linewidth}{<xsl:for-each select="table/tbody/tr[1]/td"><xsl:if test="position() &gt; 1">&#160;</xsl:if>L</xsl:for-each>}
\toprule
<xsl:for-each select="table/tbody/tr"><xsl:choose><xsl:when test="position() = 1"><xsl:for-each select="td"><xsl:if test="position() &gt; 1">&#160;&amp;&#160;</xsl:if>{<xsl:apply-templates />}</xsl:for-each>\\
\midrule</xsl:when>
<xsl:otherwise>
<xsl:for-each select="td"><xsl:if test="position() &gt; 1">&#160;&amp;&#160;</xsl:if><xsl:apply-templates /></xsl:for-each>\\
</xsl:otherwise>
</xsl:choose>
</xsl:for-each>
\bottomrule
\end{tabularx}
<xsl:if test="caption/p">
\begin{tablenotes}
<xsl:for-each select="caption/p">\item <xsl:apply-templates /></xsl:for-each>
\end{tablenotes}</xsl:if>
\end{table*}
&#160;
</xsl:template>

<xsl:template match="fig">
\begin{figure*}[bt!]
\centering
\includegraphics[width=.8\textwidth]{<xsl:value-of select="substring-before(graphic/@xlink:href,'.')"/>}
\caption{<xsl:apply-templates select="caption/p"/>}\label{<xsl:value-of select="./@id"/>}
\end{figure*}
&#160;
</xsl:template>

<xsl:template match="list">

\begin{itemize}<xsl:for-each select="list-item/p">
\item <xsl:apply-templates />
</xsl:for-each>
\end{itemize}
</xsl:template>

<xsl:template match="contrib-id[@contrib-id-type='orcid']">\orcid{<xsl:value-of select="substring-after(.,'orcid.org/')"/>}</xsl:template>

<xsl:template match="back/ack">
\subsection{Acknowledgements}
<xsl:for-each select="p"><xsl:apply-templates /></xsl:for-each>
&#160;
</xsl:template>

<xsl:template match="ext-link">
<xsl:choose>
<xsl:when test="contains(., 'orcid.org/')">\orcid{<xsl:value-of select="substring-after(.,'orcid.org/')" />}</xsl:when>
<xsl:otherwise>\href{<xsl:value-of select="./@xlink:href"/>}{<xsl:apply-templates />}</xsl:otherwise>
</xsl:choose>
</xsl:template>

</xsl:stylesheet>