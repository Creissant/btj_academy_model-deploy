import os
import pandas as pd
import joblib
import mlflow
import mlflow.sklearn

from dotenv import load_dotenv
from pathlib import Path

from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.impute import SimpleImputer
from sklearn.neural_network import MLPClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix, classification_report

# Load environment variables
load_dotenv(".env.development")

# Load model + handling cross platform
BASE_DIR = Path(__file__).resolve().parent.parent.parent
MODEL_PATH = BASE_DIR / "data" / "raw" / "Titanic-Dataset.csv"

# MLflow tracking + logging
mlflow.set_tracking_uri(f"http://{os.getenv('MLFLOW_TRACKING_URI_IP')}:{os.getenv('MLFLOW_TRACKING_URI_PORT')}")
mlflow.set_experiment("titanic_models_pipeline")

ARTIFACT_PATH="titanic_classification_mlp_pipeline"
REGISTERED_MODEL_NAME="TitanicMLPModel"


def load_data(path: str):
    df = pd.read_csv(path)

    # Handle missing values
    df['Age'].fillna(df['Age'].median(), inplace=True)
    df['Embarked'].fillna(df['Embarked'].mode()[0], inplace=True)

    # Extract NameTitle
    def split_title(x):
        return x['Name'].split(',')[1].split('.')[0].strip()

    df['NameTitle'] = df.apply(split_title, axis=1)

    def simplify_title(title):
        if title in ['Mr']:
            return 'Mr'
        elif title in ['Miss', 'Ms', 'Mlle']:
            return 'Miss'
        elif title in ['Mrs', 'Mme']:
            return 'Mrs'
        elif title == 'Master':
            return 'Master'
        else:
            return 'Rare'

    df['NameTitle'] = df['NameTitle'].apply(simplify_title)

    # Drop irrelevant columns
    df.drop(columns=['Cabin', 'Name', 'Ticket', 'PassengerId'], inplace=True)

    return df


def build_pipeline():
    numeric_features = ['Age', 'SibSp', 'Parch', 'Fare']
    categorical_features = ['Pclass', 'Sex', 'Embarked', 'NameTitle']

    numeric_transformer = Pipeline(steps=[
        ('imputer', SimpleImputer(strategy='median')),
        ('scaler', StandardScaler())
    ])

    categorical_transformer = Pipeline(steps=[
        ('imputer', SimpleImputer(strategy='most_frequent')),
        ('onehot', OneHotEncoder(drop='first', handle_unknown='ignore'))
    ])

    preprocessor = ColumnTransformer(
        transformers=[
            ('num', numeric_transformer, numeric_features),
            ('cat', categorical_transformer, categorical_features)
        ]
    )

    model = Pipeline(steps=[
        ('preprocessor', preprocessor),
        ('classifier', MLPClassifier(max_iter=300, random_state=42))
    ])

    return model


def train_and_log(data_path: str, model_output: str = "titanic_model-mlflow.pkl"):
    df = load_data(data_path)
    X = df.drop('Survived', axis=1)
    y = df['Survived']

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.3, random_state=42, stratify=y
    )

    with mlflow.start_run(run_name="titanic_classification_pipeline_test") as run:
        # Build pipeline
        model = build_pipeline()

        # Train model
        model.fit(X_train, y_train)

        # Predict
        y_pred = model.predict(X_test)

        # Metrics
        acc = accuracy_score(y_test, y_pred)
        prec = precision_score(y_test, y_pred)
        rec = recall_score(y_test, y_pred)
        f1 = f1_score(y_test, y_pred)

        print("Accuracy:", acc)
        print("Precision:", prec)
        print("Recall:", rec)
        print("F1 Score:", f1)
        print("Confusion Matrix:\n", confusion_matrix(y_test, y_pred))
        print("Classification Report:\n", classification_report(y_test, y_pred))

        # Log metrics
        mlflow.log_metric("accuracy", acc)
        mlflow.log_metric("precision", prec)
        mlflow.log_metric("recall", rec)
        mlflow.log_metric("f1_score", f1)

        # Log parameters
        mlflow.log_param("classifier", "MLPClassifier")
        mlflow.log_param("max_iter", 300)
        mlflow.log_param("random_state", 42)
        mlflow.log_param("test_size", 0.3)
        mlflow.log_param("n_features", X_train.shape[1])
        mlflow.log_param("n_train_samples", len(X_train))
        mlflow.log_param("n_test_samples", len(X_test))

        # Log model ke MLflow
        mlflow.sklearn.log_model(
            sk_model=model, 
            input_example=X_test, 
            name=ARTIFACT_PATH, 
            registered_model_name=REGISTERED_MODEL_NAME
        )

        # Simpan model lokal juga
        joblib.dump(model, model_output)
        print(f"✅ Model saved as {model_output}")


if __name__ == "__main__":
    train_and_log(MODEL_PATH)