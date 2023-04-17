from benchmark import Benchmark
import copy

class Scheme:

    def __init__(self, name, folder):
        self.name = name
        self.folder = folder
        self.bench = None
        self.benchmarks = []
    
    def __str__(self):
        return (f"{name}-scheme")
    
    def set_bench(self, bench):
        self.bench = bench
    
    def setup_benchmarks(self):
        assert(len(self.benchmarks) == 0)
        assert(self.bench != None)
        print(self.bench)
        for workload in self.bench.workloads:
            workload.set_scheme(self.name)
            for i in range(workload.num_iter):
                new_b = Benchmark(workload.name, i, self.bench.name)
                new_b.set_scheme(self.name)
                new_b.setup_benchmark(f"{self.bench.name}/{self.folder}")
                workload.add_benchmark(new_b)
                self.benchmarks.append(new_b)



scheme_names = [
("baseline", "bl"),
("baseline+ap", "uap"),
("delay", "mp"),
("delay+ap", "ap"),
("stt", "stt"),
("stt+ap", "sap"),
("dom", "dom"),
("dom+ap", "dap")
] 

BASE_SCHEMES = []

for x in scheme_names:
    BASE_SCHEMES.append(Scheme(x[0], x[1]))
    

class Workload:

    def __init__(self, name, full_name, num_iter):
        self.name = name
        self.full_name = full_name
        self.num_iter = num_iter
        self.benchmarks = []
        self.avg_stats = None
        self.scheme = "None"
    
    def set_scheme(self, scheme):
        self.scheme = scheme
    
    def __str__(self):
        return (f"{self.full_name}-workload-{scheme}")
    
    def add_benchmark(self, benchmark):
        self.benchmarks.append(benchmark)
    
    def combine_stats(self):
        assert(self.avg_stats == None)
        self.avg_stats = copy.deepcopy(self.benchmarks[0].combined_results)
        for i in range(1, len(self.benchmarks)):
            for key, item in self.benchmarks[i].combined_results.items():
                if key not in self.avg_stats:
                    #print("Have key not found in source dict", key)
                    self.avg_stats[key] = item
                    continue
                
                self.avg_stats[key] += item

        count = 0
        for benchmark in self.benchmarks:
            if len(benchmark.combined_results) > 1:
                count = count + 1
        
        for key, item in self.avg_stats.items():
            self.avg_stats[key] = item / float(count)

class Bench:

    def __init__(self, name, benchmarks):
        self.name = name
        self.benchmarks = benchmarks
        self.workloads = []
        for benchmark in self.benchmarks:
            self.workloads.append(Workload(benchmark[0], benchmark[2], benchmark[1]))
    
    def __str__(self):
        return (f"{self.name}-benchmarks-{len(self.benchmarks)}")


SPEC2006 = [
#int
("perlbench", 3, "400.perlbench"),
("bzip2", 6, "401.bzip2"),
("gcc", 9, "403.gcc"),
("mcf", 1, "429.mcf"),
("gobmk", 5, "445.gobmk"),
("hmmer", 2, "456.hmmer"),
("sjeng", 1, "458.sjeng"),
("libquantum", 1, "462.libquantum"),
("h264ref", 3, "464.h264ref"),
("omnetpp", 1, "471.omnetpp"),
("astar", 2, "473.astar"),
("xalancbmk", 1, "483.xalancbmk"),
#fp
("bwaves", 1, "410.bwaves"),
#("gamess", 3, "416.gamess"),
("milc", 1, "433.milc"),
("zeusmp", 1, "434.zeusmp"),
("gromacs", 1, "435.gromacs"),
("cactusADM", 1, "436.cactusADM"),
("leslie3d", 1, "437.leslie3d"),
("namd", 1, "444.namd"),
#("dealII", 1, "447.dealII"),
#("soplex", 2, "450.soplex"),
("povray", 1, "453.povray"),
("calculix", 1, "454.calculix"),
("GemsFDTD", 1, "459.GemsFDTD"),
("tonto", 1, "465.tonto"),
("lbm", 1, "470.lbm"),
("wrf", 1, "481.wrf"),
("sphinx3", 1, "482.sphinx3")
]

SPEC2017 = [
#int
("perlbench_s", 3, "600.perlbench_s"),
("gcc_s", 3, "602.gcc_s"),
("mcf_s", 1, "605.mcf_s"),
("omnetpp_s", 1, "620.omnetpp_s"),
("xalancbmk_s", 1, "623.xalancbmk_s"),
("x264_s", 3, "625.x264_s"),
("deepsjeng_s", 1, "631.deepsjeng_s"),
("leela_s", 1, "641.leela_s"),
("exchange2_s", 1, "648.exchange2_s"),
("xz_s", 2, "657.xz_s"),
#fp
("bwaves_s", 2, "603.bwaves_s"),
("cactuBSSN_s", 1, "607.cactuBSSN_s"),
("lbm_s", 1, "619.lbm_s"),
("wrf_s", 1, "621.wrf_s"),
("cam4_s", 1, "627.cam4_s"),
("pop2_s", 1, "628.pop2_s"),
("imagick_s", 1, "638.imagick_s"),
("nab_s", 1, "644.nab_s"),
("fotonik3d_s", 1, "649.fotonik3d_s"),
("roms_s", 1, "654.roms_s")
]




BENCH_SPEC2006 = Bench("2006", SPEC2006)
BENCH_SPEC2017 = Bench("2017", SPEC2017)
