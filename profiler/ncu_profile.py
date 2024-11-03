#!/usr/bin/env python3
import os
import argparse
import subprocess as subp

from ncu_metrics import *


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--bin", required=True, help="Binary executable.")
    parser.add_argument("--extra-args", default="", help="Additional arguments to pass to profiler.")
    args = parser.parse_args()

    cmd = "ncu --metrics "
    cmd += ",".join(list(METRICS_COMPUTE().keys())) + ","
    cmd += ",".join(list(METRICS_MEMORY().keys())) + ","
    cmd += ",".join(list(METRICS_ROOFLINE().keys())) + ","
    cmd += ",".join(list(METRICS_INSTRUCTION().keys())) + ","
    cmd += ",".join(list(METRICS_SCHEDULER().keys())) + ","
    cmd += ",".join(list(METRICS_OCCUPANCY().keys())) + ","
    cmd += ",".join(list(METRICS_BRANCH().keys()))

    bin_cmd = (args.bin).strip('"').strip("'")
    cmd += f" --target-processes all -f -o ncu-perf {args.extra_args} {bin_cmd}"
    print(cmd)

    with open(".tmp.sh", "w") as f:
        f.write(cmd)
        f.flush()

    out = subp.Popen(
        "bash .tmp.sh".split(" "),
        stdin=subp.PIPE,
        stdout=subp.PIPE,
        stderr=subp.STDOUT,
    ).communicate()
    print(out[0].decode())

    os.remove(".tmp.sh")


if __name__ == "__main__":
    main()