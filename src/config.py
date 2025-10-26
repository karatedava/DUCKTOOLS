"""
DEFINITION OF GLOBAL PARAMETERS
"""

from pathlib import Path

DATA_PATH = Path('./data')

CONFIG_FOLDER = Path('./configs')
DEFAULT_CONFIG_FILE = 'config_safe.json'
OUTPUT_DIR = Path('./data')
DEFAULT_SIMULATOR = 'GM' # YP is the other valid option
DEFAULT_CTIME = 100
DEFAULT_LB = 1300

OPTIM_DATA_PATH = Path('./optimization_data')