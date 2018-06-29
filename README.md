# Cross-linguality
This repository is focused on the work done towards automatic real-time monitoring and analysis of public spending information published in different languages

## API service description
To call the document comparison web service, the user should send an HTTP request to: http://wikifier.org/compare-docs. Both GET and POST requests are supported, but POST is preferred due to the server limits on the maximum length of the URL.
The request should contain the following arguments in URL-encoded form:
- doc1 = the text of the first document;
- lang1 = two-letter language code of the language of the first document in ISO 639-1 format (eg. en = English, sl = Slovene, de = German);
- doc2, lang2 = the same for the second document.
To represent non-ASCII data in the input documents, encode the text using UTF-8 and then apply %-encoding (e.g. Beyoncé  Beyonc%C3%A9).
If you want the service to calculate similarities based on translations into English, you should also pass one of the following two arguments:
- azureKey =  a Microsoft Azure subscription key ;
- azureToken = a temporary Microsoft Azure authentication token.1
The response will be a JSON object containing the results of the comparison. This object contains the following attributes:
- wikiIntersection = number of Wikipedia concepts that were common to both documents.
- wikiJaccard = Jaccard measure between the sets of Wikipedia concepts for the two documents.
- wikiCosine = cosine similarity between the vectors of Wikipedia annotations for the two documents. Unlike the intersection and Jaccard measures, this measure takes into account the fact that each annotation has a numeric score (a higher score indicates that the annotation is believed to be more relevant). Thus the set of annotations with their weights can be interpreted as a vector, and the cosine measure can be computed between two such vectors.
- ccaCosine = cosine similarity between the vectors representing the two documents in a shared semantic space, obtained by projecting the TF-IDF based representations from language-specific input spaces into a common space using CCA (canonical correlation analysis).
- translationCosineBinNoSw, translationCosineBinSw, translationCosineTfNoSw, translationCosineTfSw = cosine similarity between the translations of both input documents into English. The translated documents are represented by vectors using the bag-of-words model. Several slightly different representations (and hence slightly different values of the cosine measure) can be obtained under this model depending on whether the vectors are binary (Bin; each component indicates whether a word is present in the document or not) or based on term frequency (Tf; each component indicates the number of occurrences of a word in the document), and whether stopwords are removed (NoSw) or kept (Sw). 
- doc1 = details about the first document: this is an object that includes the text of the document, a list of Wikipedia annotations and their relevance scores (extracted from the output returned by the JSI Wikifier), the projection of the document into a shared semantic space obtained using CCA (a list of floating-point values representing the components of a 500-dimensional vector), and the English version of the document obtained using machine translation (this is given as a list of all the requests made to Azure’s translation service, with the input strings for each request and the corresponding response from Azure).
- doc2 = like doc1, but for the second document.


## Running sample Python3 application
We have two text documents (encoded in UTF-8), first is in German language (de), second in English (en):

```python3 sampleCall2.py doc1-utf8.txt de doc2-utf8.txt en```

Results:

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
