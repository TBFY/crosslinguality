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

CompareDocs("""
    Der Landkreis plant die fl\u00e4chendeckende Errichtung eines Next Generation
    Access (NGA)-Netzes in seinen unterversorgten Gebieten (wei00dfe Flecken).

    Es ist vorgesehen, ein weitr\u00e4umiges FTTB-Netz zur Versorgung von ca. 12
    015 unterversorgten Haushalten mittels Neubau und unter Umst\u00e4nden
    Nutzung vorhandener und angemieteter Infrastrukturen zu errichten. Die
    Netzkonzeption als auch der Materialeinsatz wird gem\u00e400df den Richtlinien
    und Vorgaben der \u201eF\u00f6rderung zur Unterst\u00fctzung des Breitbandausbaus in
    der Bundesrepublik Deutschland\u201c vom 22.10.2015 erfolgen.

    Dieses passive Leerrohr- und Glasfasernetz, soll an einen Betreiber
    verpachtet werden.

    Mit dieser Ausschreibung wird der entsprechende P\u00e4chter f\u00fcr das zu
    errichtende passive Leerrohr- und Glasfasernetz gesucht.

    Die Planung und der Bau des passiven Lerrohr- und Glasfasernetzes
    obliegen dem Landkreis Gifhorn und werden auch von diesem mit einer
    gesonderten Ausschreibung beauftragt, jedoch eng mit dem sp\u00e4teren
    P\u00e4chter abgestimmt.

    Der P\u00e4chter verpflichtet sich zur Nutzung des Netzes. Dazu geh\u00f6rt die
    Einbringung der aktiven Technik in die passive Infrastruktur. Auch der
    Betrieb des Netzes erfolgt durch den P\u00e4chter oder einen von ihm zu
    benennende Dritten. Der P\u00e4chter verpflichtet sich zur Zahlung einer
    Pacht f\u00fcr die Nutzung der passiven Netzinfrastruktur an den
    Auftraggeber. Zu den Aufgaben des P\u00e4chters geh\u00f6rt ferner die
    Bereitstellung eines Diensteangebotes (Internet, Telefon und TV) f\u00fcr die
    Endkunden. Dabei soll sich der P\u00e4chter (Netzbetreiber) verpflichten,
    alle Bedarfsstellen in dem Gebiet mit einem Breitband-Internetanschluss
    von mindestens 50 Mbit/s im Download zu versorgen, wobei die
    Endkundenanschl\u00fcsse auch auf deutlich h\u00f6here Bandbreiten erweiterbar
    sein m\u00fcssen.

    Die Beauftragung erfolgt unter Beachtung der Leitlinien der Europ\u00e4ischen
    Union f\u00fcr die Anwendung der Vorschriften \u00fcber staatliche Beihilfen im
    Zusammenhang mit dem schnellen Breitbandausbau (2013/C 25/01),
    beziehungsweise der Rahmenregelung der Bundesrepublik Deutschland zur
    Unterst\u00fctzung des Aufbaus einer fl\u00e4chendeckenden Next Generation Access
    (NGA)-Breitbandversorgung.

    Der Landkreis Gifhorn beabsichtigt die hiernach gegebenen M\u00f6glichkeiten
    zur F\u00f6rderung zu nutzen.

    Insbesondere kommen dabei folgende F\u00f6rderprogramme in Betracht:

    \u2014 EFRE, Darlehen (Bewilligungsstelle: Investitions- und F\u00f6rderbank
    Niedersachsen),

    \u2014 Digitale Dividende II,

    \u2014 Richtlinie \u201eF\u00f6rderung zur Unterst\u00fctzung des Breitbandausbaus in der
    Bundesrepublik Deutschland\u201c vom 22.10.2015 (Bewilligungsstelle:
    Bundesministerium f\u00fcr Verkehr und digitale Infrastruktur).

    Weitere Details werden nach Abschluss des Teilnahmewettbewerbs mit der
    Aufforderung zur Abgabe eines Angebotes im Rahmen des
    Verhandlungsverfahrens mitgeteilt.
    """,
    "de", 
    """
    The Authority has established a collaborative Dynamic Purchasing System
    (DPS) for Telephony Services. The DPS comprises a number of categories
    (lots) for the provision of Traditional Telephony, Internet Protocol
    (IP) Telephony and Enterprise Bundled Services. A key objective is to
    offer a straightforward, flexible and suitable route to market for
    Scottish public sector bodies. See section III.1.1) for details of
    public sector organisations who can access the DPS. No form of volume
    guarantee has been granted by the Authority. The Authority shall not be
    bound to order any of the services referred to in the lot descriptions.
    The DPS will be open to entrants throughout its life who meet the
    minimum criteria.""",
    "en")