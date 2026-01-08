import cv2
import os
import time
import multiprocessing

# Import the tasks from the tasks folder
from tasks import task1_grayscale, task2_blur, task3_edges, task4_sharpen, task5_brightness

# ================= Configuration =================
INPUT_DIR = "food-101-subset"
OUTPUT_DIR = "output_multiprocessing"
WORKER_COUNTS = [1, 2, 4, 8]

def apply_image_filters(data):
    image_path, output_folder = data
    img = cv2.imread(image_path)
    
    if img is None:
        return None
    
    file_name = os.path.basename(image_path)

    # --- Sequential Pipeline ---
    # We call each task one by one, passing the result of the previous to the next
    img = task1_grayscale.apply(img)
    img = task2_blur.apply(img)
    img = task3_edges.apply(img)
    img = task4_sharpen.apply(img)
    final_image = task5_brightness.apply(img)
    
    # Save the processed image
    output_path = os.path.join(output_folder, f"processed_{file_name}")
    cv2.imwrite(output_path, final_image)
    return file_name

def run_multiprocessing_test(image_paths, workers):
    tasks_list = [(path, OUTPUT_DIR) for path in image_paths]
    start_time = time.time()
    
    with multiprocessing.Pool(processes=workers) as pool:
        pool.map(apply_image_filters, tasks_list)

    return time.time() - start_time

if __name__ == "__main__":
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)

    if os.path.exists(INPUT_DIR):
        all_images = [os.path.join(INPUT_DIR, f) for f in os.listdir(INPUT_DIR) 
                      if f.lower().endswith(('.png', '.jpg', '.jpeg'))]

        if not all_images:
            print(f"❌ No images found in {INPUT_DIR}")
        else:
            print(f"🚀 Starting Parallel Processing on {len(all_images)} images...")
            results = {}

            for count in WORKER_COUNTS:
                print(f"🔄 Testing with {count} worker(s)...")
                exec_time = run_multiprocessing_test(all_images, count)
                results[count] = exec_time

            # --- Results Table ---
            print("\n" + "="*65)
            print(f"{'Workers':<10} | {'Time (s)':<12} | {'Speedup':<10} | {'Efficiency (%)':<15}")
            print("-" * 65)
            
            t_serial = results[1] 
            for p in WORKER_COUNTS:
                t_p = results[p]
                speedup = t_serial / t_p 
                efficiency = (speedup / p) * 100 
                print(f"{p:<10} | {t_p:<12.4f} | {speedup:<10.2f} | {efficiency:<15.2f}%")
            print("="*65)
    else:
        print(f"❌ Input directory '{INPUT_DIR}' not found.")
