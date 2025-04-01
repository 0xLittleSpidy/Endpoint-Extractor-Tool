import os
import re
import sys
import threading
from queue import Queue
from tqdm import tqdm
from urllib.parse import urlparse

# List of required Python packages
REQUIRED_PYTHON_PACKAGES = ['tqdm']

def debug_info(message):
    """Prints debug information."""
    print(f"[DEBUG] {message}")

def check_python_packages():
    """Check if all required Python packages are installed."""
    missing_packages = []
    for package in REQUIRED_PYTHON_PACKAGES:
        try:
            __import__(package)
            debug_info(f"Python package '{package}' is available.")
        except ImportError:
            missing_packages.append(package)
            debug_info(f"Python package '{package}' is missing.")
    
    if missing_packages:
        print(f"Missing packages: {', '.join(missing_packages)}")
        print("Run the following command to install the missing packages:")
        print(f"pip install {' '.join(missing_packages)}")
        sys.exit(1)

def check_tools():
    """Verify that all necessary tools are available before starting the task."""
    REQUIRED_TOOLS = ['grep']  # Add any other tools you need
    for tool in REQUIRED_TOOLS:
        if not any(os.access(os.path.join(path, tool), os.X_OK) for path in os.environ["PATH"].split(os.pathsep)):
            print(f"Error: {tool} is not installed or not found in PATH.")
            sys.exit(1)
        debug_info(f"Tool '{tool}' is available.")

def extract_endpoints(file_path, endpoint_queue, progress_bar, root_folder):
    """Extract endpoints from a file and include the relative path as an endpoint."""
    url_regex = re.compile(r'(https?://[^\s\'"<>]+)')
    try:
        # Add the relative path as an endpoint
        relative_path = os.path.relpath(file_path, root_folder)
        endpoint_queue.put(relative_path)
        
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as file:
            content = file.read()
            urls = url_regex.findall(content)
            for url in urls:
                parsed_url = urlparse(url)
                endpoint = parsed_url.path + ('?' + parsed_url.query if parsed_url.query else '')
                
                # Remove leading slash if it's the first character
                if endpoint.startswith('/'):
                    endpoint = endpoint[1:]
                
                # Ensure the endpoint is valid before adding
                if endpoint and not re.match(r'\s*$', endpoint):
                    endpoint_queue.put(endpoint)
            progress_bar.update(1)
    except Exception as e:
        print(f"Error processing {file_path}: {e}")

def worker(endpoint_queue, output_queue, progress_bar, root_folder):
    while True:
        file_path = endpoint_queue.get()
        if file_path is None:
            break
        extract_endpoints(file_path, output_queue, progress_bar, root_folder)
        endpoint_queue.task_done()

def extract_endpoints_from_folder(folder_path, output_file=None):
    """Extract endpoints from all files in the given folder and subfolders."""
    debug_info(f"Starting extraction from folder: {folder_path}")
    
    endpoint_queue = Queue()
    output_queue = Queue()

    # Gather all files in the folder
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            file_path = os.path.join(root, file)
            endpoint_queue.put(file_path)

    # Setup progress bar
    total_files = endpoint_queue.qsize()
    progress_bar = tqdm(total=total_files, desc="Processing Files", ncols=100)

    # Start worker threads
    threads = []
    debug_info(f"Starting {os.cpu_count()} threads for extraction.")
    for _ in range(os.cpu_count()):
        thread = threading.Thread(target=worker, args=(endpoint_queue, output_queue, progress_bar, folder_path))
        thread.start()
        threads.append(thread)

    # Wait for all tasks to complete
    endpoint_queue.join()

    # Stop workers
    for _ in range(len(threads)):
        endpoint_queue.put(None)
    for thread in threads:
        thread.join()

    # Handle output
    extracted_endpoints = set()  # Use a set to automatically remove duplicates
    if output_file:
        debug_info(f"Writing extracted endpoints to: {output_file}")
        with open(output_file, 'w', encoding='utf-8', errors='ignore') as out_file:
            while not output_queue.empty():
                endpoint = output_queue.get()
                if endpoint not in extracted_endpoints:
                    extracted_endpoints.add(endpoint)
                    out_file.write(endpoint + '\n')
                    print(endpoint)
    else:
        debug_info("No output file provided, printing extracted endpoints to console.")
        while not output_queue.empty():
            endpoint = output_queue.get()
            if endpoint not in extracted_endpoints:
                extracted_endpoints.add(endpoint)
                print(endpoint)

    progress_bar.close()
    debug_info("Extraction process completed.")

def main():
    # Debug start
    debug_info("Starting the tool.")

    # Check for required tools and Python packages
    check_tools()
    check_python_packages()

    # Parse command-line arguments
    import argparse
    parser = argparse.ArgumentParser(
        description="Tool to extract endpoints (including filenames with directory structure) from files within a folder, removing duplicates.",
        epilog="Example usage: python endpoint_extractor.py /path/to/folder -o extracted_endpoints.txt"
    )
    parser.add_argument("folder", help="Path to the folder containing files to process.")
    parser.add_argument("-o", "--output", help="Optional output file to save the extracted endpoints.")
    args = parser.parse_args()

    # Start endpoint extraction process
    extract_endpoints_from_folder(args.folder, args.output)

    # Debug end
    debug_info("Tool execution finished.")

if __name__ == "__main__":
    main()

# Note: If you encounter encoding issues, try using "utf-8-sig" instead of "utf-8" in the open() function.
