from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble.gradient_boosting import GradientBoostingClassifier
from sklearn.neural_network.rbm import BernoulliRBM


def model():

    # return RandomForestClassifier(n_estimators=50,
                                            # verbose=2,
                                            # n_jobs=1,
                                            # min_samples_split=10,
                                            # random_state=1)
                                            
    return GradientBoostingClassifier(loss='deviance',
                                        learning_rate=0.1,
                                        n_estimators=100,
                                        subsample=1.0,
                                        min_samples_split=2,
                                        min_samples_leaf=1,
                                        max_depth=3,
                                        init=None,
                                        random_state=None,
                                        max_features=None,
                                        verbose=0)

    #return BernoulliRBM(random_state=0, verbose=1)