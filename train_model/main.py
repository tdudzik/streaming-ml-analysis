import dask.dataframe as dd
from dask.distributed import Client
from dask_ml.preprocessing import StandardScaler
from dask_ml.model_selection import train_test_split
from dask_ml.linear_model import LogisticRegression
# from dask_ml.metrics import
from sklearn.metrics import roc_auc_score, accuracy_score, log_loss, mean_absolute_error, mean_squared_error
from config import logger
import pickle


def train_model():
    df = dd.read_csv("dataset.csv")

    scaler = StandardScaler()
    df[['Goal', 'Days', 'Backers']] = scaler.fit_transform(
        df[['Goal', 'Days', 'Backers']])
    scaler_filename = "scaler.dml"
    pickle.dump(scaler, open(scaler_filename, 'wb'))
    print("Saved scaler to: " + scaler_filename)

    X_train, X_test, y_train, y_test = train_test_split(df.drop(columns=['State']),
                                                        df[['State']],
                                                        test_size=0.3,
                                                        random_state=7,
                                                        shuffle=True)
    X_train, X_test, y_train, y_test = X_train.to_dask_array(lengths=True), \
        X_test.to_dask_array(lengths=True), \
        y_train.to_dask_array(lengths=True), \
        y_test.to_dask_array(lengths=True)

    model = LogisticRegression(verbose=True)
    model.fit(X_train, y_train)
    train_predictions = model.predict(X_train)
    predicted = model.predict(X_test)

    results = {"acc_train": accuracy_score(y_train, train_predictions),
               "acc_test": accuracy_score(y_test, predicted),
               "log_loss": log_loss(y_test, predicted),
               "roc_auc": roc_auc_score(y_test, predicted),
               "mae": mean_absolute_error(y_test, predicted),
               "rmse": mean_squared_error(y_test, predicted, squared=False)}

    print("Train accuracy:")
    print(results["acc_train"])
    print("Test metrics:")
    print("Accuracy:")
    print(results["acc_test"])
    print("Log loss:")
    print(results["log_loss"])
    print("AUC ROC (Area Under the Receiver Operating Characteristic Curve):")
    print(results["roc_auc"])
    print("Mean absolute error:")
    print(results["mae"])
    print("Root mean squared error:")
    print(results["rmse"])

    print("saving model...")
    model_filename = "model_LogisticRegression.dml"
    pickle.dump(model, open(model_filename, 'wb'))
    print("Saved to: " + model_filename)


if __name__ == '__main__':
    client = Client()

    train_model()

    client.shutdown()
