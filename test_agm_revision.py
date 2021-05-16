from BeliefBase import BeliefBase
import sympy as sp
from sympy.logic.boolalg import And, Not


# add a shorthand to use the sympy expression parser
pl = sp.parse_expr


if __name__ == "__main__":
    bb = BeliefBase()
    phi = pl('k')
    bb.instantiate()
    tmp = bb.beliefs.copy()
    print("\nInitial Belief Base:")
    print(bb)
    print(f'phi = {phi}')

    print("\nAGM Postulates of Revision:")

    # closure, success & vacuity
    print("\n=== CLOSURE, SUCCESS & VACUITY ===")
    print(f'\nrevise with {phi}')
    bb.revision(phi, 5)
    print(bb)

    # Subexpansion
    print("\n=== SUBEXPANSION ===")
    phi_2 = pl('z')
    print(f'\nexpand with {phi_2}')
    bb.expand(phi_2, 5)
    print(bb)
    
    bb.beliefs = tmp
    print(f'\nrevise with with "{phi_2} & {phi}"')
    bb.revision(And(phi_2, phi), 5)
    print(bb)

    # inclusion
    print("\n=== INCLUSION ===")
    print(f'\nremove {phi} from previous BB, then expand with {phi}')
    bb.contract(phi)
    bb.expand(phi, 5)
    print(bb)

    # super expansion
    print("\n=== SUPEREXPANSION ===")
    phi_1 = pl('~p')
    psi_1 = pl('~r')
    tmp = bb.beliefs.copy()
    print(f'\nrevise with "{phi_1} & {psi_1}"')
    bb.revision(And(phi_1, psi_1), 20)
    print(bb)

    print("\nRecover previous BB.")
    bb.beliefs = tmp
    print(bb)

    print(f"\nRevise with {phi_1}, expand with {psi_1}")
    bb.revision(phi_1, 20)
    bb.expand(psi_1, 20)
    print(bb)


