import os
import time
import glob
import requests
import gzip
import pandas as pd

def download_zip(url, save_path, chunk_size=128):
    r = requests.get(url, stream=True)
    with open(save_path, "wb") as fd:
        for chunk in r.iter_content(chunk_size=chunk_size):
            fd.write(chunk)

def get_data_url(url):
    r = requests.get(url)
    if r.status_code == 200:
        if r.json()["urls"]:
            return r.json()["urls"][0]["url"]
    return None
def trade_link(endpoint, exchange, instrument, starttime):
    """
    starttime: YYYY-mm-dd
    """
    base_url = f"/trade/{exchange}/{instrument}?startTime={starttime}"
    return endpoint + base_url


def gz_path(exchange, instrument, date, save_dir):
    return os.path.join(f"{save_dir}", f"{exchange}_{instrument}_{date}.gz")


def get_execution_gz(endpoint, exchange, instrument, date, save_dir, download_anyway):
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)

    gzpath = gz_path(exchange, instrument, date, save_dir)
    if os.path.exists(gzpath) and not download_anyway:
        print(
            f"{gzpath} exits. Since download_anyway option is False, Will not Download"
        )
        return

    cryptochassis_trade_api_url = trade_link(endpoint, exchange, instrument, date)
    gz_url = get_data_url(cryptochassis_trade_api_url)

    print(f"DOWNLOADING {endpoint}, {exchange}, {instrument}, {date} TO {gzpath}")
    download_zip(gz_url, gzpath)


def gz_to_dataframe(gzfile):
    with open(gzfile, "rb") as fd:
        gzip_fd = gzip.GzipFile(fileobj=fd)
        df = pd.read_csv(gzip_fd)
        instrument = os.path.basename(gzfile).split("_")[1]
        df["instrument"] = instrument
        df["datetime"] = pd.to_datetime(df["time_seconds"], unit="s", utc=True)
        df = df.set_index("datetime")
        df = df.drop_duplicates()

    return df


# if __name__ == "__main__":
#     endpoint = "https://api.cryptochassis.com/v1"
#     exchange = "binance"
#     instruments = ["eth-eur", "btc-eur"]
#     dates = pd.date_range("2022-03-01", "2022-03-28")
#     # save_dir = "./data/binance/gz"
#     save_dir = "/tmp/binance/gz"
#     download_anyway = True

#     for date in dates:
#         for instrument in instruments:
#             get_execution_gz(endpoint, exchange, instrument, date, save_dir, download_anyway)
#             time.sleep(1)

if __name__ == "__main__":
    save_dir = "/tmp/binance/gz"
    instruments = ["eth-eur", "btc-eur"]
    exchange = "binance"
    for instrument in instruments:
        l = [gz_to_dataframe(gz) for gz in glob.glob(os.path.join(save_dir, f"{exchange}_{instrument}_*.gz"))]
        df = pd.concat(l)
        pd.to_pickle(df, os.path.join(save_dir, f"{exchange}_{instrument}.pkl"))




         
    