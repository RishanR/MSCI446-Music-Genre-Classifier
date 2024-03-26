This README provides instructions on how to run our python file and notebooks.

1. Create Raw Dataset (optional)
NOTE: This step requires that you have a premium Spotify Developer account and the client, secret, and redirect_uri environment variables set.
WARNING: This step downloads about 1.5 GB worth of songs

To generate the raw dataset, run data_collector.py using python in your terminal.
This will create a raw_dataset.csv file inside the data folder. This file will be used for the data preparation step.
This step is optional since we have already created a raw_dataset.csv file for you in the data folder.

2. Data Preparation (optional - train.csv and test.csv already in data folder)
To perform all 7 steps of the data preparation pipeline on raw_dataset.csv, run data_preparation.ipynb using Jupyter Notebook.
This will create a train.csv and test.csv file inside the data folder. These 2 files will be used for training and testing in step 3.
This step is optional since we have already created the train.csv and test.csv files for you in the data folder.

3. Model Training
WARNING: This step can take a long time to execute depending on your hardware

To perform feature selection, hyperparameter tuning, and final model training on all 3 models (Gradient Boosting, Random Forest, and Support Vector Machine), run model_training.ipynb.
This will give you the confusion matrix and accuracy, f1-score, precision, and recall metrics for all 3 models.