# File name: import_data.py
# Author: Jennifer Hoang
# Date Modified: 2023-01-24

"""Uploads all CSV data from a designated folder to BigQuery table

Usage: import_data.py <input_path>

Options:
input_path      Path to data folder containing CSVs to upload (e.g. "data/clean")
"""

from docopt import docopt
from google.cloud import bigquery
import glob

opt = docopt(__doc__)


def main(opt):
    # Construct a BigQuery client object.
    client = bigquery.Client()

    # TODO: Update table name as required
    table_id = "hut-dashboard.dispatches.route_solutions"

    job_config = bigquery.LoadJobConfig(
        source_format=bigquery.SourceFormat.CSV,
        skip_leading_rows=1,
        autodetect=True,
        allow_quoted_newlines=True,
        write_disposition='WRITE_APPEND'
    )

    # Get all CSV files located in file_path
    file_path = opt['<input_path>']
    csv_files = glob.glob(file_path + '*.csv')

    for file in csv_files:
        # Load file to table
        with open(file, "rb") as source_file:
            job = client.load_table_from_file(
                source_file, table_id, job_config=job_config)

        job.result()  # Waits for the job to complete.

    table = client.get_table(table_id)  # Make an API request.
    print(
        "Loaded {} rows and {} columns to {}".format(
            table.num_rows, len(table.schema), table_id
        )
    )


if __name__ == "__main__":
    main(opt)
