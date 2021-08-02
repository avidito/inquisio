########## SCRAPER CONFIGURATION ##########
DELAY = 10
SCRAPER_META = {
    "detik": [
        ("news", "https://news.detik.com/indeks/"),
        # ("finance", "https://finance.detik.com/indeks/"),
        # ("sport", "https://sport.detik.com/indeks/"),
        # ("oto", "https://oto.detik.com/indeks/")
    ],
    "kompas": [
        ("news", "https://indeks.kompas.com/?site=news"),
        # ("tren", "https://indeks.kompas.com/?site=tren"),
        # ("hype", "https://indeks.kompas.com/?site=hype"),
        # ("money", "https://indeks.kompas.com/?site=money"),
        # ("bola", "https://indeks.kompas.com/?site=bola"),
        # ("tekno", "https://indeks.kompas.com/?site=tekno"),
        # ("sains", "https://indeks.kompas.com/?site=sains"),
        # ("edukasi", "https://indeks.kompas.com/?site=edukasi")
    ],
    "okezone": [
        ("news", "https://news.okezone.com/indeks", "GET"),
        # ("finance", "https://economy.okezone.com/indeks", "POST"),
        # ("bola", "https://bola.okezone.com/indeks/", "POST"),
        # ("sports", "https://sports.okezone.com/indeks", "GET"),
        # ("travel", "https://travel.okezone.com/indeks", "POST"),
        # ("techno", "https://techno.okezone.com/indeks", "POST")
    ],
    "sindonews": [
        ("nasional", "https://index.sindonews.com/index/5"),
        # ("metro", "https://index.sindonews.com/index/6"),
        # ("daerah", "https://index.sindonews.com/index/7"),
        # ("international", "https://index.sindonews.com/index/9"),
        # ("sports", "https://index.sindonews.com/index/10"),
        # ("edukasi", "https://index.sindonews.com/index/144"),
        # ("tekno", "https://index.sindonews.com/index/612")
    ]
}

EXCLUDED_URLS = {
    "detik": {
        "news": [
            "20.detik.com/",
            "https://news.detik.com/video/",
            "https://news.detik.com/detiktv/",
            "https://news.detik.com/foto-news/",
            "https://news.detik.com/infografis/",
            "https://news.detik.com/x/"
        ],
        "finance": [
            "20.detik.com/",
            "https://finance.detik.com/detiktv/*",
            "https://finance.detik.com/foto-bisnis/",
            "https://finance.detik.com/infografis/"
        ],
        "sport": [
            "20.detik.com/",
            "https://sport.detik.com/detiktv/",
            "https://sport.detik.com/fotosport/"
        ],
        "oto": [
            "20.detik.com/",
            "https://oto.detik.com/detiktv/"
        ]
    },
    "kompas": {
        "tekno": [
            "https://tekno.kompas.com/galeri/"
        ],
        "edukasi": [
            "https://edukasi.kompas.com/sekolah/",
            "https://edukasi.kompas.com/perguruan-tinggi/"
        ]
    },
    "okezone": {
        "news": [
            "https://news.okezone.com/play/",
            "https://news.okezone.com/view/",
            "https://news.okezone.com/detail/"
        ],
        "finance": [
            "https://news.okezone.com/play/",
            "https://news.okezone.com/view/",
            "https://promo.okezone.com/"
        ],
        "bola": [
            "https://bola.okezone.com/play",
            "https://bola.okezone.com/view"
        ],
        "sports": [
            "https://sports.okezone.com/play/",
            "https://sports.okezone.com/view/"
        ],
        "travel": [
            "https://travel.okezone.com/play",
            "https://travel.okezone.com/view"
        ],
        "techno": [
            "https://techno.okezone.com/play/",
            "https://techno.okezone.com/view/"
        ]
    },
    "sindonews": {}
}

########## PRODUCER CONFIGURATION ##########
TOPIC = "scraper-stream"
BOOTSTRAP_SERVER = "localhost:9092"
ACTIVE = False
