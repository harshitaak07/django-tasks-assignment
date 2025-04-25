import logging

# Setting up a logger for Django
logger = logging.getLogger('django')

class TaskLogger:
    """
    A logger class to log task-related activities, such as deletion, updates,
    searches, and sorting actions.

    This class is used to log information on various task operations.

    Methods:
    - log_task_deletion: Logs information about task deletions.
    - log_task_update: Logs information about partial updates on tasks.
    - log_task_search: Logs task search queries by title.
    - log_sorting: Logs task sorting preferences based on creation date.
    """
    
    @staticmethod
    def log_task_deletion(task_instance):
        """
        Logs the task deletion event, including the task title and ID.

        Args:
        task_instance (Task): The task object being deleted.
        """
        logger.info(f"Deleting Task: {task_instance.title} (ID: {task_instance.id})")

    @staticmethod
    def log_task_update(task_instance):
        """
        Logs the event of a partial update on a task, including the task title and ID.

        Args:
        task_instance (Task): The task object being updated.
        """
        logger.info(f"Partial update for Task: {task_instance.title} (ID: {task_instance.id})")
    
    @staticmethod
    def log_task_search(search_title):
        """
        Logs the search for tasks based on a title, including the search term used.

        Args:
        search_title (str): The title used for searching tasks.
        """
        logger.info(f"Searching tasks by title: {search_title} with similarity filter")

    @staticmethod
    def log_sorting(sort_by_date):
        """
        Logs the sorting action on tasks based on their creation date.

        Args:
        sort_by_date (str): A string representing whether the tasks should be sorted
                             in ascending ('false') or descending ('true') order.
        """
        if sort_by_date == 'true':
            logger.info(f"Sorting tasks by created_at in descending order")
        elif sort_by_date == 'false':
            logger.info(f"Sorting tasks by created_at in ascending order")
