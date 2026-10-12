test_results = [
    {"test_name": "device_discovery", "status": "PASS", "duration": 2.5},
    {"test_name": "smart_log_check", "status": "FAIL", "duration": 1.2},
    {"test_name": "namespace_validation", "status": "PASS", "duration": 3.0},
    {"test_name": "read_write_test", "status": "FAIL", "duration": 8.5},
    {"test_name": "firmware_check", "status": "PASS", "duration": 1.8}
]

total_tests = 0
passed_tests = 0
failed_tests = 0
failed_test_names = []
total_time = 0

for test in test_results:
    total_tests+=1
    total_time +=test["duration"]

    if test["status"] == "PASS":
        passed_tests+=1
    elif test["status"] == "FAIL":
        failed_tests+=1
        failed_test_names.append(test["test_name"])


print(f"Total tests : {total_tests}")
print(f"Passed tests : {passed_tests}")
print(f"Failed tests : {failed_tests}")
print(f"Failed test names : {failed_test_names}")
print(f"Total execution time : {total_time}")


