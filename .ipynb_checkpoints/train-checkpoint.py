import pandas as pd
from sklearn import tree
from fire import Fire
import warnings 
import git

from sklearn.metrics import mean_squared_error
from sklearn.model_selection import train_test_split
import mlflow 
from src.decorators import commitme

@commitme
def run_tree(data, target_col, max_depth, min_samples_leaf, random_state):
    warnings.filterwarnings("ignore")
    
    repo = git.Repo(search_parent_directories=True)
    sha = repo.head.commit.hexsha
    
    # Read data and split on train/validation sets
    df = pd.read_csv(data)
    train, valid = train_test_split(df, random_state=random_state)
    train_x, train_y = train.drop(target_col, axis=1), train[target_col]
    valid_x, valid_y = valid.drop(target_col, axis=1), valid[target_col]
    
    # Build and train the model
    with mlflow.start_run():
        mlflow.set_tag("git.hash", sha)
        
        # build model architecture
        clf = tree.DecisionTreeRegressor(max_depth=max_depth, min_samples_leaf=min_samples_leaf, random_state=random_state)
        clf = clf.fit(train_x, train_y)
        y_trn_pred = clf.predict(valid_x)
        
        metric = mean_squared_error(valid_y, y_trn_pred[:,1])
        mlflow.log_metric('metric', metric)
        
def main(data, target_col, max_depth, min_samples_leaf, random_state, commit=False):
    if commit:
        run_tree(data, target_col, max_depth, min_samples_leaf, random_state)
    else:
        run_tree.unwrapped(data, target_col, max_depth, min_samples_leaf, random_state)
        
if __name__ == '__main__':
    Fire(main)