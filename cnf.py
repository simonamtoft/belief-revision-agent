from sympy.logic.boolalg import And, Or, Implies, Not


def first(iterable, default=None):
    """ Returns the first element of an iterable """
    return next(iter(iterable), default)


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


def is_symbol(s):
    return isinstance(s, str) and s[:1].isalpha()


def to_cnf(s):
    """ Converts the given propositional logical sentence to CNF """
    s = convert_implications(s)
    s = move_not_inwards(s)
    s = distribute_and_over_or(s)
    return s


def convert_implications(s):
    if s.is_symbol:
        return s

    if s.func == Implies:
        a, b = s.args
        s = Or(b, Not(a))
    
    args = []
    for arg in s.args:
        args.append(convert_implications(arg))

    return s.func(*args)


def move_not_inwards(s):
    """Rewrite sentence s by moving negation sign inward. """

    if s.is_symbol:
        return s

    if s.func == Not:
        def NOTTING(b):
            return move_not_inwards(Not(b))

        a = s.args[0]
        if a.is_symbol:
            return s

        if a.func == Not:
            return move_not_inwards(a.args[0])

        if a.func == And:
            return associate(Or, list(map(NOTTING, a.args)))

        if a.func == Or:
            return associate(And, list(map(NOTTING, a.args)))
        return s

    return s.func(*list(map(move_not_inwards, s.args)))


def distribute_and_over_or(s):
    """Given a sentence 's' consisting of conjunctions and disjunctions
    of literals, return an equivalent sentence in CNF form.
    """
    if s.func == Or:
        s = associate(Or, s.args)
        if s.func != Or:
            return distribute_and_over_or(s)
        if len(s.args) == 0:
            return False
        if len(s.args) == 1:
            return distribute_and_over_or(s.args[0])
        conj = first(arg for arg in s.args if arg.func == And)
        if not conj:
            return s
        others = [a for a in s.args if a is not conj]
        rest = associate(Or, others)
        return associate(And, [distribute_and_over_or(c | rest)
                               for c in conj.args])
    elif s.func == And:
        return associate(And, list(map(distribute_and_over_or, s.args)))
    else:
        return s

