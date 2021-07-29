##### DIRECTORY #####
DMP_PATH = "D:/Project/Inquisio/archiver/__dmp"
TMP_PATH = "D:/Project/Inquisio/archiver/__tmp"

##### DATABASE #####
TABLE_LIST = {
    "news": ["news_id"],
    "categories": ["category_id"],
    "contents": ["partition_id", "news_id"],
    "tags": ["tag_id"],
    "map_news_tags": ["news_id", "tag_id"]
}
USERNAME = "inq_admin"
PASSWORD = "admin"
HOSTNAME = "localhost"
PORT = "5432"
DATABASE = "inquisio"
