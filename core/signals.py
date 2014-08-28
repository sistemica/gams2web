from blinker import signal

# Task
task_added = signal('task_added')
# TODO: task_failure = signal('task_failure')
# TODO: task_success = signal('task_success')
task_complete = signal('task_complete')

# Worker
worker_init = signal('worker_init')
worker_before_execution = signal('worker_before_execution')
worker_after_execution = signal('worker_after_execution')
