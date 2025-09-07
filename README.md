# Probe CPU program's performance

A set of scripts for profiling CPU program performance including：

* FLOP
* Cache access
* DRAM access
* arithmetic intensity
* computation complexity
* ...

## requirement

make sure you are working on a physical machine

* perf

``` bash
sudo apt update
sudo apt install linux-tools-generic
```

or on WSL2:

``` bash
wget https://mirrors.edge.kernel.org/pub/linux/kernel/tools/perf/<perf-version>.tar.gz
tar -xzvf perf-<version>.tar.gz
cd perf-<version>/tools/perf
make -j
./perf --version
sudo make install
```

* python packages: numpy, pandas

## example program

compile

``` bash
g++ -o GeMM -O3 -std=c++11 GeMM.cpp
```

usage

``` bash
./GeMM <M> <K> <N> # (M,K) (K,N) -> (M,N)
```

## analysis

