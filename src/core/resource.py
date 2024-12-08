from typing import List
from .machine import Machine

class Resource:
    """
    Represents a resource type that can have multiple machines.
    """
    def __init__(self, resource_type: str, T: int):
        """
        Initialize a resource.
        
        Args:
            resource_type: Type identifier for this resource
            T: Global time limit
        """
        self.resource_type = resource_type
        self.machines: List[Machine] = []
        self.T = T
        self.cost = 1  # Cost per machine of this type

    def add_machine(self) -> None:
        """Add a new machine of this resource type."""
        self.machines.append(Machine(machine_id=len(self.machines) + 1, T=self.T)) 