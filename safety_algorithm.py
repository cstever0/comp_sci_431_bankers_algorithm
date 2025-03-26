import numpy as np
from resource_request_algorithm import resource_request_algorithm

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
