import os
import copy


simpoint_root = "."

class Benchmark:

    def __init__(self, name, iteration, bench):
        self.name = name
        self.iteration = iteration
        self.bench = bench
        self.scheme = "None"
        self.full_name = f"{name}_{iteration}"
        self.simpoints = -1
        self.weights = []
        self.results = []
        self.combined_results = {}

    def set_scheme(self, scheme):
        self.scheme = scheme

    def add_weight(self, weight):
        self.weights.append(weight)
    
    def __str__(self):
        return f"{full_name}-simpoints:{simpoints}-weights:{weights}"
    
    def setup_sims(self):
        sim_file = get_sim_file(self.bench, self.full_name)
        weight_file = get_weight_file(self.bench, self.full_name)

        if not os.path.exists(weight_file):
            print(f"WARNING: {self.name}_{self.iteration} does not have a weights file!!")
            return

        with open(weight_file) as weight_read:
            lines = weight_read.readlines()
            for line in lines:
                self.weights.append(float(line.split()[0]))
            self.simpoints = len(lines)
    
    def get_results(self, folder):
        assert(self.simpoints != -1)
        assert(len(self.results) == 0)
        for i in range(self.simpoints):
            if not os.path.exists(f"{folder}/{self.full_name}_{i}.txt"):
                print(f"{folder}/{self.full_name}_{i} does not exist!! Weight: {self.weights[i]}")
                self.results.append({})
                continue

            with open(f"{folder}/{self.full_name}_{i}.txt") as result:
                dic = self.parse_result_file(result)
                self.results.append(dic)
    
    def parse_result_file(self, result_file):
        dic = {}

        lines = result_file.read()

        lines = lines.split("Begin Simulation Statistics")

        if len(lines) < 3:
            print(f"{self.full_name} has an  empty results file!")
            return dic

        lines = lines[2]

        lines = lines.split("\n")

        for line in lines:
            if "---------" in line:
                continue

            if line == "":
                continue

            if "Begin Simulation Statistics" in line or "End Simulation Statistics" in line:
                continue

            if not line.strip():
                continue

            data = line.split()
            dic[data[0]] = data[1]
        
        return dic
    
    def weigh_dic(self, dic, weight):
        for key, item in dic.items():
            dic[key] = weight * float(item)
        return dic


    def weigh_results(self):
        base_dic = self.weigh_dic(self.results[0], self.weights[0])

        for i in range(1, len(self.results)):
            new_dic = self.weigh_dic(self.results[i], self.weights[i])

            for key, item in new_dic.items():
                if key not in base_dic:
                    #print("Have key not found in source dict", key)
                    base_dic[key] = item
                    continue
                
                base_dic[key] += item

        self.combined_results = copy.deepcopy(base_dic)
    
    def setup_benchmark(self, folder):
        self.setup_sims()
        if self.simpoints == -1:
            return
        #print(f"Getting results for {self.scheme}_{self.name}_{self.iteration}")
        self.get_results(folder)
        self.weigh_results()



    

def get_sim_file(bench, full_name):
    return f"{simpoint_root}/{bench}/{full_name}.simpoints"

def get_weight_file(bench, full_name):
    return f"{simpoint_root}/weights/{full_name}_sorted.weights"


    