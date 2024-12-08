from typing import Dict, List, Tuple
from ..utils.scheduling_utils import assign

class Job:
    """
    Represents a job that needs to be scheduled with its resource requirements.
    """
    def __init__(self, job_id: int, task_durations: Dict[str, int], T: int):
        """
        Initialize a job with its requirements.
        
        Args:
            job_id: Unique identifier for the job
            task_durations: Dictionary mapping resource types to required duration
            T: Global time limit
        """
        self.id = job_id
        self.task_durations = task_durations
        self.available_time = [(0, T)]

    def assign(self, time_range: Tuple[int, int]) -> None:
        """
        Assign a time range to this job, updating its available time slots.
        
        Args:
            time_range: Tuple of (start_time, end_time)
        """
        self.available_time = assign(self.available_time, time_range) 