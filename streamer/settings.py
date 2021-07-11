########## SCRAPER CONFIGURATION ##########
DELAY = 10
SCRAPER_META = {
    # "okezone": [
    #     ("bola", "https://bola.okezone.com/indeks/"),
    #     ("travel", "https://travel.okezone.com/indeks")
    # ],
    "sindonews": [
        ("daerah", "https://index.sindonews.com/index/7")
    ]
}

########## PRODUCER CONFIGURATION ##########
TOPIC = "python-test"
BOOTSTRAP_SERVER = "localhost:9092"
