from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS
import subprocess
import time
import os

token = os.environ.get("INFLUXDB_TOKEN")
org = os.environ.get("INFLUXDB_ORG")
url = os.environ.get("INFLUXDB_URL")
bucket = os.environ.get("INFLUXDB_BUCKET")
write_client = InfluxDBClient(url=url, token=token, org=org)
write_api = write_client.write_api(write_options=SYNCHRONOUS)


def run_speedtest():
    result = subprocess.run(
        ["./speedtest", "--accept-license", "--accept-gdpr"],
        capture_output=True,
        text=True,
    )
    lines = result.stdout.split("\n")

    download_speed = -1.0
    upload_speed = -1.0
    for line in lines:
        if "Download:" in line:
            download_speed = float(line.split(":")[1].strip().split()[0])
        elif "Upload:" in line:
            upload_speed = float(line.split(":")[1].strip().split()[0])

    return download_speed, upload_speed


while True:
    try:
        print(
            f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] Starting the speedtest...",
            flush=True,
        )
        download_speed, upload_speed = run_speedtest()
        print(
            f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] Download: {download_speed} MB/s, Upload: {upload_speed} MB/s",
            flush=True,
        )
        point = (
            Point("speedtest")
            .field("download", download_speed)
            .field("upload", upload_speed)
        )
        write_api.write(bucket=bucket, org=org, record=point)
    except Exception as e:
        print(
            f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] Failed to write to InfluxDB: {e}",
            flush=True,
        )

    # Every hour
    time.sleep(60 * 60)
