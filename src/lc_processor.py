import lightkurve as lk
import numpy as np
import wotan
import matplotlib.pyplot as plt

def process_lc(lc_collection):
    processed_list=[]
    for lc in lc_collection:
        cleaned_lc=lc.remove_nans().remove_outliers(sigma=3)
        flat_flux, trend = wotan.flatten(cleaned_lc.time.value, cleaned_lc.flux.value, window_length=0.5, return_trend=True, method='biweight')
        processed_lc=cleaned_lc.copy()
        flat_flux_err=cleaned_lc.flux_err.value / trend
        processed_lc['flux']=flat_flux
        processed_lc['flux_err']=flat_flux_err
        processed_list.append(processed_lc)

    return lk.LightCurveCollection(processed_list).stitch()
