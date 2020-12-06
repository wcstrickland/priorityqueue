import unittest
from scheduler_classes import Employee, Job, MaxHeap, schedule, remove_emp_no, remove_job_no


class TestScheduler(unittest.TestCase):

    def setUp(self):
        self.emp_1 = Employee("john", "smith")
        self.emp_2 = Employee("carol", "kelly")
        self.h_1 = MaxHeap(1)
        self.h_2 = MaxHeap(2)
        self.h_4 = MaxHeap(4)
        # (self, unit, time_existed, time_needed, priority)
        self.j_1_1 = Job("c1", 2, 2, 1)
        self.j_1_2 = Job("c1", 4, 4, 1)
        self.j_1_3 = Job("c1", 3, 3, 1)
        self.j_2_1 = Job("c2", 4, 4, 2)
        self.j_2_2 = Job("c2", 5, 5, 2)

    def tearDown(self):
        """
        tests properties of instance upon init
        :return:
        """
        MaxHeap.heaps_list.clear()
        Employee.all_emps.clear()
        Employee.emp_number = 0
        Job.jobs_number = 0

    def test_Employee(self):
        """
        tests properties of instance upon init
        :return:
        """
        # tests auto increment of emp_numbers
        self.assertEqual(self.emp_1.number, 0)
        self.assertEqual(self.emp_2.number, 1)
        # tests addition to Employee.all_emps upon init
        self.assertEqual(Employee.all_emps, [self.emp_1, self.emp_2])

    def test_MaxHeap(self):
        """
        tests properties of instance upon init
        :return:
        """
        self.h_3 = MaxHeap(3)
        # tests that upon init a priority level is added to MaxHeap.heaps_list
        # and the list of heaps is sorted based on priority level
        self.assertEqual(MaxHeap.heaps_list, [self.h_1, self.h_2, self.h_3, self.h_4])
        # the heap is not sorted by time_needed
        # it follows heap property where children are idx*2 + 1 or 2
        # and parent >= children
        # these indexes reflect this property
        self.assertEqual(self.h_1.heap[0], self.j_1_2)
        self.assertEqual(self.h_1.heap[1], self.j_1_1)
        self.assertEqual(self.h_1.heap[2], self.j_1_3)
        # tests if attempt to create existing priority level raises err
        with self.assertRaises(ValueError):
            _ = MaxHeap(1)

    def test_Job(self):
        """
        tests properties of Job instance upon init
        :return:
        """
        # tests job number auto incrementation
        self.assertEqual(self.j_1_1.job_number, 0)
        self.assertEqual(self.j_2_2.job_number, 4)
        # tests adding job without existing priority level throws err
        with self.assertRaises(ValueError):
            # job_with_priority_not_existing
            _ = Job("c2", 5, 5, 7)

    def test_remove_emp_no(self):
        """
        test that emp is removed from Employee.all_emps
        :return:
        """
        remove_emp_no(0)
        # does emp retain emp_number?
        self.assertEqual(self.emp_2.number, 1)
        # does Employee.all_emps reflect removal of said emp
        self.assertEqual(Employee.all_emps, [self.emp_2])

    def test_remove_job_no(self):
        """
        tests if upon removing a job via linear search rather than "pop" off heap
        that the heap is reconstructed appropriately
        :return:
        """
        # todo add larger sample and more removes
        remove_job_no(2)
        self.assertEqual(self.h_1.heap[1], self.j_1_1)
        remove_job_no(1)
        self.assertEqual(self.h_1.heap[0], self.j_1_1)

    def test_schedule(self):
        pass


if __name__ == '__main__':
    unittest.main()
