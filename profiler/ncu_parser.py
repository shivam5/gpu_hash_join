#!/usr/bin/env python3

import argparse
import subprocess as subp

from collections import defaultdict

from ncu_metrics import *


def print_out(metrics_data_dict, metrics_dict):
    for metric, metric_label in metrics_dict.items():
        print(f"{metric_label}: {metrics_data_dict[metric]}")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--file-path", required=True, help="File path for report."
    )
    args = parser.parse_args()

    cmd = f"ncu --csv -i {args.file_path}"

    out, _ = subp.Popen(
        cmd.split(" "),
        stdin=subp.PIPE,
        stdout=subp.PIPE,
        stderr=subp.STDOUT,
    ).communicate()

    out = out.decode("utf-8")

    is_header = True

    fn_to_idx = defaultdict(lambda: int)
    per_kernel_metrics_dict = defaultdict(lambda: defaultdict(lambda: str))

    for line in out.split("\n"):
        if "WARNING" in line:
            continue
        if len(line) == 0:
            continue

        if is_header:
            for i, fn in enumerate(line.split(",")):
                fn = fn.strip('"')
                fn_to_idx[fn] = i
            is_header = False
        else:
            metrics_list = line.split('","')
            kernel_name = (
                metrics_list[fn_to_idx["Kernel Name"]].strip("'").strip('"')
            )
            metric_name = (
                metrics_list[fn_to_idx["Metric Name"]].strip("'").strip('"')
            )
            value = (
                metrics_list[fn_to_idx["Metric Value"]].strip("'").strip('"')
            )
            unit = metrics_list[fn_to_idx["Metric Unit"]].strip("'").strip('"')

            per_kernel_metrics_dict[kernel_name][
                metric_name
            ] = f"{value} {unit}"

    for kernel_name, per_kernel_dict in per_kernel_metrics_dict.items():
        print(f"{kernel_name}")
        print("-------------------------------------")
        print_out(per_kernel_dict, METRICS_COMPUTE())
        print("-------------------------------------")
        print_out(per_kernel_dict, METRICS_MEMORY())
        print("-------------------------------------")
        print_out(per_kernel_dict, METRICS_ROOFLINE())
        print("-------------------------------------")
        print_out(per_kernel_dict, METRICS_INSTRUCTION())
        print("-------------------------------------")
        print_out(per_kernel_dict, METRICS_SCHEDULER())
        print("-------------------------------------")
        print_out(per_kernel_dict, METRICS_OCCUPANCY())
        print("-------------------------------------")
        print_out(per_kernel_dict, METRICS_BRANCH())
        print("-------------------------------------")


if __name__ == "__main__":
    main()