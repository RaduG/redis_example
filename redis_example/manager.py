import json
from time import time

from . import logger, r
from .constants import ASSIGNMENT_QUEUE, WORK_QUEUE, RESULT_QUEUE, MAX_TIME


work_items = {1: 10, 2: 20, 3: 30, 4: 40, 5: 50}

assigned_items = {}
completed_items = {}


def make_item(item_id, value):
    return json.dumps({"id": item_id, "value": value})


def set_up():
    logger.info("Adding work items to worker queue...")
    for k, v in work_items.items():
        item = make_item(k, v)
        r.rpush(WORK_QUEUE, item)
        logger.info(f"Added {item}")
    logger.info("All items are now in the worker queue!")


def loop():
    # All items have been assigned and we've got results for all work items
    while r.llen(WORK_QUEUE) > 0 or set(work_items.keys()) != set(
        completed_items.keys()
    ):
        logger.info("Checking assigned items")
        for aid in list(assigned_items.keys()):
            # If one assignment is completed, we remove it from the assignment dict
            if aid in completed_items:
                assigned_items.pop(aid)
                continue

            # Took too long to finish?
            if time() - assigned_items[aid]["time"] > MAX_TIME:
                # Remove the assignment
                assigned_items.pop(aid)
                r.rpush(WORK_QUEUE, make_item(aid, work_items[aid]))

        # Get any new results
        logger.info("Checking new results")
        pipe = r.pipeline()
        pipe.lrange(RESULT_QUEUE, 0, -1)
        pipe.delete(RESULT_QUEUE)
        results, _ = pipe.execute()

        for result in results:
            result = json.loads(result.decode("utf-8"))
            completed_items[result["item_id"]] = result

        # Get any new assigned items
        # We need to execute a lrange and a delete as an atomic operation to get all the assignment
        # data from the queue at once, as there's no `popall`
        logger.info("Checking assignments...")
        pipe = r.pipeline()
        pipe.lrange(ASSIGNMENT_QUEUE, 0, -1)
        pipe.delete(ASSIGNMENT_QUEUE)
        assignments, _ = pipe.execute()

        for assignment in assignments:
            assignment = json.loads(assignment.decode("utf-8"))
            assigned_items[assignment["item_id"]] = assignment


if __name__ == "__main__":
    set_up()
    loop()
    logger.info("Completed all items!")
    logger.info(completed_items)
