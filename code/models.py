import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.kernel_ridge import KernelRidge
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import RandomizedSearchCV
from sklearn.gaussian_process.kernels import RationalQuadratic
from scipy.stats import loguniform
from sklearn.gaussian_process.kernels import RBF

class Model:

    def __init__(self, data_file_path):
        self.data= data = pd.read_csv(data_file_path)
        self.scaler= StandardScaler()
        self.model = None

    def train(self):
        """
        Trains the model.
        :return: None
        """
        if(self.model is None):
            X = self.data[['n', 'm', 'p']].values
            y = self.data['probability'].values
            #X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=0)
            X_train_scaled = self.scaler.fit_transform(X)
            #X_test_scaled = self.scaler.transform(X_test)
            model_t = KernelRidge(kernel=RBF())
            param_distributions = {
                "alpha": loguniform(1e0, 1e3),
                "gamma": loguniform(1e-2, 1e2),
                "kernel__length_scale": loguniform(1e-2, 1e2),
            }
            self.model = RandomizedSearchCV(
                model_t,
                param_distributions=param_distributions,
                n_iter=500,
                random_state=0,
            )
            self.model.fit(X_train_scaled, y)
            #y_pred = kernel_ridge_tuned.predict(X_test_scaled)
            #mse = mean_squared_error(y_test, y_pred)

    def predict(self,n,m,p):
        """
        If the model hasn't been trained yet, trains it before predicting.

        :param n: int
        first dimension of the layout
        :param m: int
        second dimension of the layout
        :param p: float
        probability of obstacle existence
        :return: float
        the model's prediction of the probability of tilability
        """
        if self.model is None:
            self.train()

        return self.model.predict(self.scaler.transform([[n,m,p]]))[0]