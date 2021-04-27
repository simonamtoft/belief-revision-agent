import sympy as sp
from BeliefBase import Belief, BeliefBase
from io_handler import IOHandler, print_help_menu


def placeholder(bb):
    return None


def action_bb_map(bb, action):
    """ Maps actions to Belief Base functions """
    mapping = {
        'C': ["Contraction", bb.contract],
        'E': ["Expansion", bb.expand],
        'I': ['Instantiate Beliefs', bb.instantiate],
        'P': ["Print Belief Base", placeholder],
        'R': ["Reset Belief Base", bb.reset],
        'H': ["Print help dialog", placeholder]
    }
    return mapping[action][1]


if __name__ == "__main__":
    print("Program...")
    bb = BeliefBase()
    ioh = IOHandler(bb)
    print_help_menu(bb, ioh)

    while True:
        a, logic_expr = ioh.get_user_input()
        bb_func = action_bb_map(bb, a)
        bb_func(logic_expr)

    
