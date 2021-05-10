from unidecode import unidecode
import jellyfish as jf
import pandas as pd
import numpy as np
import json
import os

from .Features import *


class FeatureManager():
    def __init__(self, tables):
        features = [Bankruptcy,Commitments,Lawsuit,
                    PaymentsHistory,Protest,LastRegistryConsults,
                    RegistryConsults,REFIN,PEFIN,OverdueDebt]
        
        self.final_line = {}
        for f in features:
            self.final_line.update(f().create_feature(tables))


    def get_features(self):
        return self.final_line




