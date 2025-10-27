# Parallel-and-Distributed-Computing
*Submitted to:* Sir Akhzar Nazir
*Submitted by:* Aimen Umar
*Registration No:* SP23-BAI-008
*Section:* A

# Performance Report: Sequential vs Parallel vs Distributed

| **Method**    | **Configuration** | **Execution Time (s)** |
|----------------|------------------|------------------------|
| Sequential     | 1                | 0.71                   |
| Parallel       | 1                | 0.63                   |
| Parallel       | 2                | 0.37                   |
| Parallel       | 4                | 0.29                   |
| Parallel       | 8                | 0.31                   |
| Distributed    | 2 nodes          | 0.82                   |

---

## Best Number of Workers
The best performance was observed with **4 workers**, achieving a time of **0.29 seconds**.  
This configuration likely balanced CPU utilization and thread management overhead.  
Increasing beyond 4 workers did not improve performance due to the **Global Interpreter Lock (GIL)** and the **limited number of available CPU cores**.

---

## Discussion
Parallelism significantly improved performance compared to sequential execution by allowing multiple images to be processed concurrently.  

However, some bottlenecks remain, including:
- Python’s **GIL** limitation  
- **Thread creation** and management overhead  
- **Data transfer time** between processes  

The **distributed approach** introduced additional synchronization and communication overhead, which made it slower than the sequential version for this relatively small dataset.  

For **larger datasets** or **heavier workloads**, distributed processing could yield greater benefits and improved scalability.



