import matplotlib.pyplot as plt
import matplotlib.patches as patches
from typing import List, Tuple
import colorsys
from random import shuffle

def generate_distinct_colors(n: int) -> List[str]:
    """
    Generate n visually distinct and pleasant colors using a soothing pastel palette.
    
    Args:
        n: Number of colors needed
        
    Returns:
        List of n distinct colors in hex format
    """
    # Curated pastel color palette with soothing, distinct colors
    base_colors = [
        '#9bd3e1',  # Soft Blue
        '#f8b4b4',  # Soft Red
        '#b8e6c0',  # Soft Green
        '#ffe5b4',  # Soft Yellow
        '#d7bde2',  # Soft Purple
        '#a3e4d7',  # Soft Turquoise
        '#f5cba7',  # Soft Orange
        '#aeb6bf',  # Soft Navy
        '#d5dbdb',  # Soft Gray
        '#a2d9ce',  # Soft Dark Turquoise
        '#edbb99',  # Soft Dark Orange
        '#a9cce3',  # Soft Dark Blue
        '#abebc6',  # Soft Dark Green
        '#d2b4de',  # Soft Dark Purple
        '#f1948a',  # Soft Dark Red
    ]
    
    if n <= len(base_colors):
        return base_colors[:n]
    
    # If we need more colors, generate them using HSV with fixed saturation and value
    additional_needed = n - len(base_colors)
    additional_colors = []
    
    for i in range(additional_needed):
        # Generate evenly spaced hues
        hue = (i * 0.618033988749895) % 1  # Golden ratio conjugate
        saturation = 0.35  # Lower saturation for pastel colors
        value = 0.95      # Higher value for lighter colors
        
        rgb = colorsys.hsv_to_rgb(hue, saturation, value)
        hex_color = '#{:02x}{:02x}{:02x}'.format(
            int(rgb[0] * 255),
            int(rgb[1] * 255),
            int(rgb[2] * 255)
        )
        additional_colors.append(hex_color)
    
    # Combine base colors with additional colors
    all_colors = base_colors + additional_colors
    
    # Shuffle to avoid similar colors being adjacent
    shuffle(all_colors)
    
    return all_colors

def plot_schedule(solution: List[Tuple[int, str, int, Tuple[int, int]]], T: int) -> None:
    """
    Visualize the scheduling solution.
    
    Args:
        solution: List of scheduled tasks (job_id, resource_type, machine_id, (start_time, end_time))
        T: Global time limit
    """
    # Get number of unique jobs for color generation
    unique_jobs = len(set(job_id for job_id, _, _, _ in solution))
    colors = generate_distinct_colors(unique_jobs)
    
    # Group tasks by resource type first, then by machine
    resource_machines = {}
    for job_id, resource_type, machine_id, time_range in solution:
        if resource_type not in resource_machines:
            resource_machines[resource_type] = set()
        resource_machines[resource_type].add(machine_id)
    
    # Calculate total height needed
    total_machines = sum(len(machines) for machines in resource_machines.values())
    
    # Create figure with appropriate height
    fig_height = max(6, total_machines * 0.8)  # At least 6 inches, or more for many machines
    fig, ax = plt.subplots(figsize=(12, fig_height))
    
    # Create y-positions for each resource-machine combination
    y_positions = {}
    current_y = 0
    for resource_type in sorted(resource_machines.keys()):
        for machine_id in sorted(resource_machines[resource_type]):
            y_positions[(resource_type, machine_id)] = current_y
            current_y += 1
            
    # Plot tasks
    for job_id, resource_type, machine_id, (start, end) in solution:
        y = y_positions[(resource_type, machine_id)]
        color = colors[job_id - 1]  # -1 because job_ids start from 1
        
        # Create rectangle for the task
        rect = patches.Rectangle(
            (start, y), 
            end - start, 
            0.8, 
            facecolor=color,
            edgecolor='black'
        )
        ax.add_patch(rect)
        
        # Add job label
        ax.text(
            (start + end) / 2, 
            y + 0.4, 
            f'J{job_id}',
            ha='center',
            va='center'
        )
    
    # Set labels and limits with padding
    ax.set_ylim(-0.5, current_y - 0.5 + 0.3)  # Add padding at the top
    ax.set_xlim(-0.2, T + 0.2)  # Add small padding on sides
    ax.set_yticks(range(current_y))
    
    # Create labels that clearly show resource type and machine number
    y_labels = [f'{resource_type}{machine_id}' 
                for resource_type, machine_id in sorted(y_positions.keys())]
    ax.set_yticklabels(y_labels)
    
    ax.set_xlabel('Time')
    ax.set_ylabel('Resource-Machine')
    ax.set_title('Schedule Visualization')
    
    plt.grid(True)
    plt.tight_layout()
    plt.show() 