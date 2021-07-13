########## SCRAPER CONFIGURATION ##########
DELAY = 10
SCRAPER_META = {
    # "okezone": [
    #     ("bola", "https://bola.okezone.com/indeks/"),
    #     ("travel", "https://travel.okezone.com/indeks")
    # ],
    "sindonews": [
        # ("daerah", "https://index.sindonews.com/index/7"),
        # ("international", "https://index.sindonews.com/index/9"),
        # ("sports", "https://index.sindonews.com/index/10"),
        ("edukasi", "https://index.sindonews.com/index/144")
    ]
}

########## PRODUCER CONFIGURATION ##########
TOPIC = "python-test"
BOOTSTRAP_SERVER = "localhost:9092"
