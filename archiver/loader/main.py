from utils import logging, get_params, get_data, export_report
from process import process_data
from load import load_data

if __name__ == "__main__":
    params = get_params()
    tmp_path = params["TMP_PATH"]

    logging(f"Start loader with: {params}")
    today_data = get_data(tmp_path, offset=0)
    yesterday_data = get_data(tmp_path, offset=-1)
    # prc_data = process_data([*today_data, *yesteday_data])

    # report = load_data(prc_data)
    # export_report(report)
    # print(report)
