import sympy as sp
from sympy.logic.boolalg import true, false, And, Or, Implies, Not, Equivalent
from entailment import entails
from utils import check_value
from cnf import to_cnf
from sortedcontainers import SortedList
import math




class BeliefBase:
    def __init__(self):
        # Sort beliefs in descending order with respect to their order value
        self.beliefs = SortedList(key=lambda b: 1 - b.order)
        self.reorder_queue = []

    def fix_belief_ordering(self):
        """ Reorders beliefs with respect to their order. """
        for belief, order in self.reorder_queue:
            # remove old belief
            self.beliefs.remove(belief)

            # add belief with new order
            if order > 0: 
                belief.order = order
                self.beliefs.add(belief)

        self.reorder_queue = []
    
    def grp_by_order(self):
        """ Group all the beliefs from the belief base by decreasing order """

        results = []
        previous_order = None

        for belief in self.beliefs:
            current_order = belief.order
            if previous_order is None:
                results.append(belief)
                previous_order = current_order
                continue
        
            # group if order of beliefs are approximately the same,
            # otherwise yield order and results and set previous order to be the current
            if math.isclose(current_order + 1, previous_order + 1):
                results.append(belief)
            else:
                yield previous_order, results
                results = []
                results.append(belief)
                previous_order = current_order
        
        # yield final results
        yield previous_order, results

    def add(self, formula, order):
        """ Adds the belief Belief(formlua, order) to the BB 
            without considering validity."""

        f = to_cnf(formula)
        print(order)
        check_value(order)
        print(f, order)

        # remove duplicates from current belief base
        self.remove(f)

        # don't add if order < 0
        if order > 0:
            belief = Belief(f, order)
            self.beliefs.add(belief)

    def degree(self, formula):
        f = to_cnf(formula)

        # if formula is a Tautologi, it has degree 1
        if entails(EMPTY_BB, f):
            return 1
        
        # return order if the group entails the formula, else 0
        base = []
        for order, group in self.grp_by_order():
            base += [b.formula for b in group]
            bb = BeliefBase()
            bb.instantiate(base)
            if entails(bb, f):
                return order
        return 0

    def remove(self, formula):
        """ Removes any beliefs with the given formula from the belief base """
        for belief in self.beliefs:
            if belief.formula == formula:
                self.reorder_queue.append((belief, 0))
        self.fix_belief_ordering()

    def contract(self, formula, order):
        """ Removes the input logical expression formula from the belief base """
        f = to_cnf(formula)

        for belief in self.beliefs:
            f_bb = belief.formula
        return NotImplementedError
    
    def expand(self, formula, order):
        """ Add the input logical expression formula to the belief base """
        
        # convert to CNF and check order
        f = to_cnf(formula)
        check_value(order)

        # ignore if the formula is always false
        if not entails(EMPTY_BB, Not(f)):
            return None

        # order 1 for Tautology
        if entails(EMPTY_BB, f):
            order = 1
        else:
            for belief in self.beliefs:
                # only want to change beliefs with lower ordering
                if belief.order > order:
                    continue

                # check degree of implication
                d = self.degree(f >> belief.formula)
                if (entails(EMPTY_BB, Equivalent(f, belief.formula)) or 
                        belief.order <= order < d):
                    self.reorder_queue.append(belief, order)
                else:
                    self.reorder_queue.append(belief, d)
            
            self.fix_belief_ordering()

    def revise(self, inp):
        """ Updates ranking for belief base revision"""
        formula = inp[1]
        order = inp[2]

        f = to_cnf(formula)
        check_value(order)
        d = self.degree(f)

        # ignore contradictions
        if not entails(EMPTY_BB, Not(f)):
            print("ignored contradiction")
            return None
        
        # tautology
        if entails(EMPTY_BB, f):
            order = 1
        elif order <= d:
            self.contract(f, order)
        else:
            self.contract(Not(f), 0)
            self.expand(f, order)
        
        self.add(f, order)


    def instantiate(self, formula):
        """ Instantiate the Belief Base with some predetermined beliefs """
        beliefs = [
            ["a|b", 0.1],
            ["c&d", 0.4]
        ]
        for f, order in beliefs:
            self.beliefs.add(Belief(sp.parse_expr(f), order))

    def reset(self, formula):
        """ Sets the belief base to be the empty set Ø """
        self.beliefs.clear()

    def __repr__(self):
        if len(self.beliefs) == 0:
            return "BeliefBase(Ø)"
        return 'BeliefBase([\n  {}\n])'.format(",\n  ".join(str(x) for x in self.beliefs))


class Belief:
    def __init__(self, formula, order):
        self.formula = formula
        self.order = order

    def __repr__(self):
        return f'Belief({self.formula}, {self.order})'
    
    def __eq__(self, other):
        return self.order == other.order and self.formula == other.formula


EMPTY_BB = BeliefBase()
