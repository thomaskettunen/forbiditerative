import os
import path

fldr = os.listdir("found_plans/done")

MS = []
for f in range(1, len(fldr) + 1):
	fname = "found_plans/done/sas_plan." + str(f)
	tmp = {}
	lines = []
	with open(fname, "r") as file:
		lines = [line[1:-2] for line in file.readlines()]
	for line in lines:
		if line in tmp:
			tmp[line] += 1
		else:
			tmp[line] = 1
	if tmp not in MS:
		MS.append(tmp)
		print("New MS added to list:")
		print(tmp)
	else:
		print(tmp)
		print("already in list")
		print(MS)
		break
print("total plans: {0}.\nUnique multisets: {1}".format(len(fldr), len(MS)))