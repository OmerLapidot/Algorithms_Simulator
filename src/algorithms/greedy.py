from typing import Dict, List, Tuple
from ..core.job import Job
from ..core.machine import Machine
from ..core.resource import Resource
from ..utils.scheduling_utils import (
    intersection_of_time_ranges, 
    find_earliest_available,
    find_earliest_availables
)

def greedy_no_preemption(jobs: List[Job], resources: Dict[str, Resource]) -> List[Tuple[int, str, int, Tuple[int, int]]]:
    """
    Implements greedy algorithm without preemption.
    
    Args:
        jobs: List of jobs to schedule
        resources: Dictionary mapping resource type to Resource objects
        
    Returns:
        List of scheduled tasks in format (job_id, resource_type, machine_id, (start_time, end_time))
    """
    solution = []
    
    # Debug print
    print("\nInitial job requirements:")
    for job in jobs:
        print(f"Job {job.id}: {job.task_durations}")
    
    for job in jobs:
        print(f"\nProcessing Job {job.id}")
        for resource_type, duration in job.task_durations.items():
            if duration <= 0:
                continue
                
            print(f"  Resource {resource_type}, Duration {duration}")
            assigned = False
            resource = resources[resource_type]
            
            # Try to assign to existing machines
            for machine in resource.machines:
                try:
                    available_slots = intersection_of_time_ranges(
                        machine.available_time, 
                        job.available_time
                    )
                    print(f"    Trying machine {machine.id}, Available slots: {available_slots}")
                    
                    first_available = find_earliest_available(available_slots, duration)
                    if first_available is not None:
                        machine.assign(first_available)
                        job.assign(first_available)
                        solution.append((job.id, resource_type, machine.id, first_available))
                        print(f"    Assigned to machine {machine.id} at time {first_available}")
                        assigned = True
                        break
                except ValueError:
                    continue
            
            # If no existing machine could handle the task, add a new one
            if not assigned:
                resource.add_machine()
                machine = resource.machines[-1]
                print(f"    Added new machine {machine.id}")
                first_available = find_earliest_available(
                    intersection_of_time_ranges(machine.available_time, job.available_time),
                    duration
                )
                if first_available is not None:
                    solution.append((job.id, resource_type, machine.id, first_available))
                    machine.assign(first_available)
                    job.assign(first_available)
                    print(f"    Assigned to new machine {machine.id} at time {first_available}")
    
    return solution 

def greedy_weak_preemption(jobs: List[Job], resources: Dict[str, Resource]) -> List[Tuple[int, str, int, Tuple[int, int]]]:
    """
    Implements greedy algorithm with weak preemption.
    Tasks can be split but only if necessary to fit into available time slots.
    
    Args:
        jobs: List of jobs to schedule
        resources: Dictionary mapping resource type to Resource objects
        
    Returns:
        List of scheduled tasks in format (job_id, resource_type, machine_id, (start_time, end_time))
    """
    solution = []
    
    print("\nInitial job requirements:")
    for job in jobs:
        print(f"Job {job.id}: {job.task_durations}")
    
    for job in jobs:
        print(f"\nProcessing Job {job.id}")
        for resource_type, duration in job.task_durations.items():
            if duration <= 0:
                continue
                
            print(f"  Resource {resource_type}, Duration {duration}")
            assigned = False
            resource = resources[resource_type]
            
            # Try to assign to existing machines
            for machine in resource.machines:
                try:
                    available_slots = intersection_of_time_ranges(
                        machine.available_time, 
                        job.available_time
                    )
                    print(f"    Trying machine {machine.id}, Available slots: {available_slots}")
                    
                    total_available_time = sum(end - start for start, end in available_slots)
                    if total_available_time >= duration:
                        # Found machine with enough total time
                        time_slots = find_earliest_availables(available_slots, duration)
                        if time_slots:  # Check if we got valid time slots
                            for time_range in time_slots:
                                machine.assign(time_range)
                                job.assign(time_range)
                                solution.append((job.id, resource_type, machine.id, time_range))
                                print(f"    Assigned to machine {machine.id} at time {time_range}")
                            assigned = True
                            break
                except ValueError:
                    continue
            
            # If no existing machine could handle the task, add a new one
            if not assigned:
                resource.add_machine()
                machine = resource.machines[-1]
                print(f"    Added new machine {machine.id}")
                time_slots = find_earliest_availables(
                    intersection_of_time_ranges(machine.available_time, job.available_time),
                    duration
                )
                if time_slots:  # Check if we got valid time slots
                    for time_range in time_slots:
                        solution.append((job.id, resource_type, machine.id, time_range))
                        machine.assign(time_range)
                        job.assign(time_range)
                        print(f"    Assigned to new machine {machine.id} at time {time_range}")
                else:
                    print(f"    WARNING: Could not find valid time slots for job {job.id} on resource {resource_type}")
    
    return solution 