from datetime import datetime
import input_output as io
from samples import Sample
from file_handler import FileHandler
from tabulate import tabulate


class Test:

    TEST_FILE = "tests.csv"
    TEST_FIELDS = [
        "ID",
        "Sample ID",
        "Status",
        "Test name",
        "Date assigned",
        "Result",
        "Date completed",
    ]

    def __str__(self):
        test_to_print = [
            [
                str(self.id),
                self.sample_id,
                self.status,
                self.test_name,
                self.date_assigned,
                self.result,
                self.date_completed,
            ]
        ]

        return tabulate(test_to_print, headers=Test.TEST_FIELDS, tablefmt="grid")

    def create(self):
        file = FileHandler()
        sample = Sample()
        print(
            f"\n-Test assignment.\n"
            f"----Please select sample.\n"
            f"Enter 'all' to show all samples ready for testing.\n"
            f"Enter sample type {Sample.SAMPLE_TYPES} to show all samples of that type.\n"
        )
        if user_input := io.request_input():
            if user_input == "all":
                io.print_samples(sample.get_samples_by_params("Status", "Ready"))

            elif user_input in Sample.SAMPLE_TYPES:
                io.print_samples(sample.get_samples_by_params("Type", user_input))
            else:
                print("\n!!!!---Selection is invalid---!!!!\n")
                self.create()
                return
            if sample := self.requesting_sample_id("Ready"):
                self.sample_id = sample.id
                self.id = file.new_id(self.TEST_FILE)
                self.status = "Ready"
                io.clear_terminal()
                print(sample)
                print(f"\nEnter name of test to be performed for '{sample.name}'.\n")
                if user_input := io.request_input():
                    self.test_name = user_input
                    self.date_assigned = str(
                        datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    )
                    self.result = "-"
                    self.date_completed = "-"
                    io.clear_terminal()
                    print(self)
                    print("\n----Do you want to assign this test? y/n\n")
                    self.save_test_to_file()

    def save_test_to_file(self, new=True):
        file = FileHandler()
        if new:
            if user_input := io.request_input():
                if user_input == "y":
                    data = {
                        "ID": self.id,
                        "Sample ID": self.sample_id,
                        "Test name": self.test_name,
                        "Status": self.status,
                        "Date assigned": self.date_assigned,
                        "Result": self.result,
                        "Date completed": self.date_completed,
                    }
                    file.file_writer(Test.TEST_FILE, Test.TEST_FIELDS, data)
        else:
            if user_input := io.request_input():
                if user_input == "y":
                    file.test_update(Test.TEST_FILE, self)

    def requesting_sample_id(self, required_status):
        sample = Sample()
        print("\nTo select sample, enter sample ID\n")
        if user_input := io.request_input():
            sample.get_sample_by_id(user_input)
            if sample.status != required_status:
                print(
                    f"\n!!!!---Selected sample status is incompatible. Please choose a sample that is {required_status}.---!!!!\n"
                )
                if sample := self.requesting_sample_id(required_status):
                    if sample.status == required_status:
                        return sample
            elif sample.status == required_status:
                return sample
        else:
            return False

    def get_test_by_sample_id(self, sample_id):
        file = FileHandler()
        file.file_reader(Test.TEST_FILE)
        tests = []
        for row in file.data:
            if row["Sample ID"] == str(sample_id):
                test = Test()
                test.id = row["ID"]
                test.sample_id = row["Sample ID"]
                test.test_name = row["Test name"]
                test.status = row["Status"]
                test.date_assigned = row["Date assigned"]
                test.result = row["Result"]
                test.date_completed = row["Date completed"]
                tests.append(test)
        return tests

    def get_test_by_test_id(self, test_id):
        file = FileHandler()
        file.file_reader(Test.TEST_FILE)
        for row in file.data:
            if row["ID"] == str(test_id):
                self.id = row["ID"]
                self.sample_id = row["Sample ID"]
                self.test_name = row["Test name"]
                self.status = row["Status"]
                self.date_assigned = row["Date assigned"]
                self.result = row["Result"]
                self.date_completed = row["Date completed"]

    def perform_test(self, test_id):
        self.get_test_by_test_id(test_id)
        print(self)
        print("\nEnter result for this test.\n")
        if user_input := io.request_input():
            self.result = user_input
            self.date_completed = str(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
            self.status = "Completed"
            print(self)
            print("\n----Do you want to save the result for this test? y/n\n")
            self.save_test_to_file(new=False)
