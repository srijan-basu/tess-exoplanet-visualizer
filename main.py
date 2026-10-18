import argparse
import sys
from src.data_fetcher import fetch_lc
from src.lc_processor import process_lc
import matplotlib.pyplot as plt

def main():

    parser=argparse.ArgumentParser(description="Automated TESS exoplanet detection pipeline")
    parser.add_argument(
        "id", type=int, help="Target TIC id number, Enter only numerics (eg: 100100827)"
    )
    args= parser.parse_args()

    print(f"Fetching lightcurve for TIC {args.id}...")
    try:
        lc_collection = fetch_lc(args.id)

        print(f"Succesfully fetched lightcurve collection")
        print(f"cleaning, applying wotan biweight filtering and stitching lightcurves from all the downloaded sectors")
        stitched_lc=process_lc(lc_collection)

        print(f"Plotting the binned lightcurve after stitching all the sectors")
        stitched_lc.bin(time_bin_size=15/60/24).plot()
        plt.show()
    except Exception as e:
        print(f"Pipeline execution failed: {e}")
        sys.exit(1)

if __name__=="__main__":
    main()