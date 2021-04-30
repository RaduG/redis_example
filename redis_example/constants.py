# new work items are added here for processing
WORK_QUEUE = "work"

# once a worker picks up an item, it confirms the assignment in this queue with a timestamp
ASSIGNMENT_QUEUE = "assignment"

# once a work item is ready, the results are added here
RESULT_QUEUE = "result"

# the maximum time (in seconds) we allow a worker to process an item before we add it back to
# the queue - in reality we might keep a count of retries and increase the allocated time per run
# or even tell the worker how much time they got
MAX_TIME = 5
