import matplotlib.pyplot as plt
import pandas as pd

def print_trends(unique_accident_df):

    # Extract the year from each accident date
    accident_year = unique_accident_df["ACCIDENTDATE"].apply(lambda x: x.split('/')[2])
    unique_accident_df.insert(2, "ACCIDENTYEAR", accident_year)

    # Drop year 2020 because incomplete
    unique_accident_df_2019 = unique_accident_df.drop(unique_accident_df[unique_accident_df.ACCIDENTYEAR == "2020"].index)

    # Create a DF for severe (Death of serious injury) and minor ( minor injury or no injury) accidents trends
    trend_accident = unique_accident_df_2019.groupby(['ACCIDENTYEAR'])['ACCIDENTYEAR'].count()
    trend_accident_severe = unique_accident_df_2019.drop(unique_accident_df_2019[unique_accident_df_2019.SEVERITY >=3 ].index).groupby(['ACCIDENTYEAR'])['ACCIDENTYEAR'].count()
    trend_accident_minor = unique_accident_df_2019.drop(unique_accident_df_2019[unique_accident_df_2019.SEVERITY < 3 ].index).groupby(['ACCIDENTYEAR'])['ACCIDENTYEAR'].count()

    # Plot the trends
    plt.figure(2)
    plt.plot(trend_accident, label='Total Accidents ')
    plt.plot(trend_accident_severe, label='Severe accidents')
    plt.plot(trend_accident_minor, label='Minor accidents')
    plt.legend()
    plt.title("Accident trends on Victoria's roads since 2000")
    plt.xlabel("year")
    plt.ylabel("Number of accidents")

def gather_others(df, number_of_cat):
    # Function to gather all minor categories for the pie chart
    main_df = df.head(number_of_cat).copy()
    others_df = pd.Series([df[5:].copy().sum()])
    return main_df.append(others_df)


def generate_prevention_plots(severe_crash_df, small_crash_df):

    # Accident Type
    plt.figure(4)
    plt.subplot(234)
    grouped_severe_acc = severe_crash_df.groupby(["ACCIDENT_TYPE"])["ACCIDENT_TYPE"].count().sort_values(ascending=False)
    gather_others(grouped_severe_acc, 5).plot(kind='pie', y='count', autopct='%1.1f%%',colormap="summer")
    plt.title("Main types of severe accidents")

    plt.subplot(231)
    grouped_minor_acc = small_crash_df.groupby(["ACCIDENT_TYPE"])["ACCIDENT_TYPE"].count().sort_values(ascending=False)
    gather_others(grouped_minor_acc, 5).plot(kind='pie', y='count', autopct='%1.1f%%',colormap="summer")
    plt.title("Main types of minor accidents")

    # DCA Code
    plt.subplot(235)
    grouped_severe_DCA = severe_crash_df.groupby(["DCA_CODE"])["DCA_CODE"].count().sort_values(ascending=False)
    gather_others(grouped_severe_DCA, 5).plot(kind='pie', y='count',  autopct='%1.1f%%',colormap="summer")
    plt.title("Main DCA code for severe accidents")
    plt.subplot(232)
    grouped_minor_DCA = small_crash_df.groupby(["DCA_CODE"])["DCA_CODE"].count().sort_values(ascending=False)
    gather_others(grouped_minor_DCA, 5).plot(kind='pie', y='count', autopct='%1.1f%%',colormap="summer")
    plt.title("Main DCA code for minor accidents")

    # Light condition: less interest
    plt.subplot(236)
    grouped_severe_lightC = severe_crash_df.groupby(["LIGHT_CONDITION"])["LIGHT_CONDITION"].count().sort_values(ascending=False)
    gather_others(grouped_severe_lightC, 4).plot(kind='pie', y='count', autopct='%1.1f%%',colormap="summer")
    plt.title("Light condition for severe accidents")
    plt.subplot(233)
    grouped_minor_lightC = small_crash_df.groupby(["LIGHT_CONDITION"])["LIGHT_CONDITION"].count().sort_values(ascending=False)
    gather_others(grouped_minor_lightC, 4).plot(kind='pie', y='count', autopct='%1.1f%%',colormap="summer")
    plt.title("Light condition for minor accidents")

    # Road Geometry: less interest
    plt.figure(5)
    plt.subplot(234)
    grouped_severe_roadG = severe_crash_df.groupby(["ROAD_GEOMETRY"])["ROAD_GEOMETRY"].count().sort_values(ascending=False)
    gather_others(grouped_severe_roadG, 4).plot(kind='pie', y='count', autopct='%1.1f%%',colormap="summer")
    plt.title("Road geometry for severe accidents")
    plt.subplot(231)
    grouped_minor_roadG = small_crash_df.groupby(["ROAD_GEOMETRY"])["ROAD_GEOMETRY"].count().sort_values(ascending=False)
    gather_others(grouped_minor_roadG, 4).plot(kind='pie', y='count', autopct='%1.1f%%',colormap="summer")
    plt.title("Road geometry for minor accidents")

    # SEX_cat: less interest
    plt.subplot(235)
    severe_crash_df.groupby(["SEX_cat"])["SEX_cat"].count().sort_values(ascending=False).plot(kind='pie', y='count', autopct='%1.1f%%',colormap="summer")
    plt.title("Gender for severe accidents")
    plt.subplot(232)
    small_crash_df.groupby(["SEX_cat"])["SEX_cat"].count().sort_values(ascending=False).plot(kind='pie', y='count', autopct='%1.1f%%',colormap="summer")
    plt.title("Gender for minor accidents")

    # AGE_GROUP_cat: less interest
    plt.subplot(236)
    grouped_severe_age = severe_crash_df.groupby(["AGE_GROUP_cat"])["AGE_GROUP_cat"].count().sort_values(ascending=False)
    gather_others(grouped_severe_age, 6).plot(kind='pie', y='count', autopct='%1.1f%%',colormap="summer")
    plt.title("Age group for severe accidents")
    plt.subplot(233)
    grouped_minor_age = small_crash_df.groupby(["AGE_GROUP_cat"])["AGE_GROUP_cat"].count().sort_values(ascending=False)
    gather_others(grouped_minor_age, 6).plot(kind='pie', y='count', autopct='%1.1f%%',colormap="summer")
    plt.title("Age group for minor accidents")

    # Speed Zones
    plt.figure(6)
    plt.subplot(223)
    grouped_severe_speed = severe_crash_df.groupby(["SPEED_ZONE"])["SPEED_ZONE"].count().sort_values(ascending=False)
    gather_others(grouped_severe_speed, 6).plot(kind='pie', y='count', autopct='%1.1f%%',colormap="summer")
    plt.title("Speed zone for severe accidents")
    plt.subplot(221)
    grouped_minor_speed = small_crash_df.groupby(["SPEED_ZONE"])["SPEED_ZONE"].count().sort_values(ascending=False)
    gather_others(grouped_minor_speed, 6).plot(kind='pie', y='count', autopct='%1.1f%%',colormap="summer")
    plt.title("Speed zone for minor accidents")

    # vehicle TYpe
    plt.subplot(224)
    grouped_severe_Vtype = severe_crash_df.groupby(["VEHICLE_TYPE"])["VEHICLE_TYPE"].count().sort_values(ascending=False)
    gather_others(grouped_severe_Vtype, 6).plot(kind='pie', y='count', autopct='%1.1f%%',colormap="summer")
    plt.title("Vehicle type in severe accidents")
    plt.subplot(222)
    grouped_minor_Vtype = small_crash_df.groupby(["VEHICLE_TYPE"])["VEHICLE_TYPE"].count().sort_values(ascending=False)
    gather_others(grouped_minor_Vtype, 6).plot(kind='pie', y='count', autopct='%1.1f%%',colormap="summer")
    plt.title("Vehicle type in minor accidents")

    # Vehicle Age
    print("Vehicle age data for severe accidents")
    print(severe_crash_df["VEHICLE_AGE"].describe())
    print("Vehicle age data for minor accidents")
    print(small_crash_df["VEHICLE_AGE"].describe())