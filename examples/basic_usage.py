from src.core.job import Job
from src.core.resource import Resource
from src.algorithms.greedy import greedy_no_preemption, greedy_weak_preemption
from src.utils.visualization import plot_schedule

def run_test_case(jobs_data: list, T: int, name: str = "Test Case", algorithm="no_preemption"):
    """
    Run a test case with given jobs data.
    
    Args:
        jobs_data: List of tuples (job_id, A_duration, B_duration)
        T: Global time limit
        name: Name of the test case
        algorithm: Which algorithm to use ("no_preemption" or "weak_preemption")
    """
    print(f"\nRunning {name}")
    print("-" * 40)
    
    # Create jobs
    jobs = [
        Job(job_id, {'A': a_dur, 'B': b_dur}, T)
        for job_id, a_dur, b_dur in jobs_data
    ]
    
    # Create resources
    resources = {
        'A': Resource('A', T),
        'B': Resource('B', T)
    }
    
    # Run selected algorithm
    if algorithm == "no_preemption":
        solution = greedy_no_preemption(jobs, resources)
    elif algorithm == "weak_preemption":
        solution = greedy_weak_preemption(jobs, resources)
    else:
        raise ValueError(f"Unknown algorithm: {algorithm}")
    
    # Print job assignments
    print("\nJob Assignments:")
    for job_id, resource_type, machine_id, (start, end) in solution:
        print(f"Job {job_id} on {resource_type}{machine_id}: {start}-{end}")
    
    # Print machine usage
    print("\nMachine Usage:")
    for resource_type, resource in resources.items():
        print(f"Resource {resource_type} uses {len(resource.machines)} machines")
    
    # Visualize result
    plot_schedule(solution, T)

def main():
    # Test Case 1: Original example with no preemption
    test_case_1 = [
        (1, 3, 2),  # Job 1: A=3, B=2
        (2, 2, 4),  # Job 2: A=2, B=4
        (3, 4, 1),  # Job 3: A=4, B=1
    ]
    run_test_case(test_case_1, T=10, name="Original Example (No Preemption)", 
                 algorithm="no_preemption")
    
    # Test Case 2: More challenging example with no preemption
    test_case_2 = [
        (1, 3, 2),  # Job 1: A=3, B=2
        (2, 5, 3),  # Job 2: A=5, B=3
        (3, 4, 5),  # Job 3: A=4, B=5
        (4, 2, 2),  # Job 4: A=2, B=2
    ]
    run_test_case(test_case_2, T=10, name="Challenging Example (No Preemption)", 
                 algorithm="no_preemption")
    
    # Test Case 3: Weak Preemption Example
    test_case_3 = [
        (1, 4, 2),  # Job 1: A=4, B=2
        (2, 3, 4),  # Job 2: A=3, B=4
        (3, 5, 3),  # Job 3: A=5, B=3
    ]
    run_test_case(test_case_3, T=5, name="Weak Preemption Example", 
                 algorithm="weak_preemption")

if __name__ == "__main__":
    main() 