import csv
import os



class FileHandler:
    """Handles file read/write operations"""

    def file_writer(
        self, file_name: str, fields: list, data: dict | list, mode="a"
    ) -> None:
        """Writes CSV files"""
        file_exists = os.path.isfile(file_name)
        with open(file_name, mode, newline="") as csvfile:
            csv_writer = csv.DictWriter(csvfile, fieldnames=fields)

            if mode == "w":
                csv_writer.writeheader()
                csv_writer.writerows(data)
            else:
                if not file_exists:
                    csv_writer.writeheader()
                csv_writer.writerow(data)

    def file_reader(self, file_name):
        """Reads file and sets the file content as object property"""
        rows = []
        if os.path.isfile(file_name):
            with open(file_name, newline="") as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    rows.append(row)
            self.data = rows
            return True
        else:
            return False

    def status_update(self, target, id, status):
        """Updates the status of a record in a file"""
        self.file_reader(target)
        fields = self.data[0].keys()
        new_data = []
        for record in self.data:
            if record["ID"] == str(id):
                record["Status"] = status
            new_data.append(record)

        self.file_writer(target, list(fields), new_data, mode="w")

    def test_update(self, target, test):
        """Updates test record status, result and date completed values in a file"""
        self.file_reader(target)
        fields = self.data[0].keys()
        new_data = []
        for record in self.data:
            if record["ID"] == str(test.id):
                record["Status"] = test.status
                record["Result"] = test.result
                record["Date completed"] = test.date_completed
            new_data.append(record)

        self.file_writer(target, list(fields), new_data, mode="w")

    def new_id(self, file_name):
        """Generated a new ID based on the last record ID in a file"""
        if self.file_reader(file_name):
            try:
                last_row = self.data[-1:][0]
            except IndexError:
                return 1
            return int(last_row["ID"]) + 1
        else:
            return 1
