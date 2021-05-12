from BeliefBase import BeliefBase
from io_handler import IOHandler, print_help_menu


if __name__ == "__main__":
    print("Program Start")
    bb = BeliefBase()
    ioh = IOHandler(bb)
    print_help_menu(bb, ioh)

    while True:
        a, f, rank = ioh.get_user_input()
        if a == 'I':
            bb.instantiate()
        elif a == 'E':
            bb.reset()
        elif a == 'R':
            bb.revision(f, rank)



    
