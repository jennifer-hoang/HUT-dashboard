# File name: pipeline.py
# Author: Jennifer Hoang
# Date Modified: 2023-02-25

"""Run data pipeline (Transform, Load) for HUT database and dashboard.

Usage: pipeline.py <input_path> <output_path>

Options:
input_path      Path to raw data file folder (e.g. "data/raw")
output_path     Path to clean data file folder (e.g. "data/clean")
"""

from docopt import docopt
import subprocess

if __name__ == "__main__":
    arguments = docopt(__doc__)
    
    subprocess.run(['python', 'src/clean_data.py', arguments['<input_path>'], arguments['<output_path>']])
    subprocess.run(['python', 'src/import_data.py', arguments['<output_path>']])