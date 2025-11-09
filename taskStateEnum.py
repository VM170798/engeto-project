from enum import Enum

#definovany vycet pro statusy tasku
class TaskStatus(Enum):
    Nezahajeno = 1
    Probiha = 2
    Hotovo = 3