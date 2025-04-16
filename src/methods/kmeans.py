import numpy as np
import itertools


class KMeans(object):
    """
    kNN classifier object.
    """

    def __init__(self, max_iters=500):
        """
        Call set_arguments function of this class.
        """
        self.max_iters = max_iters
        self.centroids = None
        self.best_permutation = None

    def fit(self, training_data, training_labels):
        """
        Trains the model, returns predicted labels for training data.
        Hint:
            (1) Since Kmeans is unsupervised clustering, 
            we don't need the labels for training. 
            But you may want to use it to determine the number of clusters.
            (2) Kmeans is sensitive to initialization. 
            You can try multiple random initializations when using this classifier.

        Arguments:
            training_data (np.array): training data of shape (N,D)
            training_labels (np.array): labels of shape (N,).
        Returns:
            pred_labels (np.array): labels of shape (N,)
        """

        """
        nbrClusters = training_labels.size 
        nbrdata = training_data.shape[0]
        init_index = np.random.choice(nbrdata, size = nbrClusters, replace = False)
        init_cluster = training_data[init_index]
        pred_labels = np.zeros(nbrdata)
        k = 0
        for i in training_data:
            y = 100000000000000000000000000000000000000000000000
            closest_cluster = -1
            for j in range(nbrClusters):
                x = np.linalg.norm(init_cluster[j] - i)
                if(x<y):
                    y = x
                    closest_cluster = j
            pred_labels[k] = closest_cluster
            k += 1
        for cluster in range(nbrClusters):
            new_centroid = np.mean(training_data[pred_labels == cluster], axis=0)
            self.centroids[cluster] = new_centroid
                

        ##
        ###
        #### YOUR CODE HERE!
        ###
        ##
        """
        # Determine number of clusters from unique labels
        unique_labels = np.unique(training_labels)
        num_clusters = len(unique_labels)
        
        # Initialize centroids randomly
        n_samples = training_data.shape[0]
        init_indices = np.random.choice(n_samples, size=num_clusters, replace=False)
        self.centroids = training_data[init_indices].copy()
        
        # Initialize labels
        prev_labels = np.zeros(n_samples)
        
        # Iterate until convergence or max iterations
        for iteration in range(self.max_iters):
            # Assign each data point to the nearest centroid
            distances = np.zeros((n_samples, num_clusters))
            for i in range(num_clusters):
                distances[:, i] = np.linalg.norm(training_data - self.centroids[i], axis=1)
            
            pred_labels = np.argmin(distances, axis=1)
            
            # Check for convergence
            if np.array_equal(pred_labels, prev_labels):
                break
                
            prev_labels = pred_labels.copy()
            
            # Update centroids
            for cluster in range(num_clusters):
                # Skip empty clusters
                if np.sum(pred_labels == cluster) > 0:
                    self.centroids[cluster] = np.mean(training_data[pred_labels == cluster], axis=0)
        
        # Map cluster indices to actual labels (optional)
        # This helps map arbitrary cluster indices to meaningful class labels
        # We try all permutations to find the best match with the provided labels
        all_permutations = list(itertools.permutations(range(num_clusters)))
        best_accuracy = -1
        best_perm = None
        
        for perm in all_permutations:
            mapped_labels = np.array([perm[label] for label in pred_labels])
            accuracy = np.sum(mapped_labels == training_labels) / len(training_labels)
            
            if accuracy > best_accuracy:
                best_accuracy = accuracy
                best_perm = perm
        
        self.best_permutation = best_perm
        
        # Map the predicted labels using the best permutation
        if self.best_permutation is not None:
            pred_labels = np.array([self.best_permutation[label] for label in pred_labels])
        
        return pred_labels
    
    def predict(self, test_data):
        """
        Runs prediction on the test data.

        Arguments:
            test_data (np.array): test data of shape (N,D)
        Returns:
            test_labels (np.array): labels of shape (N,)
        """


        ##
        ###
        #### YOUR CODE HERE!
        ###
        ##

        if self.centroids is None:
            raise Exception("Model not trained. Call fit() before predict().")
        
        # Calculate distances to each centroid
        n_samples = test_data.shape[0]
        num_clusters = self.centroids.shape[0]
        distances = np.zeros((n_samples, num_clusters))
        
        for i in range(num_clusters):
            distances[:, i] = np.linalg.norm(test_data - self.centroids[i], axis=1)
        
        # Assign each test point to nearest centroid
        test_labels = np.argmin(distances, axis=1)
        
        # Map the predicted labels using the best permutation if available
        if self.best_permutation is not None:
            test_labels = np.array([self.best_permutation[label] for label in test_labels])
        
        return test_labels
