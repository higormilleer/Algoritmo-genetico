import random
import numpy as np
import matplotlib.pyplot as plt
from typing import List, Tuple
from src.models.chromosome import Chromosome
from src.genetic.operators import GeneticOperators
from src.genetic.fitness import FitnessEvaluator
from src.utils.data import SUBJECTS, POPULATION_SIZE, GENERATIONS, MUTATION_RATE, CROSSOVER_RATE, TOURNAMENT_SIZE, TIME_SLOTS

def main():
    print("Iniciando o algoritmo genético...")
    # inicializa os componentes 
    fitness_evaluator = FitnessEvaluator()
    operators = GeneticOperators(mutation_rate=MUTATION_RATE, crossover_rate=CROSSOVER_RATE, fitness_evaluator=fitness_evaluator)
    print("Componentes inicializados.")
    # cria a populacao inicial
    population = operators.create_initial_population(POPULATION_SIZE, SUBJECTS)
    print("População inicial criada.")
    # avalia a mesma
    for i, chromosome in enumerate(population):
        chromosome.fitness, penalties_breakdown = fitness_evaluator.evaluate(chromosome)
        if i == 0: 
            print("\nDetalhes das penalidades para o primeiro cromossomo da população inicial:")
            for penalty_type, penalty_value in penalties_breakdown.items():
                print(f"  {penalty_type}: {penalty_value:.2f}")
    print("População inicial avaliada.")
    best_fitness_history = []
    avg_fitness_history = []
    # loop principal do algoritmo genetico, que refatora a populacao e avalia o fitness dos mesmos
    for generation in range(GENERATIONS):
        # Mantem os melhores individuos, atraves do elitismo
        elite = operators.elitism(population, elite_size=2)
        parents = []
        for _ in range((POPULATION_SIZE - len(elite)) // 2):
            parent1 = operators.tournament_selection(population, TOURNAMENT_SIZE)
            parent2 = operators.tournament_selection(population, TOURNAMENT_SIZE)
            parents.append((parent1, parent2))
        new_population = []
        # Crossover, mutacao e acaba avilnado o filho dos mesmos
        for parent1, parent2 in parents:
            child1, child2 = operators.crossover(parent1, parent2)
            child1 = operators.mutate(child1)
            child2 = operators.mutate(child2)
            child1.fitness, _ = fitness_evaluator.evaluate(child1)
            child2.fitness, _ = fitness_evaluator.evaluate(child2)
            new_population.extend([child1, child2])
        new_population.extend(elite)
        population = new_population
        best_fitness = max(chromosome.fitness for chromosome in population)
        avg_fitness = sum(chromosome.fitness for chromosome in population) / len(population)
        best_fitness_history.append(best_fitness)
        avg_fitness_history.append(avg_fitness)
        if (generation + 1) % 10 == 0:
            print(f"Geração {generation + 1}: Melhor Fitness = {best_fitness:.4f}, Média Fitness = {avg_fitness:.4f}")
    #Plota o grafico fitness e tambem encontra o melhor individuos entre todos
    best_chromosome = max(population, key=lambda x: x.fitness)
    print("\nMelhor Grade Horária Encontrada:")
    print(best_chromosome)
    plt.figure(figsize=(10, 6))
    plt.plot(best_fitness_history, label='Melhor Fitness')
    plt.plot(avg_fitness_history, label='Média Fitness')
    plt.xlabel('Geração')
    plt.ylabel('Fitness')
    plt.title('Evolução do Fitness')
    plt.legend()
    plt.grid(True)
    plt.savefig('fitness_evolution.png')
    plt.close()
    with open('grade_horaria.txt', 'w', encoding='utf-8') as f:
        f.write(str(best_chromosome))

if __name__ == "__main__":
    main() 