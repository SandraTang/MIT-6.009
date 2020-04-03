def satisfying_assignment(formula):
    """
    Find a satisfying assignment for a given CNF formula.
    Returns that assignment if one exists, or None otherwise.

    >>> satisfying_assignment([])
    {}
    >>> x = satisfying_assignment([[('a', True), ('b', False), ('c', True)]])
    >>> x.get('a', None) is True or x.get('b', None) is False or x.get('c', None) is True
    True
    >>> satisfying_assignment([[('a', True)], [('a', False)]])
    """
    # print("formula", formula)

    answer = {}

    # base case
    if formula == None or len(formula) == 0:
        return answer

    # simplify formula
    def simplify(form, ans):
        new_form = []
        # while unit clauses exist, 
        # find them
        # propagate effects
        form.sort(key=len)
        # form.reverse()
        for ors in form:
            if len(ors) == 1:
                var, boo = ors[0]
                # contradiction
                if var in ans and ans[var] != boo:
                    return None
                ans[var] = boo
                continue
            else:
                new_form.append([])
            for var, boo in ors:
                # if true, makes entire chunk redundant, remove []
                if var in ans and ans[var] == boo:
                    # if var in answer and answer[var] != boo:
                    #     return None
                    new_form.pop()
                    break
                # if false, redundant, remove (), aka don't add it
                # if unknown, add it
                if var not in ans:
                    new_form[-1].append((var, boo))
            if new_form != [] and new_form[-1] == []:
                return None
        # check if more unit clauses to investigate
        unit = False
        for ors in form:
            if len(ors) == 1:
                unit = True
        if unit:
            return simplify(new_form, ans)
        else:
            return new_form

    # get new, simplified formula
    new_formula = simplify(formula, answer)

    # tree
    # evaluate first var as True
    # formula: and > or > tup > var
    if new_formula == None:
        return None
    if len(new_formula) == 0:
        return answer

    chosen_tuple = new_formula[0][0]
    answer_temp = answer.copy()

    # TRUE BRANCH
    answer_temp[chosen_tuple[0]] = True
    newer_formula = simplify(new_formula, answer_temp)
    recusive_call = satisfying_assignment(newer_formula)
    if recusive_call != None:
            answer_temp.update(recusive_call)
            return answer_temp

    # TRUE BRANCH
    answer_temp[chosen_tuple[0]] = False
    newer_formula = simplify(new_formula, answer_temp)
    recusive_call = satisfying_assignment(newer_formula)
    if recusive_call != None:
            answer_temp.update(recusive_call)
            return answer_temp

    return None

print(satisfying_assignment([[("a",True),("b",True)], [("a",False),("b",False),("c",True)], [("b",True),("c",True)], [("b",True),("c",False)], [("a",False),("b",False),("c",False)]]))

[[("a",True),("b",True)], 
[("a",False),("b",False),("c",True)], 
[("b",True),("c",True)], 
[("b",True),("c",False)], 
[("a",False),("b",False),("c",False)]]
