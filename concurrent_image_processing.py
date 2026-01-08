import cv2
import numpy as np
import os
import time
from concurrent.futures import ProcessPoolExecutor, as_completed

# Import the tasks from the tasks folder
from tasks import task1_grayscale, task2_blur, task3_edges, task4_sharpen, task5_brightness

# ================= Configuration Parameters =================
INPUT_DIR = "food-101-subset" # Data source folder containing 250 Food-101 i>
OUTPUT_DIR = "output_concurrent" # Output path
WORKER_COUNTS = [1, 2, 4, 8]  # Number of processes to test

# ---------------- Run Processing using concurrent.futures ----------------
def run_concurrent_test(image_paths, workers):
    tasks = [(path, OUTPUT_DIR) for path in image_paths]
    start_time = time.time()

    with ProcessPoolExecutor(max_workers=workers) as executor:
        # Submit all tasks
        futures = [executor.submit(apply_image_filters, task) for task in ta>

        # Wait for all futures and process results
        for future in as_completed(futures):
            _ = future.result()  # Retrieve result to ensure task completion>

    duration = time.time() - start_time
    return duration

# ---------------- Main ----------------
if __name__ == "__main__":
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)

    if os.path.exists(INPUT_DIR):
        all_images = [os.path.join(INPUT_DIR, f) for f in os.listdir(INPUT_D>
                      if f.lower().endswith(('.jpg', '.jpeg', '.png'))]

        if not all_images:
            print(f"❌ No images found in {INPUT_DIR}")
        else:
            print(f"🚀 Starting Performance Analysis on {len(all_images)} im>
            results = {}

            for count in WORKER_COUNTS:
                print(f"🔄 Processing with {count} worker(s)...")
                exec_time = run_concurrent_test(all_images, count)
                results[count] = exec_time

            # --- PERFORMANCE TABLE ---
            print("\n" + "="*65)
            print(f"{'Workers':<10} | {'Time (s)':<12} | {'Speedup':<10} | {>
            print("-" * 65)

            t_serial = results[1]

            for p in WORKER_COUNTS:
                t_p = results[p]
                speedup = t_serial / t_p
                efficiency = (speedup / p) * 100
                print(f"{p:<10} | {t_p:<12.4f} | {speedup:<10.2f} | {efficie>

            print("="*65)
            print("✅ Performance data collected using concurrent.futures.")
    else:
        print(f"❌ Input directory '{INPUT_DIR}' not found. Please upload it>
