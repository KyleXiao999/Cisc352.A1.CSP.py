# =============================
# Student Names: Chang Xu, Kyle Xiao, Allen Zhang
# Group ID: 111
# Date: 29 January 2023
# =============================
# CISC 352 - W23
# propagators.py
# desc:
#


#Look for #IMPLEMENT tags in this file. These tags indicate what has
#to be implemented to complete problem solution.

'''This file will contain different constraint propagators to be used within
   bt_search.

   propagator == a function with the following template
      propagator(csp, newly_instantiated_variable=None)
           ==> returns (True/False, [(Variable, Value), (Variable, Value) ...]

      csp is a CSP object---the propagator can use this to get access
      to the variables and constraints of the problem. The assigned variables
      can be accessed via methods, the values assigned can also be accessed.

      newly_instaniated_variable is an optional argument.
      if newly_instantiated_variable is not None:
          then newly_instantiated_variable is the most
           recently assigned variable of the search.
      else:
          progator is called before any assignments are made
          in which case it must decide what processing to do
           prior to any variables being assigned. SEE BELOW

       The propagator returns True/False and a list of (Variable, Value) pairs.
       Return is False if a deadend has been detected by the propagator.
       in this case bt_search will backtrack
       return is true if we can continue.

      The list of variable values pairs are all of the values
      the propagator pruned (using the variable's prune_value method).
      bt_search NEEDS to know this in order to correctly restore these
      values when it undoes a variable assignment.

      NOTE propagator SHOULD NOT prune a value that has already been
      pruned! Nor should it prune a value twice

      PROPAGATOR called with newly_instantiated_variable = None
      PROCESSING REQUIRED:
        for plain backtracking (where we only check fully instantiated
        constraints)
        we do nothing...return true, []

        for forward checking (where we only check constraints with one
        remaining variable)
        we look for unary constraints of the csp (constraints whose scope
        contains only one variable) and we forward_check these constraints.

        for gac we establish initial GAC by initializing the GAC queue
        with all constaints of the csp


      PROPAGATOR called with newly_instantiated_variable = a variable V
      PROCESSING REQUIRED:
         for plain backtracking we check all constraints with V (see csp method
         get_cons_with_var) that are fully assigned.

         for forward checking we forward check all constraints with V
         that have one unassigned variable left

         for gac we initialize the GAC queue with all constraints containing V.
   '''

def prop_BT(csp, newVar=None):
    '''Do plain backtracking propagation. That is, do no
    propagation at all. Just check fully instantiated constraints'''

    if not newVar:
        return True, []
    for c in csp.get_cons_with_var(newVar):
        if c.get_n_unasgn() == 0:
            vals = []
            vars = c.get_scope()
            for var in vars:
                vals.append(var.get_assigned_value())
            if not c.check_tuple(vals):
                return False, []
    return True, []

def prop_FC(csp, newVar=None):
    '''Do forward checking. That is check constraints with
       only one uninstantiated variable. Remember to keep
       track of all pruned variable,value pairs and return '''
    #IMPLEMENT
    prune = []              #To track any variable value pairs that are pruned (removed) during the forward check.
    if not newVar:          #If newVar is none, call csp.get_all_cons() to assign cons
        #cons: a list of constraints
        cons = csp.get_all_cons()
    else:                   #newVar has been provided
        cons = csp.get_cons_with_var(newVar)

    for c in cons:
        if c.get_n_unasgn() == 1:      #check if num of unassigned variables in current constraints is == 1
            vari = c.get_unasgn_vars()[0]     #variale is assigned the unassigned variable value

            for d in vari.cur_domain():
                if not c.has_support(vari, d):
                    vari.prune_value(d)          #if not, current value removed from the domain of the variable
                    prune.append((vari, d))      #added to the pruned list
            if vari.cur_domain_size() == 0:      #check current domain size
                return False, prune

    return True, prune



def prop_GAC(csp, newVar=None):
    '''Do GAC propagation. If newVar is None we do initial GAC enforce
       processing all constraints. Otherwise we do GAC enforce with
       constraints containing newVar on GAC Queue'''
    #IMPLEMENT

    prune = []  # keep track of all pruned(removed) variables-value pairs
    #check if newVar provided or not
    if not newVar:
        gac_queue = csp.get_all_cons()  # get all constraints from the csp problem
    else:
        gac_queue = csp.get_cons_with_var(newVar)  # get all constraints associated with the newVar

    #checks if the current state of the variables and constraints is still consistent
    while gac_queue:

        c = gac_queue.pop()  #c: constraints; pop first constraint from the queue

        for vari in c.get_scope():  #vari: variable

            for val in vari.cur_domain(): #val: value
                if not c.has_support(vari, val):
                    vari.prune_value(vari)  #To remove the value from the domain of the variable
                    prune.append((vari, val))  #To add the variable-value pair to pruned[]
                    if vari.cur_domain_size() == 0:
                        return False, prune

                    for cons in csp.get_cons_with_var(vari):  #To get all constraints associated with the variable
                        if cons not in gac_queue:
                            gac_queue.append(cons)  #To add the constraint to the queue for GAC enforcement

    return True, prune

