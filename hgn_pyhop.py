"""
HGNpyhop is an extension that adds Hierarchical Goal Network capabilities to Pyhop.
Version: 1.0
HGNpyhop is released under the Apache License 2.0.

HGN extensions:
In HGN, goals (not tasks) are decomposed. Thus, decomposing methods generate
goals. Here each goal is an atom plan that is maintained; initially plan = empty plan
As per:
 Shivashankar, V. (2015). Hierarchical goal networks: Formalisms and algorithms for
 planning and acting (Doctoral dissertation). University of Maryland.
 https://drum.lib.umd.edu/bitstream/handle/1903/16698/Shivashankar_umd_0117E_16202.pdf?sequence=1&isAllowed=y

Let goals be the list of goals to satisfy

Case 1: if goals is empty, then return plan
Let g be the first goal of goals; remove g from goals

Case 2: if g is satisfied in the state then recursively plan generation
          for goals

Case 3: If action a has g as an effect and a is applicable then apply a,
        plan CAT a, and continue recursively plan generation for goals

Case 4: If method m has g as last subgoal and m is applicable, then
        recursive plan generation for (m's subgoals) CAT goals

The actual algorithm in the paper combines Cases 3 and 4 to choose between
"RELEVANT" methods and operators. In our implementation it tries actions first
and then it tries methods

When creating a domain, the following requirements must be satisfied:

    - The type of every object must be declared. For every type, list all objects of that type:
            <state>.<type> = {..., <object>,...}
            - Here is an example in the satellite domain:
                    state1.instruments = {'instrument0'}

    - HGNpyhop uses an state-variable representation of the form:
            <state>.<variable>={..., <object>:<value>,...}
            - Here is an example in the satellite domain:
                    state1.power_on = {'instrument0': False}

    - The name of a goal must have the same name as an state variable. It has to indicate the expected value for the object:
            (<variable>,<object>,<value>)
             - Here is an example of a goal:
                ('have_image', 'Phenomenon4', 'thermograph0')


Two examples are provided: the logistics domain and the satellite domain

-- Original Pyhop README --
Pyhop, version 1.2.2 -- a simple SHOP-like planner written in Python.
Author: Dana S. Nau, 2013.05.31

Copyright 2013 Dana S. Nau - http://www.cs.umd.edu/~nau

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

     http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.

Pyhop should work correctly in both Python 2.7 and Python 3.2.
For examples of how to use it, see the example files that come with Pyhop.

Pyhop provides the following classes and functions:

- foo = State('foo') tells Pyhop to create an empty state object named 'foo'.
  To put variables and values into it, you should do assignments such as
  foo.var1 = val1

- bar = Goal('bar') tells Pyhop to create an empty goal object named 'bar'.
  To put variables and values into it, you should do assignments such as
  bar.var1 = val1

- print_state(foo) will print the variables and values in the state foo.

- print_goal(foo) will print the variables and values in the goal foo.

- declare_operators(o1, o2, ..., ok) tells Pyhop that o1, o2, ..., ok
  are all of the planning operators; this supersedes any previous call
  to declare_operators.

- print_operators() will print out the list of available operators.

- declare_methods('foo', m1, m2, ..., mk) tells Pyhop that m1, m2, ..., mk
  are all of the methods for tasks having 'foo' as their taskname; this
  supersedes any previous call to declare_methods('foo', ...).

- print_methods() will print out a list of all declared methods.

- pyhop(state1,tasklist) tells Pyhop to find a plan for accomplishing tasklist
  (a list of tasks), starting from an initial state state1, using whatever
  methods and operators you declared previously.

- In the above call to pyhop, you can add an optional 3rd argument called
  'verbose' that tells pyhop how much debugging printout it should provide:
- if verbose = 0 (the default), pyhop returns the solution but prints nothing;
- if verbose = 1, it prints the initial parameters and the answer;
- if verbose = 2, it also prints a message on each recursive call;
- if verbose = 3, it also prints info about what it's computing.
"""

# Pyhop's planning algorithm is very similar to the one in SHOP and JSHOP
# (see http://www.cs.umd.edu/projects/shop). Like SHOP and JSHOP, Pyhop uses
# HTN methods to decompose tasks into smaller and smaller subtasks, until it
# finds tasks that correspond directly to actions. But Pyhop differs from
# SHOP and JSHOP in several ways that should make it easier to use Pyhop
# as part of other programs:
#
# (1) In Pyhop, one writes methods and operators as ordinary Python functions
#     (rather than using a special-purpose language, as in SHOP and JSHOP).
#
# (2) Instead of representing states as collections of logical assertions,
#     Pyhop uses state-variable representation: a state is a Python object
#     that contains variable bindings. For example, to define a state in
#     which box b is located in room r1, you might write something like this:
#     s = State()
#     s.loc['b'] = 'r1'
#
# (3) You also can define goals as Python objects. For example, to specify
#     that a goal of having box b in room r2, you might write this:
#     g = Goal()
#     g.loc['b'] = 'r2'
#     Like most HTN planners, Pyhop will ignore g unless you explicitly
#     tell it what to do with g. You can do that by referring to g in
#     your methods and operators, and passing g to them as an argument.
#     In the same fashion, you could tell Pyhop to achieve any one of
#     several different goals, or to achieve them in some desired sequence.
#
# (4) Unlike SHOP and JSHOP, Pyhop doesn't include a Horn-clause inference
#     engine for evaluating preconditions of operators and methods. So far,
#     I've seen no need for it; I've found it easier to write precondition
#     evaluations directly in Python. But I could consider adding such a
#     feature if someone convinces me that it's really necessary.
#
# Accompanying this file are several files that give examples of how to use
# Pyhop. To run them, launch python and type "import blocks_world_examples"
# or "import simple_travel_example".


from __future__ import print_function
import copy, sys, pprint


############################################################
# States and goals
class State:
    """A state is just a collection of variable bindings."""
    def __init__(self, name):
        self.__name__ = name


class Goal:
    """A goal is just a collection of variable bindings."""
    def __init__(self, name):
        self.__name__ = name


### print_state and print_goal are identical except for the name
def print_state(state, indent=4):
    """Print each variable in state, indented by indent spaces."""
    if state != False:
        for (name, val) in vars(state).items():
            if name != '__name__':
                for x in range(indent): sys.stdout.write(' ')
                sys.stdout.write(state.__name__ + '.' + name)
                print(' =', val)
    else:
        print('False')


def print_goal(goal, indent=4):
    """Print each variable in goal, indented by indent spaces."""
    if goal != False:
        for (name, val) in vars(goal).items():
            if name != '__name__':
                for x in range(indent): sys.stdout.write(' ')
                sys.stdout.write(goal.__name__ + '.' + name)
                print(' =', val)
    else:
        print('False')


############################################################
# Helper functions that may be useful in domain models
def forall(seq, cond):
    """True if cond(x) holds for all x in seq, otherwise False."""
    for x in seq:
        if not cond(x): return False
    return True


def find_if(cond, seq):
    """
    Return the first x in seq such that cond(x) holds, if there is one.
    Otherwise return None.
    """
    for x in seq:
        if cond(x): return x
    return None


############################################################
# Commands to tell Pyhop what the operators and methods are
operators = {}
methods = {}


def declare_operators(state_variable, *op_list):
    """
    Call this after defining the operators, to tell Pyhop what they are.
    op_list must be a list of functions, not strings.
    """
    operators.update({state_variable: list(op_list)})
    return operators[state_variable]


def declare_methods(state_variable, *method_list):
    """
    Call this once for each task, to tell Pyhop what the methods are.
    task_name must be a string.
    method_list must be a list of functions, not strings.
    """
    methods.update({state_variable: list(method_list)})
    return methods[state_variable]


############################################################
# Commands to find out what the operators and methods are
def print_operators():
    """Print out the names of the operators"""
    print('{:<20}{}'.format('STATE VARIABLE:', 'RELEVANT OPERATORS:'))
    for state_variable in operators:
        print('{:<20}'.format(state_variable) + ', '.join([f.__name__ for f in operators[state_variable]]))


def print_methods():
    """Print out a table of what the methods are for each task"""
    print('{:<20}{}'.format('STATE VARIABLE:', 'RELEVANT METHODS:'))
    for state_variable in methods:
        print('{:<20}'.format(state_variable) + ', '.join([f.__name__ for f in methods[state_variable]]))


############################################################
# The actual planner
def pyhop(state, goals, verbose=0):
    """
    Try to find a plan that accomplishes tasks in state.
    If successful, return the plan. Otherwise return False.
    """
    if verbose > 0:
        print('** hgn_pyhop, verbose={} **\n   state = {}\n   goals = {}'.format(verbose, state.__name__, goals))
    result = seek_plan(state, goals, [], 0, verbose)
    if verbose > 0:
        print('** result =', result, '\n')
    return result


def seek_plan(state, goals, plan, depth, verbose=0):
    """
    Workhorse for pyhop. state and tasks are as in pyhop.
    - plan is the current partial plan.
    - depth is the recursion depth, for use in debugging
    - verbose is whether to print debugging messages
    """
    if verbose > 1:
        print('depth {} goals {}'.format(depth, goals))
    if goals == []:
        if verbose > 2:
            print('depth {} returns plan {}'.format(depth, plan))
        return plan
    goal1 = goals[0]
    if getattr(state, goal1[0])[goal1[1]] == goal1[2]:  # Check whether goal1 is already satisfied
        if verbose > 2:
            print('depth {} new state: no actions taken'.format(depth))
            print_state(state)
        solution = seek_plan(state, goals[1:], plan, depth + 1, verbose)
        if solution is not False:
            return solution
    if goal1[0] in operators:
        relevant = operators[goal1[0]]
        for operator in relevant:  # Look for relevant operators that are applicable
            newstate = operator(copy.deepcopy(state), *goal1[1:])
            if newstate:
                if verbose > 2:
                    print('depth {} action {}'.format(depth, (operator.__name__,) + goal1[1:]))
                    print('depth {} new state:'.format(depth))
                    print_state(newstate)
                solution = seek_plan(newstate, goals[1:], plan + [(operator.__name__,) + goal1[1:]], depth + 1, verbose)
                if solution:
                    return solution
    if goal1[0] in methods:
        if verbose > 2:
            print('depth {} method instance {}'.format(depth, goal1))
        relevant = methods[goal1[0]]
        for method in relevant:  # Look for relevant methods that are applicable
            subgoals = method(state, *goal1[1:])
            if verbose > 2:
                print('depth {} new goals: {}'.format(depth, subgoals))
            if subgoals:
                solution = seek_plan(state, subgoals + goals[1:], plan, depth + 1, verbose)
                if solution:
                    return solution
    if verbose > 2:
        print('depth {} returns failure'.format(depth))
    return False
