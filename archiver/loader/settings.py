##### DIRECTORY #####
DMP_PATH = "D:/Project/Inquisio/archiver/__dmp"
TMP_PATH = "D:/Project/Inquisio/archiver/__tmp"
SQL_PATH = "D:/Project/Inquisio/archiver/loader/transformer/sql"

##### DATABASE #####
TABLE_LIST = {
    "news": ["news_id"],
    "categories": ["category_id"],
    "contents": ["partition_id", "news_id"],
    "tags": ["tag_id"],
    "map_news_tags": ["news_id", "tag_id"]
}
MAP_CATEGORIES = {
    "news": ["news", "berita"],
    "finance": ["finance", "money", "economy"],
    "hype": ["hype"],
    "sport": ["sport", "bola", "sports"],
    "automotive": ["otomotif"],
    "travel": ["travel"],
    "trend": ["tren"],
    "tech": ["inet", "tekno", "techno", "autotechno"],
    "science": ["sains"],
    "education": ["edukasi"]
}
USERNAME = "inq_admin"
PASSWORD = "admin"
HOSTNAME = "localhost"
PORT = "5432"
DATABASE = "inquisio"
