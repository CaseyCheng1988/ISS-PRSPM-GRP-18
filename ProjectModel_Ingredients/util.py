from matplotlib import pyplot as plt
import numpy as np
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import style
import seaborn as sns
import pandas as pd
from factor_analyzer import FactorAnalyzer, calculate_bartlett_sphericity
from factor_analyzer.factor_analyzer import calculate_kmo
import random

from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
'''
Generate an array of binary entries
:param integer n_row: The row dimension of the array, representing the sample size
:param integer n_col: The column dimension of the array, representing the feature size
:param bool single: If set to True, only one entry of each row will be 1 (default False)
:param bool seed: Whether to use a specific random seed value
:param int seed_val: Random seed value

:return: the binary array
:raises ValueError: if seed is set to True but no seed_val is passed.
'''

def _generate_binary_samples(n_row, n_col, single=False, seed=False,
                             seed_val=None):
    if seed==True:
        if seed_val is None:
            raise ValueError("Specify seed_val when setting seed as True.")
        else:
            np.random.seed(seed_val)

    if single==False:
        return np.random.randint(2, size=(n_row, n_col))
    else:
        output = np.zeros(shape=(n_row, n_col))
        for row in range(n_row):
            non_zero_col = np.random.randint(n_col, size=(1))
            output[row, non_zero_col] = 1
        return output

'''
Plot the histogram for all features of the data,
as well as option to save the histogram
:param pandas_dataframe df: The dataframe of data
:param bool save: Whether to save the final histogram or not (default False)

:return: plot the histogram of the data
'''
def _plot_histogram(df, save=False):
    plt.style.use('default')
    axes = df.hist(color='green', grid=True, figsize=(14,14))

    fig = axes[0][0].get_figure()
    fig.tight_layout()
    if save:
        fig.savefig('histogram.png')
    plt.show()

'''
Plot the correlation heatmap of the dataset
:param pandas_dataframe df: The dataframe of data
:param bool save: Whether to save the final heatmap or not (default False)

:return: plot the correlation heat map of the data
'''
def _plot_correlation(df, save=False):
    corr_mat = df.corr().values # compute the correlation matrix

    # convert the correlation matrix to dataframe structure
    corr_df = pd.DataFrame(np.round(corr_mat, 2),
                           index=df.columns,
                           columns=df.columns)

    # plot the heatmap
    fig = plt.figure(figsize=(15,15))
    ax = fig.add_subplot(111)
    sns.set(font_scale=1.3)
    sns.heatmap(corr_df, linewidth=1, ax=ax, square=True, annot=True)
    ax.set_title('Heat map of correlation matrix \n',
                 fontsize=20, weight='bold')

    # save figure
    if save:
        fig.savefig('correlation.fig')

'''
Plot the explained variance of the PC's (scree plot)
:param numpy_1D_array eigenvalues: 1D array of all the eigenvalues 
:param bool save: Whether to save the final scree plot

:return: plot the scree plot that demonstrates the explained variance of the PC's
'''
def _plot_scree(eigenvalues, save=False):
    # set up PC labels
    PC = []
    for i in range(len(eigenvalues)):
        PC.append(i+1)

    # convert absolute to relative percentage explained variance
    eigenvalues = eigenvalues / sum(eigenvalues)
    eigenvalues = 100 * eigenvalues

    # plot eigenvalues against the PC
    plt.style.use('classic')
    fig = plt.figure(figsize=(12,12))
    ax = fig.add_subplot(111)
    ax.plot(PC, eigenvalues, 'b-o', label='explained variance')
    ax.legend(loc='best')
    ax.set_xlabel('PC')
    ax.set_ylabel('explained variance (%)')
    ax.set_xlim(0, len(eigenvalues)+1)
    ax.set_ylim(np.floor(min(eigenvalues))-1, np.ceil(max(eigenvalues))+1)
    ax.set_title('Scree Plot \n', fontsize=20, weight='bold')
    ax.grid(True)

    if save:
        fig.savefig('scree.png')

    # revert to default style and show plot
    plt.style.use('default')
    plt.show()

'''
Plot the cumulative explained variance for the PC's
:param numpy_1D_array eigenvalues: 1D numpy array of the eigenvalues
:param bool save: whether to save the final plot or not

:return: plot the cumulative explained variance for various PC's
'''
def _plot_pareto(eigenvalues, save=False):
    # find cumulative explained variances
    cum_eigenvalues = [sum(eigenvalues[0:i]) for i in range(1, len(eigenvalues)+1)]

    # find relative cumulative explained variances in percentage
    cum_eigenvalues = cum_eigenvalues / cum_eigenvalues[-1]
    cum_eigenvalues = np.round(cum_eigenvalues*100, 2)

    # set up PC labels
    PC = []
    for i in range(len(eigenvalues)):
        PC.append(i+1)

    # plot relative cumulative explained variances against the PC
    plt.style.use('classic')
    fig = plt.figure(figsize=(12,12))
    ax = fig.add_subplot(111)
    ax.plot(PC, cum_eigenvalues, 'b-o', label='cumulative variance')
    ax.legend(loc='best')
    ax.set_xlabel('PC')
    ax.set_ylabel('relative cumulative explained variance (%)')
    ax.grid(True)
    ax.set_xlim([0, len(eigenvalues)+1])
    ax.set_ylim([np.floor(min(cum_eigenvalues))-1, 102])
    ax.set_title('Pareto Chart \n', fontsize=20, weight='bold')

    # revert to default style
    plt.style.use('default')

    # save figure
    if save:
        fig.savefig('pareto.png')

    plt.show()

'''
Plot the PCA-transformed dataset for the two specified PC's
:param numpy_array transformed: the dataset expressed with PC's
:param int PC_no_1: the number of the first required PC
:param int PC_no_2: the number of the second required PC
:param bool save: whether to save the final plot or not

:return: plot the dataset in terms of the two required PC's
'''
def _plot_score(transformed, PC_no_1, PC_no_2, save=False):
    plt.style.use('classic')
    fig = plt.figure(figsize=(12,12))
    ax = fig.add_subplot(111)
    ax.set_title('Score plot for PC {} against PC {}'.format(PC_no_2, PC_no_1),
                 fontsize=20, weight='bold')
    ax.set_xlabel('PC ' + str(PC_no_1), fontsize=16, weight='bold')
    ax.set_ylabel('PC ' + str(PC_no_2), fontsize=16, weight='bold')
    ax.scatter(transformed[:, PC_no_1], transformed[:, PC_no_2], color='blue')
    ax.grid(True)

    # revert to default style
    plt.style.use('default')

    # save to png
    if save:
        fig.savefig('scoreplot.png')

    plt.show()

'''
Plot the loading plot (decomposition of original features along PC1 and PC2
:param numpy_1D_array eigenvalues: 1D array of all the eigenvalues 
:param numpy_array eigenvectors: the PC's vectors
:param numpy_1D_array features: 1D array of the feature names
:param bool save: whether or not to save the loading plot

:return: plot the loading plot
'''
def _plot_loading(eigenvalues, eigenvectors, features=None, save=False):
    # compute the relative percentage of explained variance of the first two PC's
    sum_explained_var = sum(eigenvalues)
    pc1_explained_var = eigenvalues[0] * 100 / sum_explained_var
    pc2_explained_var = eigenvalues[1] * 100 / sum_explained_var

    #compute loadings
    loadings = np.sqrt(eigenvalues)*eigenvectors.T

    # extract the loadings of the first two PC's
    coeff = loadings[:, 0:2]

    # set figure parameters
    plt.style.use('classic')
    fig = plt.figure(figsize=(8,8))
    ax = fig.add_subplot(111)
    ax.set_title('Loading plot \n', fontsize=20, weight='bold')
    ax.set_xlim(-1,1)
    ax.set_ylim(-1,1)
    ax.set_xlabel('PC1 (' + str(np.round(pc1_explained_var, 2)) + ')',
                  fontsize=16, weight='bold')
    ax.set_ylabel('PC2 (' + str(np.round(pc2_explained_var, 2)) + ')',
                  fontsize=16, weight='bold')

    # set default features label if it is not passed in
    if features==None:
        features = ['F' + str(i) for i in range(1, len(eigenvalues)+1)]

    # plot the loading vector
    for i in range(len(eigenvalues)):
        # get the position of the text accompanying the arrow
        length = np.linalg.norm([coeff[i,0], coeff[i,1]])
        unit_vec = [coeff[i,0], coeff[i,1]] / length
        text_pos_vec = unit_vec * (length + 0.05)

        # plot the arrow
        ax.arrow(0, 0,
                 coeff[i,0], coeff[i,1],
                 color='r', alpha=0.5,
                 head_width=0.02, head_length=0.05)

        # write the accompanying text
        ax.text(text_pos_vec[0], text_pos_vec[1],
                features[i],
                fontsize=10, weight='bold', color='g',
                ha='left', va='bottom')

    # plot the unit circle
    circle = plt.Circle((0,0), 1.00, color='b', fill=False)
    ax.add_artist(circle)

    # draw the x and y axis through the origin
    ax.axhline(0, color='black')
    ax.axvline(0, color='black')

    # save to png
    if save:
        fig.savefig('loading.png')

    plt.show()

    # revert to default style
    plt.style.use('default')

'''
Return the result of Bartlett test for factor analysis
:param pandas_dataframe df: dataset in dataframe
:return: result of Bartlett test
'''
def _bartlett(df):
    # compute Bartlett statistics and p-value
    statistics, p_value = calculate_bartlett_sphericity(df)
    print("Bartlett test results: ")
    print("=================================================")
    print("statistics: {}".format(statistics))
    print("p-value: {}".format(p_value))
    if p_value < 0.05:
        print("Null hypothesis rejected. Statistical significance demonstrated for collinearity.")
    else:
        print("Null hypothesis could not be rejected. No statistical significance for collinearity.")
    print("=================================================")

'''
Return the result of KMO test for factor analysis
:param pandas_dataframe df: dataset in dataframe
:return: result of Bartlett test
'''
def _kmo(df):
    # compute statistics of kmo test
    _, statistics = calculate_kmo(df)
    print("KMO test results: ")
    print("=================================================")
    print("statistics: {}".format(np.round(statistics,2)))
    if statistics <= 0.5:
        print("Sampling is insufficient for factor analysis.")
    elif statistics <= 0.8:
        print("Sampling is sufficient for factor analysis.")
    else:
        print("Sampling is excellent for factor analysis")
    print("=================================================")

'''
Plot the centroid coordinates of the clusters in bar chart
:param numpy_array centroid: centroid coordinates of all clusters
:param float bar_width: width of a bar
:param float gap_width: gap between inter-cluster bars
:param list features: list of features names

:return: plot the centroid coordinates of the clusters in bar chart
'''
def _plot_cluster_centroid(centroids, bar_width=0.1, gap_width=1, features=None):
    # get number of clusters and features
    n_c, n_f = centroids.shape

    # length of all the bars plus one gap (group) per cluster
    L = n_f * bar_width + gap_width

    # set features labels
    labels_f = []
    if features == None:
        for i in range(n_f):
            labels_f.append('F' + str(i))
    else:
        labels_f = features

    # set clusters labels
    labels_c = []
    for i in range(n_c):
        labels_c.append('C' + str(i+1))

    # set cluster labels position
    pos_c = np.array([bar_width + 0.5 * L * (2 * i - 1) for i in range(1, n_c + 1)])
    # print(pos_c)

    # plot the bar charts
    plt.style.use('classic')
    fig = plt.figure(figsize=(12, 12))
    ax = fig.add_subplot(111)
    for i in range(n_f):
        # generate random color
        r = lambda: random.randint(0, 255)
        color = '#%02X%02X%02X' % (r(), r(), r())

        # get means of i-th feature for all clusters
        f_i_means = centroids[:, i]
        ax.bar(pos_c + bar_width * (i + 1 - (n_f + 1) / 2), f_i_means, bar_width,
               label=labels_f[i], color=color)

    # set some properties of the figure
    ax.set_ylabel('Features means', fontsize=18, weight='bold')
    ax.set_xlabel('Cluster', fontsize=18, weight='bold')
    ax.set_xticks(pos_c)
    ax.set_xticklabels(labels_c)
    ax.set_xlim([0, gap_width + L * n_c])
    ax.set_ylim([np.floor(np.min(centroids)), np.ceil(np.max(centroids))])
    ax.set_title('Cluster centroids', fontsize=22, weight='bold')
    ax.legend(loc='best')
    ax.axhline(0, 0, gap_width + L * n_c, color='black')
    ax.grid(True)
    plt.style.use('default')

def _perform_kmean(df, min=2, max=10, n_init=10, max_iter=300, random_state=42):
    MSSE = []
    silhouette = []
    for k in range(min, max+1):
        kmean = KMeans(n_clusters=k, init='k-means++',
                       n_init=n_init, max_iter=max_iter, random_state=random_state)
        kmean.fit(df)
        print("==================================================")
        print("Cluster number, k = ", k)
        mean_sse = np.round(kmean.inertia_ / len(df), 3)
        MSSE.append(mean_sse)
        print("MSSE score: ", mean_sse)

        # predict the distances between instances and centroid
        silh = np.round(silhouette_score(df, kmean.predict(df)), 3)
        print("Silhouette score: ", silh)
        silhouette.append(silh)

    # plot msse graph
    _plot_msse(MSSE, min, max)

    # plot silhouette graph
    _plot_silhouette(silhouette, min, max)

    return MSSE, silhouette

def _plot_msse(msse, min, max):
    plt.style.use('classic')
    fig = plt.figure(figsize=(12,12))
    ax = fig.add_subplot(111)
    ax.set_title("Mean SSE Score \n", fontsize=22, weight='bold')
    ax.set_xlabel("Cluster", fontsize=18, weight='bold')
    ax.set_ylabel("MMSE", fontsize=18, weight='bold')
    ax.set_xlim([min-1, max-1])
    ax.plot(range(min, max+1), msse, 'b-o', label='MSSE')
    ax.legend(loc='best')
    ax.grid(True)
    plt.show()
    plt.style.use('default')

def _plot_silhouette(silhouette, min, max):
    plt.style.use('classic')
    fig = plt.figure(figsize=(12,12))
    ax = fig.add_subplot(111)
    ax.set_title("Silhouette score \n", fontsize=22, weight='bold')
    ax.set_xlabel("Cluster", fontsize=18, weight='bold')
    ax.set_ylabel("Silhouette", fontsize=18, weight='bold')
    ax.set_xlim([min-1, max+1])
    ax.set_ylim([np.floor(np.min(silhouette))-1,
                 np.ceil(np.max(silhouette))+1])
    ax.plot(range(min, max+1), silhouette, 'r-o', label='silhouette')
    ax.legend(loc='best')
    ax.grid(True)
    plt.show()
    plt.style.use('default')