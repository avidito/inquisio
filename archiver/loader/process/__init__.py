from .utils import reconstruct_column_based, reconstruct_row_based, export_dataset
from .processor import processor

def process_data(data, tmp_path):

    data_cf = reconstruct_column_based(data)
    dataset = processor(data_cf)
    data_rf = {table: reconstruct_row_based(data) for table, data in dataset.items()}

    export_dataset(data_rf, tmp_path)
