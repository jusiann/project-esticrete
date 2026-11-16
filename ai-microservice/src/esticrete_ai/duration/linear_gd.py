"""Doğrusal regresyon, sıfırdan: MSE kaybı ve gradient descent (numpy dışında kütüphane yok)."""

import numpy as np
from sklearn.base import BaseEstimator, RegressorMixin


class GradientDescentRegressor(RegressorMixin, BaseEstimator):
    """y = Xw + b; kayıp MSE (+ isteğe bağlı L2). Girdilerin ölçeklenmiş olması beklenir."""

    def __init__(self, learning_rate: float = 0.05, n_iter: int = 5000, l2: float = 0.0, tol: float = 1e-10):
        self.learning_rate = learning_rate
        self.n_iter = n_iter
        self.l2 = l2
        self.tol = tol

    def fit(self, X, y):
        X = np.asarray(X, dtype=float)
        y = np.asarray(y, dtype=float)
        n, d = X.shape
        w, b = np.zeros(d), 0.0
        self.loss_history_ = []
        for _ in range(self.n_iter):
            error = X @ w + b - y
            loss = float(error @ error) / n + self.l2 * float(w @ w)
            self.loss_history_.append(loss)
            grad_w = (2.0 / n) * (X.T @ error) + 2.0 * self.l2 * w
            grad_b = (2.0 / n) * float(error.sum())
            w -= self.learning_rate * grad_w
            b -= self.learning_rate * grad_b
            if len(self.loss_history_) > 1 and abs(self.loss_history_[-2] - loss) < self.tol:
                break
        self.coef_, self.intercept_ = w, b
        return self

    def predict(self, X):
        return np.asarray(X, dtype=float) @ self.coef_ + self.intercept_
