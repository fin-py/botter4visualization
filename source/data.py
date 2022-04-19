import os
import io
import time
import glob
import requests
import gzip
import pandas as pd
import click


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


def depth_link(endpoint, exchange, instrument, starttime):
    """
    starttime: YYYY-mm-dd
    """
    base_url = f"/market-depth/{exchange}/{instrument}?startTime={starttime}"
    return endpoint + base_url


def gz_path(exchange, instrument, date, save_dir):
    return os.path.join(f"{save_dir}", f"{exchange}_{instrument}_{date}.gz")


def get_execution_gz(endpoint, exchange, instrument, date, save_dir, download_anyway):
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)

    gzpath = gz_path(exchange, instrument, date, save_dir)
    if os.path.exists(gzpath) and not download_anyway:
        print(f"{gzpath} exits. As download_anyway option is False, will not download")
        return

    cryptochassis_trade_api_url = trade_link(endpoint, exchange, instrument, date)
    gz_url = get_data_url(cryptochassis_trade_api_url)

    print(f"DOWNLOADING {endpoint}, {exchange}, {instrument}, {date} TO {gzpath}")
    download_zip(gz_url, gzpath)


def get_depth_gz(endpoint, exchange, instrument, date, save_dir, download_anyway):
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)

    gzpath = gz_path(exchange, instrument, date, save_dir)
    if os.path.exists(gzpath) and not download_anyway:
        print(f"{gzpath} exits. As download_anyway option is False, will not download")
        return

    cryptochassis_trade_api_url = depth_link(endpoint, exchange, instrument, date)
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


def format_dataframe_by_side(df, side):
    new_df = (
        df.loc[:, side]
        .str.split("|")
        .explode()
        .str.split("_", expand=True)
        .rename({0: "price", 1: "size"}, axis=1)
    )
    new_df = new_df.astype(float)
    new_df.loc[:, "timestamp"] = pd.to_datetime(df.loc[:, "timestamp"], unit="s")
    new_df.loc[:, "side"] = side
    new_df.set_index("timestamp", drop=False, inplace=True)
    new_df.index.name = None
    return new_df


def format_dataframe(df):
    new_df = pd.concat(
        [format_dataframe_by_side(df, "bid"), format_dataframe_by_side(df, "ask")]
    )
    return new_df.sort_index()


@click.group()
def cli():
    pass


@cli.command(help="download tick data")
@click.option("--exchange", default="binance", help="select exchange")
@click.option("--instrument", default="btc-eur", help="select market")
@click.option("--start", default="2022-03-14")
@click.option("--end", default="2022-03-27")
@click.option("--save_dir", default="./data/exec", help="select directory to save file")
@click.option(
    "--download_anyway",
    default=True,
    help="download evenif the same name file alreay exists",
)
def download_execution_files(
    exchange, instrument, start, end, save_dir, download_anyway
):
    endpoint = "https://api.cryptochassis.com/v1"
    dates = pd.date_range(start, end)

    for date in dates:
        get_execution_gz(
            endpoint, exchange, instrument, date, save_dir, download_anyway
        )
        time.sleep(1)


@cli.command(help="unzip tz and convert to pickle")
@click.option("--exchange", default="binance", help="select exchange")
@click.option("--instrument", default="btc-eur", help="select market")
@click.option(
    "-s", "--save_dir", default="./data/exec", help="select directory to save file"
)
def gz_to_pickle(exchange, instrument, save_dir):
    l = [
        gz_to_dataframe(gz)
        for gz in glob.glob(os.path.join(save_dir, f"{exchange}_{instrument}_*.gz"))
    ]
    df = pd.concat(l)
    pd.to_pickle(df, os.path.join(save_dir, f"{exchange}_{instrument}.pkl"))


@cli.command(help="download depth data")
@click.option("--exchange", default="binance", help="select exchange")
@click.option("--instrument", default="btc-eur", help="select market")
@click.option("--date", default="2022-03-14")
@click.option(
    "--save_dir", default="./data/depth", help="select directory to save file"
)
@click.option(
    "--download_anyway",
    default=True,
    help="download evenif the same name file alreay exists",
)
def download_depth_files(exchange, instrument, date, save_dir, download_anyway):
    endpoint = "https://api.cryptochassis.com/v1"
    get_depth_gz(endpoint, exchange, instrument, date, save_dir, download_anyway)
    gz_data = os.path.join(save_dir, f"{exchange}_{instrument}_{date}.gz")
    with gzip.open(gz_data, "rt") as f:
        csv_data = f.read()
    raw_df = pd.read_csv(io.StringIO(csv_data))
    raw_df.columns = "timestamp", "bid", "ask"
    df = format_dataframe(raw_df)
    df.to_pickle(os.path.join(save_dir, f"{exchange}_{instrument}_{date}.pkl"))


if __name__ == "__main__":
    cli()

