import pandas as pd
import numpy as np
from scipy import stats

def preprocessing(data_path):
    # Load Data and concatenate tables from before and after 2005
    accident_df = pd.concat([pd.read_csv(data_path + 'before_2005/ACCIDENT.csv', sep = ',', low_memory = False),pd.read_csv(data_path + 'after_2005/ACCIDENT.csv', sep = ',', low_memory = False)])
    vehicle_df = pd.concat([pd.read_csv(data_path + 'before_2005/VEHICLE.csv', sep = ',', low_memory = False),pd.read_csv(data_path + 'after_2005/VEHICLE.csv', sep = ',', low_memory = False)])
    person_df = pd.concat([pd.read_csv(data_path + 'before_2005/PERSON.csv', sep = ',', low_memory = False),pd.read_csv(data_path + 'after_2005/PERSON.csv', sep = ',', low_memory = False)])
    atmo_df = pd.concat([pd.read_csv(data_path + 'before_2005/ATMOSPHERIC_COND.csv', sep = ',', low_memory = False),pd.read_csv(data_path + 'after_2005/ATMOSPHERIC_COND.csv', sep = ',', low_memory = False)])
    surface_df = pd.concat([pd.read_csv(data_path + 'before_2005/ROAD_SURFACE_COND.csv', sep = ',', low_memory = False),pd.read_csv(data_path + 'after_2005/ROAD_SURFACE_COND.csv', sep = ',', low_memory = False)])

    # Clean Data: Keep only the interesting columns
    cleaned_accident_df = accident_df[['ACCIDENT_NO','ACCIDENTDATE', 'ACCIDENTTIME','ACCIDENT_TYPE','DAY_OF_WEEK','DCA_CODE','LIGHT_CONDITION','NO_OF_VEHICLES','NO_PERSONS','NO_PERSONS_KILLED','ROAD_GEOMETRY','SEVERITY','SPEED_ZONE']]
    cleaned_vehicle_df = vehicle_df[['ACCIDENT_NO','VEHICLE_ID', 'VEHICLE_YEAR_MANUF','ROAD_SURFACE_TYPE','VEHICLE_BODY_STYLE','VEHICLE_TYPE','TRAFFIC_CONTROL']]
    cleaned_person_df = person_df[['ACCIDENT_NO','PERSON_ID', 'VEHICLE_ID','SEX','AGE','Age Group','INJ_LEVEL','ROAD_USER_TYPE']]
    cleaned_atmo_df = atmo_df[['ACCIDENT_NO','ATMOSPH_COND']]
    cleaned_surface_df = surface_df[['ACCIDENT_NO','SURFACE_COND']]

    # Before pre-processing : print Histogram to spot weird/missing values
    #cleaned_accident_df.hist(color="g")

    # Remove unwanted/unknown data
    cleaned_accident_df = cleaned_accident_df.drop(cleaned_accident_df[cleaned_accident_df.ACCIDENT_TYPE == 9].index)       # Unknown accident type
    cleaned_accident_df = cleaned_accident_df.drop(cleaned_accident_df[cleaned_accident_df.ROAD_GEOMETRY == 9].index)       # Unknown Road Geometry
    cleaned_accident_df = cleaned_accident_df.drop(cleaned_accident_df[cleaned_accident_df.LIGHT_CONDITION == 9].index)     # Unknown Light Condition
    cleaned_accident_df = cleaned_accident_df.drop(cleaned_accident_df[cleaned_accident_df.SPEED_ZONE >= 776].index)        # Unknown or particular speed zones
    cleaned_accident_df = cleaned_accident_df.drop(cleaned_accident_df[cleaned_accident_df.DAY_OF_WEEK == 0].index)         # False value
    cleaned_accident_df = cleaned_accident_df[(np.abs(stats.zscore(cleaned_accident_df["NO_PERSONS"])) < 4)]                # Remove outliers (Case with a lot of people involved)

    cleaned_atmo_df = cleaned_atmo_df.drop(cleaned_atmo_df[cleaned_atmo_df.ATMOSPH_COND == 9].index)                        # Unknown Atmos. Condition
    cleaned_surface_df = cleaned_surface_df.drop(cleaned_surface_df[cleaned_surface_df.SURFACE_COND == 9].index)            # Unknown Surface Condition

    cleaned_person_df = cleaned_person_df.drop(cleaned_person_df[cleaned_person_df.SEX == "U"].index)                       # Unknown gender
    cleaned_person_df = cleaned_person_df.drop(cleaned_person_df[cleaned_person_df["Age Group"] == "unknown"].index)        # Unknown Age Group
    cleaned_person_df = cleaned_person_df.drop(cleaned_person_df[cleaned_person_df["ROAD_USER_TYPE"] == 9].index)           # Unknown Road User Type
    cleaned_person_df = cleaned_person_df[cleaned_person_df["ROAD_USER_TYPE"].notna()]                                      # Remove missing values

    cleaned_vehicle_df = cleaned_vehicle_df.drop(cleaned_vehicle_df[cleaned_vehicle_df["VEHICLE_YEAR_MANUF"] < 1882].index) # Remove invalid year
    cleaned_vehicle_df = cleaned_vehicle_df.drop(cleaned_vehicle_df[cleaned_vehicle_df["VEHICLE_YEAR_MANUF"] > 2020].index) # Remove invalid year
    cleaned_vehicle_df = cleaned_vehicle_df.drop(cleaned_vehicle_df[cleaned_vehicle_df["ROAD_SURFACE_TYPE"] == 9].index)    # Unknown Surface Type
    cleaned_vehicle_df = cleaned_vehicle_df.drop(cleaned_vehicle_df[cleaned_vehicle_df["VEHICLE_TYPE"] == 99].index)        # Unknown Vehicle type
    cleaned_vehicle_df = cleaned_vehicle_df.dropna()                                                                        # Drop Missing values

    # After Cleaning : No more inconsistent data
    cleaned_accident_df.hist(color='g')

    # Create a per person accident table, keeping only the drivers and its vehicle info
    cleaned_person_df['ROAD_USER_TYPE'] = cleaned_person_df['ROAD_USER_TYPE'].astype(int)
    drivers_df = cleaned_person_df[cleaned_person_df["ROAD_USER_TYPE"].isin([2,4,6,7])]
    drivers_joined_df = drivers_df.merge(cleaned_vehicle_df, on=['ACCIDENT_NO','VEHICLE_ID'], how="left").drop(["PERSON_ID","VEHICLE_ID"], axis=1)

    # Merge data with accidents and surface/atmo conditions
    accident_df_joined = cleaned_accident_df.merge(cleaned_surface_df.drop_duplicates(subset="ACCIDENT_NO"), on=['ACCIDENT_NO'], how="inner")
    accident_df_joined = accident_df_joined.merge(cleaned_atmo_df.drop_duplicates(subset="ACCIDENT_NO"), on=['ACCIDENT_NO'], how="inner")
    accident_df_joined = accident_df_joined.merge(drivers_joined_df.drop(["AGE"], axis=1), on=['ACCIDENT_NO'], how="inner")

    # 2 Accident dataframes:
    unique_accident_df = cleaned_accident_df    # 1 row per accident
    joined_accident_df = accident_df_joined     # 1 row per driver involved (with residual NaN data)

    return unique_accident_df, joined_accident_df