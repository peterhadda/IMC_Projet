from pathlib import Path

import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler


BASE_DIR = Path(__file__).resolve().parent.parent
prepared_dataset_path = BASE_DIR / "data" / "prepared" / "imc_dataset_prepared.csv"
feature_columns = ["age", "gender", "height", "weight", "bmi", "activity_level"]
target_column = "target_risk"
numeric_features = ["age", "height", "weight", "bmi"]
categorical_features = ["gender", "activity_level"]


def load_prepared_dataset(file_path=prepared_dataset_path):
    file_path = Path(file_path)
    if not file_path.exists():
        raise FileNotFoundError(f"Dataset prepare introuvable: {file_path}")

    dataframe = pd.read_csv(file_path)
    if dataframe.empty:
        raise ValueError("Le dataset prepare est vide.")
    return dataframe


def split_features_and_target(dataframe, target_column_name):
    if not isinstance(dataframe, pd.DataFrame):
        raise TypeError("dataframe doit etre un pandas DataFrame.")
    if dataframe.empty:
        raise ValueError("Le DataFrame est vide.")
    if target_column_name not in dataframe.columns:
        raise ValueError(f"La colonne cible '{target_column_name}' est absente du DataFrame.")

    missing_feature_columns = [column for column in feature_columns if column not in dataframe.columns]
    if missing_feature_columns:
        raise ValueError(f"Colonnes features manquantes: {', '.join(missing_feature_columns)}")

    valid_rows = dataframe[target_column_name].notna()
    if not valid_rows.any():
        raise ValueError(f"La colonne cible '{target_column_name}' ne contient aucune valeur exploitable.")

    X = dataframe.loc[valid_rows, feature_columns].copy()
    y = dataframe.loc[valid_rows, target_column_name].copy()
    return X, y


def encode_categorical_features(features_df):
    if not isinstance(features_df, pd.DataFrame):
        raise TypeError("features_df doit etre un pandas DataFrame.")

    missing_categorical = [column for column in categorical_features if column not in features_df.columns]
    if missing_categorical:
        raise ValueError(f"Colonnes categorielles manquantes: {', '.join(missing_categorical)}")

    return pd.get_dummies(features_df, columns=categorical_features, dtype=float)


def scale_numeric_features(features_df):
    if not isinstance(features_df, pd.DataFrame):
        raise TypeError("features_df doit etre un pandas DataFrame.")

    missing_numeric = [column for column in numeric_features if column not in features_df.columns]
    if missing_numeric:
        raise ValueError(f"Colonnes numeriques manquantes: {', '.join(missing_numeric)}")

    scaled_df = features_df.copy()
    scaler = StandardScaler()
    scaled_values = scaler.fit_transform(scaled_df[numeric_features].astype(float))
    for index, column in enumerate(numeric_features):
        scaled_df[column] = scaled_values[:, index]
    return scaled_df


def split_train_test(features, target, test_size=0.2, random_state=42):
    if not isinstance(features, pd.DataFrame):
        raise TypeError("features doit etre un pandas DataFrame.")
    if len(features) != len(target):
        raise ValueError("features et target doivent avoir le meme nombre de lignes.")

    stratify_target = target if getattr(target, "nunique", lambda **_: 0)(dropna=True) > 1 else None
    X_train, X_test, y_train, y_test = train_test_split(
        features,
        target,
        test_size=test_size,
        random_state=random_state,
        stratify=stratify_target,
    )
    return X_train, X_test, y_train, y_test


def build_preprocessing_pipeline():
    numeric_transformer = Pipeline(
        steps=[
            ("scaler", StandardScaler()),
        ]
    )
    categorical_transformer = Pipeline(
        steps=[
            ("encoder", OneHotEncoder(handle_unknown="ignore")),
        ]
    )
    return ColumnTransformer(
        transformers=[
            ("numeric", numeric_transformer, numeric_features),
            ("categorical", categorical_transformer, categorical_features),
        ]
    )


def run_preprocessing(file_path=prepared_dataset_path, test_size=0.2, random_state=42):
    dataframe = load_prepared_dataset(file_path)
    X, y = split_features_and_target(dataframe, target_column)
    X_train, X_test, y_train, y_test = split_train_test(
        X,
        y,
        test_size=test_size,
        random_state=random_state,
    )

    pipeline = build_preprocessing_pipeline()
    X_train_processed = pipeline.fit_transform(X_train)
    X_test_processed = pipeline.transform(X_test)

    return {
        "X": X,
        "y": y,
        "X_train": X_train,
        "X_test": X_test,
        "y_train": y_train,
        "y_test": y_test,
        "pipeline": pipeline,
        "X_train_processed": X_train_processed,
        "X_test_processed": X_test_processed,
    }


def main():
    result = run_preprocessing()
    print(f"Train size: {len(result['X_train'])}")
    print(f"Test size: {len(result['X_test'])}")
    print(f"Shape train apres preprocessing: {result['X_train_processed'].shape}")
    print(f"Shape test apres preprocessing: {result['X_test_processed'].shape}")


if __name__ == "__main__":
    main()
