########## SCRAPER CONFIGURATION ##########
DELAY = 10
SCRAPER_META = {
    "detik": [
        # ("finance", "https://finance.detik.com/indeks/"),
        # ("sport", "https://sport.detik.com/indeks/"),
        # ("oto", "https://oto.detik.com/indeks/")
    ],
    "kompas": [
        # ("tren", "https://indeks.kompas.com/?site=tren"),
        # ("bola", "https://indeks.kompas.com/?site=bola"),
        # ("sains", "https://indeks.kompas.com/?site=sains")
    ],
    "okezone": [
        # ("bola", "https://bola.okezone.com/indeks/"),
        # ("travel", "https://travel.okezone.com/indeks")
    ],
    "sindonews": [
        ("daerah", "https://index.sindonews.com/index/7"),
        # ("international", "https://index.sindonews.com/index/9"),
        # ("sports", "https://index.sindonews.com/index/10"),
        # ("edukasi", "https://index.sindonews.com/index/144")
    ]
}

EXCLUDED_URLS = {
    "detik": {
        "finance": [
            "20.detik.com/",
            "https://finance.detik.com/infografis/"
        ],
        "sport": [
            "20.detik.com/",
            "https://sport.detik.com/fotosport/"
        ],
        "oto": [
            "https://oto.detik.com/indeks/"
        ]
    },
    "kompas": {},
    "okezone": {
        "bola": [
            "https://bola.okezone.com/play",
            "https://bola.okezone.com/view"
        ],
        "travel": [
            "https://travel.okezone.com/play",
            "https://travel.okezone.com/view"
        ]
    },
}

########## PRODUCER CONFIGURATION ##########
TOPIC = "python-test"
BOOTSTRAP_SERVER = "localhost:9092"
ACTIVE = False
