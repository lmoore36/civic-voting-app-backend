import csv


def tsv_to_csv(tsv_file, csv_file):
    with open(tsv_file, "r", newline="", encoding="utf-8", errors="replace") as tsvfile:
        tsvreader = csv.reader(tsvfile, delimiter="\t")

        with open(csv_file, "w", newline="", encoding="utf-8") as csvfile:
            csvwriter = csv.writer(csvfile)

            for row in tsvreader:
                # Replace empty strings with NULL
                row = [
                    (
                        ""
                        if field == "" or field == " " or field == "##/##/####"
                        else field
                    )
                    for field in row
                ]
                csvwriter.writerow(row)


tsv_to_csv("./wake_county/wake.txt", "index4.csv")
print("successfully converted")
