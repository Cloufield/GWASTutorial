# Job Scheduling System

Job scheduling systems (also called workload managers or batch systems) are essential tools for running computational tasks on high-performance computing (HPC) clusters. They manage resource allocation, queue jobs, and ensure fair distribution of computing resources among users.

!!! note "When to use job schedulers"
    Job schedulers are typically used when:
    - Running long-running analyses that exceed a few minutes
    - Working on shared computing clusters
    - Requiring specific resources (CPU cores, memory, GPUs)
    - Running multiple jobs in parallel

## Common Job Scheduling Systems

Two of the most commonly used job scheduling systems:

- **[Slurm Workload Manager](https://slurm.schedmd.com/documentation.html)**: Widely used in academic and research computing environments
- **[Univa Grid Engine (UGE)](https://en.wikipedia.org/wiki/Univa_Grid_Engine)**: Also known as Sun Grid Engine (SGE), commonly used in various HPC environments

## Slurm Workload Manager

### Basic Commands

- `sbatch <script.sh>`: Submit a job script to the queue
- `squeue` or `sq`: View job queue status
- `scancel <job_id>`: Cancel a running or queued job
- `sinfo`: Display information about nodes and partitions
- `sacct`: View accounting information for jobs

!!! example "Check job status"
    ```bash
    # View all jobs in queue
    $ squeue
    
    # View your jobs only
    $ squeue -u $USER
    
    # View detailed information
    $ squeue -l
    ```

### Slurm Job Script Example

Create a job script (e.g., `my_job.sh`):

```bash
#!/bin/bash
#SBATCH --job-name=my_analysis
#SBATCH --output=output_%j.log
#SBATCH --error=error_%j.log
#SBATCH --time=01:00:00
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --cpus-per-task=4
#SBATCH --mem=8G

# Load required modules (if using module system)
# module load plink/2.0

# Your analysis commands
plink --bfile data --out results
```

Submit the job:

```bash
$ sbatch my_job.sh
```

### Common Slurm Directives

- `#SBATCH --job-name=<name>`: Set job name
- `#SBATCH --output=<file>`: Standard output file
- `#SBATCH --error=<file>`: Standard error file
- `#SBATCH --time=<time>`: Maximum wall-clock time (format: HH:MM:SS)
- `#SBATCH --nodes=<n>`: Number of nodes
- `#SBATCH --ntasks=<n>`: Number of tasks
- `#SBATCH --cpus-per-task=<n>`: CPUs per task
- `#SBATCH --mem=<size>`: Memory requirement (e.g., 8G, 16G)
- `#SBATCH --partition=<name>`: Specify partition/queue

## Univa Grid Engine (UGE)

### Basic Commands

- `qsub <script.sh>`: Submit a job script to the queue
- `qstat`: View job queue status
- `qdel <job_id>`: Cancel a running or queued job
- `qhost`: Display information about execution hosts

!!! example "Check job status"
    ```bash
    # View all jobs in queue
    $ qstat
    
    # View your jobs only
    $ qstat -u $USER
    
    # View detailed information
    $ qstat -f <job_id>
    ```

### UGE Job Script Example

Create a job script (e.g., `my_job.sh`):

```bash
#!/bin/bash
#$ -S /bin/bash
#$ -cwd
#$ -o output.log
#$ -e error.log
#$ -q default.q
#$ -l mem_req=8G,s_vmem=8G
#$ -pe def_slot 4

# Set environment variables
export PATH=~/tools/bin:$PATH
export OMP_NUM_THREADS=4

# Your analysis commands
plink --bfile data --out results
```

Submit the job:

```bash
$ qsub my_job.sh
```

### Common UGE Directives

- `#$ -S /bin/bash`: Specify shell
- `#$ -cwd`: Run job in current working directory
- `#$ -o <file>`: Standard output file
- `#$ -e <file>`: Standard error file
- `#$ -q <queue>`: Specify queue name
- `#$ -l <resource>`: Resource requirements (e.g., `mem_req=8G,s_vmem=8G`)
- `#$ -pe <parallel_env> <slots>`: Parallel environment and number of slots (cores)

!!! example "UGE script from tutorial"
    ```bash
    #!/bin/bash
    #$ -S /bin/bash
    #$ -cwd
    #$ -o temp
    #$ -e temp
    #$ -q '!mjobs_rerun.q' 
    #$ -l mem_req=18G,s_vmem=18G 
    #$ -pe def_slot 1
    export PATH=~/tools/bin:$PATH
    export OMP_NUM_THREADS=1
    
    # Your commands here
    ```

## Best Practices

!!! tip "Job submission tips"
    - **Estimate resources accurately**: Request enough memory and time, but not excessive amounts
    - **Use meaningful job names**: Makes it easier to identify your jobs
    - **Redirect output**: Always specify output and error files to avoid cluttering your home directory
    - **Test with small jobs first**: Verify your script works before submitting large jobs
    - **Check queue policies**: Different queues may have different time limits and resource restrictions
    - **Monitor your jobs**: Regularly check job status to catch errors early

!!! warning "Resource limits"
    - Jobs that exceed requested memory or time will be killed
    - Requesting too many resources may delay job start time
    - Check your cluster's documentation for default limits

## Additional Resources

- **Slurm**: [Official Documentation](https://slurm.schedmd.com/documentation.html)
- **UGE**: [Wikipedia - Univa Grid Engine](https://en.wikipedia.org/wiki/Univa_Grid_Engine)
- Check with your cluster administrator for system-specific documentation and available queues
