from Services.dayService import DayService
from Services.summaryService import SummaryService
from Services.analysisService import AnalysisService
from tqdm import tqdm
import threading
import pandas as pd
import numpy as np

if __name__ == "__main__":
    SummaryService.Update()
    DayService.Update()
    AnalysisService.Update(6)
    
