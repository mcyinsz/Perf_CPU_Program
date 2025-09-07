#!/bin/bash

if [ $# -lt 1 ]; then
    echo "usage: $0 <exe> [program params...]"
    exit 1
fi

# program path
PROGRAM=$2

# output path
OUTPUT_DIR=$1

# shift twice to get residual params
shift
shift

# perf event list
EVENTS="\
cycles,instructions,\
cache-references,cache-misses,\
LLC-loads,LLC-load-misses,LLC-stores,LLC-store-misses,\
L1-dcache-loads,L1-dcache-load-misses,L1-dcache-stores,\
dTLB-loads,dTLB-load-misses,\
# mem_inst_retired.all_loads,mem_inst_retired.all_stores,\
fp_arith_inst_retired.scalar_single,fp_arith_inst_retired.scalar_double,\
fp_arith_inst_retired.128b_packed_single,fp_arith_inst_retired.128b_packed_double,\
fp_arith_inst_retired.256b_packed_single,fp_arith_inst_retired.256b_packed_double,\
fp_arith_inst_retired.512b_packed_single,fp_arith_inst_retired.512b_packed_double,\
uops_executed.x87,uops_executed.core,uops_issued.any"

# using numactl binding to the first CPU node and its memory field
echo "probing performance events..."
echo "execute cmd: numactl --cpunodebind=0 --membind=0 $PROGRAM $@"

perf stat -e "$EVENTS" -o $OUTPUT_DIR numactl --cpunodebind=0 --membind=0 $PROGRAM "$@"
