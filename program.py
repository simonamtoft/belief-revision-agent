import sympy as sp
from io_handler import IOHandler

legal_actions = {
    "R": ["Revision", 0],
    "C": ["Contraction", 1],
    "P": ["Print Belief Base", 2]
}


if __name__ == "__main__":
    print("Program...")
    ioh = IOHandler(legal_actions)
    ioh.print_help_menu()
    action = ioh.get_user_input()
    print(action)
    # print(sp.to_cnf("a << b & a >> b", simplify=True))
