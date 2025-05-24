from celery import shared_task
from datetime import datetime
import time
import logging

logger = logging.getLogger(__name__)

@shared_task(name='restapi.simple_task')
def simple_task():
    """
    A simple task that just logs a message
    """
    logger.info(f"Simple task executed at {datetime.now()}")
    return "Simple task completed"

@shared_task(name='restapi.long_running_task')
def long_running_task(seconds: int = 10):
    """
    A task that simulates a long-running operation
    """
    logger.info(f"Starting long running task at {datetime.now()}")
    time.sleep(seconds)
    logger.info(f"Long running task completed at {datetime.now()}")
    return f"Task completed after {seconds} seconds"

@shared_task(name='restapi.error_task')
def error_task():
    """
    A task that raises an exception to demonstrate error handling
    """
    logger.info("Starting error task")
    raise Exception("This is a sample error")

@shared_task(name='restapi.periodic_task')
def periodic_task():
    """
    A task that can be scheduled to run periodically
    """
    current_time = datetime.now()
    logger.info(f"Periodic task executed at {current_time}")
    return f"Periodic task completed at {current_time}"

@shared_task(name='restapi.chain_task')
def chain_task(value: int):
    """
    A task that can be used in a chain of tasks
    """
    logger.info(f"Chain task received value: {value}")
    return value * 2 