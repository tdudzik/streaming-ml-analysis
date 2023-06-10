import dask.dataframe as dd
from dask.distributed import Client
from dask_ml.linear_model import LogisticRegression
from dask_ml.preprocessing import StandardScaler
from joblib import load
import pandas as pd


def prepare_dataset(df: pd.DataFrame, model_categories: list[str]) -> pd.DataFrame:
    # Drop irrelevant columns
    df = df.drop(columns=['ID', 'Name', 'Pledged', 'State'])

    # Extract date from 'Launched' column and convert it into datetime format
    df['Launched'] = df['Launched'].str.split(' ').str[0]
    df['Launched'] = pd.to_datetime(df['Launched'], format='%Y-%m-%d')

    # Convert 'Deadline' column into datetime format
    df['Deadline'] = pd.to_datetime(df['Deadline'], format='%Y-%m-%d')

    # Calculate the number of days between launch and deadline
    df['Days'] = (df['Deadline'] - df['Launched']).dt.days

    # Drop the 'Launched' and 'Deadline' columns as we now have 'Days' column
    df = df.drop(columns=['Launched', 'Deadline'])

    # Perform one-hot encoding on the 'Category' column
    cats = pd.get_dummies(df.Category, prefix='Category')

    # Convert boolean values to 1s and 0s
    for cat in cats.columns:
        cats[cat] = cats[cat].map(lambda x: 1 if x == True else 0)

    # Add missing categories as columns with 0s
    for model_category in model_categories:
        if model_category not in cats.columns:
            df[model_category] = 0

    # Drop the original 'Category', 'Country', and 'Subcategory' columns
    df = df.drop(columns=['Category', 'Country', 'Subcategory'])

    # Convert 'Goal', 'Days', and 'Backers' columns to float
    for column in ['Goal', 'Days', 'Backers']:
        df[column] = df[column].astype(float)

    # Join the original dataframe with the one-hot encoded categories dataframe
    df = pd.concat([df, cats], axis=1)
    return df


def run(model: LogisticRegression, scaler: StandardScaler, model_categories: list[str], input: pd.DataFrame) -> bool:
    prepared_input = prepare_dataset(input, model_categories)
    client = Client()
    dd_input = dd.from_pandas(prepared_input, npartitions=2)
    dd_input[['Goal', 'Days', 'Backers']] = scaler.transform(
        dd_input[['Goal', 'Days', 'Backers']])
    dd_input = dd_input.to_dask_array(lengths=True)
    predicted = model.predict(dd_input)
    client.shutdown()

    return bool(predicted.compute()[0])
