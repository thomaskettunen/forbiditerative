#! /usr/bin/env python

"""
Experiment for the FI+groups planner
"""

import os

from downward import suites
from downward.reports.absolute import AbsoluteReport
from lab.environments import LocalEnvironment
from lab.experiment import Experiment
from lab.reports import Attribute, geometric_mean


# Create custom report class with suitable info and error attributes.
class BaseReport(AbsoluteReport):
    INFO_ATTRIBUTES = ["time_limit", "memory_limit"]
    ERROR_ATTRIBUTES = [
        "domain",
        "problem",
        "algorithm",
        "unexplained_errors",
        "error",
        "node",
    ]

junk = [".git", ".github", ".gitignore", "export.py", "README.md", "suites.py", "tests.py", "tox.ini"]
benchmarks = os.listdir("../../benchmarks")
for j in junk:
    if j in benchmarks:
        benchmarks.remove(j)

BENCHMARKS_DIR = os.environ["DOWNWARD_BENCHMARKS"]
ENV = LocalEnvironment(processes=2)
SUITE = benchmarks
ATTRIBUTES = [
    "error",
    Attribute("exit code"),
    Attribute("total time", min_wins=True),
    Attribute("coverage", min_wins=False, scale="linear"),
    Attribute("plans found", min_wins=False),
    Attribute("last plan time", min_wins=True, function=geometric_mean),
]
TIME_LIMIT = 1800
MEMORY_LIMIT = 2048


# Create a new experiment.
exp = Experiment(environment=ENV)

from parser import FIParser
exp.add_parser(FIParser())

for task in suites.build_suite(BENCHMARKS_DIR, SUITE):
    run = exp.add_run()
    # Create symbolic links and aliases. This is optional. We
    # could also use absolute paths in add_command().
    run.add_resource("domain", task.domain_file, symlink=True)
    run.add_resource("problem", task.problem_file, symlink=True)
    # 'ff' binary has to be on the PATH.
    # We could also use exp.add_resource().
    run.add_command(
        "run-planner",
        [os.environ["PLANNER"], "{domain}", "{problem}", f'{os.environ["K"]}'],
        time_limit=TIME_LIMIT,
        memory_limit=MEMORY_LIMIT,
    )
    # AbsoluteReport needs the following properties:
    # 'domain', 'problem', 'algorithm', 'coverage'.
    run.set_property("domain", task.domain)
    run.set_property("problem", task.problem)
    run.set_property("algorithm", "FI+groups")
    # BaseReport needs the following properties:
    # 'time_limit', 'memory_limit'.
    run.set_property("time_limit", TIME_LIMIT)
    run.set_property("memory_limit", MEMORY_LIMIT)
    run.set_property("k", f'{os.environ["K"]}')
    # Every run has to have a unique id in the form of a list.
    # The algorithm name is only really needed when there are
    # multiple algorithms.
    run.set_property("id", ["FI+groups", task.domain, task.problem])

# Add step that writes experiment files to disk.
exp.add_step("build", exp.build)

# Add step that executes all runs.
exp.add_step("start", exp.start_runs)

# Add step that parses log output into "properties" files.
exp.add_step("parse", exp.parse)

# Add step that collects properties from run directories and
# writes them to *-eval/properties.
exp.add_fetcher(name="fetch")

# Make a report.
exp.add_report(BaseReport(attributes=ATTRIBUTES), outfile="report.html")

# Parse the commandline and run the specified steps.
exp.run_steps()