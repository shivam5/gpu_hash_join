#!/usr/bin/env python3
import os
import argparse
import subprocess as subp
import pandas as pd
from ncu_metrics import *

def format_metrics_output(txt_file):
    """Format the metrics from txt file into a readable report."""
    try:
        # Read txt file
        df = pd.read_txt(txt_file)
        
        # Create formatted output
        output = ["=== NCU Profiling Results ===\n"]
        
        # Group metrics by category
        metric_groups = {
            "Compute": METRICS_COMPUTE(),
            "Memory": METRICS_MEMORY(),
            "Roofline": METRICS_ROOFLINE(),
            "Instruction": METRICS_INSTRUCTION(),
            "Scheduler": METRICS_SCHEDULER(),
            "Occupancy": METRICS_OCCUPANCY(),
            "Branch": METRICS_BRANCH()
        }
        
        for group_name, metrics in metric_groups.items():
            output.append(f"\n{group_name} Metrics:")
            output.append("-" * (len(group_name) + 8))
            
            for metric in metrics.keys():
                if metric in df.columns:
                    value = df[metric].iloc[0]  # Get the first value
                    description = metrics[metric]
                    output.append(f"{metric}:")
                    output.append(f"  Value: {value}")
                    output.append(f"  Description: {description}\n")
        
        return "\n".join(output)
    except Exception as e:
        return f"Error formatting metrics: {str(e)}"

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--bin", required=True, help="Binary executable.")
    parser.add_argument("--extra-args", default="", help="Additional arguments to pass to profiler.")
    parser.add_argument("--output", default="ncu-perf", help="Base output file name.")
    parser.add_argument("--format", choices=['nsight', 'text', 'both'], default='both',
                      help="Output format: 'nsight' for .ncu-rep file, 'text' for readable metrics, 'both' for both outputs")
    args = parser.parse_args()

    # Base metrics command
    metrics = []
    metrics.extend(list(METRICS_COMPUTE().keys()))
    metrics.extend(list(METRICS_MEMORY().keys()))
    metrics.extend(list(METRICS_ROOFLINE().keys()))
    metrics.extend(list(METRICS_INSTRUCTION().keys()))
    metrics.extend(list(METRICS_SCHEDULER().keys()))
    metrics.extend(list(METRICS_OCCUPANCY().keys()))
    metrics.extend(list(METRICS_BRANCH().keys()))
    
    metrics_str = ",".join(metrics)
    bin_cmd = (args.bin).strip('"').strip("'")

    # Generate both NSight and text outputs
    if args.format == 'both':
        # First run: NSight output
        nsight_output = f"{args.output}.ncu-rep"
        cmd_nsight = f"ncu --metrics {metrics_str} --target-processes all -f -o {nsight_output} {args.extra_args} {bin_cmd}"
        
        print("Generating NSight report...")
        print(cmd_nsight)
        
        with open(".tmp_nsight.sh", "w") as f:
            f.write(cmd_nsight)
            f.flush()

        out = subp.Popen(
            "bash .tmp_nsight.sh".split(" "),
            stdin=subp.PIPE,
            stdout=subp.PIPE,
            stderr=subp.STDOUT,
        ).communicate()
        print(out[0].decode())
        os.remove(".tmp_nsight.sh")

        # Second run: txt for text output
        txt_output = f"{args.output}.txt"
        cmd_txt = f"ncu --metrics {metrics_str} --target-processes all {args.extra_args} {bin_cmd}"
        
        print("\nGenerating text report...")
        print(cmd_txt)
        
        with open(".tmp_txt.sh", "w") as f:
            f.write(cmd_txt)
            f.flush()

        out = subp.Popen(
            "bash .tmp_txt.sh".split(" "),
            stdin=subp.PIPE,
            stdout=subp.PIPE,
            stderr=subp.STDOUT,
        ).communicate()
        print(out[0].decode())
        os.remove(".tmp_txt.sh")

        print(f"\nOutputs generated:")
        print(f"NSight report: {nsight_output}")

    elif args.format == 'nsight':
        # Only NSight output
        cmd = f"ncu --metrics {metrics_str} --target-processes all -f -o {args.output} {args.extra_args} {bin_cmd}"
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

    else:  # text format
        # Only text output
        txt_output = f"{args.output}.txt"
        cmd = f"ncu --metrics {metrics_str} --target-processes all {args.extra_args} {bin_cmd}"
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