from concurrent.futures import ProcessPoolExecutor


def run_tasks_in_parallel(tasks):
    with ProcessPoolExecutor() as executor:
        running_tasks = [executor.submit(task) for task in tasks]
        for running_task in running_tasks:
            running_task.result()
