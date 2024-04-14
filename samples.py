from file_handler import FileHandler
from datetime import datetime
from tabulate import tabulate
import input_output as io


class Sample:

    SAMPLE_TYPES = ("water", "air", "product")
    SAMPLE_PARAMS = [
        "ID",
        "Type",
        "Name",
        "Status",
        "Sampling location",
        "Description",
        "Date created",
    ]
    SAMPLE_STATUS = ("Ready", "Completed", "Cancelled")
    SAMPLE_FILE = "samples.csv"

    def __str__(self):
        sample_to_print = [
            [
                str(self.id),
                self.type,
                self.name,
                self.status,
                self.location,
                self.desc,
                self.date,
            ]
        ]

        return tabulate(sample_to_print, headers=Sample.SAMPLE_PARAMS, tablefmt="grid")

    @property
    def type(self):
        return self._type

    @type.setter
    def type(self, type: str):
        if type not in Sample.SAMPLE_TYPES:
            raise ValueError(
                f"Wrong sample type, valid types are: {Sample.SAMPLE_TYPES}"
            )
        self._type = type

    @property
    def status(self):
        return self._status

    @status.setter
    def status(self, status):
        if status in Sample.SAMPLE_STATUS:
            self._status = status
            if not status == "Ready":
                file = FileHandler()
                file.status_update(Sample.SAMPLE_FILE, self.id, self._status)
        else:
            print("Invalid sample status")

    def create(self):
        print(
            f"-Sample Creation.\n"
            f"----Please select sample type {Sample.SAMPLE_TYPES}\n"
        )
        if user_input := io.request_input():
            try:
                self.type = user_input
            except ValueError as e:
                io.clear_terminal()
                print("!!!!---", e, "---!!!!")
                self.create()
                return
            print("\n----Enter sample name.\n")
            if user_input := io.request_input():
                self.name = user_input
                print("\n----Enter sampling location.\n")
                if user_input := io.request_input():
                    self.location = user_input
                    print("\n----Enter sample description.\n")
                    if user_input := io.request_input():
                        self.desc = user_input
                        self.status = "Ready"
                        self.date = str(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                        self.id = self.new_sample_id()
                        io.clear_terminal()
                        print(self)
                        print("\n----Do you want to save this sample? y/n\n")
                        if user_input := io.request_input():
                            if user_input == "y":
                                data = {
                                    "ID": self.id,
                                    "Type": self.type,
                                    "Name": self.name,
                                    "Status": self.status,
                                    "Sampling location": self.location,
                                    "Description": self.desc,
                                    "Date created": self.date,
                                }

                                file = FileHandler()
                                file.file_writer(
                                    Sample.SAMPLE_FILE, Sample.SAMPLE_PARAMS, data
                                )

    def new_sample_id(self):
        file = FileHandler()
        return file.new_id(Sample.SAMPLE_FILE)

    def get_sample_by_id(self, id):
        file = FileHandler()
        file.file_reader(Sample.SAMPLE_FILE)
        for row in file.data:
            if row["ID"] == str(id):
                self.id = row["ID"]
                self.type = row["Type"]
                self.name = row["Name"]
                self.status = row["Status"]
                self.location = row["Sampling location"]
                self.desc = row["Description"]
                self.date = row["Date created"]
        return [self]

    def get_samples_by_params(self, parameter, value):
        file = FileHandler()
        file.file_reader(Sample.SAMPLE_FILE)
        samples = []
        for row in file.data:
            if row[parameter.capitalize()] == value:
                sample = Sample()

                sample.id = row["ID"]
                sample.type = row["Type"]
                sample.name = row["Name"]
                sample.status = row["Status"]
                sample.location = row["Sampling location"]
                sample.desc = row["Description"]
                sample.date = row["Date created"]

                samples.append(sample)
        return samples

    def get_all_samples(self):
        file = FileHandler()
        file.file_reader(Sample.SAMPLE_FILE)
        samples = []
        for row in file.data:
            sample = Sample()

            sample.id = row["ID"]
            sample.type = row["Type"]
            sample.name = row["Name"]
            sample.status = row["Status"]
            sample.location = row["Sampling location"]
            sample.desc = row["Description"]
            sample.date = row["Date created"]
            samples.append(sample)
        return samples
