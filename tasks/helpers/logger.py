import logging

# Setting up a logger for Django
logger = logging.getLogger('django')

class TaskLogger:
   # A class for logging events related to tasks, such as creation, deletion, and updates.
    @staticmethod
    def log_task_deletion(task_instance):
        # Logs the event of a task being deleted, including the task title and ID.
        logger.info(f"Deleting Task: {task_instance.title} (ID: {task_instance.id})")

    @staticmethod
    def log_task_update(task_instance):
        # Logs the event of a task being updated, including the task title and ID.
        logger.info(f"Partial update for Task: {task_instance.title} (ID: {task_instance.id})")
    
    @staticmethod
    def log_task_search(search_title):
        # Logs the event of searching tasks by title, including the search term.
        logger.info(f"Searching tasks by title: {search_title} with similarity filter")

    @staticmethod
    def log_sorting(sort_by_date):
        # Logs the event of sorting tasks by creation date, including the sort order.
        if sort_by_date == 'true':
            logger.info(f"Sorting tasks by created_at in descending order")
        elif sort_by_date == 'false':
            logger.info(f"Sorting tasks by created_at in ascending order")
