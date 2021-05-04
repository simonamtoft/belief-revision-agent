import sympy as sp
from sympy.logic.boolalg import Or, And

_op_identity = {'&': True, '|': False}


def unique(sequence):
    """ Returns the sequence without duplicate elements """
    return list(set(sequence))


def conjuncts(sentence):
    """ Returns a list of all the conjuncts in the given sentence """
    return dissociate(And, [sentence])


def disjuncts(sentence):
    """ Returns a list of all the disjuncts in the given sentence """
    return dissociate(Or, [sentence])


def dissociate(op, args):
    """ Given an associative operator, return a flattened list result """
    result = []

    def collect(subargs):
        for arg in subargs:
            if arg.op == op:
                collect(arg.args)
            else:
                result.append(arg)

    collect(args)
    return result


def associate(op, args):
    """ Given an associative operator, return an flattened expression 
    such that nested instances of the same operator is at the top level.
    """
    args = dissociate(op, args)
    if len(args) == 0:
        return _op_identity[op]
    elif len(args) == 1:
        return args[0]
    else:
        return op(*args)
