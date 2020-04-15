<p align="center"><img width=50% src="https://github.com/TBFY/general/blob/master/figures/tbfy-logo.png"></p>
<p align="center"><img width=40% src="https://github.com/TBFY/crosslinguality/blob/master/logo.png"></p>

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
![Docker](https://img.shields.io/badge/python-v3.7-blue.svg)
[![Build Status](https://travis-ci.org/TBFY/crosslinguality.svg?branch=master)](https://travis-ci.org/TBFY/crosslinguality)
[![](https://jitpack.io/v/TBFY/crosslinguality.svg)](https://jitpack.io/#TBFY/crosslinguality)
[![GitHub Issues](https://img.shields.io/github/issues/TBFY/crosslinguality.svg)](https://github.com/TBFY/crosslinguality/issues)
[![License](https://img.shields.io/badge/license-Apache2.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![DOI](https://zenodo.org/badge/167214336.svg)](https://zenodo.org/badge/latestdoi/167214336)

## Basic Overview

This repository is focused on the work done towards automatic real-time monitoring and analysis of public spending information published in different languages.

## API service description
To call the document comparison web service, the user should send an HTTP request to: http://wikifier.org/compare-docs. Both GET and POST requests are supported, but POST is preferred due to the server limits on the maximum length of the URL.
The request should contain the following arguments in URL-encoded form:
- **doc1** = the text of the first document;
- **lang1** = two-letter language code of the language of the first document in ISO 639-1 format (eg. en = English, sl = Slovene, de = German);
- **doc2**, **lang2** = the same for the second document.
To represent non-ASCII data in the input documents, encode the text using UTF-8 and then apply %-encoding (e.g. Beyoncé  Beyonc%C3%A9).
If you want the service to calculate similarities based on translations into English, you should also pass one of the following two arguments:
- **azureKey** =  a Microsoft Azure subscription key ;
- **azureToken** = a temporary Microsoft Azure authentication token.1
The response will be a JSON object containing the results of the comparison. This object contains the following attributes:
- **wikiIntersection** = number of Wikipedia concepts that were common to both documents.
- **wikiJaccard** = Jaccard measure between the sets of Wikipedia concepts for the two documents.
- **wikiCosine** = cosine similarity between the vectors of Wikipedia annotations for the two documents. Unlike the intersection and Jaccard measures, this measure takes into account the fact that each annotation has a numeric score (a higher score indicates that the annotation is believed to be more relevant). Thus the set of annotations with their weights can be interpreted as a vector, and the cosine measure can be computed between two such vectors.
- **ccaCosine** = cosine similarity between the vectors representing the two documents in a shared semantic space, obtained by projecting the TF-IDF based representations from language-specific input spaces into a common space using CCA (canonical correlation analysis).
- **translationCosineBinNoSw**, **translationCosineBinSw**, **translationCosineTfNoSw**, **translationCosineTfSw** = cosine similarity between the translations of both input documents into English. The translated documents are represented by vectors using the bag-of-words model. Several slightly different representations (and hence slightly different values of the cosine measure) can be obtained under this model depending on whether the vectors are binary (Bin; each component indicates whether a word is present in the document or not) or based on term frequency (Tf; each component indicates the number of occurrences of a word in the document), and whether stopwords are removed (NoSw) or kept (Sw). 
- **doc1** = details about the first document: this is an object that includes the text of the document, a list of Wikipedia annotations and their relevance scores (extracted from the output returned by the JSI Wikifier), the projection of the document into a shared semantic space obtained using CCA (a list of floating-point values representing the components of a 500-dimensional vector), and the English version of the document obtained using machine translation (this is given as a list of all the requests made to Azure’s translation service, with the input strings for each request and the corresponding response from Azure).
- **doc2** = like *doc1*, but for the second document.

## Running sample Python3 application
For example, we have two text documents (encoded in UTF-8), first document (*doc1-utf8.txt*) is in German language (*de*), second document (*doc2-utf8.txt*) is in English (*en*). We run *sampleCall2.py* with the following arguments:

```python3 sampleCall2.py doc1-utf8.txt de doc2-utf8.txt en```

Example of results we get:

```
Similarity based on Wikifier annotations:
 - Cosine measure: 0.0549141
 - Intersection: 1
 - Jaccard measure: 0.0204082
Similarity based on CCA projections:
 - Cosine measure: 0.45718
Similarity based on translations into English:
 - Cosine measure over binary vectors, stopwords removed: 0.0718782
 - Cosine measure over binary vectors, stopwords kept: 0.162828
 - Cosine measure over TF vectors, stopwords removed: 0.0373881
 - Cosine measure over TF vectors, stopwords kept: 0.712192
 ```
Both the Cosine and the Jaccard measure return values in the range from 0 to 1, with higher values indicating greater similarity. 

## Background
Since input are text documents in different languages, we must compute the similarity with removed effect of the language. There are several methods to compute similarity from multi lingual documents: statistical cross-lingual computation, semantic cross-lingual computation and similarity computation through machine translation. We have implemented all three methods in our document similarity computation service.

The document comparison service builds on top of several existing services to provide cross-lingual comparison of documents based on several different representations:

- **Wikipedia concepts**. We call the JSI Wikifier service  for each input document to obtain a set of Wikipedia concepts relevant to that document. Each concept also includes a numeric relevance score. The concepts from different-language Wikipedias are mapped into their English-language equivalents using the Wikipedia’s cross-language links. Various measures of similarity are then computed between the resulting sets of annotations for each input document.

- **CCA projections**. Traditionally, in text mining, documents are represented by high-dimensional vectors using the “bag of words” model, where each dimension corresponds to one word of the input language. Thus, documents in different languages are represented by vectors in different high-dimensional spaces and cannot be compared directly. CCA (canonical correlation analysis) is a statistical technique that computes projections (mappings) from these spaces into a new, shared (language-independent) space. Vectors representing two documents in this new space can then be compared using any of the usual measures, e.g. the cosine measure or the Eucliean distance. Our service reports the cosine measure as it is independent of the length of the documents.

- **Translations**. We call a machine-translation service to translate both input documents into English. Now that they are in the same language, they can be represented by vectors using the usual bag-of-words model and similarity between them can be computed using the cosine measure. Currently the Microsoft Azure translator is used and calculating the translation-based similarity measures requires the caller to provide an Azure subscription key or authorization token. Currently the Azure service has a limit of 5000 characters per 1 translation call, but our document comparison service works around this by automatically splitting the document into shorter chunks and making multiple calls as needed. When splitting the document, breaks are only made at sentence boundaries (as defined by the Unicode sentence breaking rules ), to maintain as much of the integrity of the text as possible. 
To minimize the usage of the monthly quota associated with the given Azure subscription, our service caches the responses so that if the same document appears in multiple calls, it will only be translated once. If cached translations of both input documents are available, our document comparison service will report the translation-based similarity measures even if no Azure key or token was provided in the request.
