# File name: clean_data.py
# Author: Jennifer Hoang
# Date Modified: 2023-01-24

"""This script cleans Routific solution files for the HUT database and dashboard.

Usage: clean_data.py <input_path> <output_path>

Options:
input_path      Path to raw data file folder (e.g. "data/raw")
output_path     Path to clean data file folder (e.g. "data/clean")
"""

from docopt import docopt
import os
import re
import pandas as pd
import numpy as np

opt = docopt(__doc__)


def get_file_names(input_path):
    """Get all Routific solution file names from a folder.
    
    Parameters
    ----------
    input_path : str
    
    Returns
    -------
    list of str
        List of file names containing 'solution'
    """
    file_list = []
    for file_name in os.listdir(input_path):
        if 'solution' in file_name.lower() and '.csv' in file_name:
            file_list.append(file_name)
    return file_list


def clean_route(input_path, file_name, output_path):
    """Clean raw route solution csv file and export clean data as csv file.
        
    Parameters
    ----------
    input_path : str
        Path to read data
    file_name : str
        Name of data file (csv)
    output_path : str
        Path to export data
    
    Returns
    -------
    None
    """
    raw_data = pd.read_csv(os.path.join(input_path, file_name))

    cols = [
        "Driver Name",
        "Stop Number",
        "Visit Name",
        "Address",
        "Start at",
        "Finish by",
        "Distance(km)",
        "Stop Status",
        "Completion/skipped Time",
        "Skipped Reason",
        "Driver Notes",
        "FamilyID",
    ]

    # Clean column names for upload (letters, numbers, underscores only)
    col_names = [re.sub("(\s|/|\(|\))", "_", s) for s in cols]

    # Select required columns and rename
    clean_data = raw_data[cols].copy()
    clean_data.columns = col_names

    # Extract FSA from Address
    clean_data["FSA"] = (clean_data["Address"]
        .str.extract(
            r"([ABCEGHJ-NPRSTVXY]\d[ABCEGHJ-NPRSTV-Z])",
            flags = re.IGNORECASE,
            expand = False
        )
        .str.upper()
    )

    # Extract Postal Code from Address
    clean_data["Postal_Code"] = (clean_data["Address"]
        .str.extract(
            r"([ABCEGHJ-NPRSTVXY]\d[ABCEGHJ-NPRSTV-Z][ -]?\d[ABCEGHJ-NPRSTV-Z]\d)",
            flags = re.IGNORECASE,
            expand = False
        )
        .str.upper()
        .str.replace("\W", '', regex = True)
        .str.split(r"([ABCEGHJ-NPRSTVXY]\d[ABCEGHJ-NPRSTV-Z])")
        .str.join(' ')
    )

    # Create binarized Stop Completion variable
    clean_data["Stop_Completion"] = np.where(
        clean_data["Stop_Status"] == "done",
        "1",
        np.where(
            clean_data["Stop_Status"] == "skipped",
            "0",
            np.where(
                (
                    clean_data["Stop_Status"].isna()
                    & clean_data["Driver_Notes"].isna()
                    & clean_data["Distance_km_"].notna()
                ),
                "1",  # If driver forgets to mark status and didn't leave note, assume done
                None,
            ),
        ),
    ).astype("int")

    # Create File Name variable to extract dispatch information
    clean_data["File_Name"] = file_name

    clean_data["Dispatch_Date"] = clean_data["File_Name"].str.extract(
        r"(\d{4}-\d{2}-\d{2})"
    )

    clean_data["Dispatch_Type"] = np.where(
        clean_data["File_Name"].str.contains("FSP"),
        "FSP",
        np.where(
            clean_data["File_Name"].str.contains("MOP"),
            "MOP",
            np.where(clean_data["File_Name"].str.contains(
                "Special"), "Special", "Other"),
        ),
    )

    clean_data["Dispatch_Name"] = clean_data["Dispatch_Date"].str.cat(
        clean_data["Dispatch_Type"], sep=" "
    )

    # Remove Start/Finish times exceeding 24 hours
    clean_data["Start_at"] = np.where(
        clean_data["Start_at"].str.split(':').str.get(0).astype(
            float) > 23, None, clean_data["Start_at"]
    )
    clean_data["Finish_by"] = np.where(
        clean_data["Finish_by"].str.split(':').str.get(0).astype(
            float) > 23, None, clean_data["Finish_by"]
    )

    # Convert times to Datetime formats and calculate duration between stops in minutes
    clean_data["Start_at"] = pd.to_datetime(clean_data["Dispatch_Date"]).dt.tz_localize(
        "US/Eastern"
    ) + pd.to_timedelta(clean_data["Start_at"] + ":00")
    
    clean_data["Finish_by"] = pd.to_datetime(clean_data["Dispatch_Date"]).dt.tz_localize(
        "US/Eastern"
    ) + pd.to_timedelta(clean_data["Finish_by"] + ":00")
    
    clean_data["Duration_mins"] = clean_data.groupby("Driver_Name")[
        "Start_at"
    ].diff() / pd.Timedelta(minutes=1)

    # Clean Driver and Visit names
    clean_data['Driver_Name'] = (clean_data['Driver_Name']
        .str.title()
        .str.replace(r'\(Route .+\)', '', regex=True)
        .str.strip()
    )

    clean_data['Visit_Name'] = (clean_data['Visit_Name']
        .str.title()
        .str.strip()
    )

    # Write to CSV
    clean_data.to_csv(os.path.join(output_path, "Clean_" + file_name), index=False)


def main(opt):
    raw_files = get_file_names(opt['<input_path>'])
    output_files = []
    error_files = []

    for file_name in raw_files:
        print(file_name)
        try:
            clean_route(opt['<input_path>'], file_name, opt['<output_path>'])
            output_files.append(file_name)
        except Exception as e:
            print(e)
            error_files.append(file_name)

    print(f"{len(output_files)} file(s) created in: {opt['<output_path>']}")
    if len(error_files):
        print(f"Something went wrong in {len(error_files)} file(s): {error_files}")


if __name__ == "__main__":
    main(opt)
