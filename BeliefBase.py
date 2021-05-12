import sympy as sp
from sympy.logic.boolalg import true, false, And, Or, Implies, Not, Equivalent
from entailment2 import entails
from utils import check_value
from cnf import to_cnf
from sortedcontainers import SortedList
from functools import reduce
import math




class BeliefBase:
    def __init__(self):
        # Sort beliefs in descending order with respect to their order value
        self.beliefs = SortedList(key=lambda b: -b.order)
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

    def instantiate(self, formula=None):
        """ Instantiate the Belief Base with some predetermined beliefs """
        beliefs = [
            ["a|b", 1],
            ["c&d", 4]
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

    def rank(self, formula):
        formula = to_cnf(formula)
        bb = true
        r = self.beliefs[0].order if self.beliefs else 0
        for belief in self.beliefs:
            if belief.order < r:
                if entails(bb, formula):
                    return r
                r = belief.order
            bb = bb & to_cnf(belief.formula)
        return r if entails(bb, formula) else 0
    
    def expand(self, formula, newrank):
        if self.rank(Not(formula)) > 0:
            print(">>> Formula is inconsistent with belief basis")
            return
        oldrank = self.rank(formula)
        if newrank <= oldrank:
            print(">>> Desired rank is lower than or equal to existing rank")
            return
        for belief in self.beliefs:
            if formula == belief.formula:
                self.beliefs.remove(belief)
        self.beliefs.add(Belief(formula, newrank))
        print(f">>> {formula} added to belief basis with rank {newrank}")
        for belief in self.beliefs:
            if oldrank <= belief.order <= newrank:
                bb = [to_cnf(x.formula) for x in filter(lambda x: x.order >= belief.order and x != belief, self.beliefs)]
                bb = reduce(lambda x, y: x & y, bb, true)
                if entails(bb, belief.formula):
                    print(f">>> Removed {belief} as it is redundant")
                    self.beliefs.remove(belief)
    
    def contract(self, formula):
        if entails(true, formula):
            print(f">>> {formula} is a tautology")
            return
        oldrank = self.rank(formula)
        delta = BeliefBase()
        delta.beliefs = self.beliefs.copy()
        for belief in self.beliefs:
            if belief.order <= oldrank:
                bb = [to_cnf(x.formula) for x in filter(lambda x: x.order >= (oldrank + 1), delta.beliefs)]
                bb = reduce(lambda x, y: x & y, bb, true)
                if not entails(bb, formula | belief.formula):
                    r = delta.rank(belief.formula)
                    delta.beliefs.remove(belief)
                    print(f">>> {belief} removed by (C-) condition")
                    if r < oldrank or not entails(bb, formula >> belief.formula):
                        for b in self.beliefs:
                            if formula >> belief.formula == b.formula:
                                delta.beliefs.remove(b)
                        t = Belief(formula >> belief.formula, r)
                        delta.beliefs.add(t)
                        print(f">>> Added {t} to belief basis to satisfy (K-5)")
        self.beliefs = delta.beliefs

    def revision(self, formula, newrank):
        self.contract(Not(formula))
        self.expand(formula, newrank)
            


class Belief:
    def __init__(self, formula, order):
        self.formula = formula
        self.order = order

    def __repr__(self):
        return f'Belief({self.formula}, rank={self.order})'
    
    def __eq__(self, other):
        return self.order == other.order and self.formula == other.formula


EMPTY_BB = BeliefBase()


if __name__ == "__main__":
    pl = sp.parse_expr
    bb = BeliefBase()
    # bb.beliefs.add(Belief(sp.parse_expr("p"),    1))
    # bb.beliefs.add(Belief(sp.parse_expr("q"),    1))
    # bb.beliefs.add(Belief(sp.parse_expr("p>>q"), 1))

    # bb.contract(sp.parse_expr("~(q>>p)"))
    # print(bb)
    # bb.expand(sp.parse_expr("q>>p"), 1)
    # print(bb)

    #  Example from Wobcke paper
    bb.expand(pl("(p & q) >> r"), 100)
    bb.expand(pl("r"), 10)
    bb.expand(pl("p"), 20)
    bb.expand(pl("q"), 30)
    bb.expand(pl("p|r"), 40)
    assert bb.rank(pl("r")) == 30
    #print(bb)

    # Contract r
    bb.contract(pl("r"))
    #print(bb)

    bb.revision(pl("~r"), 40)
    print(bb)
