import sys
import os

# Add the project root to Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = current_dir  # Since we're already in the root directory
sys.path.append(project_root)

# Now run the example
from examples.basic_usage import main

if __name__ == "__main__":
    print("Starting scheduling algorithm tests...")
    print("=" * 50)
    main()
    print("\nAll tests completed.") 