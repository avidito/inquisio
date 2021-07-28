import json

from process import (
    cvt_lowercase,
    clr_exc_whitespace,
    cvt_ts_to_datetime
)

def process_data(data):
    """Preprocess single result"""

    # Pipeline
    prc0_data = json.loads(data).copy()
    prc1_data = cvt_lowercase(prc0_data)
    prc2_data = clr_exc_whitespace(prc1_data)
    prc3_data = cvt_ts_to_datetime(prc2_data)

    result = prc3_data.copy()
    return result
