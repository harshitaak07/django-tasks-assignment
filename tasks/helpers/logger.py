import logging

logger = logging.getLogger('django')

class TaskLogger:
    @staticmethod
    def log_task_deletion(task_instance):
        logger.info(f"Deleting Task: {task_instance.title} (ID: {task_instance.id})")

    @staticmethod
    def log_task_update(task_instance):
        logger.info(f"Partial update for Task: {task_instance.title} (ID: {task_instance.id})")
    
    @staticmethod
    def log_task_search(search_title):
        logger.info(f"Searching tasks by title: {search_title} with similarity filter")

    @staticmethod
    def log_sorting(sort_by_date):
        if sort_by_date == 'true':
            logger.info(f"Sorting tasks by created_at in descending order")
        elif sort_by_date == 'false':
            logger.info(f"Sorting tasks by created_at in ascending order")