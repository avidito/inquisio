import json

from .process import (
    cvt_lowercase,
    clr_symbol
)

def process_data(data):
    """Preprocess single result"""

    # Pipeline
    prc0_data = json.loads(data).copy()
    prc1_data = cvt_lowercase(prc0_data)
    prc2_data = clr_symbol(prc1_data)

    result = prc2_data.copy()
    return result
