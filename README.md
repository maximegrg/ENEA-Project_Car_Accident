﻿# Accident Analysis for Victoria's government

This is a gentle analysis of the CrashStats dataset published by VicRoads

## Installation

Data should be placed in data/raw, or run main.py with data_path argument

## Code description
This includes:
  - Data preprocessing
  - Data corrections (removal of missing values, edge cases identification using z-score)
  - Data overview before and after corrections
  - Trend analysis
  - Determination of the determinant features that influence the severity of an accident using the Chi2 test
  - Pie chart visualization of results

Posible future evolutions
  - Using clustering methods on accident localisations to locate epicentres
  - Logistic regression to regress missing values and understand the importance of each features regarding another
  - Removal of outliers
