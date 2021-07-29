from utils import logging, get_params, get_data, check_dir_path
from process import process_data
from load import load_data_to_db

if __name__ == "__main__":
    params = get_params()
    dmp_path = params["DMP_PATH"]
    tmp_path = params["TMP_PATH"]

    logging(f"Start loader with: {params}")
    today_data = get_data(dmp_path, offset=0)
    yesterday_data = get_data(dmp_path, offset=-1)
    if (today_data or yesterday_data):
        logging(f"Processing `{'today' if (today_data) else 'yesterday'}` data")
        process_data([*today_data, *yesterday_data], tmp_path)

        logging(f"Startloading  `{'today' if (today_data) else 'yesterday'}` data")
        load_data_to_db(params)
