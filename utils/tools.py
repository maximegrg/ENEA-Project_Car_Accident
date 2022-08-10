import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from sklearn.feature_selection import chi2
from sklearn.linear_model import LogisticRegression

def Chi2_test(joined_regression_df):

    joined_regression_df_test = joined_regression_df.drop(["ACCIDENT_NO","SEX","Age Group"], axis=1).dropna()

    # Correlation Matrix, not wise for categorical values
    # sns.heatmap(joined_regression_df.corr(),annot=True,lw=1)

    # Chi2 test
    chi2_df = pd.DataFrame(data=[(0 for i in range(len(joined_regression_df_test.columns))) for i in range(len(joined_regression_df_test.columns))], columns=list(joined_regression_df_test.columns))
    chi2_df.set_index(pd.Index(list(joined_regression_df_test.columns)), inplace = True)

    # Finding p_value for all columns and putting them in the resultant matrix
    for i in list(joined_regression_df_test.columns):
        for j in list(joined_regression_df_test.columns):
            if i != j:
                chi2_value, p_value = chi2(np.array(joined_regression_df_test[i]).reshape(-1, 1), np.array(joined_regression_df_test[j]).reshape(-1, 1))
                chi2_df.loc[i,j] = p_value

    # Plotting a heatmap
    plt.figure(3)
    sns.heatmap(chi2_df, annot=True, cmap='Blues')
    plt.title('Chi2 Test Results')

def logistic_regression(joined_regression_df):
    # One hot encoder
    X = pd.get_dummies(data=joined_regression_df, columns=["ACCIDENT_TYPE","DAY_OF_WEEK","DCA_CODE","LIGHT_CONDITION","ROAD_GEOMETRY","SPEED_ZONE","SEX", "Age Group", "VEHICLE_AGE","ROAD_SURFACE_TYPE","VEHICLE_TYPE","SURFACE_COND","ATMOSPH_COND"], drop_first=False)
    X = X.drop(["ACCIDENT_NO","SEVERITY"], axis=1)
    Y = joined_regression_df["SEVERITY"]

    # Regression
    model = LogisticRegression(class_weight="'balanced")

    model.fit(X,Y)