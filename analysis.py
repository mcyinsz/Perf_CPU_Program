#!/usr/bin/env python3

import re
import pandas as pd
import numpy as np
import os

GLOBAL_DATAFRAME_PATH = os.path.join(os.path.dirname(__file__), "global_dataframe_search.csv")

def parse_perf_results(filename):
    """parse perf output file"""
    results = {}
    with open(filename, 'r') as f:
        content = f.read()
    
    # re match performance counter
    pattern = r'(\d[\d,]*)\s+([\w\-:\.]+)'
    matches = re.findall(pattern, content)
    
    for value, key in matches:
        # transform to int
        value = int(value.replace(',', ''))
        results[key.strip()] = value
    
    return results

def get_time(filename):
    """
        the first string in last line
    """
    with open(filename, 'r') as f:
        lines = f.readlines()
    return float(lines[33 - 1].split()[0].strip()) # two empty tail lines

def calculate_arithmetic_intensity(results, cacheline_size=64):
    """calculat arithmetic intensity"""
    
    # grab basic information
    instructions = results.get('instructions', 0)
    inst_retired_any = results.get('inst_retired.any', instructions)
    uops_retired_all = results.get('uops_issued.any', 0)
    
    # grab floating-point metrics
    fp_scalar_single = results.get('fp_arith_inst_retired.scalar_single', 0)
    fp_scalar_double = results.get('fp_arith_inst_retired.scalar_double', 0)
    fp_128b_single = results.get('fp_arith_inst_retired.128b_packed_single', 0)
    fp_128b_double = results.get('fp_arith_inst_retired.128b_packed_double', 0)
    fp_256b_single = results.get('fp_arith_inst_retired.256b_packed_single', 0)
    fp_256b_double = results.get('fp_arith_inst_retired.256b_packed_double', 0)
    fp_512b_single = results.get('fp_arith_inst_retired.512b_packed_single', 0)
    fp_512b_double = results.get('fp_arith_inst_retired.512b_packed_double', 0)
    
    total_fp_ops = (
        fp_scalar_single * 1 +          # scalar single instruction：1 FLOP/ins
        fp_scalar_double * 1 +          # scalar double instruction：1 FLOP/ins
        fp_128b_single * 4 +           # 128 bit packed single instruction：4 FLOP/ins
        fp_128b_double * 2 +           # 128 bit packed double instruction：2 FLOP/ins
        fp_256b_single * 8 +           # 256 bit packed single instruction：8 FLOP/ins
        fp_256b_double * 4 +            # 256 bit packed double instructino：4 FLOP/指令
        fp_512b_single * 16 +
        fp_512b_double * 8
    )

    
    # memory access metrics
    cache_refs = results.get('cache-references', 0)
    cache_misses = results.get('cache-misses', 0)
    llc_loads = results.get('LLC-loads', 0)
    llc_stores = results.get('LLC-stores', 0)
    llc_load_misses = results.get('LLC-load-misses', 0)
    llc_store_misses = results.get('LLC-store-misses', 0)
    
    # calculate byte access amount
    dram_access_bytes = (llc_load_misses + llc_store_misses) * cacheline_size
    llc_access_bytes = (llc_loads + llc_stores) * cacheline_size
    total_cache_access_bytes = cache_refs * cacheline_size
    
    # calculate arithmetic intensity for floating point numbers
    ai_dram_fp = total_fp_ops / dram_access_bytes if dram_access_bytes > 0 else float('inf')
    ai_llc_fp = total_fp_ops / llc_access_bytes if llc_access_bytes > 0 else float('inf')
    ai_cache_fp = total_fp_ops / total_cache_access_bytes if total_cache_access_bytes > 0 else float('inf')
    
    return {
        'instructions': instructions,
        'inst_retired_any': inst_retired_any,
        'uops_retired_all': uops_retired_all,
        'cycles': results.get('cycles', 0),
        'fp_operations': total_fp_ops,
        'fp_scalar_single': fp_scalar_single,
        'fp_scalar_double': fp_scalar_double,
        'fp_128b_single': fp_128b_single,
        'fp_128b_double': fp_128b_double,
        'fp_256b_single': fp_256b_single,
        'fp_256b_double': fp_256b_double,
        'fp_512b_single': fp_512b_single,
        'fp_512b_double': fp_512b_double,
        'dram_access_bytes': dram_access_bytes,
        'llc_access_bytes': llc_access_bytes,
        'cache_access_bytes': total_cache_access_bytes,
        'ai_dram_fp': ai_dram_fp,
        'ai_llc_fp': ai_llc_fp,
        'ai_cache_fp': ai_cache_fp,
        'cache_miss_rate': cache_misses / cache_refs if cache_refs > 0 else 0
    }

def main(
    M: int,
    K:int, 
    N:int,
    target_result_raw:str
):
    
    # parse performance results
    results = parse_perf_results(target_result_raw)
    
    # get execution time
    time = get_time(target_result_raw)

    # calculate ai
    ai_metrics = calculate_arithmetic_intensity(results)
    
    # print results
    print("=" * 70)
    print("program arithmetic intensity analysis results")
    print("=" * 70)
    print(f"total instruction num: {ai_metrics['instructions']:,}")
    print(f"retired instrucction num: {ai_metrics['inst_retired_any']:,}")
    print(f"uop num: {ai_metrics['uops_retired_all']:,}")
    print(f"total cycle num: {ai_metrics['cycles']:,}")
    
    print("\nfloating point num:")
    print(f"  total FLOP: {ai_metrics['fp_operations']:,}")
    print(f"    scalar single FP: {ai_metrics['fp_scalar_single']:,}")
    print(f"    scalar double FP: {ai_metrics['fp_scalar_double']:,}")
    print(f"    128-bit packed single: {ai_metrics['fp_128b_single']:,}")
    print(f"    128-bit packed double: {ai_metrics['fp_128b_double']:,}")
    print(f"    256-bit packed single: {ai_metrics['fp_256b_single']:,}")
    print(f"    256-bit packed double: {ai_metrics['fp_256b_double']:,}")
    print(f"    512-bit packed single: {ai_metrics['fp_512b_single']:,}")
    print(f"    512-bit packed double: {ai_metrics['fp_512b_double']:,}")
    
    print(f"\nMemory access:")
    print(f"  DRAM access Byte num: {ai_metrics['dram_access_bytes']:,}")
    print(f"  LLC access Byte num: {ai_metrics['llc_access_bytes']:,}")
    print(f"  Cache access Byte num: {ai_metrics['cache_access_bytes']:,}")
    print(f"  Cache miss rate: {ai_metrics['cache_miss_rate']:.4f}")
    
    print("\nArithmetic intensity (for Floating point ops):")
    print(f"  to DRAM: {ai_metrics['ai_dram_fp']:.4f} FLOP/byte")
    print(f"  to LLC: {ai_metrics['ai_llc_fp']:.4f} FLOP/byte")
    print(f"  to Cache: {ai_metrics['ai_cache_fp']:.4f} FLOP/byte")
    print("=" * 70)

    print(f"actual GFLOPS: {ai_metrics['fp_operations']/time/1e9:.2f}")
    print("=" * 70)


    new_row = pd.DataFrame({
            "M": [M], 
            "K": [K], 
            "N": [N],
            "total_fp_ops": [ai_metrics['fp_operations']],
            "total_cache_access_bytes": [ai_metrics['cache_access_bytes']],
            "dram_access_bytes": [ai_metrics['dram_access_bytes']],
            "llc_access_bytes": [ai_metrics['llc_access_bytes']],
            "ai_dram_fp": [ai_metrics['ai_dram_fp']],
            "ai_llc_fp": [ai_metrics['ai_llc_fp']],
            "ai_cache_fp": [ai_metrics['ai_cache_fp']],
            "time": time,
            "actually_ops": ai_metrics['fp_operations']/time
        })

    if os.path.exists(GLOBAL_DATAFRAME_PATH):
        """
            M | K | N | total_fp_ops | total_cache_access_bytes | dram_access_bytes | llc_access_bytes | ai_dram_fp | ai_llc_fp | ai_cache_fp | time | actual_ops
        
        """
        df = pd.read_csv(GLOBAL_DATAFRAME_PATH)
        df = pd.concat([df, new_row], ignore_index=True)

    else:
        df = new_row

    df.to_csv(GLOBAL_DATAFRAME_PATH, index=False)

if __name__ == "__main__":

        # GeMM params
        M = 10
        K = 10
        N = 10

        current_dir = os.path.dirname(__file__)

        # measure perf bash script
        script_path = os.path.join(os.path.dirname(__file__), "measure_perf.sh")
        os.chmod(script_path, 0o755)

        # executable
        execute_path = os.path.join(os.path.dirname(__file__), "GeMM")
        assert os.path.exists(execute_path), f"execute file not found"
        
        # perf result dir
        result_dir = os.path.join(current_dir, "generated")
        os.makedirs(result_dir, exist_ok=True)

        # store perf result
        raw_result_path = os.path.join(result_dir,f"perf_GeMM_{M}_{K}_{N}.txt")

        # run perf 
        exit_code = os.system(script_path + " " + raw_result_path + " " + execute_path + " " + f"{M} {K} {N}")

        main(
            M,
            K,
            N,
            target_result_raw = raw_result_path
        )
        
