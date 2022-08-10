import matplotlib.pyplot as plt
import argparse
from utils.preprocess import preprocessing
from utils.tools import Chi2_test, logistic_regression
from utils.visualize import print_trends, generate_prevention_plots


def main():

    parser = argparse.ArgumentParser(description="Victoria Accident analysis")
    parser.add_argument("--data_path", type=str, default='data/raw/', help="path to raw data (Default : data/raw)")
    args = parser.parse_args()

    # Preprocess data and print trends over the last few years
    unique_accident_df, joined_accident_df = preprocessing(args.data_path)
    print_trends(unique_accident_df)


    ## Keep Values after 2017

    joined_accident_year_df = joined_accident_df["ACCIDENTDATE"].apply(lambda x: x.split('/')[2])
    joined_accident_df.insert(2, "ACCIDENTYEAR", joined_accident_year_df)
    # For both table, keep values from 2017
    unique_accident_df['ACCIDENTYEAR'] = unique_accident_df['ACCIDENTYEAR'].astype(int)
    unique_accident_from_2017 = unique_accident_df[unique_accident_df['ACCIDENTYEAR'] >=2017]
    joined_accident_df['ACCIDENTYEAR'] = joined_accident_df['ACCIDENTYEAR'].astype(int)
    joined_accident_from_2017 = joined_accident_df[joined_accident_df['ACCIDENTYEAR'] >=2017]

    # Compute and add the age of vehicle
    vehicle_age_df = joined_accident_from_2017["ACCIDENTYEAR"]-joined_accident_from_2017["VEHICLE_YEAR_MANUF"]
    joined_accident_from_2017.insert(13, "VEHICLE_AGE", vehicle_age_df)
    joined_accident_from_2017 = joined_accident_from_2017.drop(joined_accident_from_2017[joined_accident_from_2017["VEHICLE_AGE"] < 0].index)



    ## Prepare tables for covariance & chi2 test
    # Severety is denoted as 1 if there was a death or serious injury, 0 instead
    unique_regression_df = unique_accident_from_2017[["ACCIDENT_NO", "ACCIDENT_TYPE", "DAY_OF_WEEK", "DCA_CODE", "LIGHT_CONDITION","ROAD_GEOMETRY", "SPEED_ZONE" ,"SEVERITY"]]
    unique_regression_df["SEVERITY"] = unique_regression_df["SEVERITY"].apply(lambda x: 0 if x >= 3 else 1)
    joined_regression_df = joined_accident_from_2017[["ACCIDENT_NO", "ACCIDENT_TYPE", "DAY_OF_WEEK", "DCA_CODE", "LIGHT_CONDITION","ROAD_GEOMETRY", "SPEED_ZONE" ,"SEVERITY","SEX", "Age Group", "ROAD_SURFACE_TYPE","VEHICLE_TYPE","VEHICLE_AGE","SURFACE_COND","ATMOSPH_COND"]]
    joined_regression_df["SEVERITY"] = joined_regression_df["SEVERITY"].apply(lambda x: 0 if x >= 3 else 1)

    # Encode gender and Age categories
    joined_regression_df["SEX_cat"] = joined_regression_df["SEX"].astype('category').cat.codes
    joined_regression_df["AGE_GROUP_cat"] = joined_regression_df["Age Group"].astype('category').cat.codes


    # Perform Chi2 test
    Chi2_test(joined_regression_df)

    # Perform Logistic regression: not currently working
    #logistic_regression(joined_accident_df)

    # Separate severe and minor crash for further analysis, using the identified discriminant features
    severe_crash_df = joined_regression_df[joined_regression_df["SEVERITY"] ==1] #19000
    small_crash_df = joined_regression_df[joined_regression_df["SEVERITY"] ==0]  #45000

    generate_prevention_plots(severe_crash_df, small_crash_df)
    plt.show()


if __name__ == '__main__':
    main()