from benchmark import Benchmark
from config import *
import copy

#BENCH_SPEC2017 and BENCH_SPEC2006 = Benches
#BASE_SCHEMES = Schemes

ipc = ["system.switch_cpus.ipc"]
cpi = ["system.switch_cpus.cpi"]

memory = [
"system.cpu.dcache.overallAccesses::total",
"system.l2.overallAccesses::total",
"system.l3.overallAccesses::total",
"system.mem_ctrls0.dram.numReads::total",
"system.mem_ctrls1.dram.numReads::total"
]

def main():
    spec2006_dataset = []
    spec2017_dataset = []
    for scheme in BASE_SCHEMES:
        spec2006_scheme = copy.deepcopy(scheme)
        spec2017_scheme = copy.deepcopy(scheme)

        spec2006_scheme.set_bench(copy.deepcopy(BENCH_SPEC2006))
        spec2006_scheme.setup_benchmarks()

        spec2017_scheme.set_bench(copy.deepcopy(BENCH_SPEC2017))
        spec2017_scheme.setup_benchmarks()

        spec2006_dataset.append(spec2006_scheme)
        spec2017_dataset.append(spec2017_scheme)
    
    workloads = []
    for scheme in spec2006_dataset:
        for workload in scheme.bench.workloads:
            workload.combine_stats()
            workloads.append(workload)
    
    for scheme in spec2017_dataset:
        for workload in scheme.bench.workloads:
            workload.combine_stats()
            workloads.append(workload)

    write_out(cpi, "test_results.csv", workloads)



def write_out(stats, dst_file, workloads):
    sorted_workloads = {}
    for workload in workloads:
        if workload.name not in sorted_workloads:
            sorted_workloads[workload.name] = [workload]
        else:
            sorted_workloads[workload.name].append(workload)

    num = 0    
    for key in sorted_workloads:
        if num == 0:
            num = len(sorted_workloads[key])
        assert(len(sorted_workloads[key]) == num)
    
    with open(dst_file, "w") as out:
        print_string = "benchmarks, "
        for workload in next(iter(sorted_workloads.values())):
            print_string += workload.scheme + ", "
        out.write(print_string)
        out.write("\n")

        for stat in stats:
            for key, item in sorted_workloads.items():
                print_string = f"{stat}, {key}, "
                for workload in item:
                    if stat in workload.avg_stats:
                        print_string += str(round(workload.avg_stats[stat], 3)) + ", "
                    else:
                        print_string += ", "
                out.write(print_string)
                out.write("\n")





main()
