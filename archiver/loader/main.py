from utils import logging, get_params, get_data, check_dir_path
from process import process_data
from load import load_data_to_db

if __name__ == "__main__":
    # Get parameters
    params = get_params()
    dmp_path = params["DMP_PATH"]
    tmp_path = params["TMP_PATH"]
    table_list = params["TABLE_LIST"]
    username = params["USERNAME"]
    password = params["PASSWORD"]
    hostname = params["HOSTNAME"]
    port = params["PORT"]
    database = params["DATABASE"]

    logging(f"Start loader. Get data from dmp folder")
    today_data = get_data(dmp_path, offset=0)
    yesterday_data = get_data(dmp_path, offset=-1)

    if (today_data or yesterday_data):
        logging(f"Processing `{'today' if (today_data) else 'yesterday'}` data")
        process_data([*today_data, *yesterday_data], tmp_path)

        logging(f"Startloading  `{'today' if (today_data) else 'yesterday'}` data")
        load_data_to_db(tmp_path, table_list, username, password, hostname, port, database)
