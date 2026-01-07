import json
import os
import matplotlib.pyplot as plt
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-runtimes", action='store_true')
parser.add_argument("-compare", action='store_true')
args = parser.parse_args()

runs = {}
for file in os.listdir("runs"):
    with open(f"runs/{file}/data/experiments-eval/properties","r") as f:
        runs[file] = json.load(f)


tasks = runs["their_run"].keys()
print(len(tasks))
filteredtasks = []

for task in tasks:
    count = 0
    for planner in runs.keys():
        if "coverage" not in runs[planner][task]:
            count +=1
    if count == 0:
        filteredtasks.append(task)
tasks = filteredtasks

def GetTotalAndLastPlanTime(planner):
    coverage1 = []
    coverage0 = []
    unsolvable = 0
    print("----------------------------------------")
    print(f"For the planner {planner}:")
    for task in tasks:
        if "plans found" in runs[planner][task] and runs[planner][task]["plans found"] != 0:
                if runs[planner][task]["coverage"] == 1:
                     coverage1.append((runs[planner][task]["last plan time_mean"],runs[planner][task]["total time"]))
                else:
                     coverage0.append((runs[planner][task]["last plan time_mean"],runs[planner][task]["total time"]))
        elif "plans found" in runs[planner][task] and runs[planner][task]["plans found"] == 0 and runs[planner][task]["coverage"] == 1:
            unsolvable +=1
    print(f"{len(coverage1)} planning tasks are solved.")
    print(f"{unsolvable} tasks are unsolvable.")
    print(f"At least one plan is found for {len(coverage0)} unsolved planning tasks")
    print(f"{len(tasks) -(len(coverage0)+len(coverage1)+unsolvable)} planning tasks are unsolved.")
    return coverage0, coverage1

def ComparePlannerTimes(planner1, planner2):
    times = []
    for task in tasks:
        Err = False
        if "coverage" in runs[planner1][task]:
            if runs[planner1][task]["coverage"] == 0:
                planner1_time = 600
            elif "total time" in runs[planner1][task]:
                planner1_time = runs[planner1][task]["total time"]
            else:
                Err = True
        else:
            Err = True

        if "coverage" in runs[planner2][task]:
            if runs[planner2][task]["coverage"] == 0:
                planner2_time = 600
            elif "total time" in runs[planner2][task]:
                planner2_time = runs[planner2][task]["total time"]
            else:
                Err = True
        else:
            Err = True
        if not Err:
            times.append((planner1_time, planner2_time))

    return times

def CountUnsolved(times):
    both_unsolved = 0
    unsolved_1 = 0
    unsolved_2 = 0
    for task in times:
        if task[0] == 600 and task[1] == 600:
            both_unsolved+= 1
        elif task[0] == 600:
            unsolved_1 += 1
        elif task[1] == 600:
            unsolved_2 += 1
    return both_unsolved, unsolved_1, unsolved_2
                 

if args.runtimes:
    for planner in runs.keys():
        coverage0, coverage1 = GetTotalAndLastPlanTime(planner)
        for coverage in [("unsolved", coverage0), ("solved", coverage1)]:    
            x_val = [data[0] for data in coverage[1]]
            y_val = [data[1] for data in coverage[1]]
            if coverage[0] == "unsolved":
                plt.ecdf(x_val)
            else:
                plt.scatter(x_val,y_val)
                plt.ylabel("total time")
                plt.ylim(0,600)
            plt.title(planner +" "+ coverage[0])
            plt.xlabel("last plan time")
            plt.xlim(0,600)
            plt.savefig("analysisFolder/"+ planner +" "+ coverage[0])
            plt.close()

if args.compare:
    for planner in ["our_run_prefix1","our_run_prefix2"]:
        times = ComparePlannerTimes(planner, "their_run")
        x_val = [data[0] for data in times]
        y_val = [data[1] for data in times]

        both_unsolved, our_unsolved, their_unsolved = CountUnsolved(times)

        print(f"Of {len(times)} planning tasks, {their_unsolved} tasks were unsolved by their planner, {our_unsolved} were unsolved by our planner, {both_unsolved} were unsolved by both")

        plt.scatter(x_val,y_val)
        plt.title(f"Their run vs {planner}")
        plt.xlabel(planner)
        plt.ylabel("their_run")
        plt.xlim(0,600)
        plt.ylim(0,600)
        plt.savefig("analysisFolder/" + "their run" +" vs "+ planner)
        plt.close()
        