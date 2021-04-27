import sympy as sp
from sympy.logic.boolalg import true, false, And, Or, Amplies, Not


class BeliefBase:
    def __init__(self, beliefs = []):
        self.beliefs = beliefs
    
    def entails(self, formula):
        """ Check BLABLA """
        
        # Some helpers
        def pl_true(KB, model={}):
            pass
        def tt_check_all(KB, formula, symbols, model):
            pass

        formula = sp.to_cnf(formula, simplify=True)
        pass

    def contract(self, formula):
        """ Removes the input logical expression formula from the belief base """
        formula = sp.to_cnf(formula, simplify=True)
        pass
    
    def expand(self, formula):
        """ Add the input logical expression formula to the belief base """
        formula = sp.to_cnf(formula, simplify=True)
        pass
    
    def instantiate(self, formula):
        """ Instantiate the Belief Base with some predetermined beliefs """
        b_str = [
            "a|b",
            "c&d"
        ]
        self.beliefs = [ Belief(sp.parse_expr(x)) for x in b_str ]
    
    def reset(self, formula):
        """ Sets the belief base to be the empty set Ø """
        self.beliefs = []

    def __repr__(self):
        if len(self.beliefs) == 0:
            return "BeliefBase(Ø)"
        return 'BeliefBase([\n  {}\n])'.format(",\n  ".join(str(x) for x in self.beliefs))


class Belief:
    def __init__(self, formula):
        self.formula = formula

    def __repr__(self):
        return f'Belief({self.formula})'
