import sympy as sp
from sympy.logic.boolalg import Or

from utils import unique, conjuncts, disjuncts, associate
from cnf import to_cnf

def entails(bb, formula):
    """ Check Entailment of given formula in belief base bb """

    formula = to_cnf(formula)

    # Split all formulas from belief base into conjuncts
    sentences = []
    for belief in bb.beliefs:
        sentences += conjuncts(belief.formula)

    # Add contradiction to start resolution
    sentences += conjuncts(to_cnf(~formula))

    # Check if any of the sentences are already false
    if False in sentences:
        return True

    result = set()
    while True:
        n = len(sentences)
        pairs = [
            (sentences[i], sentences[j])
            for i in range(n) for j in range(i + 1, n)
        ]

        for si, sj in pairs:
            resolvents = resolve(si, sj)
            if False in resolvents:
                return True
            result = result.union(set(resolvents))

        if result.issubset(set(sentences)):
            return False
        for s in result:
            if s not in sentences:
                sentences.append(c)


def resolve(si, sj):
    """ Perform resolution on the two sentences si and sj """

    sentences = []
    dsi = disjuncts(si)
    dsj = disjuncts(sj)

    for di in dsi:
        for dj in dsj:
            if di == ~dj or ~di == dj:
                # Create list of all disjuncts except di and dj
                res = removeall(di, dsi) + removeall(dj, dsj)

                # Remove duplicates
                res = unique(res)
                
                # Join into new clause
                dnew = associate(Or, res)

                sentences.append(dnew)

    return sentences
