import sympy as sp
from BeliefBase import Belief, BeliefBase
from io_handler import IOHandler, print_help_menu
from sympy.logic.boolalg import Or, And, Implies, Not

from cnf import to_cnf


def placeholder(bb):
    return None


def action_bb_map(bb, action):
    """ Maps actions to Belief Base functions """
    mapping = {
        'C': ["Contraction", bb.contract],
        'E': ["Expansion", bb.expand],
        'I': ['Instantiate Beliefs', bb.instantiate],
        'P': ["Print Belief Base", placeholder],
        'E': ["Empty Belief Base", bb.reset],
        'H': ["Print help dialog", placeholder],
        'R': ["Belief Revision", bb.revise],
    }
    return mapping[action][1]


if __name__ == "__main__":
    print("Program Start")
    bb = BeliefBase()
    ioh = IOHandler(bb)
    print_help_menu(bb, ioh)

    while True:
        a, f, order = ioh.get_user_input()
        # print(f, order)
        bb_func = action_bb_map(bb, a)
        bb_func(f)

    
