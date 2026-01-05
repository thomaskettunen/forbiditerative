import os
import json
import os

runs = {}
for file in os.listdir("runs"):
    with open(f"runs/{file}/data/experiments-eval/properties","r") as f:
        runs[file] = json.load(f)


tasks = runs["their_run"].keys()

def ReadData(parameter):
    parameterValues = {}
    for task in tasks:
        results = {}
        error = False
        for planner in runs.keys():
            if parameter in runs[planner][task]:
                results[planner] = runs[planner][task][parameter]
            else:
                error = True
        if(not error):        
            if(runs[planner][task]["domain"] in parameterValues):
                for planner in runs.keys():
                    parameterValues[runs[planner][task]["domain"]][planner] += results[planner]
            else:
                parameterValues[runs[planner][task]["domain"]] = results
    return parameterValues

def DifferentResultsAndTotal(results):
    differentresults= {}
    for result in results:
        if(not all(results[result][i] == results[result]["their_run"] for i in results[result].keys())):
            differentresults[result] = results[result]
    total = {}
    for planner in runs.keys():
        sum = 0
        for task in differentresults:
            sum += differentresults[task][planner]
        total[planner] = sum

    differentresults["total"] = total
    return differentresults

def generateTable(resultDict, table):
    with open("analysisFolder/" + table, "w") as f:
        f.write("\\hline \n")
        line = ""
        for planner in runs.keys():
            line += f"{planner} & "
        line = line.removesuffix(" & ")
        line += " \\\\"
        f.write(line + "\n")
        f.write("\\hline \n")
        for task in resultDict:
            line = f"{task} & "
            for planner in runs.keys():
                line += f"{resultDict[task][planner]} & "
            line = line.removesuffix(" & ")
            line += " \\\\"
            f.write(line + "\n")
            f.write("\\hline \n")

parameters = ["coverage", "plans found", "total time"]
for parameter in parameters:
    coverage = ReadData(parameter)
    coverageDiff = DifferentResultsAndTotal(coverage)
    generateTable(coverageDiff, "table_" + parameter.replace(" ", "_"))