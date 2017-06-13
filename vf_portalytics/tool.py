# coding=utf-8
import numpy as np
import os
import shutil
from sklearn.metrics import mean_absolute_error, r2_score


def rm_file_or_dir(path):
    if os.path.exists(path):
        if os.path.isdir(path):
            if os.path.islink(path):
                os.unlink(path)
            else:
                shutil.rmtree(path)
        else:
            if os.path.islink(path):
                os.unlink(path)
            else:
                os.remove(path)


def create_train_test_sets(df, mask, prediction_model, prediction_target='lift', debug=True):
    # convert
    train_df = prediction_model.pre_processing(df[mask], create_label_encoding=True, remove_nan=True)
    train_lift = train_df[prediction_target]
    del train_df[prediction_target]

    test_df = prediction_model.pre_processing(df[-mask], create_label_encoding=True, remove_nan=True)
    test_lift = test_df[prediction_target]
    del test_df[prediction_target]

    if debug:
        print('Train set: ' + str(len(train_df)))
        print('Test set: ' + str(len(test_df)))

    return train_df, train_lift, test_df, test_lift


def mean_absolute_percentage_error(y_true, y_pred):
    return np.mean(np.abs((y_true - y_pred) / y_true)) * 100


def forecast_error(real_lift, predicted_lift, baseline_units):
    predicted_units = baseline_units * predicted_lift
    real_units = baseline_units * real_lift
    error_units = abs(real_units - predicted_units)
    return (sum(error_units) / sum(real_units)) * 100


def score_model(predict_lift, test_lift, baseline=None):
    print(u"R²:" + str(r2_score(predict_lift, test_lift)))
    print("MAE:" + str(mean_absolute_error(predict_lift, test_lift)))
    print("MAPE:" + str(mean_absolute_percentage_error(predict_lift, test_lift)))
    if baseline is not None:
        print("Forecast error:" + str(forecast_error(predict_lift, test_lift, baseline)))

