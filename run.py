import argparse
import logging
import sys
import time
import json
import os

import pandas as pd
import numpy as np
import yaml


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

    # Load config
    try:
        with open(args.config, "r") as f:
            config = yaml.safe_load(f)

        seed = config["seed"]
        window = config["window"]
        version = config["version"]

        np.random.seed(seed)

        logging.info(f"Config loaded successfully: seed={seed}, window={window}, version={version}")

    except Exception as e:
        error_output = {
            "version": "v1",
            "status": "error",
            "error_message": str(e)
        }
    # Validate input file
    if not os.path.exists(args.input):
        error_output = {
            "version": version,
            "status": "error",
            "error_message": "Input file does not exist"
        }
        print(json.dumps(error_output))
        sys.exit(1)

    try:
        df = pd.read_csv(args.input)
        logging.info(f"CSV loaded successfully with {len(df)} rows")

    except Exception as e:
        error_output = {
            "version": version,
            "status": "error",
            "error_message": f"Failed to read CSV: {str(e)}"
        }
        print(json.dumps(error_output))
        sys.exit(1)

    if df.empty:
        error_output = {
            "version": version,
            "status": "error",
            "error_message": "Input CSV is empty"
        }
        print(json.dumps(error_output))
        sys.exit(1)

    if "close" not in df.columns:
        error_output = {
            "version": version,
            "status": "error",
            "error_message": "Missing 'close' column in CSV"
        }
        print(json.dumps(error_output))
        sys.exit(1)

    # Compute rolling mean
    df["rolling_mean"] = df["close"].rolling(window=window).mean()
    logging.info("Rolling mean calculated")

    # Generate signal
    df["signal"] = (df["close"] > df["rolling_mean"]).astype(int)
    logging.info("Signal column generated")
    # Calculate metrics
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

    # Write output JSON file
    with open(args.output, "w") as f:
        json.dump(output_data, f, indent=4)

    logging.info(f"Metrics calculated: {output_data}")
    logging.info("Job completed successfully")

    # Print JSON to stdout
    print(json.dumps(output_data))
if __name__ == "__main__":
    main()