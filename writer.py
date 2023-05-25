import csv
import portalocker
import os


def write_results(newrow, overwrite_identifier, results_file):
    # duplicate_identifier must be a lambda function which, when passed a row
    # from the csv should return whether or not the current result (in new
    # row) should overwrite this row

    lock = portalocker.Lock(results_file)

    existing_results = []
    with lock:
        if os.path.exists(results_file):
            with open(results_file, 'r') as ifile:
                reader = csv.DictReader(ifile)
                existing_results = list(reader)

        existing_results = [x for x in existing_results
                            if not overwrite_identifier(x)]

        existing_results.append(newrow)

        with open(results_file, mode="w") as ofile:
            writer = csv.DictWriter(ofile, fieldnames=newrow.keys())
            writer.writeheader()
            for row in existing_results:
                writer.writerow(row)
