from utils import logging, get_params, get_data, check_dir_path
from database import engine
from process import process_data
from load import load_data_to_db
from transformer import build_dw

if __name__ == "__main__":
    # Get parameters
    dir_params, db_params = get_params()
    dmp_path = dir_params["DMP_PATH"]
    tmp_path = dir_params["TMP_PATH"]
    sql_path = dir_params["SQL_PATH"]

    table_list = db_params["TABLE_LIST"]
    map_categories = db_params["MAP_CATEGORIES"]
    username = db_params["USERNAME"]
    password = db_params["PASSWORD"]
    hostname = db_params["HOSTNAME"]
    port = db_params["PORT"]
    database = db_params["DATABASE"]

    logging(f"Start loader. Get data from dmp folder")
    db_session = engine.session_factory(username, password, hostname, port, database)
    today_data = get_data(dmp_path, offset=0)
    yesterday_data = get_data(dmp_path, offset=-1)

    if (today_data or yesterday_data):
        logging(f"Processing SRC data")
        process_data([*today_data, *yesterday_data], tmp_path, map_categories)

        logging(f"Start loading SRC data")
        load_data_to_db(tmp_path, table_list, db_session)

        logging(f"Start building DW data")
        build_dw(sql_path, db_session)
