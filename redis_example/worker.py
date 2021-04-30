import os
import json
from time import time, sleep
from random import randint

from . import logger, r
from .constants import ASSIGNMENT_QUEUE, WORK_QUEUE, RESULT_QUEUE, MAX_TIME


WORKER_ID = os.getenv("WORKER_ID")


class CustomError(Exception):
    pass


def process(value: int) -> int:
    """
    This may take more than MAX_TIME seconds, or it may error out. Everything is possible!

    Args:
        value:

    Returns:
        A number, but it is irrelevant

    Raises:
        CustomError: if it decides to
    """
    n = randint(0, 10)

    if n == 10:
        logger.info("Raising an error!")
        raise CustomError("oopsy")

    elif n in (8, 9):
        logger.info("We're gonna sleep for a bit...")
        sleep(MAX_TIME)

    return value ** 2


def loop():
    while True:
        # We can either use a while loop for polling redis as well or we can straight use blpop
        # timeout is number of seconds to wait; 0 means forever
        logger.info("Waiting for work item...")
        # This returns a tuple of key, value
        _, work_item = r.blpop(WORK_QUEUE, timeout=0)
        work_item = json.loads(work_item.decode("utf-8"))
        logger.info(f"Picked up work_item: {work_item}")

        # Let's record the fact that we picked up the item
        r.rpush(
            ASSIGNMENT_QUEUE,
            json.dumps(
                {"item_id": work_item["id"], "worker_id": WORKER_ID, "time": time()}
            ),
        )

        try:
            # Now we can process the item
            result = process(work_item["value"])
            logger.info(f"Result: {result}")

            # Let's record the result
            r.rpush(
                RESULT_QUEUE,
                json.dumps(
                    {
                        "item_id": work_item["id"],
                        "worker_id": WORKER_ID,
                        "time": time(),
                        "result": result,
                    }
                ),
            )
        except CustomError as e:
            logger.error("Oh, no!", e)


if __name__ == "__main__":
    loop()
