import random
from typing import List, Tuple
from ..models.chromosome import Chromosome, ClassSlot
from ..utils.data import DAYS, TIME_SLOTS, PROFESSORS, CLASSROOMS, SUBJECTS
from ..genetic.fitness import FitnessEvaluator

class GeneticOperators:
    def __init__(self, mutation_rate: float = 0.1, crossover_rate: float = 0.8, fitness_evaluator: FitnessEvaluator = None):
        self.mutation_rate = mutation_rate
        self.crossover_rate = crossover_rate
        self.fitness_evaluator = fitness_evaluator 

    def tournament_selection(self, population: List[Chromosome], tournament_size: int = 3) -> Chromosome:
        """Seleção por torneio"""
        tournament = random.sample(population, tournament_size)
        return max(tournament, key=lambda x: x.fitness)

    def crossover(self, parent1: Chromosome, parent2: Chromosome) -> Tuple[Chromosome, Chromosome]:
        """Operador de crossover que preserva a contagem de slots por disciplina"""
        if random.random() > self.crossover_rate:
            return parent1, parent2

        child1 = Chromosome()
        child2 = Chromosome()

        all_subjects_codes = list(set(slot.subject.code for slot in parent1.slots))
        random.shuffle(all_subjects_codes)

        for subject_code in all_subjects_codes:
            parent1_subject_slots = [slot for slot in parent1.slots if slot.subject.code == subject_code]
            parent2_subject_slots = [slot for slot in parent2.slots if slot.subject.code == subject_code]

            if random.random() < 0.5:  
                child1.slots.extend(parent1_subject_slots)
                child2.slots.extend(parent2_subject_slots)
            else:  
                child1.slots.extend(parent2_subject_slots)
                child2.slots.extend(parent1_subject_slots)
        
        random.shuffle(child1.slots)
        random.shuffle(child2.slots)

        return child1, child2

    def mutate(self, chromosome: Chromosome) -> Chromosome:
        """Operador de mutação inteligente: tenta mover um slot para minimizar a penalidade total do cromossomo
        Explora um número limitado de movimentos aleatórios para otimizar o desempenho."""
        if self.fitness_evaluator is None:
            raise ValueError("A instância de FitnessEvaluator deve ser fornecida para GeneticOperators para mutação inteligente.")

        mutated = Chromosome()
        mutated.slots = chromosome.slots.copy()
        
        num_slots = len(mutated.slots)

        slots_to_mutate_indices = random.sample(range(num_slots), int(num_slots * self.mutation_rate))

        for i in slots_to_mutate_indices:
            original_slot = mutated.slots[i]
            best_mutated_slot = original_slot
            best_found_fitness = self.fitness_evaluator.evaluate(mutated)[0] # Avalia o estado atual do cromossomo inteiro

            temp_slots_without_current = mutated.slots[:i] + mutated.slots[i+1:]
            
            num_mutation_attempts_per_slot = 50 
            for _ in range(num_mutation_attempts_per_slot):
                day = random.choice(DAYS)
                time_slot = random.choice(TIME_SLOTS)
                professor = random.choice(PROFESSORS)
                classroom = random.choice(CLASSROOMS)

                hypothetical_slot = ClassSlot(
                    subject=original_slot.subject,
                    day=day,
                    time_slot=time_slot,
                    professor=professor,
                    classroom=classroom,
                    is_theory=original_slot.is_theory
                )

                if not self._is_slot_valid(hypothetical_slot, temp_slots_without_current):
                    continue # Pula se houver conflito direto

                temp_chromosome_with_hypothetical = Chromosome()
                temp_chromosome_with_hypothetical.slots = temp_slots_without_current + [hypothetical_slot]
                
                hypothetical_fitness, _ = self.fitness_evaluator.evaluate(temp_chromosome_with_hypothetical)
                
                if hypothetical_fitness > best_found_fitness:
                    best_found_fitness = hypothetical_fitness
                    best_mutated_slot = hypothetical_slot
            
            if best_mutated_slot != original_slot:
                mutated.slots[i] = best_mutated_slot
            mutated.fitness = best_found_fitness 
                
        return mutated

    def _is_slot_valid(self, potential_slot: ClassSlot, existing_slots: List[ClassSlot]) -> bool:
        """Verifica se um slot potencial entra em conflito com qualquer slot existente em termos de professor, sala e período."""
        for existing_slot in existing_slots:
            if (existing_slot.day == potential_slot.day and
                existing_slot.time_slot == potential_slot.time_slot):
                if existing_slot.professor == potential_slot.professor:
                    return False
                if existing_slot.classroom == potential_slot.classroom:
                    return False
                if existing_slot.subject.period == potential_slot.subject.period:
                    return False
        return True

    def create_initial_population(self, size: int, subjects: List) -> List[Chromosome]:
        """Cria a população inicial, tentando alocar slots para minimizar conflitos (professor, sala, período)."""
        population = []
        for _ in range(size):
            chromosome = Chromosome()
            
            all_required_slots_info = []
            for subject in subjects:
                for _ in range(subject.theory_hours):
                    all_required_slots_info.append({'subject': subject, 'is_theory': True})
                for _ in range(subject.practice_hours):
                    all_required_slots_info.append({'subject': subject, 'is_theory': False})
            
            random.shuffle(all_required_slots_info)
            current_chromosome_slots_for_validation = [] 

            for slot_info in all_required_slots_info:
                current_subject = slot_info['subject']
                is_theory = slot_info['is_theory']
                
                found_placement = False
                attempts = 0
                max_attempts = 200 

                while not found_placement and attempts < max_attempts:
                    day = random.choice(DAYS)
                    time_slot = random.choice(TIME_SLOTS)
                    professor = random.choice(PROFESSORS)
                    classroom = random.choice(CLASSROOMS)

                    potential_slot = ClassSlot(
                        subject=current_subject,
                        day=day,
                        time_slot=time_slot,
                        professor=professor,
                        classroom=classroom,
                        is_theory=is_theory
                    )

                    if self._is_slot_valid(potential_slot, current_chromosome_slots_for_validation):
                        chromosome.add_slot(potential_slot)
                        current_chromosome_slots_for_validation.append(potential_slot)
                        found_placement = True
                    attempts += 1
                
                if not found_placement:
                    new_slot = ClassSlot(
                        subject=current_subject,
                        day=random.choice(DAYS),
                        time_slot=random.choice(TIME_SLOTS),
                        professor=random.choice(PROFESSORS),
                        classroom=random.choice(CLASSROOMS),
                        is_theory=is_theory
                    )
                    chromosome.add_slot(new_slot)
                    current_chromosome_slots_for_validation.append(new_slot)
            
            population.append(chromosome)
        
        return population

    def elitism(self, population: List[Chromosome], elite_size: int = 2) -> List[Chromosome]:
        """Mantém os melhores indivíduos da população"""
        return sorted(population, key=lambda x: x.fitness, reverse=True)[:elite_size] 