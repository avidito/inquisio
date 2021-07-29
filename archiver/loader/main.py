from utils import logging, get_params, get_data, check_dir_path, export_report
from process import process_data
from load import load_data_to_db

if __name__ == "__main__":
    params = get_params()
    dmp_path = params["DMP_PATH"]
    tmp_path = params["TMP_PATH"]

    logging(f"Start loader with: {params}")
    today_data = get_data(dmp_path, offset=0)
    yesterday_data = get_data(dmp_path, offset=-1)
    process_data([*today_data, *yesterday_data], tmp_path)

    load_data_to_db(params)
    # export_report(report)
    # print(report)
