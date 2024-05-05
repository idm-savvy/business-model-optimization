import os
import glob
import gzip


def merge(timestamp):
    path = os.path.join(os.path.abspath('.'), "var", timestamp)
    file_list = glob.glob(f"{path}/?????.csv.gz")

    with gzip.open(f"{path}/merged.csv.gz","wb") as fout:

        # first file
        filename = file_list.pop()
        with gzip.open(filename, "rb") as f:
            fout.write(f.read())
        print(f"appended {filename}")

        # the rest    
        for filename in file_list:
            with gzip.open(filename, "rb") as f:
                next(f) # skip the header
                fout.write(f.read())
            print(f"appended {filename}")


if __name__ == "__main__":
    merge("20240505-163334")
