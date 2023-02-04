# =============================
# Student Names: Xu Chang, Kyle Xiao, Allen Zhang
# Group ID: 111
# Date: 2023 02 03
# =============================
# CISC 352 - W23
# heuristics.py
# desc:
#


#Look for #IMPLEMENT tags in this file. These tags indicate what has
#to be implemented to complete problem solution.

'''This file will contain different constraint propagators to be used within
   the propagators

var_ordering == a function with the following template
    var_ordering(csp)
        ==> returns Variable

    csp is a CSP object---the heuristic can use this to get access to the
    variables and constraints of the problem. The assigned variables can be
    accessed via methods, the values assigned can also be accessed.

    var_ordering returns the next Variable to be assigned, as per the definition
    of the heuristic it implements.
   '''

def ord_dh(csp):
    ''' return variables according to the Degree Heuristic '''
    # IMPLEMENT
    unassignedVars = []
    for vari in csp.variables:
        if vari.is_assigned() is False:
            unassignedVars.append(vari)

    maxDegree = -1  #to keep track maximum degree of the variables
    dhVar = None    #to keep track variable with the maximum degree

    for vari in unassignedVars: #for each unassigned vaiable degree is initialized to 0
        degree = 0

        for constraint in csp.constraints:    #check if var is in the scope of the constraint
            if vari in constraint.var_scope:
                degree += 1
        if degree > maxDegree:     #check if the degree of var is greater than the current maximum degree
            maxDegree = degree     #max_degree is updated to the degree of var
            dhVar = vari            #dh_var is updated to var.

    return dhVar


def ord_mrv(csp):
    ''' return variable according to the Minimum Remaining Values heuristic '''
    # IMPLEMENT
    unassignedVars = []  # initialized with an empty list unassigned_vars

    for vari in csp.variables:  #check if the variable is assigned
        if not vari.is_assigned():
            unassignedVars.append(vari)  # vari is appended to the unassigned_vars list

    min_remaining = float("inf")  # to keep track of the minimum remaining values of the variables
    mrv_var = None  # to keep track of the variable with the minimum remaining values

    for vari in unassignedVars:  # compare each unassigned variable with current minimum remaining value min_remaining_val
        if len(vari.domain) < min_remaining:
            min_remaining = len(vari.domain)  # min_remaining_val is updated to the length of the domain of var
            mrv_var = vari  # mrv_var is updated to var

    return mrv_var  # return minimum remaining values


