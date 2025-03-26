import numpy as np
from calculate_need_matrix import calculate_need_matrix
from safety_algorithm import safety_algorithm
from resource_request_algorithm import resource_request_algorithm

# Main Function of the Banker's Algorithm
def bankers_algorithm(processes, allocation, max_need, available):
    # calculate the need matrix
    need = calculate_need_matrix(allocation, max_need)
    return safety_algorithm(processes, allocation, need, available)


# Data Set given from assignment to test functionality
processes = np.array(["P0", "P1", "P2", "P3", "P4"])
allocation = np.array([[0, 1, 0], [2, 0, 0], [3, 0, 2], [2, 1, 1], [0, 0, 2]])
max_need = np.array([[7, 5, 3], [3, 2, 2], [9, 0, 2], [2, 2, 2], [4, 3, 3]])
available = np.array([3, 3, 2])

# Demonstrating functionality of Banker's Algorithm
is_safe, safe_sequence = bankers_algorithm(processes, allocation, max_need, available)
if is_safe:
    print(f"The system completed all processes and remained in a Safe State. The Safe Sequence of processes was: {safe_sequence}")
else:
    print(f"The system is not in a Safe State. All processes could not be completed.")
