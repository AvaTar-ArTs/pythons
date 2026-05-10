"""
Parallel processing utilities for batch image operations.

This module provides multiprocessing support for faster batch processing.
"""

import multiprocessing
from concurrent.futures import ProcessPoolExecutor, as_completed
from typing import Callable, List, Optional, Tuple, TypeVar

T = TypeVar("T")
R = TypeVar("R")


def process_batch_parallel(:
    items: List[T],
    process_func: Callable[[T], R],
    max_workers: Optional[int] = None,
    show_progress: bool = False,
) -> List[R]:
    """
    Process items in parallel using multiprocessing.

    Args:
        items: List of items to process
        process_func: Function to process each item
        max_workers: Maximum number of worker processes.
                    If None, uses 75% of CPU cores (min 2, max 8)
        show_progress: Whether to show progress (requires tqdm)

    Returns:
        List of results in the same order as input
    """
    if max_workers is None:
        # Use 75% of CPU cores for better system responsiveness
        # Minimum 2, maximum 8 to avoid diminishing returns
        cpu_count = multiprocessing.cpu_count()
        max_workers = max(2, min(8, int(cpu_count * 0.75)))

    if max_workers == 1:
        # Single-threaded fallback
        return [process_func(item) for item in items]

    results = []
    with ProcessPoolExecutor(max_workers=max_workers) as executor:
        # Submit all tasks
        future_to_item = {executor.submit(process_func, item): item for item in items}

        # Collect results with optional progress
        if show_progress:
            try:
                from tqdm import tqdm

                with tqdm(total=len(items), desc="Processing") as pbar:
                    for future in as_completed(future_to_item):
                        results.append((future_to_item[future], future.result()))
                        pbar.update(1)
            except ImportError:
                # Fallback if tqdm not available
                for future in as_completed(future_to_item):
                    results.append((future_to_item[future], future.result()))
        else:
            for future in as_completed(future_to_item):
                results.append((future_to_item[future], future.result()))

    # Sort results to maintain input order
    item_to_result = dict(results)
    return [item_to_result[item] for item in items]


def process_images_parallel(:
    image_files: List[str],
    process_func: Callable[[str], Tuple[bool, dict]],
    max_workers: Optional[int] = None,
    show_progress: bool = True,
) -> List[Tuple[bool, dict]]:
    """
    Process images in parallel.

    Args:
        image_files: List of image file paths
        process_func: Function that takes image path, returns (success, result)
        max_workers: Maximum number of worker processes
        show_progress: Whether to show progress bar

    Returns:
        List of (success, result) tuples
    """
    return process_batch_parallel(
        image_files, process_func, max_workers=max_workers, show_progress=show_progress
    )
