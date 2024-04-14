from tabulate import tabulate
from samples import Sample
from tests import Test
import report
from file_handler import FileHandler
import input_output as io


def main():
    """Creates the 'main menu'"""
    while True:
        io.clear_terminal()
        intro()
        if request_mode() == False:
            break


def intro():
    print(
        "Welcome to the Laboratory Information Management System\n\n",
        "Please select what action to perform.\n\n",
        "Available actions:\n",
        "sample - To manage samples\n",
        "test - To assign a test to a sample\n",
        "result - To enter a result for a test\n",
        "report - To generate a sample testing report\n",
    )


def request_mode():
    """Requests user input and calls required functions"""
    if user_input := io.request_input():
        if user_input == "sample":
            io.clear_terminal()
            sample_mode()
        elif user_input == "test":
            io.clear_terminal()
            test = Test()
            test.create()
        elif user_input == "result":
            io.clear_terminal()
            result_entry()
        elif user_input == "report":
            sample = Sample()
            io.print_samples(sample.get_all_samples())
            print("\nSelect sample ID to generate testing report for this sample\n")
            if user_input := io.request_input():
                sample.get_sample_by_id(user_input)
                report_gen(sample)
        else:
            print("\n!!!!---Incorrect selection---!!!!\n")
            request_mode()
    elif user_input == False:
        return False


def sample_mode():
    """Sample management mode, request user input to select actions with samples"""
    while True:
        sample = Sample()
        print(
            "Sample management options:\n",
            "da - To display all samples\n",
            "f - To display samples filtered by some property\n",
            "add - To create new sample\n",
            "x - To cancel samples\n"
        )
        if user_input := io.request_input():
            if user_input == "da":
                io.print_samples(sample.get_all_samples())
            elif user_input == "f":
                io.clear_terminal()
                print(
                    "Select filtering criteria\n",
                    "r - Will return all 'Ready' samples\n",
                    "c - Will return all 'Completed' samples\n",
                    "x - Will return all 'Cancelled' samples\n",
                    "water - Will return all 'water' type samples\n",
                    "air - Will return all 'air' type samples\n",
                    "product - Will return all 'product' type samples\n",
                )
                if user_input := io.request_input():
                    if user_input == "r":
                        io.print_samples(
                            sample.get_samples_by_params("status", "Ready")
                        )
                    elif user_input == "c":
                        io.print_samples(
                            sample.get_samples_by_params("status", "Completed")
                        )
                    elif user_input == "x":
                        io.print_samples(
                            sample.get_samples_by_params("status", "Cancelled")
                        )
                    elif user_input == "water":
                        io.print_samples(
                            sample.get_samples_by_params("type", "water")
                        )
                    elif user_input == "air":
                        io.print_samples(
                            sample.get_samples_by_params("type", "air")
                        )
                    elif user_input == "product":
                        io.print_samples(
                            sample.get_samples_by_params("type", "product")
                        )
                    else:
                        print("\nInvalid entry\n")
            elif user_input == "add":
                sample.create()
            elif user_input == "x":
                io.print_samples(
                            sample.get_samples_by_params("status", "Ready")
                        )
                print("\nSelect sample ID to cancel that sample\n")
                if user_input := io.request_input():
                    sample.get_sample_by_id(user_input)
                    io.clear_terminal()
                    print(sample)
                    print("\nAre you sure you want to cancel this sample? y/n\n")
                    if user_input := io.request_input():
                        if user_input == "y":
                            sample.status = "Cancelled"
        elif user_input == False:
            break


def result_entry():
    """Handles fetching requested sample, selecting assigned test and entering results"""
    sample = Sample()
    test = Test()
    io.print_samples(sample.get_samples_by_params("status", "Ready"))
    print("\nSelect sample that will be tested.\n")
    if user_input := io.request_input():
        if len(test.get_test_by_sample_id(user_input)) == 0:
            io.clear_terminal()
            print(
                "\nThe selected sample has no tests assigned, please select different sample\n"
            )
            result_entry()
            return
        else:
            io.clear_terminal()
            io.print_samples(sample.get_sample_by_id(user_input))
            io.print_tests(test.get_test_by_sample_id(user_input))

        print("\nSelect test ID for result entry\n")

        if user_input := io.request_input():
            test.perform_test(user_input)
            test_id = test.id
            tests = test.get_test_by_sample_id(sample.id)
            n = 0
            for t in tests:
                if t.id != test_id and t.status == "Ready":
                    n += 1
            if n == 0:
                sample.status = "Completed"








def report_gen(sample):

    sample_data = [
        Sample.SAMPLE_PARAMS,
        [
            sample.id,
            sample.type,
            sample.name,
            sample.status,
            sample.location,
            sample.desc,
            sample.date,
        ],
    ]

    test = Test()
    tests = test.get_test_by_sample_id(sample.id)
    test_data = [Test.TEST_FIELDS]
    for test in tests:
        test_data.append(
            [
                test.id,
                test.sample_id,
                test.status,
                test.test_name,
                test.date_assigned,
                test.result,
                test.date_completed,
            ]
        )

    report.create_pdf_report(f"Sample ID {sample.id} testing report.pdf", sample_data, test_data)


if __name__ == "__main__":
    main()
