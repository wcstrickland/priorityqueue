class Employee:
    all_emps = []
    today_emps = []
    off_emps = []

    def __init__(self, f_name, l_name, max_hours=8):
        self.f_name = f_name
        self.l_name = l_name
        self.max_hours = max_hours
        self.today_hours = 0
        self.today_jobs = []
        Employee.all_emps.append(self)


class JobsUrgency:
    urgencies = {}


class Job:

    def __init__(self, number, urgency, estimated_hours, hours_existed, unit, _priority_levels, _urgency_levels):
        if urgency in priority_levels.priority_queues_names:
            self.number = number
            self.urgency = urgency
            self.estimated_hours = estimated_hours
            self.hours_existed = hours_existed
            self.unit = unit
            _priority_levels.priority_queues[_urgency_levels.urgencies[urgency]].insert(self)
        else:
            print("Error: Invalid urgency level")


class PriorityLevels:
    priority_queues_names = []
    priority_queues = []


class PriorityLevel:

    def __init__(self, name, _priority_levels, _urgency_levels):
        self.heap = []
        self.name = name
        _priority_levels.priority_queues_names.append(self.name)
        _priority_levels.priority_queues_names.sort()
        _priority_levels.priority_queues.append(self)
        _urgency_levels.urgencies[name] = len(_priority_levels.priority_queues_names) - 1

    # def build_heap(self, array):
    #     f_parent = (len(array) - 2) // 2
    #     for cur_idx in reversed(range(f_parent + 1)):
    #         self.sift_down(cur_idx, len(array) - 1, array)
    #     return array

    def sift_down(self, cur_idx, end_idx, heap):
        fchild_idx = cur_idx * 2 + 1
        while fchild_idx <= end_idx:
            schild_idx = cur_idx * 2 + 2 if cur_idx * 2 + 2 <= end_idx else -1
            if schild_idx != -1 and heap[schild_idx] < heap[fchild_idx]:
                swap_idx = schild_idx
            else:
                swap_idx = fchild_idx
            if heap[swap_idx] < heap[cur_idx]:
                self.swap(cur_idx, swap_idx, heap)
                cur_idx = swap_idx
                fchild_idx = cur_idx * 2 + 1
            else:
                return

    def sift_up(self, cur_idx, heap):
        parent_idx = (cur_idx - 1) // 2
        while cur_idx > 0 and heap[cur_idx] < heap[parent_idx]:
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
        idx = job.hours_existed
        
        self.heap.append()
        self.sift_up(len(self.heap) - 1, self.heap)

    def swap(self, i, j, heap):
        heap[i], heap[j] = heap[j], heap[i]


urgency_levels = JobsUrgency
priority_levels = PriorityLevels

a = PriorityLevel("a", priority_levels, urgency_levels)
b = PriorityLevel("b", priority_levels, urgency_levels)
c = PriorityLevel("c", priority_levels, urgency_levels)
d = PriorityLevel("d", priority_levels, urgency_levels)

print(priority_levels.priority_queues_names)
print(priority_levels.priority_queues)

a123 = Job("123", "a", 3, "c1", priority_levels, urgency_levels)

print(a.peek())
