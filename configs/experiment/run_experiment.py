import m5
from m5.objects import *
import os
import sys

def systemcreation(l2_size="256kB", l2_assoc=8, cache_line_size=64):
    # Create system
    system = System()
    
    # Clock domain
    system.clk_domain = SrcClockDomain()
    system.clk_domain.clock = '3GHz'
    system.clk_domain.voltage_domain = VoltageDomain()
    
    # Memory configuration
    system.mem_mode = 'timing'
    system.mem_ranges = [AddrRange('8GB')]
    
    # CPU and Interrupt controller
    system.cpu = TimingSimpleCPU()
    system.cpu.createInterruptController()
    
    # L1 ICache
    system.cpu.icache = Cache()
    system.cpu.icache.size = '32kB'
    system.cpu.icache.assoc = 8
    system.cpu.icache.tag_latency = 1
    system.cpu.icache.data_latency = 1
    system.cpu.icache.response_latency = 1
    system.cpu.icache.mshrs = 16
    system.cpu.icache.tgts_per_mshr = 20
    
    # L1 DCache
    system.cpu.dcache = Cache()
    system.cpu.dcache.size = '32kB'
    system.cpu.dcache.assoc = 8
    system.cpu.dcache.tag_latency = 1
    system.cpu.dcache.data_latency = 1
    system.cpu.dcache.response_latency = 1
    system.cpu.dcache.mshrs = 16
    system.cpu.dcache.tgts_per_mshr = 20
    
    # Connect L1 caches to CPU
    system.cpu.icache.cpu_side = system.cpu.icache_port
    system.cpu.dcache.cpu_side = system.cpu.dcache_port
    
    # L2 Bus
    system.l2bus = L2XBar()
    system.cpu.icache.mem_side = system.l2bus.cpu_side_ports
    system.cpu.dcache.mem_side = system.l2bus.cpu_side_ports
    
    # L2 Cache
    system.l2cache = Cache()
    system.l2cache.size = l2_size
    system.l2cache.assoc = l2_assoc
    system.l2cache.tag_latency = 16
    system.l2cache.data_latency = 16
    system.l2cache.response_latency = 10
    system.l2cache.mshrs = 20
    system.l2cache.tgts_per_mshr = 12
    system.l2cache.cpu_side = system.l2bus.mem_side_ports
    
    # Memory bus
    system.membus = SystemXBar()
    system.l2cache.mem_side = system.membus.cpu_side_ports
    
    # Connect interrupt controller ports
    system.cpu.interrupts[0].pio = system.membus.mem_side_ports
    system.cpu.interrupts[0].int_requestor = system.membus.cpu_side_ports
    
    # Memory controller
    system.mem_ctrl = MemCtrl()
    system.mem_ctrl.dram = DDR3_1600_8x8()
    system.mem_ctrl.dram.range = system.mem_ranges[0]
    system.mem_ctrl.port = system.membus.mem_side_ports
    
    # System port
    system.system_port = system.membus.cpu_side_ports
    
    # Cache line size
    system.cache_line_size = cache_line_size
    
    return system

# Function to extract stats reading from stats.txt file
def get_cache_stats(system):
    """Extract cache statistics by parsing the stats.txt file"""
    try:
        print("Reading cache statistics from stats.txt...")
        
        # Read the stats file that gem5 generates
        stats_file = 'm5out/stats.txt'
        
        if not os.path.exists(stats_file):
            print(f"Stats file {stats_file} not found!")
            return None
            
        stats = {}
        
        with open(stats_file, 'r') as f:
            lines = f.readlines()
        
        # Parse cache statistics from the file
        for line in lines:
            line = line.strip()
            if not line or line.startswith('#'):
                continue
                
            # Look for cache stats
            if '::total' in line and any(cache in line for cache in ['icache', 'dcache', 'l2cache']):
                parts = line.split()
                if len(parts) >= 2:
                    stat_name = parts[0]
                    try:
                        stat_value = float(parts[1])
                        stats[stat_name] = stat_value
                    except ValueError:
                        continue
        
        print(f"Found {len(stats)} cache statistics")
        
        # Extract the specific stats needed
        try:
            # L1 ICache
            l1i_hits = stats.get('system.cpu.icache.overallHits::total', 0)
            l1i_accesses = stats.get('system.cpu.icache.overallAccesses::total', 1)
            
            # L1 DCache  
            l1d_hits = stats.get('system.cpu.dcache.overallHits::total', 0)
            l1d_accesses = stats.get('system.cpu.dcache.overallAccesses::total', 1)
            
            # L2 Cache
            l2_hits = stats.get('system.l2cache.overallHits::total', 0)
            l2_accesses = stats.get('system.l2cache.overallAccesses::total', 1)
            
            # Calculate hit rates
            l1i_rate = (l1i_hits / l1i_accesses * 100) if l1i_accesses > 0 else 0
            l1d_rate = (l1d_hits / l1d_accesses * 100) if l1d_accesses > 0 else 0
            l2_rate = (l2_hits / l2_accesses * 100) if l2_accesses > 0 else 0
            
            print(f"Cache statistics extracted:")
            print(f"  L1 ICache: {l1i_hits}/{l1i_accesses} = {l1i_rate:.1f}%")
            print(f"  L1 DCache: {l1d_hits}/{l1d_accesses} = {l1d_rate:.1f}%") 
            print(f"  L2 Cache:  {l2_hits}/{l2_accesses} = {l2_rate:.1f}%")
            
            return {
                'l1i_rate': l1i_rate,
                'l1d_rate': l1d_rate,  
                'l2_rate': l2_rate,
                'l1i_hits': int(l1i_hits),
                'l1i_accesses': int(l1i_accesses),
                'l1d_hits': int(l1d_hits),
                'l1d_accesses': int(l1d_accesses),
                'l2_hits': int(l2_hits),
                'l2_accesses': int(l2_accesses),
                'method': 'stats.txt parsing'
            }
            
        except Exception as e:
            print(f"Error extracting specific stats: {e}")
            print("Available cache stats:")
            for key in sorted(stats.keys()):
                if any(cache in key for cache in ['icache', 'dcache', 'l2cache']):
                    print(f"  {key}: {stats[key]}")
            return None
            
    except Exception as e:
        print(f"Error reading stats file: {e}")
        return None

# Configuration dictionary
configs = {
    'baseline': {"name": "Baseline", "l2_size": "256kB", "l2_assoc": 16, "block_size": 64},
    'lrg_l2': {"name": "Larger L2 Cache", "l2_size": "1MB", "l2_assoc": 16, "block_size": 64},
    'low_assoc': {"name": "Lower Associativity", "l2_size": "256kB", "l2_assoc": 8, "block_size": 64},
    'lrg_block': {"name": "Larger Blocks", "l2_size": "256kB", "l2_assoc": 16, "block_size": 128},
}

# Parse command line argument for configuration
if len(sys.argv) > 1:
    config_key = sys.argv[1].replace('--config=', '')
    if config_key not in configs:
        print(f"Error: Unknown configuration '{config_key}'")
        print(f"Available configs: {list(configs.keys())}")
        sys.exit(1)
    selected_configs = [config_key]
else:
    # If no config specified, run all
    selected_configs = list(configs.keys())

binary = 'tests/test-progs/hello/bin/x86/linux/hello'

print("gem5 Cache Hierarchy Experiment")
print("-" * 25)

for config_key in selected_configs:
    config = configs[config_key]
    print(f"\nRunning configuration: {config['name']}")
    print(f"L2 Size: {config['l2_size']}, L2 Assoc: {config['l2_assoc']}, Block Size: {config['block_size']}")
    print("-" * 40)
    
    try:
        # Create system with specified configuration
        system = systemcreation(
            l2_size=config["l2_size"],
            l2_assoc=config["l2_assoc"],
            cache_line_size=config["block_size"]
        )
        
        # Set up workload
        system.workload = SEWorkload.init_compatible(binary)
        
        # Create process
        process = Process()
        process.cmd = [binary]
        process.cwd = os.getcwd()
        process.executable = binary
        
        # Link to CPU
        system.cpu.workload = process
        system.cpu.createThreads()
        
        # Run Simulation
        root = Root(full_system=False, system=system)
        m5.instantiate()
        
        print("Starting simulation...")
        exit_event = m5.simulate()
        
        ticks = m5.curTick()
        print(f"Simulation completed at tick {ticks}")
        print(f"Exit reason: {exit_event.getCause()}")
        
        if ticks > 0:
            print("SUCCESS: Simulation ran successfully!")
            
            # Write stats
            m5.stats.dump()
            stats = get_cache_stats(system)
            
            if stats:
                print("\nCache Hit Rates:")
                print(f"  L1 ICache: {stats['l1i_rate']:.1f}% ({stats['l1i_hits']}/{stats['l1i_accesses']})")
                print(f"  L1 DCache: {stats['l1d_rate']:.1f}% ({stats['l1d_hits']}/{stats['l1d_accesses']})")
                print(f"  L2 Cache:  {stats['l2_rate']:.1f}% ({stats['l2_hits']}/{stats['l2_accesses']})")
                
                # Save each results
                result_file = f"results_{config_key}.txt"
                with open(result_file, 'w') as f:
                    f.write(f"Configuration: {config['name']}\n")
                    f.write(f"L2 Size: {config['l2_size']}, L2 Assoc: {config['l2_assoc']}, Block Size: {config['block_size']}\n")
                    f.write(f"Simulation Ticks: {ticks}\n\n")
                    f.write("Cache Hit Rates:\n")
                    f.write(f"L1 ICache: {stats['l1i_rate']:.1f}% ({stats['l1i_hits']}/{stats['l1i_accesses']})\n")
                    f.write(f"L1 DCache: {stats['l1d_rate']:.1f}% ({stats['l1d_hits']}/{stats['l1d_accesses']})\n")
                    f.write(f"L2 Cache:  {stats['l2_rate']:.1f}% ({stats['l2_hits']}/{stats['l2_accesses']})\n")
                
                print(f"\nResults saved to: {result_file}")
            # Error Handling    
            else:
                print("Warning: Could not extract statistics")
        else:
            print("Warning: Simulation completed at tick 0")
            
    except Exception as e:
        print(f"ERROR: {str(e)}")
        sys.exit(1)

print(f"\nConfiguration {config['name']} completed successfully!")