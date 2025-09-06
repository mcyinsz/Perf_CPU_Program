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

