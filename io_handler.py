import sympy as sp

L_PROMPT = ">> "    # console prompt for logic expression
A_PROMPT = "> "     # console prompt for action


class IOHandler():
    def __init__(self, bb):
        self.legal_actions = LEGAL_ACTIONS
        self.bb = bb

    def get_user_input(self):
        while True:
            print('\nPick an action')
            action = input(A_PROMPT).upper()
            try:
                logic_expr = self.legal_actions[action][1](self.bb, self)
                return action, logic_expr, None
            except Exception as e:
                print(f"Error: {e} is not a valid action key.")
                print(f"Possible keys: {list(self.legal_actions.keys())}")


def print_help_menu(bb, ioh):
    print('\nAction\tDescription')
    for key, val in ioh.legal_actions.items():
        print(f'  {key}\t{val[0]}')


def get_contraction(bb, ioh):
    while True:
        print("Input expression for contraction")
        action = input(L_PROMPT)
        try:
            return sp.parse_expr(action), None, None
        except Exception as e:
            print(f"Error: {e} is not a valid logical expression.")


def get_expansion(bb, ioh):
    while True:
        print("Input expression for expansion")
        action = input(L_PROMPT)
        try:
            return sp.parse_expr(action), None, None
        except Exception as e:
            print(f"Error: {e} is not a valid logical expression.")


def get_revision(bb, ioh):
    while True:
        print("Input expression for revision")
        action = input(L_PROMPT)
        try:
            f = sp.parse_expr(action)
        except Exception as e:
            print(f"Error: {e} is not a valid logical expression.")
        
        print("Select order (from 0 to 1)")
        try:
            order = float(input(L_PROMPT))
        except Exception as e:
            print(f"Error: {e} is not a valid float number.")
        
        return action, f, order


def print_beliefbase(bb, ioh):
    print("The current Belief Base is:")
    print(bb)
    return None, None, None


def placeholder(bb, ioh):
    return None, None, None


LEGAL_ACTIONS = {
    'C': ["Contraction", get_contraction],
    'E': ["Expansion", get_expansion],
    'I': ["Instantiate Belief Base", placeholder],
    'P': ["Print Belief Base", print_beliefbase],
    'E': ["Empty Belief Base", placeholder],
    'H': ["Print help dialog", print_help_menu],
    'R': ["Belief Revision", get_revision],
}


