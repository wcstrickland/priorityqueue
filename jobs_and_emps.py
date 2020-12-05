from scheduler_classes import Job, Employee, MaxHeap
import random

# list of first names for generating random employees
fnames = ["james", "trevor", "jim", "marsha", "benji", "barbara", "liz", "don",
          "patty", "eric", "sally", "jammie", "greg", "kristy", "minday", "palo"]

# list of last names for generating random employees
lnames = ["mustard", "kelly", "strickland", "smith", "lanister",
          "snow", "steele", "finley", "stevens", "argenta"]

# alphabet list  used for generating random variable names for each employee
alphabet = list("abcdefghijklmnopqrstuvwxyz")

# initial construction of priority queues

p1 = MaxHeap(1)
p2 = MaxHeap(2)
p3 = MaxHeap(3)
p4 = MaxHeap(4)
p5 = MaxHeap(5)

# generate 100 random jobs
for i in range(100):
    _ = Job((random.choice(alphabet) + str(random.randint(1, 200))),
            random.randint(1, 5), random.randint(1, 3), random.randint(1, 5))

# generate 50 random employees
for i in range(50):
    f_name = random.choice(fnames) + str(random.randint(0, 9))
    l_name = " " + random.choice(lnames) + str(random.randint(0, 9))
    _ = Employee(f_name, l_name)

if __name__ == '__main__':

    # prints all priority queues
    for heap in MaxHeap.heaps_list:
        print("*" * 90)
        print(heap, "\t", "jobs in heap:", len(heap.heap))
        print("*" * 90)
        print(heap.heap)
        print("*" * 90)

    # prints all employees
    for emp in Employee.all_emps:
        print(emp)
