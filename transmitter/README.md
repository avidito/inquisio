# Transmitter

## Overview
`Transmitter` is a service to processed stream data and publish it to another Pub/Sub topics. `Transmitter` will only cleaning and add some metadata to stream data. Then this stream data will be forwarded to another topics that open to public. User can subscribe to this topic to get real-time data.

![Transmitter](../docs/transmitter.png)

### Installation
1. Install requirements from `requirements.txt` in `Transmitter` directory.
```sh
pip install -r requirements.txt
```

2. Run `main.py` script.
```sh
python main.py
```
