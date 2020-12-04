import random


class Employee:
    emp_number = 0
    all_emps = []
    today_emps = []
    off_emps = []

    def __init__(self, fname, lname, max_hours=8, today_hours=0):
        self.number = self.emp_number
        self.fname = fname
        self.lname = lname
        self.max_hours = max_hours
        self.today_hours = today_hours
        self.today_jobs = []
        self.booked = False
        self.all_emps.append(self)
        Employee.emp_number += 1

    def __repr__(self):
        return f"{self.number}: {self.fname}{self.lname} scheduled:{self.today_hours}, max:{self.max_hours}"


class Job:
    jobs_number = 0

    def __init__(self, unit, time, priority):
        self.unit = unit
        self.time = time
        self.priority = priority
        self.job_number = self.jobs_number
        for heap in MaxHeap.heaps_list:
            if priority == heap.priority_level:
                heap.insert(self)
        Job.jobs_number += 1

    def __repr__(self):
        return f"job#:{self.job_number}, unit:{self.unit}, time:{self.time}, plevel:{self.priority}"


class MaxHeap:
    heaps_list = []

    def __init__(self, priority_level):
        for heap in self.heaps_list:
            if priority_level == heap.priority_level:
                print("Error: Priority Level already exists")
                return
        self.heap = []
        self.priority_level = priority_level
        self.heaps_list.append(self)

    def __str__(self):
        return f"plevel: {self.priority_level}"

    def __repr__(self):
        return f"heap 0bj plevel: {self.priority_level}"

    def siftDown(self, cur_idx, end_idx, heap):
        fchild_idx = cur_idx * 2 + 1
        while fchild_idx <= end_idx:
            schild_idx = cur_idx * 2 + 2 if cur_idx * 2 + 2 <= end_idx else -1
            if schild_idx != -1 and heap[schild_idx].time > heap[fchild_idx].time:
                swap_idx = schild_idx
            else:
                swap_idx = fchild_idx
            if heap[swap_idx].time > heap[cur_idx].time:
                self.swap(cur_idx, swap_idx, heap)
                cur_idx = swap_idx
                fchild_idx = cur_idx * 2 + 1
            else:
                return

    def siftUp(self, cur_idx, heap):
        parent_idx = (cur_idx - 1) // 2
        while cur_idx > 0 and heap[cur_idx].time > heap[parent_idx].time:
            self.swap(cur_idx, parent_idx, heap)
            cur_idx = parent_idx
            parent_idx = (cur_idx - 1) // 2

    def peek(self):
        return self.heap[0]

    def remove(self):
        self.swap(0, len(self.heap) - 1, self.heap)
        remove_val = self.heap.pop()
        self.siftDown(0, len(self.heap) - 1, self.heap)
        return remove_val

    def insert(self, job):
        self.heap.append(job)
        self.siftUp(len(self.heap) - 1, self.heap)

    def swap(self, i, j, heap):
        heap[i], heap[j] = heap[j], heap[i]


def schedule(off_employees: list):
    """
    loop through employees and assign most prioritized job until all queues are empty or employees are empty. remove employee when scheduled time exceeds 7
    """
    # update "today_employees" by removing emps specified to be off

    for emp in off_employees:
        Employee.off_emps.append(emp)

    for emp in Employee.all_emps:
        if emp not in Employee.off_emps:
            Employee.today_emps.append(emp)

    all_booked = False
    for heap in MaxHeap.heaps_list:
        counter = 0
        while len(heap) and not all_booked:

            next_job = heap.remove()
            all_booked = True

            for emp in Employee.today_emps:
                if emp.booked:
                    continue

                if emp.today_hours > 7:
                    emp.booked = True
                    continue

                for emp in Employee.today_emps:
                    if not emp.booked:
                        all_booked = False

                if next_job.time + emp.today_hours < 8:
                    emp.today_hours += next_job.time
                    emp.today_jobs.append(next_job)
                    break

                if next_job + emp.today_hours > 8:
                    counter += 1

                if counter == 1000:
                    break
