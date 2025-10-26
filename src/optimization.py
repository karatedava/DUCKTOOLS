import numpy as np
import pandas as pd
import json
from pathlib import Path
from src.growth_modeler.growth_modeler import GrowthModeler

def load_json_data(filepath:Path):

    with open(filepath, 'r') as f:
        data = json.load(f)
    
    return data

def extract_correct_biomass(df:pd.DataFrame, hp:int):

    bm_values = []
    for bm, time in zip(df['biomass'], df['time']):

        if time % hp == 0:
            bm_values.append(round(bm,3))
    
    return np.array(bm_values)

def optimize(optimdata:Path, configname:Path, lb:float):

    data = load_json_data(optimdata)

    growth_consts = np.arange(0.1,1.0,0.1)
    predicted_growth_const = 0.0

    for run_id, run_params in data.items():

        print(run_id)

        hp = run_params['hp']
        hr = run_params['hr']
        w0 = run_params['data'][0]
        recorder_bm = np.array(run_params['data'][1:])

        cultivation_time = (len(recorder_bm) * hp) - hp
        model = GrowthModeler(cultivation_time, Path('configs/config_superfast.json'), './', lb)

        best_rmse = float('inf')
        best_growth_const = 0.0

        for c in growth_consts:

            model.parameters['growth_const'] = c
            _, bm_df, _ = model.run_single(hp,hr,w0)
            predicted_bm = extract_correct_biomass(bm_df,hp)
            rmse = np.sqrt(np.mean((recorder_bm - predicted_bm) ** 2))

            if rmse < best_rmse:
                best_rmse = rmse
                best_growth_const = c
        
        predicted_growth_const += best_growth_const
    
    predicted_growth_const = predicted_growth_const / len(data)

    # construct and save new config file

    new_config = {

        "integration_step": 0.1,

        "limiting_biomass": lb,
        "initial_growth_rate": 0.323,

        "growth_const": predicted_growth_const
    }

    with open(configname, 'w') as f:
        json.dump(new_config, f, indent=4)






