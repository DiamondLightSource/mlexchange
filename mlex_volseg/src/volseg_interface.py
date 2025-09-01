#!/usr/bin/env python3
import argparse
import subprocess
import sys
from pathlib import Path
from generate_volseg_settings import generate_volseg_settings
def run_command(command: list, use_shell=False):
    try:
        if use_shell:
            command_str = ' '.join(command)
            result = subprocess.run(
                command_str,
                shell=True,
                check=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
        else:
            result = subprocess.run(
                command,
                check=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
        print(result.stdout)
    except subprocess.CalledProcessError as e:
        print(f"Error: Command failed with exit code {e.returncode}", file=sys.stderr)
        print(e.stderr, file=sys.stderr)
        sys.exit(e.returncode)
def check_files_exist(paths):
    for path in paths:
        if not Path(path).is_file():
            print(f"Error: File not found — {path}", file=sys.stderr)
            sys.exit(2)
def do_train(data_files, label_files):
    check_files_exist(data_files + label_files)
    print("Generating training settings...")
    generate_volseg_settings("train")
    print("Running training...")
    data_args = ' '.join(f'"{f}"' for f in data_files)  # Quote file paths
    label_args = ' '.join(f'"{f}"' for f in label_files)
    command = f"model-train-2d --data {data_args} --labels {label_args}"
    run_command([command], use_shell=True)
def do_predict(model_file, volume_file):
    check_files_exist([model_file, volume_file])
    print("Generating prediction settings...")
    generate_volseg_settings("predict")
    print("Running prediction...")
    command = f'model-predict-2d "{model_file}" "{volume_file}"'
    run_command([command], use_shell=True)
    
def main():
    parser = argparse.ArgumentParser(description="Volume Segmantics CLI Wrapper")
    subparsers = parser.add_subparsers(dest="command", required=True)
    train_parser = subparsers.add_parser("train", help="Train a model")
    train_parser.add_argument("--data", nargs="+", required=True)
    train_parser.add_argument("--labels", nargs="+", required=True)
    predict_parser = subparsers.add_parser("predict", help="Predict using trained model")
    predict_parser.add_argument("--model", required=True)
    predict_parser.add_argument("--volume", required=True)
    args = parser.parse_args()
    if args.command == "train":
        do_train(args.data, args.labels)
    elif args.command == "predict":
        do_predict(args.model, args.volume)
if __name__ == "__main__":
    main()