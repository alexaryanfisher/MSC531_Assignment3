# Exploring Memory Hierarchy Design

This repository contains my third assignment for MSCS532. It is a memory hierarchy experiment using the gem5 computer architecture simulator. This project implements and compares different cache configurations to analyze their impact on system performance through detailed cache hit rate analysis.

## Project Overview

This project demonstrates the implementation of various cache hierarchy configurations in gem5 and analyzes their performance characteristics. The experiment focuses on comparing L2 cache optimizations including size variations, associativity changes, and cache block size modifications to understand their impact on cache hit rates and overall system performance.

### **Part 1: Cache Configuration Implementation**
This section implements four distinct cache hierarchy configurations using gem5's timing simulation mode. Each configuration maintains identical L1 cache specifications while varying L2 cache parameters to isolate the impact of specific design choices.

### **Part 2: Analysis**  
This section collects and analyzes cache statistics including hit rates, miss rates, and access patterns for each configuration. The analysis provides insights into how different cache parameters affect memory hierarchy performance.

## Project Deliverables

`run_experiment.py`: Python script containing the complete gem5 simulation framework with cache hierarchy implementations and statistics collection for all four configurations.

`results_baseline.txt`: Results file containing cache hit rates and performance metrics for the baseline configuration (256kB L2, 16-way associative, 64B blocks).

`results_lrg_l2.txt`: Results file for the large L2 cache configuration (1MB L2, 16-way associative, 64B blocks).

`results_low_assoc.txt`: Results file for the reduced associativity configuration (256kB L2, 8-way associative, 64B blocks).

`results_lrg_block.txt`: Results file for the large block size configuration (256kB L2, 16-way associative, 128B blocks).

## Cache Configurations Tested

| Configuration | L2 Size | L2 Associativity | Block Size | Purpose |
|--------------|---------|------------------|------------|---------|
| Baseline | 256kB | 16-way | 64B | Reference configuration |
| Large L2 | 1MB | 16-way | 64B | Test capacity impact |
| Low Associativity | 256kB | 8-way | 64B | Test conflict miss reduction |
| Large Blocks | 256kB | 16-way | 128B | Test spatial locality improvement |

## Summary of Findings

The cache hierarchy experiment revealed important insights about memory system design and the relationship between cache parameters and performance. The analysis showed that for simple workloads like the "hello world" program used in testing, cache configuration changes had minimal impact on overall performance due to the program's small working set and brief execution time.

The L1 caches demonstrated high effectiveness across all configurations, achieving instruction cache hit rates of 96.8-98.1% and data cache hit rates of 93.3-95.6%. This indicates that the L1 cache design successfully captures the majority of memory accesses for this workload type.

The L2 cache analysis revealed hit rates of 0.3-0.9% across configurations, which is expected behavior since L2 only services L1 misses. The low L2 hit rates reflect the effectiveness of the L1 caches rather than poor L2 design. The larger block configuration showed modest improvements in L1 hit rates (98.1% instruction, 95.6% data) demonstrating the benefit of increased spatial locality capture.

Key observations include: The cache hierarchy effectively filters memory requests with L1 caches handling 93-97% of all memory accesses. L2 cache configuration changes showed minimal impact for simple workloads, suggesting that L1 cache optimization may be more critical for basic programs. Larger cache blocks demonstrated slight performance improvements by better exploiting spatial locality in memory access patterns.

The experiment successfully validated the gem5 simulation framework and demonstrated that cache hierarchy performance is highly dependent on workload characteristics. For more complex applications with larger working sets and varied access patterns, the cache configuration differences would likely show more pronounced performance impacts.

## System Requirements

- gem5
- Python 3
- X86 gem5 build
- gem5 test programs

## How to Run the Experiment

1. Setup gem5 environment
2. Clone or save experiment file
3. Run individual configurations
4. View Results
