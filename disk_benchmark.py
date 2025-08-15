import os
import time
import sys

def test_disk_write_speed(file_path, block_size, blocks_count):
    """
    Tests disk write speed.
    """
    try:
        # Using os.open for low-level file operations
        f = os.open(file_path, os.O_CREAT | os.O_WRONLY, 0o777)
    except OSError as e:
        print(f"Error opening file for writing: {e}")
        return

    total_bytes_written = 0
    # Create a block of random data
    data_block = os.urandom(block_size)
    
    start_time = time.time()
    for _ in range(blocks_count):
        bytes_written = os.write(f, data_block)
        if bytes_written != block_size:
            print("Error during write operation.")
            os.close(f)
            return
        total_bytes_written += bytes_written
    
    # os.fsync() forces the write of file to disk
    os.fsync(f)
    end_time = time.time()
    
    os.close(f)

    duration = end_time - start_time
    if duration > 0:
        # Calculate speed in MB/s
        speed_mbps = (total_bytes_written / (1024 * 1024)) / duration
        print(f"Disk Write Speed: {speed_mbps:.2f} MB/s")
    else:
        print("Write test completed too quickly to measure speed.")

    return total_bytes_written

def test_disk_read_speed(file_path, block_size, total_size):
    """
    Tests disk read speed.
    """
    try:
        f = os.open(file_path, os.O_RDONLY)
    except OSError as e:
        print(f"Error opening file for reading: {e}")
        return

    total_bytes_read = 0
    start_time = time.time()
    
    while total_bytes_read < total_size:
        data_block = os.read(f, block_size)
        if not data_block:
            break # End of file
        total_bytes_read += len(data_block)

    end_time = time.time()
    os.close(f)

    duration = end_time - start_time
    if duration > 0:
        # Calculate speed in MB/s
        speed_mbps = (total_bytes_read / (1024 * 1024)) / duration
        print(f"Disk Read Speed: {speed_mbps:.2f} MB/s")
    else:
        print("Read test completed too quickly to measure speed.")


def main():
    """
    Main function to run the disk benchmark.
    """
    file_name = "disk_benchmark_test_file.dat"
    # Create the test file in the current working directory
    file_path = os.path.join(os.getcwd(), file_name)
    
    # Parameters for the test can be adjusted here
    block_size = 1024 * 1024  # 1 MB
    blocks_count = 10240    # Write 10240 blocks, for a total file size of 10 GB

    print(f"Starting disk benchmark with a {blocks_count * block_size / (1024*1024)} MB file...")
    print("-" * 30)

    # Test write speed first
    total_size = test_disk_write_speed(file_path, block_size, blocks_count)

    if total_size:
        # Then test read speed on the same file
        test_disk_read_speed(file_path, block_size, total_size)

    print("-" * 30)
    # Clean up the created test file
    try:
        os.remove(file_path)
        print(f"Successfully cleaned up the test file: {file_path}")
    except OSError as e:
        print(f"Error during file cleanup: {e}")

if __name__ == "__main__":
    main()
