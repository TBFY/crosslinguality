import urllib.parse, urllib.request, json

def CompareDocs(text1, lang1, text2, lang2):
    # Prepare the request.
    data = urllib.parse.urlencode([
        ("doc1", text1), ("lang1", lang1),
        ("doc2", text2), ("lang2", lang2), 
        # ("azureKey", "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"),  # insert your key here
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
        print(" - Cosine measure over binary vectors, stopwords removed: %g" %
              response["translationCosineBinNoSw"])
        print(" - Cosine measure over binary vectors, stopwords kept: %g" %
              response["translationCosineBinSw"])
        print(" - Cosine measure over TF vectors, stopwords removed: %g" % 
              response["translationCosineTfNoSw"])
        print(" - Cosine measure over TF vectors, stopwords kept: %g" % 
              response["translationCosineTfSw"])

CompareDocs("""
    All human beings are born free and equal in dignity and rights. 
    They are endowed with reason and conscience and should act towards 
    one another in a spirit of brotherhood.
    Everyone is entitled to all the rights and freedoms set forth in 
    this Declaration, without distinction of any kind, such as race, 
    colour, sex, language, religion, political or other opinion, 
    national or social origin, property, birth or other status. 
    Furthermore, no distinction shall be made on the basis of the 
    political, jurisdictional or international status of the country 
    or territory to which a person belongs, whether it be independent, 
    trust, non-self-governing or under any other limitation of 
    sovereignty.""",
    "en", 
    """
    Alle Menschen sind frei und gleich an W\u00fcrde und Rechten geboren. 
    Sie sind mit Vernunft und Gewissen begabt und sollen einander im 
    Geist der Br\u00fcderlichkeit begegnen. 
    Jeder hat Anspruch auf die in dieser Erkl\u00e4rung verk\u00fcndeten Rechte
    und Freiheiten ohne irgendeinen Unterschied, etwa nach Rasse, 
    Hautfarbe, Geschlecht, Sprache, Religion, politischer oder sonstiger 
    \u00dcberzeugung, nationaler oder sozialer Herkunft, Verm\u00f6gen, Geburt
    oder sonstigem Stand. 
    Des weiteren darf kein Unterschied gemacht werden auf Grund der 
    politischen, rechtlichen oder internationalen Stellung des Landes 
    oder Gebiets, dem eine Person angeh\u00f6rt, gleichg\u00fcltig ob dieses 
    unabh\u00e4ngig ist, unter Treuhandschaft steht, keine Selbstregierung 
    besitzt oder sonst in seiner Souver\u00e4nit\u00e4t eingeschr\u00e4nkt ist.
    """,
    "de")
