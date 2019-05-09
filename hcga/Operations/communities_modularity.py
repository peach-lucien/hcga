# -*- coding: utf-8 -*-
"""
Created on Sun Mar  3 18:30:46 2019

@author: Rob
"""

import pandas as pd
import numpy as np

from networkx.algorithms.community import greedy_modularity_communities
from networkx.algorithms.community.quality import modularity

class ModularityCommunities():
    def __init__(self, G):
        self.G = G
        self.feature_names = []
        self.features = []

    def feature_extraction(self):

        """Find communities in graph using Clauset-Newman-Moore greedy modularity
        maximization. This method currently supports the Graph class and does not
        consider edge weights.

        Greedy modularity maximization begins with each node in its own community
        and joins the pair of communities that most increases modularity until no
        such pair exists.

        Parameters
        ----------
        G : NetworkX graph

        Returns
        -------
        feature_list:  list
            List of features related to modularity

        Notes
        -----
        Greedy modularity implemented using networkx:
            https://networkx.github.io/documentation/stable/_modules/networkx/algorithms/community/modularity_max.html#greedy_modularity_communities

        References
        ----------
        .. [1] M. E. J Newman 'Networks: An Introduction', page 224
           Oxford University Press 2011.
        .. [2] Clauset, A., Newman, M. E., & Moore, C.
           "Finding community structure in very large networks."
           Physical Review E 70(6), 2004.
        """

        self.feature_names = ['num_comms_greedy_mod','mod_val_greedy_mod','ratio_max_min_num_nodes','ratio_max_2max_num_nodes']

        G = self.G

        feature_list = []

        # basic normalisation parameters
        N = G.number_of_nodes()
        E = G.number_of_edges()

        # The optimised number of communities using greedy modularity
        c = list(greedy_modularity_communities(G))
        
        # calculate number of communities
        feature_list.append(len(c))
        
        # modularity of the clustering
        feature_list.append(modularity(G,c))
        
        # calculate ratio of largest to smallest community
        feature_list.append((len(c[0])/len(c[-1])))

        # calculate ratio of largest to 2nd largest community
        if len(c)>1:
            feature_list.append((len(c[0])/len(c[1])))
        else:
            feature_list.append(np.nan)

        self.features = feature_list
