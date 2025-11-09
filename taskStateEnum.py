from enum import Enum

#definovany vycet pro statusy tasku
class TaskStatus(Enum):
    New = 1
    Updated = 2
    Closed = 3