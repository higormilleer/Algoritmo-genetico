from typing import List, Tuple, Dict
from ..models.chromosome import Chromosome, ClassSlot
from ..utils.data import SUBJECTS, TIME_SLOTS, PENALTIES

class FitnessEvaluator:
    def __init__(self):
        self.penalties = PENALTIES
    #realiza a verificacao de todos os conflitos e penalidades
    def evaluate(self, chromosome: Chromosome) -> Tuple[float, Dict[str, float]]:
        """
        Avalia a qualidade do cromossomo (grade horária)
        Retorna um valor de fitness (quanto maior, melhor) e um dicionário com o detalhamento das penalidades.
        """
        total_penalty = 0.0
        penalties_breakdown = {}

        p = self._check_professor_conflicts(chromosome)
        total_penalty += p
        penalties_breakdown['professor_conflict'] = p

        p = self._check_prerequisite_conflicts(chromosome)
        total_penalty += p
        penalties_breakdown['prerequisite_conflict'] = p

        p = self._check_classroom_conflicts(chromosome)
        total_penalty += p
        penalties_breakdown['classroom_conflict'] = p

        p = self._check_period_conflicts(chromosome)
        total_penalty += p
        penalties_breakdown['period_conflict'] = p

        p = self._check_balanced_distribution(chromosome)
        total_penalty += p
        penalties_breakdown['unbalanced_distribution'] = p

        p = self._check_schedule_gaps(chromosome)
        total_penalty += p
        penalties_breakdown['gap_penalty'] = p

        p = self._check_workload(chromosome)
        total_penalty += p
        penalties_breakdown['workload_penalty'] = p

        fitness = 1.0 / (1.0 + total_penalty)
        return fitness, penalties_breakdown

    def _check_professor_conflicts(self, chromosome: Chromosome) -> float:
        """Verifica conflitos de horário dos professores"""
        penalty = 0.0
        for professor in set(slot.professor for slot in chromosome.slots):
            professor_slots = chromosome.get_slots_by_professor(professor)
            for i, slot1 in enumerate(professor_slots):
                for slot2 in professor_slots[i+1:]:
                    if slot1.day == slot2.day and slot1.time_slot == slot2.time_slot:
                        penalty += self.penalties['professor_conflict']
        return penalty

    def _check_prerequisite_conflicts(self, chromosome: Chromosome) -> float:
        """Verifica conflitos de pré-requisitos"""
        penalty = 0.0
        for subject in SUBJECTS:
            if not subject.prerequisites:
                continue
            
            subject_slots = chromosome.get_slots_by_subject(subject.code)
            for prerequisite in subject.prerequisites:
                prereq_slots = chromosome.get_slots_by_subject(prerequisite)
                
                for subject_slot in subject_slots:
                    for prereq_slot in prereq_slots:
                        if (subject_slot.day == prereq_slot.day and 
                            subject_slot.time_slot == prereq_slot.time_slot):
                            penalty += self.penalties['prerequisite_conflict']
        return penalty

    def _check_classroom_conflicts(self, chromosome: Chromosome) -> float:
        """Verifica conflitos de salas"""
        penalty = 0.0
        for classroom in set(slot.classroom for slot in chromosome.slots):
            classroom_slots = chromosome.get_slots_by_classroom(classroom)
            for i, slot1 in enumerate(classroom_slots):
                for slot2 in classroom_slots[i+1:]:
                    if slot1.day == slot2.day and slot1.time_slot == slot2.time_slot:
                        penalty += self.penalties['classroom_conflict']
        return penalty

    def _check_period_conflicts(self, chromosome: Chromosome) -> float:
        """Verifica conflitos de horário no mesmo período"""
        penalty = 0.0
        for period in range(1, 5):
            period_slots = chromosome.get_slots_by_period(period)
            for i, slot1 in enumerate(period_slots):
                for slot2 in period_slots[i+1:]:
                    if slot1.day == slot2.day and slot1.time_slot == slot2.time_slot:
                        penalty += self.penalties['period_conflict']
        return penalty
    #realiza a verificacao de se a distribuicao das aulas esta equilibrada
    def _check_balanced_distribution(self, chromosome: Chromosome) -> float:
        """Verifica se a distribuição das aulas está equilibrada"""
        penalty = 0.0
        for period in range(1, 5):
            period_slots = chromosome.get_slots_by_period(period)
            days_count = {day: 0 for day in set(slot.day for slot in period_slots)}
            
            for slot in period_slots:
                days_count[slot.day] += 1
            
            max_count = max(days_count.values())
            min_count = min(days_count.values())
            if max_count - min_count > 2:  
                penalty += self.penalties['unbalanced_distribution'] * (max_count - min_count)
        
        return penalty

    def _check_schedule_gaps(self, chromosome: Chromosome) -> float:
        """Verifica buracos no horário"""
        penalty = 0.0
        for period in range(1, 5):
            period_slots = chromosome.get_slots_by_period(period)
            for day in set(slot.day for slot in period_slots):
                day_slots = [slot for slot in period_slots if slot.day == day]
                day_slots.sort(key=lambda x: x.time_slot)
                
                for i in range(len(day_slots) - 1):
                    current_idx = TIME_SLOTS.index(day_slots[i].time_slot)
                    next_idx = TIME_SLOTS.index(day_slots[i + 1].time_slot)
                    if next_idx - current_idx > 1:
                        penalty += self.penalties['gap_penalty'] * (next_idx - current_idx - 1)
        
        return penalty

    def _check_workload(self, chromosome: Chromosome) -> float:
        """Verifica se a carga horária está correta"""
        penalty = 0.0
        for subject in SUBJECTS:
            subject_slots = chromosome.get_slots_by_subject(subject.code)
            theory_count = sum(1 for slot in subject_slots if slot.is_theory)
            practice_count = sum(1 for slot in subject_slots if not slot.is_theory)
            
            if theory_count != subject.theory_hours:
                penalty += abs(theory_count - subject.theory_hours) * 100
            if practice_count != subject.practice_hours:
                penalty += abs(practice_count - subject.practice_hours) * 100
        
        return penalty 