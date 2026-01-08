# Parallel Image Processing System  
CST435: Parallel and Cloud Computing – Assignment 2

## Overview
This project implements a parallel image processing system using Python on
Google Cloud Platform (GCP). The system applies a sequence of image filters to
a subset of the Food-101 dataset and evaluates performance using different
parallel programming paradigms.

Two Python-based parallel implementations are provided:
1. Python multiprocessing
2. Python concurrent.futures

Both implementations apply the same image processing pipeline to ensure fair
and meaningful performance comparison.

---

## Dataset
The Food-101 dataset is used as the input source. A smaller subset of 250 images
is selected to ensure manageable execution time during testing.

Each image is processed independently, making the workload well-suited for
data parallelism.

---

## Image Processing Pipeline
Each image undergoes the following five processing stages:

1. **Grayscale Conversion**  
   Converts RGB images to grayscale to reduce data complexity and processing
   overhead.

2. **Gaussian Blur (3×3 Kernel)**  
   Smooths the image to reduce noise and improve edge detection accuracy.

3. **Edge Detection (Sobel Filter)**  
   Detects horizontal and vertical edges by computing image gradients.

4. **Image Sharpening**  
   Enhances edges and details using a custom convolution kernel.

5. **Brightness Adjustment**  
   Increases pixel intensity to improve visual clarity.

All filters operate on individual pixels or small neighborhoods, making them
suitable for parallel execution.

---

## Implementation 1: Python multiprocessing
**File:** `multiprocesing.py`

### Parallel Paradigm
- **Paradigm:** Process-based parallelism
- **Module:** Python `multiprocessing`
- **Parallel Model:** Data parallelism

### Parallelization Strategy
This implementation uses Python’s `multiprocessing.Pool` to create multiple
worker processes. Each worker independently processes a single image through
the complete image processing pipeline.

The workload is distributed using `pool.map()`, which automatically assigns
different images to different worker processes. Since each image is processed
independently, no shared memory or synchronization primitives are required.

### Rationale for Using Multiprocessing
Image processing operations such as convolution, edge detection, and
filtering are CPU-bound tasks. Python multiprocessing is chosen because it:
- Bypasses the Global Interpreter Lock (GIL)
- Enables true parallel execution on multi-core CPUs
- Provides good scalability for compute-intensive workloads

This approach ensures efficient utilization of available CPU cores on the
GCP virtual machine.

### Load Balancing and Synchronization
- Each process handles one image at a time
- Tasks are evenly distributed across workers
- No shared state is used, preventing race conditions
- Output files are written independently with unique filenames

This design results in effective load balancing and minimal synchronization
overhead.

### Performance Evaluation
The program measures execution time using different numbers of worker
processes:
- 1 process (serial baseline)
- 2 processes
- 4 processes
- 8 processes

The following performance metrics are calculated:
- **Execution Time**
- **Speedup**
- **Parallel Efficiency**

These metrics are used to analyze scalability and resource utilization.

---

## Implementation 2: Python concurrent.futures
**File:** `image_concurrent.py`

### Parallel Paradigm
- **Paradigm:** Executor-based parallelism
- **Module:** Python `concurrent.futures`

### Parallelization Strategy
> 

### Rationale and Design Decisions
> 

### Performance Evaluation
> 

---

## Performance Analysis
Both implementations are tested on the same dataset and execution environment
to ensure fair comparison.

Performance is evaluated using:
- Execution time
- Speedup
- Parallel efficiency

Results are analyzed to study scalability, bottlenecks, and the impact of
parallel overhead in real-world cloud environments.

---

## Platform and Environment
- **Cloud Platform:** Google Cloud Platform (GCP)
- **Execution Environment:** Multi-core Virtual Machine
- **Programming Language:** Python
- **Libraries:** OpenCV, NumPy, multiprocessing, concurrent.futures

---

## How to Run

### Prerequisites
Install required Python libraries:
```bash
pip install opencv-python numpy
