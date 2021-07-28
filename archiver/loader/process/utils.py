from datetime import datetime
import csv
import os

def reconstruct_column_based(data_list):
    """Reconstruct data to column based"""

    fields = data_list[0].keys()
    value_list = [list(zip(*data.items()))[1] for data in data_list]
    values_transpose = list(zip(*value_list))
    data_col_format = {key: value for key, value in zip(fields, values_transpose)}
    return data_col_format

def reconstruct_row_based(data):
    """Reconstruct data to row based"""

    fields = data.keys()
    value_list = [values for _, values in data.items()]
    values_transpose = list(zip(*value_list))
    data_row_format = [fields, *values_transpose]
    return data_row_format

def vectorize(func):
    """Vectorize function"""

    def vec_func(data):
        result = [
            func(value) if (not isinstance(value, list)) else\
            [func(v) for v in value] \
            for value in data
        ]
        return result
    return vec_func

def log_process(func):
    """Logging wrapper to add time data"""

    def wrapper(*data):
        time_namespace = datetime.now().strftime("[%Y-%m-%d %H:%M:%S]")
        message = f"Running `{func.__name__}` process"
        print(f"{time_namespace} {message}")
        result = func(*data)
        return result
    return wrapper

def check_dir_path(path):
    """Check dump folder existence and create if the folder is not exist"""

    if (os.path.exists(path)):
        return True
    os.mkdir(path)

def export_dataset(dataset, path):
    """Export data"""
    check_dir_path(path)
    for label, data in dataset.items():
        exp_path = os.path.join(path, f"prc_{label}.csv")
        with open(exp_path, "w+", newline='') as file:
            writer = csv.writer(file)
            for row in data:
                writer.writerow(row)
