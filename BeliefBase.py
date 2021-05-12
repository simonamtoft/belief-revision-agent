import sympy as sp
from sympy.logic.boolalg import true, Not
from entailment import entails
from cnf import to_cnf
from sortedcontainers import SortedList
from functools import reduce

# add a shorthand to use the sympy expression parser
pl = sp.parse_expr


class BeliefBase:
    def __init__(self):
        # Sort beliefs in descending order with respect to their rank value
        self.beliefs = SortedList(key=lambda b: -b.rank)

    def instantiate(self):
        """ Instantiate the Belief Base with some predetermined beliefs """
        self.reset()
        self.expand(pl("(p & q) >> r"), 100)
        self.expand(pl("r"), 10)
        self.expand(pl("p"), 20)
        # self.expand(pl("q"), 30)

    def reset(self):
        """ Sets the belief base to be the empty set Ø """
        self.beliefs.clear()

    def __repr__(self):
        if len(self.beliefs) == 0:
            return "BeliefBase(Ø)"
        return 'BeliefBase([\n  {}\n])'.format(",\n  ".join(str(x) for x in self.beliefs))

    def rank(self, formula):
        formula = to_cnf(formula)
        bb = true
        r = self.beliefs[0].rank if self.beliefs else 0
        for belief in self.beliefs:
            if belief.rank < r:
                if entails(bb, formula):
                    return r
                r = belief.rank
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

        beliefs = self.beliefs.copy() # work around shenanigans that happen when deleting from a SortedList you're iterating over
        for belief in beliefs:
            if formula == belief.formula:
                self.beliefs.remove(belief)
        self.beliefs.add(Belief(formula, newrank))
        print(f">>> {formula} added to belief basis with rank {newrank}")

        beliefs = self.beliefs.copy()
        for belief in beliefs:
            if oldrank <= belief.rank <= newrank:
                bb = [to_cnf(x.formula) for x in filter(lambda x: x.rank >= belief.rank and x != belief, self.beliefs)]
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
            if belief.rank <= oldrank:
                bb = [to_cnf(x.formula) for x in filter(lambda x: x.rank >= (oldrank + 1), delta.beliefs)]
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
        if 0 <= newrank:
            self.contract(Not(formula))
            self.expand(formula, newrank)
        else: 
            print(f"Rank {newrank} is negative.\nRevision not done.")


class Belief:
    def __init__(self, formula, rank):
        self.formula = formula
        self.rank = rank

    def __repr__(self):
        return f'Belief({self.formula}, rank = {self.rank})'
    
    def __eq__(self, other):
        return self.rank == other.rank and self.formula == other.formula


if __name__ == "__main__":
    bb = BeliefBase()

    #  Example from Wobcke paper
    bb.expand(pl("(p & q) >> r"), 100)
    bb.expand(pl("r"), 10)
    bb.expand(pl("p"), 20)
    bb.expand(pl("q"), 30)
    bb.expand(pl("p|r"), 40)
    assert bb.rank(pl("r")) == 30
    print(bb)

    # Contract r
    bb.contract(pl("r"))
    print(bb)

    bb.revision(pl("~r"), 40)
    print(bb)
