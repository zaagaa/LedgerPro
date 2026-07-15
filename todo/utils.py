from datetime import timedelta
from dateutil.relativedelta import relativedelta
from .models import Task

def create_next_repeating_task(task):
    if task.task_repeat == 0:  # One Time
        return

    next_date = task.task_date
    if task.task_repeat == 1:  # Every Day
        next_date += timedelta(days=1)
    elif task.task_repeat == 2:  # Every Week
        next_date += timedelta(weeks=1)
    elif task.task_repeat == 3:  # Every Month
        next_date += relativedelta(months=1)
    elif task.task_repeat == 4:  # Every Year
        next_date += relativedelta(years=1)

    Task.objects.create(
        task_name=task.task_name,
        description=task.description,
        task_date=next_date,
        deadline=task.deadline,
        task_type=task.task_type,
        task_repeat=task.task_repeat,
        user=task.user,
    )