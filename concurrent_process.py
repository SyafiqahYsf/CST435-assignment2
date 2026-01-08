import cv2
import os
import time
from concurrent.futures import ProcessPoolExecutor, as_completed

# ---------------- Import Image Processing Tasks ----------------
# Import the pre-defined tasks from the tasks folder.
# These tasks represent a sequential pipeline of image filters.
from tasks import task1_grayscale, task2_blur, task3_edges, task4_sharpen, task5_brightness

# ================= Configuration Parameters =================
INPUT_DIR = "food-101-subset"        # Input folder containing images to process
OUTPUT_DIR = "output_concurrent_process"     # Folder where processed images will be saved
WORKER_COUNTS = [1, 2, 4, 8]         # Number of parallel workers to test

# ---------------- Image Processing Function ----------------
def apply_image_filters(data):
    """
    Function to apply sequential image processing filters on a single image.
    Each image passes through a pipeline of tasks: grayscale, blur, edges,
    sharpen, and brightness adjustment. The final processed image is saved
    to the output folder.	
    """
    image_path, output_folder = data
    img = cv2.imread(image_path)  # Read the image from disk

    if img is None:
        # If the image cannot be read, return None
        return None
    
    file_name = os.path.basename(image_path)

    # --- Sequential Pipeline ---
    # Each task is applied one after another. This mimics a real-world
    # image processing workflow where operations are dependent on the
    # previous step's output.
    img = task1_grayscale.apply(img)
    img = task2_blur.apply(img)
    img = task3_edges.apply(img)
    img = task4_sharpen.apply(img)
    final_image = task5_brightness.apply(img)
    
    # Save the final processed image to the output folder
    output_path = os.path.join(output_folder, f"concurrent_{file_name}")
    cv2.imwrite(output_path, final_image)
    
    return file_name

# ---------------- Run Processing using concurrent.futures ----------------
def run_concurrent_test(image_paths, workers):
    """
    Executes image processing using concurrent.futures with multiple workers.
    Measures the total time taken to process all images.
    """
    # Prepare the tasks for submission
    tasks_list = [(path, OUTPUT_DIR) for path in image_paths]
    start_time = time.time()  # Start timer for performance measurement

    # Using ProcessPoolExecutor to run multiple processes concurrently
    with ProcessPoolExecutor(max_workers=workers) as executor:
        # Submit all image processing tasks to the executor
        futures = [executor.submit(apply_image_filters, task) for task in tasks_list]

        # Ensure that all tasks are completed
        # `as_completed` returns futures as they finish, which is memory-efficient
        for future in as_completed(futures):
            _ = future.result()  # Retrieve result to catch exceptions if any

    # Calculate total execution time
    return time.time() - start_time

# ---------------- Main Execution ----------------
if __name__ == "__main__":
    # Create the output directory if it does not exist
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)

    # Verify that input folder exists and contains images
    if os.path.exists(INPUT_DIR):
        all_images = [os.path.join(INPUT_DIR, f) for f in os.listdir(INPUT_DIR)
                      if f.lower().endswith(('.png', '.jpg', '.jpeg'))]

        if not all_images:
            print(f"❌ No images found in {INPUT_DIR}")
        else:
            print(f"🚀 Starting Concurrent Processing on {len(all_images)} images...")
            results = {}

            # Loop through different numbers of workers for performance testing
            for count in WORKER_COUNTS:
                print(f"🔄 Testing with {count} worker(s)...")
                exec_time = run_concurrent_test(all_images, count)
                results[count] = exec_time

            # --- Performance Summary Table ---
            print("\n" + "="*65)
            print(f"{'Workers':<10} | {'Time (s)':<12} | {'Speedup':<10} | {'Efficiency (%)':<15}")
            print("-" * 65)

            # Serial execution time (1 worker) is used as baseline for speedup calculation
            t_serial = results[1]
            for p in WORKER_COUNTS:
                t_p = results[p]
                speedup = t_serial / t_p                 # Speedup = serial / parallel
                efficiency = (speedup / p) * 100        # Efficiency = speedup / workers * 100%
                print(f"{p:<10} | {t_p:<12.4f} | {speedup:<10.2f} | {efficiency:<15.2f}%")
            print("="*65)
            print("✅ Performance data collected using concurrent.futures.")
    else:
        print(f"❌ Input directory '{INPUT_DIR}' not found.")
