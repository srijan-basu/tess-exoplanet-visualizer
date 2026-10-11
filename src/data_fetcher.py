import lightkurve as lk
import matplotlib.pyplot as plt

def fetch_lc(id: int):
    target_id= f"TIC {id}"

    search_lc=lk.search_lightcurve(target_id, author="SPOC")
    if len(search_lc)>0:
        print(f"Pre-computed lightcurves found.\nReturning stictched lightcurves from {len(search_lc)} sectors...")
        return search_lc.download_all().stitch(corrector_func= lambda x:x.remove_nans().remove_outliers().normalize().flatten())
    
    print(f"No pre-computed lightcurve for {target_id} found.\nChecking FFI availability...")
    search_ffi=lk.search_tesscut(target_id)
    if len(search_ffi)>0:
        print(f"FFIs from {len(search_ffi)} sectors found.\nGenerating lightcurves from these FFIs")

        lc_list=[]
        ffi_collection= search_ffi.download_all(cutout_size=11)
        for ffi in ffi_collection:
            mask=ffi.create_threshold_mask(threshold=5,reference_pixel='center')
            lc_list.append(ffi.to_lightcurve(aperture_mask=mask))

        lc_collection=lk.LightCurveCollection(lc_list)
        return lc_collection.stitch(corrector_func= lambda x:x.remove_nans().remove_outliers().normalize().flatten())
