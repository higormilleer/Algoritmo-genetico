from dataclasses import dataclass
from typing import List, Optional

@dataclass
class Subject:
    code: str
    name: str
    period: int
    theory_hours: int
    practice_hours: int
    prerequisites: List[str]

SUBJECTS = [
    Subject("CC1AED1", "Algoritmos e Estrutura de Dados I", 1, 4, 2, []),
    Subject("CC1CC", "Introdução à Ciência da Computação", 1, 3, 0, []),
    Subject("CC1MBD", "Modelagem de Banco de Dados", 1, 2, 2, []),
    Subject("ENADE.I", "Enade Ingressante", 1, 0, 0, []),
    Subject("HU1LA", "Linguagem Acadêmica", 1, 2, 1, []),
    Subject("MA1FM", "Fundamentos de Matemática", 1, 4, 0, []),
    Subject("MA1LM", "Lógica Matemática", 1, 3, 0, []),

    Subject("CC2AED2", "Algoritmos e Estrutura de Dados II", 2, 2, 2, ["CC1AED1"]),
    Subject("CC2CLD", "Circuitos Lógicos Digitais", 2, 2, 2, ["MA1LM"]),
    Subject("CC2ER", "Engenharia de Requisitos", 2, 3, 1, []),
    Subject("CC2POO", "Programação Orientada a Objetos", 2, 2, 2, ["CC1AED1"]),
    Subject("MA2MA", "Matemática Aplicada", 2, 4, 0, []),

    Subject("CC3AED3", "Algoritmos e Estrutura de Dados III", 3, 3, 1, ["CC2AED2"]),
    Subject("CC3AOC", "Arquitetura e Organização de Computadores", 3, 3, 3, []),
    Subject("CC3ES", "Engenharia de Software", 3, 3, 1, ["CC1AED1", "CC2ER"]),
    Subject("CC3PI1", "Projeto Integrador I", 3, 1, 8, []),
    Subject("MA3AL", "Álgebra Linear", 3, 3, 0, []),
    Subject("MA3CA", "Cálculo Aplicado", 3, 4, 0, []),

    Subject("CC4IHC", "Interação Humano Computador", 4, 2, 2, []),
    Subject("CC4LBD", "Laboratório de Banco de Dados", 4, 1, 3, ["CC1MBD"]),
    Subject("CC4PO", "Pesquisa e Ordenação", 4, 3, 1, ["CC3AED3", "MA1FM"]),
    Subject("CC4RC", "Redes de Computadores", 4, 2, 2, ["CC3AOC"]),
    Subject("CC4SO", "Sistemas Operacionais", 4, 2, 2, ["CC3AOC"]),
    Subject("MA4PE", "Probabilidade e Estatística", 4, 4, 0, []),
]

DAYS = ["Segunda", "Terça", "Quarta", "Quinta", "Sexta"]
TIME_SLOTS = ["1º", "2º", "3º", "4º", "5º", "6º"]

PROFESSORS = [
    "Prof. Silva",
    "Prof. Santos",
    "Prof. Oliveira",
    "Prof. Souza",
    "Prof. Lima",
    "Prof. Costa",
    "Prof. Ferreira",
    "Prof. Pereira",
    "Prof. Rodrigues",
    "Prof. Almeida",
]

CLASSROOMS = [
    "Sala 101",
    "Sala 102",
    "Sala 103",
    "Sala 104",
    "Lab 201",
    "Lab 202",
    "Lab 203",
]

POPULATION_SIZE = 100
GENERATIONS = 500
MUTATION_RATE = 0.2
CROSSOVER_RATE = 0.8
TOURNAMENT_SIZE = 5

PENALTIES = {
    'professor_conflict': 100,  # conflito de horario 
    'prerequisite_conflict': 0,  # conflito de pre-requisito
    'classroom_conflict': 50,  # conflito de sala
    'period_conflict': 100,  # conflito de horario no mesmo periodo
    'unbalanced_distribution': 20,  # cistribuicao desequilibrada
    'gap_penalty': 10,  # penalidade por buracos no horario
    'workload_penalty': 100, # penalidade por carga horaria incorreta
} 