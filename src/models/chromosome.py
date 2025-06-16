from dataclasses import dataclass
from typing import List, Dict, Optional
from ..utils.data import Subject, DAYS, TIME_SLOTS, PROFESSORS, CLASSROOMS

@dataclass
class ClassSlot:
    subject: Subject
    day: str
    time_slot: str
    professor: str
    classroom: str
    is_theory: bool

# representa uma solucao possivel para o problema de grade horaria,contendo uma lista de slots de aula e um valor de fitness que indica a qualdiade da solucao
class Chromosome:
    def __init__(self):
        self.slots: List[ClassSlot] = []
        self.fitness: float = 0.0

    def add_slot(self, slot: ClassSlot):
        self.slots.append(slot)

    def get_slots_by_period(self, period: int) -> List[ClassSlot]:
        return [slot for slot in self.slots if slot.subject.period == period]

    def get_slots_by_subject(self, subject_code: str) -> List[ClassSlot]:
        return [slot for slot in self.slots if slot.subject.code == subject_code]

    def get_slots_by_professor(self, professor: str) -> List[ClassSlot]:
        return [slot for slot in self.slots if slot.professor == professor]

    def get_slots_by_day_time(self, day: str, time_slot: str) -> List[ClassSlot]:
        return [slot for slot in self.slots if slot.day == day and slot.time_slot == time_slot]

    def get_slots_by_classroom(self, classroom: str) -> List[ClassSlot]:
        return [slot for slot in self.slots if slot.classroom == classroom]

    def to_dict(self) -> Dict:
        """Converte o cromossomo para um dicionário organizado por período"""
        schedule = {}
        for period in range(1, 5):
            period_slots = self.get_slots_by_period(period)
            schedule[period] = {
                day: {
                    time: [slot for slot in period_slots if slot.day == day and slot.time_slot == time]
                    for time in TIME_SLOTS
                }
                for day in DAYS
            }
        return schedule
    #Converte a grade em uma representacao visual em texto, organizada por periodos,com dias da semana nas colunas e horario nas respectivas linhas
    def __str__(self) -> str:
        """Retorna uma representação em string da grade horária"""
        schedule = self.to_dict()
        output = []
        
        for period in range(1, 5):
            output.append(f"\nPeríodo {period}")
            output.append("=" * 50)
            
            
            header = "Horário | " + " | ".join(DAYS)
            output.append(header)
            output.append("-" * len(header))
            
            
            for time in TIME_SLOTS:
                row = [time]
                for day in DAYS:
                    slots = schedule[period][day][time]
                    if slots:
                        slot = slots[0]  
                        cell = f"{slot.subject.code} ({slot.professor})"
                    else:
                        cell = "-"
                    row.append(cell)
                output.append(" | ".join(row))
            
            output.append("")  
        
        return "\n".join(output) 