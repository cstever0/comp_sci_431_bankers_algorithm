import numpy as np

# Function to calculate the need matrix
def calculate_need_matrix(allocation, max_need):
    return max_need - allocation


# Function to check if the system is in a safe state or not - Safety Algorithm
def safety_algorithm(processes, allocation, need, available):
    resources = available.copy()
    complete = np.full(len(processes), False, dtype=bool)
    safe_sequence = []

    print(f"Available resources before beginning process execution: {resources} \n")
    print("------------ Attempting Process Execution ------------------ \n")

    # Loop through processes until all processes have been flagged as complete
    while not np.all(complete):
        found = False # flag that tells if a process that can be completed is found

        # Check if processes can be allocated resources
        for i in range(len(processes)):
            # Check if process is complete and the resources needed is less than the resources available
            if not complete[i] and np.all(need[i] <= resources):
                # Print statement to demonstrate resources available before process execution.
                print(f"Process {processes[i]} is executing. Resources available before allocation: {resources}")

                resources += allocation[i] # release resources previously allocated to the process
                complete[i] = True # flag the process as complete
                safe_sequence.append(str(processes[i])) # add the process to the safe_sequence of processes
                found = True # set found flag to true

                # Print statement to demonstrate resources available after process completion.
                print(f"Process {processes[i]} has completed execution. Updated resources available: {resources} \n")

        # Process that can be completed was not found and system is not in a safe state
        if not found:
            return False, []

    # a sequence of processes was found that could complete all processes with the available resources
    return True, safe_sequence


# Main Function of the Banker's Algorithm
def bankers_algorithm(processes, allocation, max_need, available):
    # calculate the need matrix
    need = calculate_need_matrix(allocation, max_need)
    return safety_algorithm(processes, allocation, need, available)


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
