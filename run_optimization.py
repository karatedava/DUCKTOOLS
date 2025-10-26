from pathlib import Path
import argparse

from src.optimization import optimize

from src.config import OPTIM_DATA_PATH, CONFIG_FOLDER, DEFAULT_LB

def main(args):

    data_file = Path(OPTIM_DATA_PATH / args.optimfile)
    if not data_file.is_file():
        raise FileNotFoundError(f"Config file {data_file} does not exist.")
    
    configname = args.configname
    if configname is None:
        raise FileNotFoundError(f"you need to provide config name via --configname flag")

    lb = args.lb

    print(data_file)
    print(CONFIG_FOLDER / configname)
    
    optimize(
        optimdata=data_file,
        configname=CONFIG_FOLDER / configname,
        lb=lb
    )

def _parse_arguments():

    parser = argparse.ArgumentParser()

    parser.add_argument(
        '--optimfile',
        type=str,
        default=None,
        help='name of file with measured data in the optimization data folder'
    )

    parser.add_argument(
        '--configname',
        type=str,
        default=None,
        help='name for new configuration file'
    )

    parser.add_argument(
        '--lb',
        type=float,
        default=DEFAULT_LB,
        help='limiting biomass (point of full gorwh saturation) [g/m^2], Default: 1300'
    )

    args = parser.parse_args()
    return args

if __name__ == '__main__':

    args = _parse_arguments()
    main(args)