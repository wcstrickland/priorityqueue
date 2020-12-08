# Priorityqueue
## Concept
The program allows the creation of Employees, Jobs, and Priority levels. Jobs have several properties including a priority level, a length of time the job has been listed, and an estimated time the job will take to complete. The program assigns “jobs” to employees always prioritizing the highest priority level job that has been listed the longest. This system ensures priority jobs are evenly distributed across employees for simultaneous completion to prevent bottlenecking. Employees are scheduled up until they reach their “max hours” for the day, which may vary if the employee is part-time or working a half-day. A thresh hold can be set to provide an alert if there are jobs left outstanding in a priority level after scheduling to determine resource management such as authorizing overtime or using temp employees. 

## Practical Highlights:
- Reusable
- Versatile: can be applied to any allocation of a prioritized workflow (maintenance work orders, call center hold queue, patient intake in a hospital)
- Efficient
- Streamlined: user input required only at the level of necessity such as creating a work order or determining employees who are not working on a given day. Jobs are automatically added to appropriate queues, and warnings are provided if inputs are malformed such as creating a job with a priority level that does not exist.

## Technical Highlights:
- Use of max heap to create priority queues based on the attribute of an object to optimize performance
- Use of a non-built-in sorting algorithm to sort a list of objects based on a property
- Use of modulo in a  generator in conjunction with a range-based for loop to “wrap” around to the beginning of a list and “remember” the last item the next time the for loop is accessed in code.

### Sample alert and individual schedule 
![alt text](priorityqueue/images/sample alert.png)
