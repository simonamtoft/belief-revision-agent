from BeliefBase import BeliefBase
import sympy as sp

# add a shorthand to use the sympy expression parser
pl = sp.parse_expr


if __name__ == "__main__":
    bb = BeliefBase()
    phi = pl('r')
    bb.instantiate()
    
    print("\nInitial Belief Base:")
    print(bb)
    print(f'phi = {phi}')
    
    print("\nAGM Postulates of Contraction:")
    
    # success + inclusion
    print(f'\ncontract with {phi}')
    bb.contract(phi)
    print(bb)
    
    # vacuity
    print(f'\ncontract with {phi}')
    bb.contract(phi)
    print(bb)
    
    # recovery
    print(f'\nexpand with {phi}')
    bb.expand(phi, 10)
    print(bb)

    

