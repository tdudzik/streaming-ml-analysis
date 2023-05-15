import pandas as pd
def prepare_dataset():
    pd.options.display.max_columns = 100
    df = pd.read_csv("kickstarter_projects.csv")

    # drop unneeded
    df = df.drop(columns=['ID', 'Name', 'Pledged'])
    # map y variable
    df['State'] = df['State'].map(lambda x: 1 if x == 'Successful' else 0)

    # get days
    df['Launched'] = df['Launched'].str.split(' ').str[0]
    df['Launched'] = pd.to_datetime(df['Launched'], format='mixed')
    df['Deadline'] = pd.to_datetime(df['Deadline'], format='mixed')
    df['Days'] = (df['Deadline'] - df['Launched']).dt.days
    df = df.drop(columns=['Launched', 'Deadline'])

    # et dummy variables
    cats = pd.get_dummies(df.Category, prefix='Category')
    for cat in cats.columns:
        cats[cat] = cats[cat].map(lambda x: 1 if x == True else 0)

    conts = pd.get_dummies(df.Country, prefix='Country')
    for cont in conts.columns:
        conts[cont] = conts[cont].map(lambda x: 1 if x == True else 0)

    subs = pd.get_dummies(df.Subcategory, prefix='Subcategory')
    for sub in subs.columns:
        subs[sub] = subs[sub].map(lambda x: 1 if x == True else 0)

    df = df.drop(columns=['Category', 'Country', 'Subcategory'])
    df = df.join(cats)
    df = df.join(conts)
    df = df.join(subs)

    # save prepared dataset
    df.to_csv("dataset.csv", index=False)

def test_model():
    from sklearn.preprocessing import StandardScaler
    from sklearn.model_selection import train_test_split

    prepare_dataset()
    df = pd.read_csv("dataset.csv")

    print("preparing...")
    scaler = StandardScaler()
    df[['Goal', 'Days', 'Backers']] = scaler.fit_transform(df[['Goal', 'Days', 'Backers']])
    dfx = df.drop(columns=['State'])

    from sklearn.decomposition import PCA
    from sklearn.linear_model import LogisticRegression
    from sklearn.metrics import accuracy_score
    from sklearn.neural_network import MLPClassifier
    import warnings

    warnings.filterwarnings('ignore')

    # pca = PCA(n_components=100)
    # dfx = pca.fit_transform(dfx)
    X_train, X_test, y_train, y_test = train_test_split(dfx, df[['State']],
                                                        test_size=0.3, random_state=7)
    print("initializing model...")
    model = LogisticRegression(verbose=True)
    model.fit(X_train, y_train)
    print(accuracy_score(y_train, model.predict(X_train)))
    print(accuracy_score(y_test, model.predict(X_test)))

    # model = MLPClassifier(hidden_layer_sizes=(10, 5),
    #                       random_state=1,
    #                       warm_start=True,
    #                       solver='sgd',
    #                       learning_rate='adaptive',
    #                       learning_rate_init=0.1)
    # for epoch in range(100):
    #     model.fit(X_train, y_train)
    #     print(epoch + 1 )
    #     print(accuracy_score(y_train, model.predict(X_train)))
    #     print(accuracy_score(y_test, model.predict(X_test)))

    # model = SVC(verbose=True)
    # print("fitting...")


if __name__ == '__main__':
    prepare_dataset()
    # test_model()

