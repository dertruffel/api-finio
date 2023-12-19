from celery import current_app


class CeleryHelper:
    @staticmethod
    def is_being_executed(task_name: str) -> bool:

        active_tasks = current_app.control.inspect().active()
        print(active_tasks)
        for worker, running_tasks in active_tasks.items():
            for task in running_tasks:
                if task["name"] == task_name:
                    return True

        return False