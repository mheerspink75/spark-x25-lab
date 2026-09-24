"""
Simple Test Runner for the GitHub Issue Triage project.

Executes all test functions from the tests module without requiring
pytest. Each test function starting with `test_` is executed and
results are reported.
"""

import importlib
import sys
from pathlib import Path

# Add the project root to sys.path so tests can import src.
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

# Import the test modules.
from tests import test_categorizer
from tests import test_stats
from tests import test_reporter


def run_test_function(func):
    """Run a single test function and return (passed, error_message)."""
    try:
        func()
        return True, ""
    except Exception as exc:
        return False, str(exc)


def main() -> int:
    """Run all test functions and print results."""
    print("=" * 70)
    print("GitHub Issue Triage — Test Suite")
    print("=" * 70)
    print()

    total_tests = 0
    passed_tests = 0
    failed_tests = 0

    all_results = []

    # Collect all test functions from all test modules.
    test_modules = [test_categorizer, test_stats, test_reporter]
    all_test_functions = []

    for module in test_modules:
        module_test_functions = [
            obj for name, obj in vars(module).items()
            if name.startswith("test_") and callable(obj)
        ]
        all_test_functions.extend(module_test_functions)

    total_tests = len(all_test_functions)
    print(f"Found {total_tests} test function(s).")
    print()

    for idx, test_func in enumerate(all_test_functions, 1):
        passed, error = run_test_function(test_func)

        all_results.append({
            "index": idx,
            "function": test_func.__name__,
            "passed": passed,
            "error": error,
        })

        if passed:
            passed_tests += 1
            print(f"[PASS] Test {idx:3d}: {test_func.__name__}")
        else:
            failed_tests += 1
            print(f"[FAIL] Test {idx:3d}: {test_func.__name__}")
            if error:
                print(f"        Error: {error}")
        print()

    # Summary
    print("=" * 70)
    print("Test Summary")
    print("=" * 70)
    print(f"Total Tests: {total_tests}")
    print(f"Passed: {passed_tests}")
    print(f"Failed: {failed_tests}")
    print()

    if failed_tests > 0:
        print("FAILED TESTS:")
        for result in all_results:
            if not result["passed"]:
                print(f"  - {result['function']}: {result['error']}")
        return 1
    else:
        print("All tests passed successfully!")
        return 0


if __name__ == "__main__":
    sys.exit(main())
