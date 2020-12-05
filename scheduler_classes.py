# TODO create a sorting function that will sort the priority queues in "heaps_list"
# Todo test: normal behavior of que, test schedule is generated and never infinite loops


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

    def __init__(self, unit, time_existed, time_needed, priority):
        self.unit = unit
        self.time_existed = time_existed
        self.time_needed = time_needed
        self.priority = priority
        self.job_number = self.jobs_number
        self.emps_checked = []
        self.has_priority_level = False
        for heap in MaxHeap.heaps_list:
            if priority == heap.priority_level:
                self.has_priority_level = True
                heap.insert(self)
        if not self.has_priority_level:
            raise ValueError("priority level does not exist")

        Job.jobs_number += 1

    def __repr__(self):
        return f"job#:{self.job_number}, unit:{self.unit}, time_existed:{self.time_existed},\\" \
               f" time_needed: {self.time_needed}, plevel:{self.priority}"


class MaxHeap:
    heaps_list = []

    def __init__(self, priority_level):
        for heap in self.heaps_list:
            if priority_level == heap.priority_level:
                raise ValueError(": Priority Level already exists")
        self.heap = self.build_heap([])
        self.no_match_jobs = []
        self.priority_level = priority_level
        self.heaps_list.append(self)

    def __str__(self):
        return f"plevel: {self.priority_level}"

    def __repr__(self):
        return f"heap 0bj plevel: {self.priority_level}"

    def build_heap(self, array):
        f_parent = (len(array) - 2) // 2
        for cur_idx in reversed(range(f_parent + 1)):
            self.sift_down(cur_idx, len(array) - 1, array)
        return array

    def sift_down(self, cur_idx, end_idx, heap):
        fchild_idx = cur_idx * 2 + 1
        while fchild_idx <= end_idx:
            schild_idx = cur_idx * 2 + 2 if cur_idx * 2 + 2 <= end_idx else -1
            if schild_idx != -1 and heap[schild_idx].time_existed >= heap[fchild_idx].time_existed:
                swap_idx = schild_idx
            else:
                swap_idx = fchild_idx
            if heap[swap_idx].time_existed >= heap[cur_idx].time_existed:
                self.swap(cur_idx, swap_idx, heap)
                cur_idx = swap_idx
                fchild_idx = cur_idx * 2 + 1
            else:
                return

    def sift_up(self, cur_idx, heap):
        parent_idx = (cur_idx - 1) // 2
        while cur_idx > 0 and heap[cur_idx].time_existed >= heap[parent_idx].time_existed:
            self.swap(cur_idx, parent_idx, heap)
            cur_idx = parent_idx
            parent_idx = (cur_idx - 1) // 2

    def peek(self):
        return self.heap[0]

    def pop_max(self):
        self.swap(0, len(self.heap) - 1, self.heap)
        remove_val = self.heap.pop()
        self.sift_down(0, len(self.heap) - 1, self.heap)
        return remove_val

    def insert(self, job):
        self.heap.append(job)
        self.sift_up(len(self.heap) - 1, self.heap)

    def swap(self, i, j, heap):
        heap[i], heap[j] = heap[j], heap[i]


def remove_emp_no(employee_number):
    """
    removes an employee using emp.number
    :param employee_number: number matched against emp.number
    :return:
    """
    for emp in Employee.all_emps:
        if emp.number == employee_number:
            Employee.all_emps.remove(emp)


def remove_job_no(job_id_number):
    """
    deletes a job via its job number and reconstructs the heap
    :param job_id_number: job number to match job.job_number
    :return:
    """
    for heap in MaxHeap.heaps_list:
        for job in heap.heap:
            if job.job_number == job_id_number:
                heap.heap.remove(job)
                heap.heap = heap.build_heap(heap.heap)


# todo test this steaming pile of bugs waiting to happen
def schedule(off_employees: list):
    """
    loop through employees and assign most prioritized job until all queues are empty or employees are empty. remove
    employee when scheduled time exceeds 7
    """
    # update "today_employees" by removing emps specified to be off

    for emp in off_employees:
        Employee.off_emps.append(emp)

    for emp in Employee.all_emps:
        if emp not in Employee.off_emps:
            Employee.today_emps.append(emp)

    all_booked = False
    for heap in MaxHeap.heaps_list:
        while len(heap) and not all_booked:

            next_job = heap.pop_max()
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

                if next_job.time_needed + emp.today_hours < 8:
                    emp.today_hours += next_job.time_needed
                    emp.today_jobs.append(next_job)
                    break

            heap.no_match_jobs.append(next_job)
        for job in heap.no_match_jobs:
            heap.insert(job)


if __name__ == '__main__':
    pass
