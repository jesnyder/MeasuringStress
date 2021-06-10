
from c0100_clean_data import clean_data
from c0119_compile_formatted import compile_formatted
from c0200_plot_clean import plot_cleaned
from c0300_analyze_records import analyze_records
from c0400_analyze_regression import analyze_regression
from c0500_count_inflections import count_inflections

from c8000_openscad_modeling import openscad_modeling
from c9000_make_report import make_report


def main():
    """
    each study is assigned a 2-3 letter code
    each study has a folder named with a 2-3 letter code
    inside each folder is the source data
    the source data are folder downloaded from the cloud client

    this program analyzes the data from:
    Step 1: Cleaning the source data
    Step 2: Check data quality using plots
    Step 3: Statistical analysis
    Step 4: Regression analysis
    Step 5: Count inflections
    Step 6: Machine learning
    Step 7: Prepare documentation
    Step 8: Build 3D models

    The final deliverable is a comprehnesive latex report
    and 3D models.
    """

    print("running main")

    # list paths to all the original data
    print("Step 1: Cleaning the source data.")
    clean_data()
    # compile_formatted()
    print("complete.")

    print("Step 2: Check data quality using plots")
    # plot_cleaned()

    print("Step 3: Statistical analysis")
    analyze_records()

    print("Step 4: Regression analysis")
    analyze_regression()

    print("Step 5: Count inflections")
    # count_inflections()


    print("Step 6: Machine learning")


    print("Step 7: Documentation")
    make_report()

    print("Step 8: Build 3D models")
    openscad_modeling()

    print("completed main")


if __name__ == "__main__":
    main()
