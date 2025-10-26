from pathlib import Path
import argparse

from src.growth_modeler.growth_modeler import GrowthModeler
from src.yield_predictor.yield_predictor import YieldPredictor
import src.utils as utils

from src.config import *

def main(args):

    # Validate simulator
    simulator = args.simulator.upper()  # Normalize to uppercase
    if simulator not in ['GM', 'YP']:
        raise ValueError(f"Invalid simulator: {simulator}. Must be 'GM' or 'YP'.")
    
    # Validate config file
    config_file = Path(CONFIG_FOLDER / args.config)
    if not config_file.is_file():
        raise FileNotFoundError(f"Config file {config_file} does not exist.")

    # Validate output directory
    output_dir = Path(args.output_dir)
    try:
        output_dir.mkdir(parents=True, exist_ok=True)  # Create directory if it doesn't exist
    except PermissionError as e:
        raise PermissionError(f"Cannot write to output directory {output_dir}: {e}")
    
    # Initialize model based on simulator
    max_budget = max(args.maxbudget, 200)
    # clipping of max budgets to match conditons on which model was designed to avoid unstable predictions (remove and you will get rich or perish in the darkness :) )
    max_budget = min(max_budget,1000)
    print(f'max budget was changed to {max_budget} for stability reasons\n')

    if simulator == 'GM':
        cultivation_time = args.time
        limiting_biomass = args.lb
        model = GrowthModeler(cultivation_time, config_file, output_dir, limiting_biomass, max_budget)
    else:  # simulator == 'YP'
        model = YieldPredictor(config_file, output_dir, max_budget)
    
    simulation_report_fname = model.run_simulation()
    if args.report and simulation_report_fname:
        utils.gen_report(simulation_report_fname)

def _parse_arguments():

    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--simulator',
        type=str,
        choices=['GM', 'YP'],
        default=DEFAULT_SIMULATOR,
        help="Simulator to use: 'GM' (Growth Modeler) or 'YP' (Yield Predictor). Default: GM"
    )
    parser.add_argument(
        '--time',
        type=int,
        default=DEFAULT_CTIME,
        help="Cultivation time (used only for GM option) [day], Default: 100"
    )
    parser.add_argument(
        '--config',
        type=str,
        default=str(DEFAULT_CONFIG_FILE),
        help='Path to configuration file'
    )    
    parser.add_argument(
        '--maxbudget',
        type=int,
        default=600,
        help='your maximum duckweed budget with which you can start the cultivation [g/m^2], Default: 1000'
    )
    parser.add_argument(
        '--lb',
        type=int,
        default=None,
        help='limiting biomass (point of full gorwh saturation) [g/m^2], Default: 1300'
    )
    parser.add_argument(
        '--report',
        action='store_true',
        default=True,
        help='generate a graphical report (default: True)'
    )
    parser.add_argument(
        '--output_dir',
        type=str,
        default=str(OUTPUT_DIR),
        help='directory for outputs'
    )

    args = parser.parse_args()
    return args

if __name__ == '__main__':

    args = _parse_arguments()
    main(args)