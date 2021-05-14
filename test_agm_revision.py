from BeliefBase import BeliefBase
import sympy as sp

# add a shorthand to use the sympy expression parser
pl = sp.parse_expr


if __name__ == "__main__":
    bb = BeliefBase()
    phi = pl('k')
    bb.instantiate()

    print("\nInitial Belief Base:")
    print(bb)
    print(f'phi = {phi}')

    print("\nAGM Postulates of Revision:")

    # closure, success & vacuity
    print(f'\nrevise with {phi}')
    bb.revision(phi, 30)
    print(bb)

    # inclusion
    print(f'\rcontract with {phi}, then expand with {phi}')
    bb.contract(phi)
    bb.expand(phi, 30)
    print(bb)


