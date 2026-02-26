import argparse
import logging
import sys
import time
import json
import os

import pandas as pd
import numpy as np
import yaml


def write_error(output_path, version, message):
    print("WRITING ERROR FILE")
    error_output = {
        "version": version,
        "status": "error",
        "error_message": message
    }

    with open(output_path, "w") as f:
        json.dump(error_output, f, indent=4)

    logging.error(message)
    print(json.dumps(error_output))
    sys.exit(1)


def main():
    parser = argparse.ArgumentParser(description="Deterministic Rolling Signal Pipeline")

    parser.add_argument("--input", required=True, help="Path to input CSV file")
    parser.add_argument("--config", required=True, help="Path to config YAML file")
    parser.add_argument("--output", required=True, help="Path to output metrics JSON file")
    parser.add_argument("--log-file", required=True, help="Path to log file")

    args = parser.parse_args()

    logging.basicConfig(
        filename=args.log_file,
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s"
    )

    logging.info("Job started")
    start_time = time.time()

    # ----------------------
    # Load + Validate Config
    # ----------------------
    try:
        with open(args.config, "r") as f:
            config = yaml.safe_load(f)

        seed = config["seed"]
        window = config["window"]
        version = config["version"]

        np.random.seed(seed)

        logging.info(f"Config loaded successfully: seed={seed}, window={window}, version={version}")

    except Exception as e:
        write_error(args.output, "v1", f"Config error: {str(e)}")

    # ----------------------
    # Validate Input File
    # ----------------------
    if not os.path.exists(args.input):
        write_error(args.output, version, "Input file does not exist")

    # ----------------------
    # Load CSV
    # ----------------------
    try:
        df = pd.read_csv(args.input)
        logging.info(f"CSV loaded successfully with {len(df)} rows")

    except Exception as e:
        write_error(args.output, version, f"Invalid CSV format: {str(e)}")

    if df.empty:
        write_error(args.output, version, "Input CSV is empty")

    if "close" not in df.columns:
        write_error(args.output, version, "Missing 'close' column in CSV")

    # ----------------------
    # Rolling Mean
    # ----------------------
    df["rolling_mean"] = df["close"].rolling(window=window).mean()
    logging.info("Rolling mean calculated")

    # ----------------------
    # Signal
    # ----------------------
    df["signal"] = (df["close"] > df["rolling_mean"]).astype(int)
    logging.info("Signal column generated")

    # ----------------------
    # Metrics
    # ----------------------
    rows_processed = len(df)
    signal_rate = float(df["signal"].mean())
    latency_ms = int((time.time() - start_time) * 1000)

    output_data = {
        "version": version,
        "rows_processed": rows_processed,
        "metric": "signal_rate",
        "value": signal_rate,
        "latency_ms": latency_ms,
        "seed": seed,
        "status": "success"
    }

    # Write metrics file
    with open(args.output, "w") as f:
        json.dump(output_data, f, indent=4)

    logging.info(f"Metrics calculated: {output_data}")
    logging.info("Job completed successfully")

    print(json.dumps(output_data))


if __name__ == "__main__":
    main()