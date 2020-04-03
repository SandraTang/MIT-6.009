#!/usr/bin/env python3
"""6.009 Lab 5 -- Boolean satisfiability solving"""

import sys
sys.setrecursionlimit(10000)
# NO ADDITIONAL IMPORTS

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

    # # base case
    if formula == None:
        return None
    if len(formula) == 0:
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

    answer_temp[chosen_tuple[0]] = True
    newer_formula = simplify(new_formula, answer_temp)
    recusive_call = satisfying_assignment(newer_formula)
    if recusive_call != None:
            answer_temp.update(recusive_call)
            return answer_temp

    # FALSE BRANCH
    answer_temp[chosen_tuple[0]] = False
    newer_formula = simplify(new_formula, answer_temp)
    recusive_call = satisfying_assignment(newer_formula)
    if recusive_call != None:
            answer_temp.update(recusive_call)
            return answer_temp

    return None

def rule_1(student_preferences, session_capacities):
    """
    Students are only assigned to sessions included in their preferences.
    """
    locations = set(session_capacities.keys())
    rule = []
    for student, preferences in student_preferences.items():
        rule.append([])
        for preference in preferences:
            rule[-1].append((student + '_' + preference, True))
    return rule

def rule_2(student_preferences, session_capacities):
    """
    Each student is assigned to exactly one session.
    Each student is in at least one session. (REDUNDANT)
    Each student is in at most one session. 
    For any pair of sessions, any given student can be in only one session. 
    """
    students = list(student_preferences.keys())
    locations = list(session_capacities.keys())
    rule = []
    for student, preference in student_preferences.items():
        groups = groupings(locations, 2)
        for chunk in groups:
            for index in range(len(chunk)):
                # chunk[index] is currently student's name
                chunk[index] = (student + '_' + chunk[index], False)
        # for index in range(len(locations)):
        #     one = (student + '_' + locations[index-1], False)
        #     two = (student + '_' + locations[index], False)
            # rule.append([one, two])
        rule = rule + groups
    return rule

def groupings(students, n):
    """
    Returns all possible groupings of students.
    """
    if n == 0:
        return [[]]
    if len(students) == 0:
        return []
    add_student = [students[0]]
    rest_students = students[1:]
    new_grouping = [add_student + rest for rest in groupings(rest_students, n-1)]
    return new_grouping + groupings(rest_students, n)

def rule_3(student_preferences, session_capacities):
    """
    No session has more assigned students than it can fit.
    """
    students = list(student_preferences.keys())
    rule = []
    for session, capacity in session_capacities.items():
        if capacity < len(students):
            groups = groupings(students, capacity+1)
            for chunk in groups:
                for index in range(len(chunk)):
                    # chunk[index] is currently student's name
                    chunk[index] = (chunk[index] + '_' + session, False)
            rule = rule + groups
    return rule

def boolify_scheduling_problem(student_preferences, session_capacities):
    """
    Convert a quiz-room-scheduling problem into a Boolean formula.

    student_preferences: a dictionary mapping a student name (string) to a set
                         of session names (strings) that work for that student
    session_capacities: a dictionary mapping each session name to a positive
                        integer for how many students can fit in that session

    Returns: a CNF formula encoding the scheduling problem, as per the
             lab write-up
    We assume no student or session names contain underscores.
    """
    # print(student_preferences)
    # print(session_capacities)
    formula = rule_1(student_preferences, session_capacities) + rule_2(student_preferences, session_capacities) + rule_3(student_preferences, session_capacities)
    return formula

if __name__ == '__main__':
    import doctest
    _doctest_flags = doctest.NORMALIZE_WHITESPACE | doctest.ELLIPSIS
    doctest.testmod(optionflags=_doctest_flags)
