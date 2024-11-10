def METRICS_COMPUTE():
    return {
        "sm__throughput.avg.pct_of_peak_sustained_elapsed": "Compute (SM) Throughput",
        "gpu__time_duration.sum": "Duration",
        "gpu__compute_memory_throughput.avg.pct_of_peak_sustained_elapsed": "Memory Throughput",
        "gpc__cycles_elapsed.max": "Elapsed Cycles",
        "l1tex__throughput.avg.pct_of_peak_sustained_active": "L1/TEX Cache Throughput",
        "lts__throughput.avg.pct_of_peak_sustained_elapsed": "L2 Cache Throughput",
        "gpu__dram_throughput.avg.pct_of_peak_sustained_elapsed": "DRAM Throughput",
        "launch__waves_per_multiprocessor": "Waves Per SM",
        "sm__inst_executed_pipe_tensor_op_dmma": "# of warp instructions executed by tensor pipe (DMMA ops)",
        "sm__inst_executed_pipe_tensor_op_gmma": "# of warp instructions executed by tensor pipe",
        "sm__inst_executed_pipe_tensor_op_hmma": "# of warp instructions executed by tensor pipe",
        "sm__inst_executed_pipe_tensor_op_hmma_type_hfma2": "# of warp instructions executed by tensor pipe (HFMA2.MMA ops)",
        "sm__inst_executed_pipe_tensor_op_imma": "# of warp instructions executed by tensor pipe (IMMA/IGMMA/BMMA/BGMMA)"
    }


def METRICS_ROOFLINE():
    return {
        "dram__bytes.sum": "# of Bytes",
        "smsp__inst_executed.sum": "# of Insts",
        "sm__sass_thread_inst_executed_op_integer_pred_on.sum.peak_sustained": "Peak Inst/Cycle (INT)",
    }


def METRICS_MEMORY():
    return {
        "sm__memory_throughput.avg.pct_of_peak_sustained_elapsed": "Mem Pipes Busy",
        "smsp__sass_inst_executed_op_memory_8b.sum": "8-bit Mem Inst",
        "smsp__sass_inst_executed_op_memory_16b.sum": "16-bit Mem Inst",
        "smsp__sass_inst_executed_op_memory_32b.sum": "32-bit Mem Inst",
        "smsp__sass_inst_executed_op_memory_64b.sum": "64-bit Mem Inst",
        "smsp__sass_inst_executed_op_memory_128b.sum": "128-bit Mem Inst",
        # L1 cache
        "l1tex__t_sectors_pipe_lsu_mem_global_op_ld.sum": "# Sec L1 (Global Load)",
        "l1tex__t_sectors_pipe_lsu_mem_global_op_st.sum": "# Sec L1 (Global Store)",
        "l1tex__t_sectors_pipe_lsu_mem_local_op_ld.sum": "# Sec L1 (Local Load)",
        "l1tex__t_sectors_pipe_lsu_mem_local_op_st.sum": "# Sec L1 (Local Store)",
        "l1tex__t_requests_pipe_lsu_mem_global_op_ld.sum": "# Req L1 (Global Load)",
        "l1tex__t_requests_pipe_lsu_mem_global_op_st.sum": "# Req L1 (Global Store)",
        "l1tex__t_requests_pipe_lsu_mem_local_op_ld.sum": "# Req L1 (Local Load)",
        "l1tex__t_requests_pipe_lsu_mem_local_op_st.sum": "# Req L1 (Local Store)",
        # L2 cache
        "lts__t_sectors_srcunit_tex_op_read.sum": "# Sec L2 Load",
        "lts__t_sectors_srcunit_tex_op_write.sum": "# Sec L2 Store",
        "lts__t_requests_srcunit_tex_op_read.sum": "# Req L2 Load",
        "lts__t_requests_srcunit_tex_op_write.sum": "# Req L2 Store",
        "lts__t_sectors_srcunit_tex_op_read_lookup_hit.sum": "# L2 Load Hit",
        "lts__t_sectors_srcunit_tex_op_read_lookup_miss.sum": "# L2 Load Misses",
        # cache
        "LTS.TriageCompute.lts__average_t_sector_hit_rate_realtime" : "hit rate",
        "LTS.TriageCompute.lts__average_t_sector_hit_rate_srcunit_tex_realtime" : "hit rate",
        "SM_B.TriageCompute.l1tex__t_sector_hit_rate" : "hit rate",
        "idc__request_hit_rate" : "hit rate",
        "l1tex__t_sector_hit_rate" : "hit rate",
        "l1tex__t_sector_pipe_lsu_hit_rate" : "hit rate",
        "l1tex__t_sector_pipe_lsu_mem_global_op_atom_hit_rate" : "hit rate",
        "l1tex__t_sector_pipe_lsu_mem_global_op_ld_hit_rate" : "hit rate",
        "l1tex__t_sector_pipe_lsu_mem_global_op_ldgsts_cache_access_hit_rate" : "hit rate",
        "l1tex__t_sector_pipe_lsu_mem_global_op_red_hit_rate" : "hit rate",
        "l1tex__t_sector_pipe_lsu_mem_global_op_st_hit_rate" : "hit rate",
        "l1tex__t_sector_pipe_lsu_mem_lg_hit_rate" : "hit rate",
        "l1tex__t_sector_pipe_lsu_mem_local_op_ld_hit_rate" : "hit rate",
        "l1tex__t_sector_pipe_lsu_mem_local_op_st_hit_rate" : "hit rate",
        "l1tex__t_sector_pipe_tex_hit_rate" : "hit rate",
        "l1tex__t_sector_pipe_tex_mem_surface_hit_rate" : "hit rate",
        "l1tex__t_sector_pipe_tex_mem_surface_op_atom_hit_rate" : "hit rate",
        "l1tex__t_sector_pipe_tex_mem_surface_op_ld_hit_rate" : "hit rate",
        "l1tex__t_sector_pipe_tex_mem_surface_op_red_hit_rate" : "hit rate",
        "l1tex__t_sector_pipe_tex_mem_surface_op_st_hit_rate" : "hit rate",
        "l1tex__t_sector_pipe_tex_mem_texture_hit_rate" : "hit rate",
        "l1tex__t_sector_pipe_tex_mem_texture_op_ld_hit_rate" : "hit rate",
        "l1tex__t_sector_pipe_tex_mem_texture_op_tex_hit_rate" : "hit rate",
        "lts__t_request_hit_rate" : "hit rate",
        "lts__t_sector_hit_rate" : "hit rate",
        "lts__t_sector_op_atom_dot_alu_hit_rate" : "hit rate",
        "lts__t_sector_op_atom_dot_cas_hit_rate" : "hit rate",
        "lts__t_sector_op_atom_hit_rate" : "hit rate",
        "lts__t_sector_op_read_hit_rate" : "hit rate",
        "lts__t_sector_op_red_hit_rate" : "hit rate",
        "lts__t_sector_op_write_hit_rate" : "hit rate",

    }


def METRICS_OCCUPANCY():
    return {
        "sm__maximum_warps_per_active_cycle_pct": "Theoretical Occupancy",
        "sm__maximum_warps_avg_per_active_cycle": "Theoretical Active Warps Per SM",
        "sm__warps_active.avg.pct_of_peak_sustained_active": "Achieved Occupancy",
        "sm__warps_active.avg.per_cycle_active": "Achieved Active Warps Per SM",
        "launch__occupancy_limit_registers": "Block Limit Registers",
        "launch__occupancy_limit_shared_mem": "Block Limit Shared Mem",
        "launch__occupancy_limit_warps": "Block Limit Warp",
        "launch__occupancy_limit_blocks": "Block Limit SM",
    }


def METRICS_INSTRUCTION():
    return {
        "smsp__inst_executed.sum": "Executed Insts",
        "smsp__inst_issued.sum": "Issued Insts",
        "smsp__inst_executed.avg": "Avg. Executed Insts Per Scheduler",
        "smsp__inst_issued.avg": "Avg. Issued Insts Per Scheduler",
    }


def METRICS_SCHEDULER():
    return {
        "smsp__warps_active.avg.per_cycle_active": "Active Warps Per Scheduler",
        "smsp__warps_eligible.avg.per_cycle_active": "Eligible Warps Per Scheduler",
        "smsp__issue_active.avg.per_cycle_active": "Issued Warps Per Scheduler",
        "smsp__issue_inst0.avg.pct_of_peak_sustained_active": "No Eligible",
        "smsp__issue_active.avg.pct_of_peak_sustained_active": "One or More Eligible",
        "smsp__warps_active.avg.peak_sustained": "GPU Maximum Warps Per Scheduler",
        "smsp__maximum_warps_avg_per_active_cycle": "Theoretical Warps Per Scheduler",
    }


def METRICS_BRANCH():
    return {
        "smsp__inst_executed_op_branch.sum": " # Branch Insts",
        "smsp__sass_average_branch_targets_threads_uniform.pct": "Branch Efficiency",
    }