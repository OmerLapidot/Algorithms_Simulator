from typing import List, Tuple
from ..utils.scheduling_utils import assign

class Machine:
    """
    Represents a single machine that can process jobs.
    """
    def __init__(self, machine_id: int, T: int):
        """
        Initialize a machine.
        
        Args:
            machine_id: Unique identifier for the machine
            T: Global time limit
        """
        self.id = machine_id
        self.available_time = [(0, T)]

    def assign(self, task_to_assign: Tuple[int, int]) -> None:
        """
        Assign a task to this machine, updating its available time slots.
        
        Args:
            task_to_assign: Tuple of (start_time, end_time)
        """
        self.available_time = assign(self.available_time, task_to_assign) 