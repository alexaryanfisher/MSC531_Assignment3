# Implementation: gem5 X86 ISA 

## Implementation and Setup

In the intial set up of the gem5 simulation. The following steps were completed based on the guideline followed in the gem5 documentation (gem5, 2025). The simulation was ran in the Unbuntu 24.04 environment within WSL. 

The first step is updating the environment and installing dependencies needed. This is completed with the use of `sudo apt-get`. Figure 1 visualizes the specific code.

<strong>Figure 1</strong><br> 
<em> Checking for Updates and installing dependencies</em>
![Installing updates and dependencies](https://github.com/alexaryanfisher/MSC531_Assignment3/blob/main/images/step1.jpg "Step 1: Installing updates and dependencies")

The second setup is cloning the gem5 repository with the use of `git` as shown in Figure 2. 

<strong>Figure 2</strong><br> 
<em>Cloning gem5 repository</em>
![Cloning gem5 repository](https://github.com/alexaryanfisher/MSC531_Assignment3/blob/main/images/step2.jpg "Step 2: Cloning gem5 repository")

After toggling into the newly added gem5 directory, the gem5 simulation is build with the use of `scons` for the X86 ISA. The building process takes around 20 minutes to process.

<strong>Figure 3</strong><br> 
<em>Building gem5 for X86 ISA</em>
![Building gem5 X86 ISA ](https://github.com/alexaryanfisher/MSC531_Assignment3/blob/main/images/step3.jpg "Step 3: Building gem5 X86 ISA")

During the initial build there was one error captured, which was the missing precommit hooks. It was easily resolved by hitting enter, Figure 4. The build continued once the packages were installed.

<strong>Figure 4</strong><br> 
<em>Missing precommit error</em>
![Missing precommit error](https://github.com/alexaryanfisher/MSC531_Assignment3/blob/main/images/error1.jpg "Error 1: Missing precommit")

<strong>Figure 5</strong><br> 
<em>Successful completion of the build</em>
![Successful completion of the build](https://github.com/alexaryanfisher/MSC531_Assignment3/blob/main/images/step3comp.jpg "Step 3: Successful Completion")

The system was designed with a TimingSimpleCPU running at 3GHz and 8GB of DDR3_1600_8x8 memory. The baseline configuration consisted of two L1 caches: information (I) and data (D) caches. Each of these were 32kB in size and had 8-way associativity. In addition to the L1 caches, there was a shared L2 cache with 256kB with 16-way associativity and a block size of 64. All the system creation, parameters, and simulation scripts were included on the `configs/experiment/run_experiment.py` file.


# Optimization of Cache Parameters
To explore the different performance effects, the parameters of the L2 cache were adjusted. The different configurations included the following:
* Larger L2 size : The L2 cache size was increased from 256kB to 1MB.
* Lower Associativity: The associativity was adjusted from 16-way to 8-way
* Larger Block Size: The block size was doubled from 64 to 128.

Figure 6 provides a screenshot of the configuration scripts.

<strong>Figure 6</strong><br> 
<em>Configuration Scripts</em>

![Configuration Scripts](https://github.com/alexaryanfisher/MSC531_Assignment3/blob/main/images/configs.jpg "Configuration Scripts")

Each configuration was separately ran and exported to individual files for analysis. To run the scripts the following code was ran reflecting the separate changes.
```
./build/X86/gem5.opt configs/experiment/run_experiment.py --config=baseline

./build/X86/gem5.opt configs/experiment/run_experiment.py --config=lrg_l2

./build/X86/gem5.opt configs/experiment/run_experiment.py --config=low_assoc

./build/X86/gem5.opt configs/experiment/run_experiment.py --config=lrg_block
```
Figures 7-10 provide the outputs from each simulation run.

<strong>Figure 7</strong><br> 
<em>Simulation Output of Baseline Cache Parameters</em>
![Simulation Output of Baseline](https://github.com/alexaryanfisher/MSC531_Assignment3/blob/main/images/baseline.jpg "Simulation Output of Baseline")

<strong>Figure 8</strong><br> 
<em>Simulation Output of Larger L2 Cache size</em>
![Simulation Output of Larger L2 Cache size](https://github.com/alexaryanfisher/MSC531_Assignment3/blob/main/images/lrgl2size.jpg "Simulation Output of Larger L2 Cache size")

<strong>Figure 9</strong><br> 
<em>Simulation Output of Lower Associativity</em>
![Simulation Output  of Lower Associativity](https://github.com/alexaryanfisher/MSC531_Assignment3/blob/main/images/lowassoc.jpg "Simulation Output  of Lower Associativity")

<strong>Figure 10</strong><br> 
<em>Simulation Output of Larger Block size</em>
![Simulation Output of Larger Block size](https://github.com/alexaryanfisher/MSC531_Assignment3/blob/main/images/lrgblock.jpg "Simulation Output of Larger Block size")

# Experiment Results and Analysis
| Configuration | L1 ICache Hit Rate | L1 DCache Hit Rate | L2 Cache Hit Rate |
|---|---|---|---|
| Baseline | 96.8 % | 93.3 % | 0.3 % |
| Larger L2 Cache | 96.8 % | 93.3 % | 0.3 % |
| Lower Associativity | 96.8 %| 93.3 % | 0.3 % |
| Larger Block Size | 98.1 % | 95.6 % | 0.9 % |

The results of the experiment provided some interesting results. The output statistics for the baseline, lower associativity, and larger L2 cache were exactly the same. The L1 instruction cache acheived a 96.8%  hit rate with the data cache hovering at 93.3 %. However the L2 Cache only reached 0.3 %. This could very likely be due to the `hello world` script being so short, not allowing for a build up of reusable data in the L2 cache. The change in the configurations had a minimal impact overall. The larger block size did provide a better performance acheiving a 98.1% L1 instruction cache hit rate and the data cache reaching 95.6%. It underscores strong spatial locality and allows the larger blocks to prefetch data efficently.
