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

    def print_schedule(self):
        print((self.fname + " " + self.lname).upper())
        for number, job in enumerate(self.today_jobs):
            print("-" * 68)
            print("|", number + 1, "|", job, "|")
            print("-" * 68)


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
        not_null = [time_needed, time_existed, priority]
        for must_have in not_null:
            if isinstance(must_have, str):
                raise TypeError("time needed and time existed must be numeric values")
            if must_have is None or must_have < 0:
                raise ValueError("time needed and time existed must be positive values")

        Job.jobs_number += 1

    def __repr__(self):
        return f"JOB#:{self.job_number}, unit:{self.unit}, time_existed:{self.time_existed}," \
               f" time_needed: {self.time_needed}, plevel:{self.priority}"


class MaxHeap:
    heaps_list = []

    def __init__(self, priority_level: int):
        if isinstance(priority_level, str):
            raise TypeError("priority level must be numeric value")
        if priority_level < 0 or priority_level is None:
            raise ValueError("Priority level must be a positive value")
        for heap in self.heaps_list:
            if priority_level == heap.priority_level:
                raise ValueError(": Priority Level already exists")
        self.heap = self.build_heap([])
        self.no_match_jobs = []
        self.priority_level = priority_level
        self.heaps_list.append(self)
        self.heaps_list.sort(key=lambda x: x.priority_level)

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


def get_job_no(job_id_number):
    """
    gets a job via job number
    :param job_id_number:
    :return:
    """
    for heap in MaxHeap.heaps_list:
        for job in heap.heap:
            if job.job_number == job_id_number:
                return job


def get_emp_no(employee_number):
    """
    gets an employee via emp number
    :param employee_number:
    :return:
    """
    for emp in Employee.all_emps:
        if emp.number == employee_number:
            return emp


def remove_emp_no(employee_number):
    """
    removes an employee using emp.number
    :param employee_number: number matched against emp.number
    :return:
    """
    emp_to_remove = get_emp_no(employee_number)
    Employee.all_emps.remove(emp_to_remove)


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


def emp_gen(lst, n=0):
    """
    a generator allowing one to loop through a list and remember where to start next time
    :param lst:
    :param n:
    :return:
    """
    yield n % len(lst)
    yield from emp_gen(lst, n + 1)


def reset_day():
    """
    resets scheduling defaults
    :return:
    """
    Employee.today_emps = []
    Employee.off_emps = []
    for emp in Employee.all_emps:
        emp.today_hours = 0
        emp.today_jobs = []
        emp.booked = False
    for heap in MaxHeap.heaps_list:
        heap.no_match_jobs = []


# todo generate 'static' jobs, emps, and heaps to create a test for this\
# todo create a case where emps never reach max to ensure jobs are left behind as needed
# todo create a case where all emps are booked quickly and func terminates

def schedule(off_employees: list, threshold: int):
    """
    assign emps high priority jobs evenly until schedules are full or no jobs remain
    prints an alert if any jobs within threshold priority level are not assigned
    :param off_employees: list of employees who are not to be scheduled
    :param threshold: priority level threshold. if all in range not assigned creates an alert
    :return:
    """
    # reset the day
    reset_day()
    # update "today_employees" by removing emps specified to be off
    for emp in off_employees:
        Employee.off_emps.append(emp)
    for emp in Employee.all_emps:
        if emp not in Employee.off_emps:
            Employee.today_emps.append(emp)

    # create a generator to "remember" the last employee checked
    gen = emp_gen(Employee.today_emps)

    # init a variable determining if all employees are booked
    all_booked = False

    # traverse each queue in heaps_list
    for heap in MaxHeap.heaps_list:

        # while the heap has jobs and not all emps are "booked"
        while heap.heap and not all_booked:

            # pop a new job and temporarily set all_booked to true
            if heap.heap:
                next_job = heap.pop_max()
            else:
                break

            # set all booked to true this is later turned off if any employee isn't booked
            all_booked = True
            # set the current job to being incompatible with an employees schedule
            job_no_match = True

            # iterate through the number of emps in today's list
            # ensures every emp is checked for a given job
            for i in range(len(Employee.today_emps)):
                # the employee is remembered via generator
                emp = Employee.today_emps[next(gen)]
                job_no_match = True

                # if the emp is booked move to next emp
                if emp.booked:
                    continue

                # if the emp reaches max hours mark as booked
                if emp.today_hours == emp.max_hours:
                    emp.booked = True
                    continue

                # if the job doesnt put them over 8hrs
                if next_job.time_needed + emp.today_hours <= 8:
                    # update hours and add the job
                    emp.today_hours += next_job.time_needed
                    emp.today_jobs.append(next_job)
                    # job picked. is match.
                    job_no_match = False
                    # check to see if any jobs left
                    # also check to see if this is last emp if it is we dont want to pop a
                    # new job, end the loop and then pop a new one under the while loop.
                    # we would lose the job popped in the middle
                    if heap.heap and i < len(Employee.today_emps):
                        # if so pop a new job and go back up to get a new emp
                        next_job = heap.pop_max()
                        continue
                    # if the heap is done
                    else:
                        break

            # if after checking all emps a job is not compatible add it to a nomatch list
            if job_no_match:
                heap.no_match_jobs.append(next_job)

            # go through emps if any are free reset allbooked to false
            # and break out of the check(only need one)
            for emp in Employee.today_emps:
                if not emp.booked:
                    all_booked = False
                    break
            # if the check above doesnt find any free emps all booked will remain true from above
            # and the next while loop will not initiate

    # at the end of a heap all no match jobs are put back in
    for heap in MaxHeap.heaps_list:
        for job in heap.no_match_jobs:
            heap.insert(job)

    # checks heaps in list through thresh hold and prints an alert about status of jobs left in heap
    for i in range(threshold):
        if MaxHeap.heaps_list[i].heap:
            print(f"{len(MaxHeap.heaps_list[i].heap)} jobs left in priority level {MaxHeap.heaps_list[i].priority_level}:", MaxHeap.heaps_list[i].heap)
        else:
            print(f"All jobs in Priority level {i + 1} assigned")


if __name__ == '__main__':
    pass
