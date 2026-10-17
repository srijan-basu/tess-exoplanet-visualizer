import lightkurve as lk
import numpy as np

def fetch_lc(id: int):
    target_id= f"TIC {id}"

    #searching for pre-computed lc
    search_lc=lk.search_lightcurve(target_id, author="SPOC")
    if len(search_lc)>0:                                                
        print(f"Pre-computed lightcurves from {len(search_lc)} sectors have been found")
        return search_lc.download_all()
    
    print(f"No pre-computed lightcurve for {target_id} found.\nChecking FFI availability...")

    #searching for ffis to convert to lc
    search_ffi=lk.search_tesscut(target_id)
    if len(search_ffi)>0:                                                 
        print(f"FFIs from {len(search_ffi)} sectors found.\nGenerating lightcurves from these FFIs...")

        lc_list=[]
        ffi_collection= search_ffi.download_all(cutout_size=11)
        for ffi in ffi_collection:
            #creating threshold mask
            mask=ffi.create_threshold_mask(threshold=10,reference_pixel='center')
            raw_lc=ffi.to_lightcurve(aperture_mask=mask)

            #applying regression correction
            regressors=ffi.flux[:, ~mask]
            dm=lk.DesignMatrix(regressors, name='regressors').pca(5).append_constant()
            rc=lk.RegressionCorrector(raw_lc)
            _=rc.correct(dm)
            corrected_lc=raw_lc - rc.model_lc + np.percentile(rc.model_lc.flux, 5)

            lc_list.append(corrected_lc)

        lc_collection=lk.LightCurveCollection(lc_list)
        return lc_collection