import urllib.parse, urllib.request, json

def CompareDocs(text1, lang1, text2, lang2):
    # Prepare the request.
    data = urllib.parse.urlencode([
        ("doc1", text1), ("lang1", lang1),
        ("doc2", text2), ("lang2", lang2), 
        # ("azureKey", "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"),
        ])
    url = "http://www.wikifier.org/compare-docs"
    # Call the server and read the response.
    req = urllib.request.Request(url, data=data.encode("utf8"), method="POST")
    with urllib.request.urlopen(req, timeout = 60) as f:
        response = f.read()
        #g = open("response.txt", "wb"); g.write(response); g.close()
        response = json.loads(response.decode("utf8"))
    # Output the results.
    print("Similarity based on Wikifier annotations:")
    print(" - Cosine measure: %g" % response["wikiCosine"])
    print(" - Intersection: %d" % response["wikiIntersection"])
    print(" - Jaccard measure: %g" % response["wikiJaccard"])
    print("Similarity based on CCA projections:")
    print(" - Cosine measure: %g" % response["ccaCosine"])
    if "translationCosineBinSw" in response:
        print("Similarity based on translations into English:")
        print(" - Cosine measure over binary vectors, stopwords removed: %g" % response["translationCosineBinNoSw"])
        print(" - Cosine measure over binary vectors, stopwords kept: %g" % response["translationCosineBinSw"])
        print(" - Cosine measure over TF vectors, stopwords removed: %g" % response["translationCosineTfNoSw"])
        print(" - Cosine measure over TF vectors, stopwords kept: %g" % response["translationCosineTfSw"])

import sys
if len(sys.argv) != 5: print("Usage: sampleCall.py fileName1.txt lang1 fileName2.txt lang2"); sys.exit(0)
with open(sys.argv[1], "rt", encoding = "utf8") as f: doc1 = f.read()
with open(sys.argv[3], "rt", encoding = "utf8") as f: doc2 = f.read()
CompareDocs(doc1, sys.argv[2], doc2, sys.argv[4])
