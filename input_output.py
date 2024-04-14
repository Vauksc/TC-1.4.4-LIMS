from tabulate import tabulate
import os


def request_input():
    """Requests for user input or 'back' command"""
    back_cmd = ("b", "back")
    print(f"-To go back enter: {back_cmd}")
    if user_input := input("Enter: ").strip().lower():
        if user_input in back_cmd:
            clear_terminal()
            return False
        return user_input
    else:
        return request_input()


def print_samples(samples):
    """Prints a table with one or more sample records"""
    if not type(samples) == list:
        print(samples)
    else:
        samples_to_print = []
        for sample in samples:
            samples_to_print.append(
                [
                    str(sample.id),
                    sample.type,
                    sample.name,
                    sample.status,
                    sample.location,
                    sample.desc,
                    sample.date,
                ]
            )
        print(
            tabulate(
                samples_to_print,
                headers=[
                    "ID",
                    "Type",
                    "Name",
                    "Status",
                    "Sampling location",
                    "Description",
                    "Date created",
                ],
                tablefmt="grid",
            )
        )


def print_tests(tests):
    """Prints a table with one or more test records"""
    if not type(tests) == list:
        print(tests)
    else:
        tests_to_print = []
        for test in tests:
            tests_to_print.append(
                [
                    str(test.id),
                    test.sample_id,
                    test.test_name,
                    test.status,
                    test.date_assigned,
                    test.result,
                    test.date_completed,
                ]
            )
        print(
            tabulate(
                tests_to_print,
                headers=[
                    "ID",
                    "Sample ID",
                    "Status",
                    "Test name",
                    "Date assigned",
                    "Result",
                    "Date completed",
                ],
                tablefmt="grid",
            )
        )


def clear_terminal():
    """Clears the terminal screen."""
    os.system("cls" if os.name == "nt" else "clear")
