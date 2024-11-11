import time
import psutil
import logging

logger = logging.getLogger('benchmark')

def benchmark(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        process = psutil.Process()
        memory_before = process.memory_info().rss
        cpu_before = process.cpu_percent(interval=None)

        result = func(*args, **kwargs)

        memory_after = process.memory_info().rss
        cpu_after = process.cpu_percent(interval=None)
        end_time = time.time()

        logger.info(f"Start Time: {start_time}")
        logger.info(f"End Time: {end_time}")
        logger.info(f"Elapsed Time: {end_time - start_time} seconds")
        logger.info(f"Memory Usage: {memory_after - memory_before} bytes")
        logger.info(f"CPU Usage: {cpu_after - cpu_before}%")

        return result
    return wrapper
