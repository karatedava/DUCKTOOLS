from abc import abstractmethod
from pathlib import Path
import numpy as np
import json

class Simulator():

    def __init__(self, config_path:Path, data_dir:Path, max_w0_budget:int = 1000):
        
        self.parameters = json.load(config_path.open())
        self.data_dir = data_dir

        # default ranges for grid search
        self.HPs = np.arange(1,11,1)
        self.HRs = np.arange(0.1,0.9,0.1)
        self.W0s = np.arange(100,max_w0_budget + 100,100)

        self.lb = self.parameters['limiting_biomass']
        
    def _effective_gr_(self) -> float:
        
        """
        computes effective growth rate
        - initial growth rate scaled by species specific growth const
        """

        r0 = self.parameters['initial_growth_rate']
        growth_const = self.parameters['growth_const']

        eff_gr = r0 * growth_const

        return eff_gr

    @abstractmethod
    def run_single(self, HP, HR, W0) -> float:
        pass

    @abstractmethod
    def run_simulation(self) -> Path:
        pass