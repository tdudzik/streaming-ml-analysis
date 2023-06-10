import dask.dataframe as dd
import joblib
import pandas as pd
import json
from config import logger
from dask.distributed import Client
from dask_ml.preprocessing import StandardScaler
from dask_ml.model_selection import train_test_split
from dask_ml.linear_model import LogisticRegression
from sklearn.metrics import roc_auc_score, accuracy_score, log_loss, mean_absolute_error, mean_squared_error


def prepare_dataset(dataset_path: str) -> tuple[pd.DataFrame, list[str]]:
    # Read the dataset from a CSV file
    df = pd.read_csv(dataset_path)

    # Drop irrelevant columns
    df = df.drop(columns=['ID', 'Name', 'Pledged'])

    # Convert the 'State' column into a binary format
    df['State'] = df['State'].map(lambda x: 1 if x == 'Successful' else 0)

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

    model_categories = [col for col in cats.columns]

    # Convert boolean values to 1s and 0s
    for cat in cats.columns:
        cats[cat] = cats[cat].map(lambda x: 1 if x == True else 0)

    # Drop the original 'Category', 'Country', and 'Subcategory' columns
    df = df.drop(columns=['Category', 'Country', 'Subcategory'])

    # Join the original dataframe with the one-hot encoded categories dataframe
    df = df.join(cats)
    return df, model_categories


def train_model(df: dd.DataFrame) -> tuple[LogisticRegression, StandardScaler, dict]:
    # Initialize a scaler and scale numeric columns
    scaler = StandardScaler()
    df[['Goal', 'Days', 'Backers']] = scaler.fit_transform(
        df[['Goal', 'Days', 'Backers']])

    # Split the dataset into train and test sets
    X_train, X_test, y_train, y_test = train_test_split(
        df.drop(columns=['State']),
        df[['State']],
        test_size=0.3,
        random_state=7,
        shuffle=True
    )

    # Convert Dask DataFrames to Dask arrays
    X_train, X_test = X_train.to_dask_array(
        lengths=True), X_test.to_dask_array(lengths=True)
    y_train, y_test = y_train.to_dask_array(
        lengths=True), y_test.to_dask_array(lengths=True)

    # Train a Logistic Regression model
    model = LogisticRegression(verbose=True)
    model.fit(X_train, y_train)

    # Make predictions on the train and test sets
    train_predictions = model.predict(X_train)
    predicted = model.predict(X_test)

    # Calculate and store performance metrics
    metrics = {
        "acc_train": accuracy_score(y_train, train_predictions),
        "acc_test": accuracy_score(y_test, predicted),
        "log_loss": log_loss(y_test, predicted),
        "roc_auc": roc_auc_score(y_test, predicted),
        "mae": mean_absolute_error(y_test, predicted),
        "rmse": mean_squared_error(y_test, predicted, squared=False)
    }

    return model, scaler, metrics


def run(training_id: str, dataset_uri: str) -> dict:
    prepared_df, model_categories = prepare_dataset(dataset_uri)
    print("example: " +
          str(json.loads(prepared_df.to_json(orient='records'))[0]))
    client = Client()
    df = dd.from_pandas(prepared_df, npartitions=2)
    model, scaler, metrics = train_model(df)
    joblib.dump(model, f'./model/{training_id}.joblib')
    joblib.dump(scaler, f'./model/{training_id}.scaler.joblib')
    with open(f'./model/{training_id}.categories.json', 'w') as f:
        json.dump(model_categories, f)
    client.shutdown()
    return metrics


if __name__ == '__main__':
    metrics = run('test', '../datasets/kickstarter_100.csv')
    logger.info('metrics: ' + str(metrics))
