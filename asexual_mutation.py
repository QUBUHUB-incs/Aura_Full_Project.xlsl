"""
bio_quantum_core.py
-------------------
Biologically inspired "quantum tissue" simulation for Aura.
Author: Seriki Yakub (KUBU LEE)
Year: 2025
"""

from qiskit import QuantumCircuit, Aer, execute
import random, json, copy, numpy as np

class BioCell:
    """A single living quantum cell."""
    def __init__(self, dna=None):
        self.energy = 1.0
        self.age = 0
        self.dna = dna or self.random_dna()
        self.circuit = self.express(self.dna)
        self.fitness = 0.0

    # --- DNA / gene logic -------------------------------------------------
    def random_dna(self):
        """Generate a random genetic blueprint."""
        return {
            "qubits": random.randint(1, 3),
            "gates": [random.choice(["h", "x", "y", "z"]) for _ in range(random.randint(1, 4))]
        }

    def express(self, dna):
        """Translate DNA into a quantum circuit (phenotype)."""
        qc = QuantumCircuit(dna["qubits"])
        for i, gate in enumerate(dna["gates"]):
            target = i % dna["qubits"]
            getattr(qc, gate)(target)
        return qc

    # --- life functions ---------------------------------------------------
    def evaluate(self):
        """Compute fitness based on entropy (complexity proxy)."""
        backend = Aer.get_backend("statevector_simulator")
        state = execute(self.circuit, backend).result().get_statevector()
        probs = np.abs(state) ** 2
        self.fitness = -np.sum(probs * np.log2(probs + 1e-10))
        return self.fitness

    def mutate(self):
        """Random DNA mutation: gate or qubit change."""
        dna = copy.deepcopy(self.dna)
        if random.random() < 0.5 and len(dna["gates"]) < 6:
            dna["gates"].append(random.choice(["h", "x", "y", "z"]))
        else:
            dna["gates"][random.randint(0, len(dna["gates"]) - 1)] = random.choice(["h", "x", "y", "z"])
        self.dna = dna
        self.circuit = self.express(dna)

    def reproduce(self):
        """Asexual reproduction with mutation."""
        child = BioCell(dna=copy.deepcopy(self.dna))
        child.mutate()
        return child

    def tick(self):
        """Advance one life cycle."""
        self.age += 1
        self.energy *= 0.95
        if self.energy <= 0:
            return False
        return True

class BioQuantumTissue:
    """A colony of BioCells interacting and evolving."""
    def __init__(self, population=5):
        self.cells = [BioCell() for _ in range(population)]
        self.generation = 0

    def evolve(self, generations=5):
        for g in range(generations):
            self.generation += 1
            print(f"\n🌱 Generation {self.generation}")
            for cell in self.cells:
                cell.evaluate()
                cell.energy += cell.fitness / 10
            self.cells.sort(key=lambda c: c.fitness, reverse=True)
            survivors = self.cells[:len(self.cells)//2]
            offspring = [c.reproduce() for c in survivors]
            self.cells = survivors + offspring
            print(f"Best fitness: {self.cells[0].fitness:.4f}")

    def export_genome_pool(self, file="aura_genome.json"):
        pool = [c.dna for c in self.cells]
        with open(file, "w") as f:
            json.dump(pool, f, indent=2)
        print(f"Genome pool saved to {file}")

# Example usage -------------------------------------------------------------
if __name__ == "__main__":
    tissue = BioQuantumTissue(population=8)
    tissue.evolve(generations=6)
    tissue.export_genome_pool()
