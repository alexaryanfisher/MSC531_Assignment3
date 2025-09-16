# Implementation: gem5 X86 ISA 

## Implementation and Setup

In the intial set up of the gem5 simulation. The following steps were completed based on the guideline followed in the gem5 documentation (gem5, 2025). The simulation was ran in the Unbuntu 24.04 environment within WSL. 

The first step is updating the environment and installing dependencies needed. This is completed with the use of `sudo apt-get`. Figure 1 visualizes the specific code.

<strong>Figure 1</strong><br> 
<em> Checking for Updates and installing dependencies</em>
![Installing updates and dependencies](https://github.com/alexaryanfisher/MSC531_Assignment3/blob/main/images/step1.jpg "Step 1: Installing updates and dependencies")

The second setup is cloning the gem5 repository with the use of `git`. 

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



