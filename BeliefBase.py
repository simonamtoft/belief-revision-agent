import sympy as sp
from sympy.logic.boolalg import true, false, And, Or, Implies, Not, Equivalent
from entailment import entails
from cnf import to_cnf

class BeliefBase:
    def __init__(self, beliefs = []):
        self.beliefs = beliefs

    def contract(self, formula, order):
        """ Removes the input logical expression formula from the belief base """
        f = to_cnf(formula, simplify=True)

        for belief in self.beliefs:
            f_bb = belief.formula
        return NotImplementedError
    
    def expand(self, formula):
        """ Add the input logical expression formula to the belief base """
        formula = to_cnf(formula, simplify=True)
        return NotImplementedError
    
    def instantiate(self, formula):
        """ Instantiate the Belief Base with some predetermined beliefs """
        beliefs = [
            ["a|b", 0.1],
            ["c&d", 0.4]
        ]
        self.beliefs = [ Belief(sp.parse_expr(f), order) for f, order in beliefs ]
    
    def reset(self, formula):
        """ Sets the belief base to be the empty set Ø """
        self.beliefs = []

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
