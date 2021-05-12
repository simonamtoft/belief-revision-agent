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
                logic_expr, rank = self.legal_actions[action][1](self.bb, self)
                return action, logic_expr, rank
            except Exception as e:
                print(f"Error: {e}.")
                print(f"Possible keys: {list(self.legal_actions.keys())}")


def print_help_menu(bb, ioh):
    print('\nAction\tDescription')
    for key, val in ioh.legal_actions.items():
        print(f'  {key}\t{val[0]}')
    return None, None


def get_revision(bb, ioh):
    while True:
        print("Input expression for revision")
        action = input(L_PROMPT)
        try:
            f = sp.parse_expr(action)
        except Exception as e:
            print(f"Error: {e} is not a valid logical expression.")
        
        print("Select rank (integer value):")
        rank = None
        try:
            rank = int(input(L_PROMPT))
        except Exception as e:
            print(f"Error: {e} is not a valid integer.")
        
        return f, rank


def get_contraction(bb, ioh):
    while True:
        print("Input expression for contraction")
        action = input(L_PROMPT)
        try:
            f = sp.parse_expr(action)
        except Exception as e:
            print(f"Error: {e} is not a valid logical expression.")
        
        return f, None


def get_expansion(bb, ioh):
    while True:
        print("Input expression for expansion")
        action = input(L_PROMPT)
        try:
            f = sp.parse_expr(action)
        except Exception as e:
            print(f"Error: {e} is not a valid logical expression.")
        
        print("Select rank (integer value):")
        rank = None
        try:
            rank = int(input(L_PROMPT))
        except Exception as e:
            print(f"Error: {e} is not a valid integer.")
        
        return f, rank


def print_beliefbase(bb, ioh):
    print("The current Belief Base is:")
    print(bb)
    return None, None


def placeholder(bb, ioh):
    return None, None


LEGAL_ACTIONS = {
    'I': ["Instantiate Belief Base", placeholder],
    'P': ["Print Belief Base", print_beliefbase],
    'E': ["Empty Belief Base", placeholder],
    'H': ["Print help dialog", print_help_menu],
    'R': ["Belief Revision", get_revision],
    'C': ["Belief Contraction", get_contraction],
    'A': ["Belief Expansion", get_expansion],
}
