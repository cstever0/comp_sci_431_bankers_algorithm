import numpy as np

# Function to calculate the need matrix
def calculate_need_matrix(allocate, max_need):
    return max_need - allocate


# Function to check if the system is in a safe state or not - Safety Algorithm
def safety_algorithm(processes, allocate, need, available):
    work = available.copy()
    complete = np.full(len(processes), False, dtype=bool)
    safe_sequence = []

    # Loop through processes until all processes have been flagged as complete
    while not np.all(complete):
        found = False # flag that tells if a process that can be completed is found

        # Check if processes can be allocated resources
        for i in range(len(processes)):
            # Check if process is complete and the resources needed is less than the resources available
            if not complete[i] and np.all(need[i] <= work):
                work += allocate[i] # release resources previously allocated to the process
                complete[i] = True # flag the process as complete
                safe_sequence.append(processes[i]) # add the process to the safe_sequence of processes
                found = True # set found flag to true
                break

        # Process that can be completed was not found and system is not in a safe state
        if not found:
            return False, []

    # a sequence of processes was found that could complete all processes with the available resources
    return True, safe_sequence


# Main Function of the Banker's Algorithm
def bankers_algorithm(processes, allocate, max_need, available):
    # calculate the need matrix
    need = calculate_need_matrix(allocate, max_need)
    return safety_algorithm(processes, allocate, need, available)


# A function that can dynamically check processes requesting resources and allocate available resources if safe
def resource_request_algorithm(processes, allocate, max_need, available, process_index, resource_request):
    # calculate the need matrix
    need = calculate_need_matrix(allocate, max_need)

    # Step 1: check if requested resources exceeds the max resources needed for that process
    if np.any(resource_request > need[process_index]):
        return False # resource request exceeds max need for the process

    # Step 2: Check if there are resources available to complete the resource request
    if np.any(resource_request > available):
        return False # resource request exceeds available resources

    # Step 3: Resources are available and the resource request can be allocated
    temp_allocate = allocate.copy()
    temp_available = available.copy()

    # allocate resources to the requesting process
    temp_allocate[process_index] += resource_request
    temp_available -= resource_request

    # recalculate the need matrix
    temp_need = calculate_need_matrix(temp_allocate, max_need)

    # Step 4: Check if the system is in a safe state after allocation
    is_safe, sequence = safety_algorithm(processes, temp_allocate, temp_need, temp_available)

    return is_safe


# Data Set given from assignment to test functionality
processes = np.array(["P0", "P1", "P2", "P3", "P4"])
allocate = np.array([[0, 1, 0], [2, 0, 0], [3, 0, 2], [2, 1, 1], [0, 0, 2]])
max_need = np.array([[7, 5, 3], [3, 2, 2], [9, 0, 2], [2, 2, 2], [4, 3, 3]])
available = np.array([3, 3, 2])

# Demonstrating functionality of Banker's Algorithm
is_safe, safe_sequence = bankers_algorithm(processes, allocate, max_need, available)
if is_safe:
    print(f"The system completed all processes and remained in a Safe State. The Safe Sequence of processes was: {safe_sequence}")
else:
    print(f"The system is not in a Safe State. All processes could not be completed.")
