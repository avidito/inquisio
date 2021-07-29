from datetime import datetime

def remove_duplicate(data, header, pk):
    """Removing duplicate data based on its table primary key"""

    check = set()
    pk_id = [header.index(key) for key in pk]
    cln_data = []
    for row in data:
        row_pk_value = tuple(row[i] for i in pk_id)
        if (row_pk_value in check):
            continue
        else:
            cln_data.append(row)
            check.add(row_pk_value)
    return cln_data

def log_process(func):
    """Logging wrapper to add time data"""

    def wrapper(table_name, **params):
        time_namespace = datetime.now().strftime("[%Y-%m-%d %H:%M:%S]")
        message = f"Running `{func.__name__}` process for `{table_name}`"
        print(f"{time_namespace} {message}")
        result = func(table_name, **params)
        return result
    return wrapper
