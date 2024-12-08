from typing import List, Tuple

def intersection_of_time_ranges(arr1: List[Tuple[int, int]], 
                              arr2: List[Tuple[int, int]]) -> List[Tuple[int, int]]:
    """
    Find the intersection of two lists of time ranges.
    
    Args:
        arr1: First list of time ranges
        arr2: Second list of time ranges
        
    Returns:
        List of intersecting time ranges
    """
    result = []
    arr1.sort(key=lambda x: x[0])
    arr2.sort(key=lambda x: x[0])

    i, j = 0, 0
    while i < len(arr1) and j < len(arr2):
        start1, end1 = arr1[i]
        start2, end2 = arr2[j]

        if end1 < start2:
            i += 1
        elif end2 < start1:
            j += 1
        else:
            intersection_start = max(start1, start2)
            intersection_end = min(end1, end2)

            if result and result[-1][1] >= intersection_start:
                result[-1] = (result[-1][0], max(result[-1][1], intersection_end))
            else:
                result.append((intersection_start, intersection_end))

            if end1 < end2:
                i += 1
            else:
                j += 1

    return result

def find_earliest_available(time_ranges: List[Tuple[int, int]], 
                          duration: int) -> Tuple[int, int]:
    """
    Find the earliest available time slot of required duration.
    
    Args:
        time_ranges: List of available time ranges
        duration: Required duration
        
    Returns:
        Tuple of (start_time, end_time) or None if no suitable slot found
    """
    time_ranges.sort(key=lambda x: x[0])
    
    for start, end in time_ranges:
        if end - start >= duration:
            return (start, start + duration)
            
    return None 

def assign(available_time: List[Tuple[int, int]], task_to_assign: Tuple[int, int]) -> List[Tuple[int, int]]:
    """
    Assign a task to a time slot and update available time ranges.
    
    Args:
        available_time: List of available time ranges [(start, end), ...]
        task_to_assign: Time range to assign (start, end)
        
    Returns:
        Updated list of available time ranges
    """
    task_start, task_end = task_to_assign
    updated_available_time = []

    # Check if the task is completely outside the available time ranges
    task_within_available_time = False
    for start, end in available_time:
        if start <= task_start < task_end <= end:
            task_within_available_time = True
            break

    if not task_within_available_time:
        raise ValueError("Task cannot be assigned within the available time ranges.")

    for start, end in available_time:
        if end <= task_start or start >= task_end:
            # Time range doesn't overlap with task, keep it as is
            updated_available_time.append((start, end))
        else:
            # Time range overlaps with task, split it if necessary
            if start < task_start:
                updated_available_time.append((start, task_start))
            if end > task_end:
                updated_available_time.append((task_end, end))

    return updated_available_time 

def find_earliest_availables(time_ranges: List[Tuple[int, int]], duration: int) -> List[Tuple[int, int]]:
    """
    Find earliest available time slots that sum up to the required duration.
    
    Args:
        time_ranges: List of available time ranges
        duration: Total required duration
        
    Returns:
        List of (start_time, end_time) tuples that sum to duration,
        or empty list if cannot find enough slots
    """
    result = []
    remaining_duration = duration
    time_ranges.sort(key=lambda x: x[0])  # Sort by start time

    for start, end in time_ranges:
        if remaining_duration <= 0:
            break
            
        slot_duration = min(end - start, remaining_duration)
        result.append((start, start + slot_duration))
        remaining_duration -= slot_duration

    # Return empty list instead of None if we couldn't find enough slots
    if remaining_duration > 0:
        return []
        
    return result