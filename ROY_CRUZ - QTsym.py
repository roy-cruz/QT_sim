import numpy as n
import cirq as cq
from cirq import InsertStrategy


def qteleport_circuit_construction(phi, theta, Q0, Q1, Q2):
    circuit = cq.Circuit()
    # Moments which set the state to the desired INITIAL state, representing the message to be sent
    # (inM <=> "initialization moment")
    inM_0 = cq.Moment([cq.Y(Q0) ** (theta / n.pi)])
    inM_1 = cq.Moment([cq.Z(Q0) ** (phi / n.pi)])

    # Circuit to ENTANGLE A and B's qubits
    # (enM <=> "entanglement moment")
    enM_0 = cq.Moment([cq.H(Q1)])
    enM_1 = cq.Moment([cq.CNOT(Q1, Q2)])

    # Quantum TELEPORTATION circuit
    M_0 = cq.Moment([cq.CNOT(Q0, Q1)])
    M_1 = cq.Moment([cq.H(Q0)])
    M_2 = cq.Moment([cq.measure(Q0, Q1)])

    # Construction of circuit
    circuit.append((inM_0, inM_1, enM_0, enM_1, M_0, M_1, M_2, cq.CNOT(Q1, Q2), cq.CZ(Q0, Q2)),
                   strategy=InsertStrategy.NEW)
    print(circuit)

    return circuit


def main():
    # Creation of the three qubits to be used; Q0 = qubit containing message to be sent, Q1 & Q2 = A & B's respective
    # entangled qubits
    (Q0, Q1, Q2) = cq.LineQubit.range(3)

    # Angles which specify the state Q0 is initially in; If theta = 0 or theta = pi, then phi is set to 0 (global
    # phase is discarded)
    phi = 1  # 0 <= phi <= 2pi
    theta = 2  # 0 <= theta <= pi
    if theta == 0 or theta == n.pi:
        phi = 0

    circ = qteleport_circuit_construction(phi, theta, Q0, Q1, Q2)

    # Print A's original message (In cartesian and spherical Bloch coords)
    original_msg = cq.Simulator().simulate(cq.Circuit([cq.Y(Q0) ** (theta / n.pi), cq.Z(Q0) ** (phi / n.pi)]))
    AX, AY, AZ = cq.bloch_vector_from_state_vector(original_msg.final_state, 0)
    # Cartesian
    print('\nInitial state of messenger qubit (X, Y, Z): ', '(', round(AX, 3), ',', round(AY, 3), ',',
          round(AZ, 3), ')')
    # Spherical
    rhoA = n.sqrt(AX ** 2 + AY ** 2 + AZ ** 2)
    print('Initial state of messenger qubit (theta, phi, rho): ', '(', round(theta, 3), ',', round(phi, 3), ',',
          round(rhoA, 3), ')')

    # Simulate circuit & print B's received message (In cartesian and spherical Bloch coords)
    sim = cq.Simulator().simulate(circ)
    BX, BY, BZ = cq.bloch_vector_from_state_vector(sim.final_state, 2)
    # Cartesian
    print('\nFinal state of Bob\'s qubit (X, Y, Z): ', '(', round(BX, 3), ',', round(BY, 3), ',',
          round(BZ, 3), ')')
    # Spherical
    rB = n.sqrt(BX ** 2 + BY ** 2)
    thetaB = n.arccos(BZ / 1)
    if theta == 0 or theta == n.pi:
        phiB = 0
    else:
        phiB = n.arccos(BX / rB)
    rhoB = BX ** 2 + BY ** 2 + BZ ** 2
    print('Final state of Bob\'s qubit (theta, phi, rho): ', '(', round(thetaB, 3), ',', round(phiB, 3), ',',
          round(rhoB, 3), ')')


if __name__ == "__main__":
    main()
