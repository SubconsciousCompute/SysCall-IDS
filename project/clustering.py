from collections import defaultdict
from sklearn.mixture import GaussianMixture
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
import joblib
import numpy as np

syscall_to_cluster = {}
init_called = False
pca = None
scaler = None


def init_cluster_mapping(padded_feature_vectors, method="GMM"):
    global syscall_to_cluster, init_called, pca, scaler

    pca = PCA(n_components=3)
    scaler = StandardScaler()

    syscall_vectors = defaultdict(list)

    feature_vector_attributes = np.array([vector[1:] for vector in padded_feature_vectors])
    normalized_features = scaler.fit_transform(feature_vector_attributes)
    transformed_features = pca.fit_transform(normalized_features)

    joblib.dump(pca, 'pca_model.pkl')
    joblib.dump(scaler, 'scaler.pkl')

    print("=> Initializing cluster mapping")

    for idx, vec in enumerate(padded_feature_vectors):
        syscall_idx = vec[0]
        syscall_vectors[syscall_idx].append(transformed_features[idx])

    for syscall_idx, vectors in syscall_vectors.items():
        if len(vectors) >= 2:
          if method == "KMEANS":
              clustering = KMeans(n_clusters=min(10, len(vectors)), random_state=42, n_init=10, tol=1e-3)
              clustering.fit(vectors)
              syscall_to_cluster[syscall_idx] = clustering

          elif method == "GMM":
              lowest_bic = np.infty
              best_gmm = None
              for n_components in range(2, min(10, len(vectors))):
                  gmm = GaussianMixture(n_components=n_components, covariance_type='full')
                  gmm.fit(vectors)
                  bic = gmm.bic(np.array(vectors))
                  if bic < lowest_bic:
                      lowest_bic = bic
                      best_gmm = gmm

              if best_gmm is not None:
                  syscall_to_cluster[syscall_idx] = best_gmm

    init_called = True
    print("=> Done!")

    return syscall_to_cluster


def features_to_states(feature_vectors):
    global syscall_to_cluster, init_called, pca, scaler

    if not init_called:
        raise Exception("Must call init_cluster_mapping() before calling features_to_states()")

    feature_vector_attributes = np.array([vector[1:] for vector in feature_vectors])
    normalized_features = scaler.transform(feature_vector_attributes)
    transformed_features = pca.transform(normalized_features)

    states = []
    for idx, vec in enumerate(feature_vectors):
        syscall_idx = vec[0]
        clustering = syscall_to_cluster.get(syscall_idx, None)
        if not clustering:
            cluster_label = 0
        else:
            cluster_label = clustering.predict([transformed_features[idx]])[0]
        states.append((syscall_idx, cluster_label))

    return states