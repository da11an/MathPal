

x_train,x_test,y_train,y_test = sklearn.train_test_split(x,y,test_size=0.2)
X = df.iloc[:, :TRAIN_STEPS]
y = df.iloc[:, TRAIN_STEPS:]

X_train = X.iloc[:SPLIT_IDX, :]
y_train = y.iloc[:SPLIT_IDX, :]

X_test = X.iloc[SPLIT_IDX:, :]
y_test = y.iloc[SPLIT_IDX:, :]
 
tscv = sklearn.model_selection.TimeSeriesSplit(n_splits=5)

def build_model(_alpha, _l1_ratio):
    estimator = ElasticNet(
        alpha=_alpha,
        l1_ratio=_l1_ratio,
        fit_intercept=True,
        normalize=False,
        precompute=False,
        max_iter=16,
        copy_X=True,
        tol=0.1,
        warm_start=False,
        positive=False,
        random_state=None,
        selection='random'
    )
    return MultiOutputRegressor(estimator, n_jobs=4)

params = {
    'estimator__alpha':(0.1, 0.3, 0.5, 0.7, 0.9),
    'estimator__l1_ratio':(0.1, 0.3, 0.5, 0.7, 0.9)
}

for i in range(100):
    model = build_model(_alpha=1.0, _l1_ratio=0.3)

    finder = GridSearchCV(
        estimator=model,
        param_grid=params,
        scoring=r2,
        fit_params=None,
        n_jobs=None,
        iid=False,
        refit=False,
        cv=kfcv,  # change this to the splitter subject to test
        verbose=1,
        pre_dispatch=8,
        error_score=-999,
        return_train_score=True
    )

    finder.fit(X_train, y_train)

    best_params = finder.best_params_