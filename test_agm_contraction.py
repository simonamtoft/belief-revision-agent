from BeliefBase import BeliefBase
import sympy as sp
from sympy.logic.boolalg import And, Not

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
    
    # closure, success + inclusion
    print("\n=== CLOSURE, SUCCESS & INCLUSION ===")
    print(f'\ncontract with {phi}')
    bb.contract(phi)
    print(bb)
    
    # vacuity
    print("\n=== VACUITY ===")
    print(f'\ncontract with {phi}')
    bb.contract(phi)
    print(bb)
    
    # recovery
    print("\n=== RECOVERY ===")
    print(f'\nexpand with {phi}')
    bb.expand(phi, 20)
    print(bb)

    # conjunctive inclusion
    print("\n=== CONJUNCTIVE INCLUSION / OVERLAP ===")
    psi = pl('p')
    tmp = bb.beliefs.copy()

    print(f'\ncontract with "{phi} & {psi}"')
    bb.contract(And(phi, psi))
    print(bb)

    print("\nrecover previous BB")
    bb.beliefs = tmp.copy()
    # print(bb)

    print(f"\ncontract with {phi}")
    bb.contract(phi)
    print(bb)

    # conjunctive overlap
    print("recover BB again")
    bb.beliefs = tmp.copy()
    # print(bb)
    print(f'\ncontract with {psi}')
    bb.contract(psi)
    print(bb)

