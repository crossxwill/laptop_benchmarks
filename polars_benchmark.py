import polars as pl
import numpy as np
import os
import time


def polars_disk_benchmark():
    # Step 2: Create a polars DataFrame with 1,000,000 rows and 100 columns
    n_rows = 1_000_000
    n_cols = 100
    data = {f"col_{i}": np.random.rand(n_rows) for i in range(n_cols)}
    df = pl.DataFrame(data)

    parquet_file = "polars_benchmark.parquet"

    # Step 3: Write the DataFrame to a parquet file and measure write speed
    start_write = time.time()
    df.write_parquet(parquet_file)
    end_write = time.time()
    write_time = end_write - start_write
    file_size = os.path.getsize(parquet_file) / (1024 * 1024)  # MB
    write_speed = file_size / write_time if write_time > 0 else float('inf')

    print(f"Write time: {write_time:.2f} seconds")
    print(f"Parquet file size: {file_size:.2f} MB")
    print(f"Write speed: {write_speed:.2f} MB/s")

    # Step 5: Read the parquet file into memory and measure read speed
    start_read = time.time()
    df_read = pl.read_parquet(parquet_file)
    end_read = time.time()
    read_time = end_read - start_read
    read_speed = file_size / read_time if read_time > 0 else float('inf')

    print(f"Read time: {read_time:.2f} seconds")
    print(f"Read speed: {read_speed:.2f} MB/s")


if __name__ == "__main__":
    polars_disk_benchmark()
