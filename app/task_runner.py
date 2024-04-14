"""Module responsible for handling the threads."""

from queue import Queue, Empty
from threading import Thread, Event
import time
import os
import multiprocessing

class ThreadPool:
    """Class representing the Thread Pool."""

    def __init__(self, data_ingestor):
        self.task_queue = Queue()
        self.thread_list = []
        self.data_ingestor = data_ingestor
        self.accept_tasks = Event()
        self.accept_tasks.set()

        if 'TP_NUM_OF_THREADS' in os.environ:
            self.nr_threads = os.environ['TP_NUM_OF_THREADS']
        else:
            self.nr_threads = multiprocessing.cpu_count()

        for i in range(self.nr_threads):
            t = TaskRunner(self.task_queue, i, self.data_ingestor, self.accept_tasks)
            t.start()
            self.thread_list.append(t)

    def add_task(self, task):
        """Function responsible for adding tasks to the queue."""
        if self.accept_tasks:
            self.task_queue.put(task)

    def stop(self):
        """Function responsible for signaling that no more tasks shall be accepted."""
        self.accept_tasks.clear()
        for t in self.thread_list:
            t.join()

class TaskRunner(Thread):
    """Class representing a worker"""

    def __init__(self, task_queue, index, data_ingestor, accept_tasks):
        super().__init__()
        self.index = index
        self.task_queue = task_queue
        self.data_ingestor = data_ingestor
        self.accept_tasks = accept_tasks


    def run(self):
        while self.accept_tasks:
            try:
                task = self.task_queue.get(timeout = 1)
                job_id = task[0]
                request_type = task[1]
                question = task[2]['question']

                match request_type:
                    case "states_mean":
                        self.data_ingestor.states_mean(job_id, question)

                    case "state_mean":
                        state_name = task[2]['state']
                        self.data_ingestor.state_mean(job_id, question, state_name)

                    case "best5":
                        self.data_ingestor.best_five(job_id, question)

                    case "worst5":
                        self.data_ingestor.worst_five(job_id, question)

                    case "global_mean":
                        self.data_ingestor.global_mean(job_id, question)

                    case "state_diff_from_mean":
                        state_name = task[2]['state']
                        self.data_ingestor.state_diff_from_mean(job_id, question, state_name)

                    case "diff_from_mean":
                        self.data_ingestor.diff_from_mean(job_id, question)

                    case "state_mean_by_category":
                        state_name = task[2]['state']
                        self.data_ingestor.state_mean_by_category(job_id, question, state_name)

                    case "mean_by_category":
                        self.data_ingestor.mean_by_category(job_id, question)

                    case _:
                        break
            except Empty:
                if not self.accept_tasks.is_set():
                    break
                time.sleep(1)
