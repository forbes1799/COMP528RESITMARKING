import click
import requests
import os


def download_file(url, filename):
    if os.path.isfile(filename):
        print("File exists. Skipping...")
        return
    r = requests.get(url, stream=True)
    with open(filename,'wb') as f:
        for chunk in r.iter_content(chunk_size=1024):
         if chunk:
             f.write(chunk)


@click.command()
@click.option('--file-list', required=True, help='The file with a list of files to be downloaded')
def run(file_list):
    with open(file_list) as file:
        for line in file:
            url, name = line.rstrip().split(" ")
            print("Downloading file %s..." % name)
            download_file(url, name)


if __name__ == "__main__":
    run()