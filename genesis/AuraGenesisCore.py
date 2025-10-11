"""
AuraGenesisCore.py
------------------
Quantum Self-Replicating Ecosystem
Author: Seriki Yakub (KUBU LEE)
Project: Aura
Year: 2025

This system builds an ecosystem of self-evolving quantum circuits.
Each "Aura Core" is a living entity that competes and collaborates
in a generational evolution cycle.
"""

from qiskit import QuantumCircuit, Aer, execute
import numpy as np
import random
import copy

class AuraCore:
    def __init__(self, qubits=2):
        self.circuit = QuantumCircuit(qubits)
        for q in range(qubits):
            self.circuit.h(q)
        self.fitness = 0.0

    def mutate(self):
        """Randomly change the quantum circuit."""
        action = random.choice(["add_qubit", "add_gate"])
        if action == "add_qubit":
            self._add_qubit()
        else:
            self._add_gate()

    def _add_qubit(self):
        n = self.circuit.num_qubits + 1
        new_circuit = QuantumCircuit(n)
        new_circuit.compose(self.circuit, inplace=True)
        new_circuit.h(n-1)
        self.circuit = new_circuit

    def _add_gate(self):
        q = random.randint(0, self.circuit.num_qubits - 1)
        gates = [self.circuit.h, self.circuit.x, self.circuit.y, self.circuit.z]
        random.choice(gates)(q)

    def evaluate(self):
        """Entropy-based fitness (quantum chaos = potential)."""
        backend = Aer.get_backend("statevector_simulator")
        result = execute(self.circuit, backend).result()
        statevector = result.get_statevector()
        probs = np.abs(statevector)**2
        entropy = -np.sum(probs * np.log2(probs + 1e-10))
        self.fitness = entropy
        return entropy

    def reproduce(self):
        """Clone and mutate to create a new generation."""
        child = copy.deepcopy(self)
        child.mutate()
        return child

class AuraGenesis:
    def __init__(self, population_size=5):
        self.population = [AuraCore() for _ in range(population_size)]
        self.generation = 0

    def evolve(self, generations=5):
        print("⚛️ [Aura Genesis] Evolution begins...")
        for gen in range(generations):
            self.generation += 1
            print(f"\n🌱 Generation {self.generation}")

            # Evaluate all cores
            for core in self.population:
                score = core.evaluate()
                print(f"   ▪ Core fitness: {score:.4f}")

            # Select top performers
            self.population.sort(key=lambda c: c.fitness, reverse=True)
            top_half = self.population[:len(self.population)//2]

            # Reproduce from the best
            offspring = []
            for parent in top_half:
                child = parent.reproduce()
                offspring.append(child)

            # Merge new generation
            self.population = top_half + offspring

            best = self.population[0]
            print(f"✨ Best core fitness: {best.fitness:.4f}")
        
        print("\n🌌 [Aura Genesis] Evolution complete.")
        print(f"Total generations: {self.generation}")

    def visualize_best(self):
        best = max(self.population, key=lambda c: c.fitness)
        print("\n🧠 [Aura] Best Quantum Brain Structure:")
        return best.circuit.draw(output="text")


# Example usage
if __name__ == "__main__":
    aura_system = AuraGenesis(population_size=6)
    aura_system.evolve(generations=8)
    print(aura_system.visualize_best())
