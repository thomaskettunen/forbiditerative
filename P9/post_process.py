#! /bin/python3

import argparse
import os
import shutil
import re
from dataclasses import dataclass

import relations


@dataclass
class Plan:
	name: str
	cost: int
	cost_str: str
	plan: list


def get_relation(relation_string):
	if relation_string == "reorder":
		return relations.reorder_relation
	elif relation_string == "operator_dominance":
		return relations.op_dom
	elif relation_string == "group_prefix_operator_dominance":
		return relations.prefix_group_op_dom


# def filter_related_plans[T](relation: Callable[[List[T], List[T]], Optional[Bool]], ordered_plans: List[List[T]]) -> List[List[T]]
def filter_related_plans(relation, ordered_plans) -> list:
	# Does not find minimum cover set
	unrelated_plans = []
	for curr_plan in ordered_plans:
		covered = False
		for plan in unrelated_plans:
			if relation(plan.plan, curr_plan.plan):
				covered = True
				# print(curr_plan[:-1])
				# print("plan is related to")
				# print(plan[:-1])
				break
		if not covered:
			unrelated_plans.append(curr_plan)
			# print("New plan added to list:")
			# print(curr_plan[:-1])
	return unrelated_plans


def dump_plans(plan_path, plans):
	for plan in plans:
		with open(os.path.join(plan_path, plan.name), "w") as file:
			for op in plan.plan:
				file.write(f"({op})\n")
			file.write(plan.cost_str)


def read_plans(found_plans_path):
	if not os.path.exists(found_plans_path):
		print(f"No plan folder found at: {found_plans_path}")
	plans = []
	for plan_file in os.listdir(found_plans_path):
		with open(os.path.join(found_plans_path, plan_file), "r") as file:
			lines = file.readlines()
			operations = [line[1:-2] for line in lines[:-1]]
			cost_str = lines[-1]
			cost = int(re.compile(r"cost = (\d+)").findall(cost_str)[0])
			plans.append(
				Plan(
					name = plan_file,
					cost = cost,
					cost_str = cost_str,
					plan = operations,
				)
			)
	return plans


if __name__ == "__main__":
	parser = argparse.ArgumentParser()
	parser.add_argument("input_plan_path", help="Path to the plans to process")
	parser.add_argument("output_plan_path", help="Path to output the filtered plans")
	parser.add_argument("--relation", help="Choice of predefined relations", choices=["reorder", "operator_dominance", "group_prefix_operator_dominance"])
	args = parser.parse_args()

	relation = get_relation(args.relation)

	new_plans_path = args.output_plan_path
	if os.path.exists(new_plans_path):
		shutil.rmtree(new_plans_path)
	os.mkdir(new_plans_path)
	plans = read_plans(args.input_plan_path)
	plans.sort(key = lambda p: p.cost)
	plans = filter_related_plans(relation, plans)
	dump_plans(new_plans_path, plans)