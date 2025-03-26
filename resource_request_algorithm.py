import numpy as np
from bankers_algorithm import calculate_need_matrix
from bankers_algorithm import safety_algorithm

# A function that can dynamically check processes requesting resources and allocation available resources if safe
def resource_request_algorithm(processes, allocation, max_need, available, process_idx, resource_request):
    # calculate the need matrix
    need = calculate_need_matrix(allocation, max_need)

    # Step 1: check if requested resources exceeds the max resources needed for that process
    if np.any(resource_request > need[process_idx]):
        return False # resource request exceeds max need for the process

    # Step 2: Check if there are resources available to complete the resource request
    if np.any(resource_request > available):
        return False # resource request exceeds available resources

    # Step 3: Resources are available and the resource request can be allocated
    temp_allocation = allocation.copy()
    temp_available = available.copy()

    # allocation resources to the requesting process
    temp_allocation[process_idx] += resource_request
    temp_available -= resource_request

    # recalculate the need matrix
    temp_need = calculate_need_matrix(temp_allocation, max_need)

    # Step 4: Check if the system is in a safe state after allocation
    is_safe, sequence = safety_algorithm(processes, temp_allocation, temp_need, temp_available)

    return is_safe
