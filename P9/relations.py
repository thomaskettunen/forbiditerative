def reorder_relation(new_plan, old_plan):
	if len(new_plan) != len(old_plan):
		return False
	old_tmp = {}
	for op in old_plan:
		if op in old_tmp:
			old_tmp[op] += 1
		else:
			old_tmp[op] = 1
	new_tmp = {}
	for op in new_plan:
		if op in new_tmp:
			new_tmp[op] += 1
		else:
			new_tmp[op] = 1
	return old_tmp == new_tmp

def op_dom(aa, bb):
    """does a *operator dominate* b?
    returns:
        - True if a operator dominates b
        - False if b operator dominates a
        - None otherwise
    """
    from functools import reduce
    ac = {}
    bc = {}
    for ao in aa:
        ac[ao] = (ac[ao] if ao in ac else 0) + 1
    for bo in bb:
        bc[bo] = (bc[bo] if bo in bc else 0) + 1
    adb = reduce(lambda t, o: t and (ac[o] <= (bc[o] if o in bc else 0)), ac, True)
    bda = reduce(lambda t, o: t and (bc[o] <= (ac[o] if o in ac else 0)), bc, True)
    if adb == False and bda == False: return None
    return adb	

def group_op_dom(f, aa, bb):
    """does a *group operator dominate* b?
    returns:
        - True if a group operator dominates b
        - False if b group operator dominates a
        - None otherwise
    """
    from functools import reduce
    ac = {}
    bc = {}
    aa = map(f, aa)
    bb = map(f, bb)
    for ao in aa:
        ac[ao] = (ac[ao] if ao in ac else 0) + 1
    for bo in bb:
        bc[bo] = (bc[bo] if bo in bc else 0) + 1
    adb = reduce(lambda t, o: t and (ac[o] <= (bc[o] if o in bc else 0)), ac, True)
    bda = reduce(lambda t, o: t and (bc[o] <= (ac[o] if o in ac else 0)), bc, True)
    if adb == False and bda == False: return None
    return adb

from functools import partial
prefix_group_op_dom = partial(group_op_dom, lambda o: o.split(' ')[0])