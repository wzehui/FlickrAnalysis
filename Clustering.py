## How to do DBSCAN based Clustering in Python
def Snippet_159():
    print()
    print(format('How to do DBSCAN based Clustering in Python','*^82'))

    import warnings
    warnings.filterwarnings("ignore")

    # load libraries
    from sklearn import datasets
    from sklearn.preprocessing import StandardScaler
    from sklearn.cluster import DBSCAN
    import pandas as pd
    #import seaborn as sns
    import matplotlib.pyplot as plt

    # Load data
    iris = datasets.load_iris()
    X = iris.data; data = pd.DataFrame(X)
    cor = data.corr()

    #fig = plt.figure(figsize=(10,10))
    #sns.heatmap(cor, square = True); plt.show()

    # Standarize features
    scaler = StandardScaler()
    X_std = scaler.fit_transform(X)

    # Conduct DBSCAN Clustering
    clt = DBSCAN()

    # Train model
    model = clt.fit(X_std)

    # Predict clusters
    clusters = pd.DataFrame(model.fit_predict(X_std))
    data['Cluster'] = clusters

    # Visualise cluster membership
    fig = plt.figure(figsize=(10,10)); ax = fig.add_subplot(111)
    scatter = ax.scatter(data[0],data[1], c=data['Cluster'],s=50)
    ax.set_title('DBSCAN Clustering')
    ax.set_xlabel('X0'); ax.set_ylabel('X1')
    plt.colorbar(scatter); plt.show()

Snippet_159()