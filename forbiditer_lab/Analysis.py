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

def CountExitCodes():
    planners = ["our_run_prefix1", "our_run_prefix2"]
    results={}
    for planner in planners:
        results[planner] = {}
    for task in tasks:
        error = False
        for planner in runs.keys():
            if not "exit code" in runs[planner][task]:
                error = True
        if(not error):        
            for planner in planners:
                if runs[planner][task]["exit code"] in results[planner]:
                    results[planner][runs[planner][task]["exit code"]] += 1
                else:
                    results[planner][runs[planner][task]["exit code"]] = 0
    return results


def GetTotals(results):
    total = {}
    for planner in runs.keys():
        sum = 0
        for task in results:
            sum += results[task][planner]
        total[planner] = sum

    return total

def ResultsAndTotal(results):
    allresults= results
    total = {}
    for planner in runs.keys():
        sum = 0
        for task in allresults:
            sum += allresults[task][planner]
        total[planner] = sum

    allresults["total"] = total
    return allresults

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

def generateExitCodeTable(exitCodeDict):
    with open("analysisFolder/ExitCodes", "w") as f:
        f.write("\\hline \n")
        line = "Exit Code & "
        for planner in exitCodeDict.keys():
            line += f"{planner} & "
        line = line.removesuffix(" & ")
        line += " \\\\"
        f.write(line + "\n")
        f.write("\\hline \n")
        for code in exitCodeDict["our_run_prefix1"]:
            line = f"{code} & "
            for planner in exitCodeDict.keys():
                line += f"{exitCodeDict[planner][code]} & "
            line = line.removesuffix(" & ")
            line += " \\\\"
            f.write(line + "\n")
            f.write("\\hline \n")


parameters = ["coverage", "plans found", "total time"]
totals = {}
for parameter in parameters:
    data = ReadData(parameter)
    totals[parameter] = GetTotals(data)
    dataDiff = ResultsAndTotal(data)
    generateTable(dataDiff, "table_" + parameter.replace(" ", "_"))

generateTable(totals, "table_totals")
generateExitCodeTable(CountExitCodes())