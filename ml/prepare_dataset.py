from pathlib import Path

import pandas as pd


BASE_DIR = Path(__file__).resolve().parent.parent
raw_dataset_path = BASE_DIR / "data" / "raw" / "sample_records.csv"
prepared_dataset_path = BASE_DIR / "data" / "prepared" / "imc_dataset_prepared.csv"
selected_columns = ["age", "gender", "height", "weight", "bmi", "activity_level", "target_risk"]
target_column = "target_risk"

RENAME_MAPPING = {
    "age": "age",
    "user_age": "age",
    "gender": "gender",
    "sex": "gender",
    "sexe": "gender",
    "height": "height",
    "height_cm": "height",
    "height_m": "height",
    "taille": "height",
    "weight": "weight",
    "poids": "weight",
    "weight_kg": "weight",
    "bmi": "bmi",
    "bmi_value": "bmi",
    "imc": "bmi",
    "activity_level": "activity_level",
    "activity": "activity_level",
    "niveau_activite": "activity_level",
    "target_risk": "target_risk",
    "risk_level_rule": "target_risk",
    "risk_category": "target_risk",
}

GENDER_MAPPING = {
    "homme": "male",
    "male": "male",
    "m": "male",
    "femme": "female",
    "female": "female",
    "f": "female",
    "autre": "other",
    "other": "other",
    "o": "other",
}

ACTIVITY_MAPPING = {
    "faible": "low",
    "low": "low",
    "sedentary": "low",
    "sedentaire": "low",
    "moderee": "medium",
    "modere": "medium",
    "medium": "medium",
    "moderate": "medium",
    "elevee": "high",
    "elevee": "high",
    "high": "high",
    "active": "high",
}

TARGET_MAPPING = {
    "moindre": "low_risk",
    "normal": "low_risk",
    "normal weight": "low_risk",
    "poids normal": "low_risk",
    "accru": "moderate_risk",
    "underweight": "moderate_risk",
    "poids insuffisant": "moderate_risk",
    "overweight": "moderate_risk",
    "exces de poids": "moderate_risk",
    "eleve": "high_risk",
    "tres eleve": "high_risk",
    "extremement eleve": "high_risk",
    "obesite classe i": "high_risk",
    "obesite classe ii": "high_risk",
    "obesite classe iii": "high_risk",
    "obese": "high_risk",
    "low_risk": "low_risk",
    "moderate_risk": "moderate_risk",
    "high_risk": "high_risk",
}


def load_raw_dataset(file_path):
    if not file_path:
        raise ValueError("Le chemin du dataset brut est vide.")

    file_path = Path(file_path)
    if not file_path.exists():
        raise FileNotFoundError(f"Fichier introuvable: {file_path}")
    if file_path.suffix.lower() != ".csv":
        raise ValueError(f"Le fichier source doit etre un CSV: {file_path}")
    if file_path.stat().st_size == 0:
        raise ValueError(f"Le fichier source est vide: {file_path}")

    read_attempts = [
        {"encoding": "utf-8", "sep": None},
        {"encoding": "utf-8-sig", "sep": None},
        {"encoding": "latin-1", "sep": None},
        {"encoding": "utf-8", "sep": ","},
        {"encoding": "utf-8", "sep": ";"},
    ]

    last_error = None
    for attempt in read_attempts:
        try:
            dataframe = pd.read_csv(
                file_path,
                sep=attempt["sep"],
                engine="python",
                encoding=attempt["encoding"],
            )
            if dataframe.empty:
                raise ValueError("Le fichier CSV a ete lu mais ne contient aucune ligne.")
            if len(dataframe.columns) == 1 and isinstance(dataframe.columns[0], str) and "," not in dataframe.columns[0] and ";" not in dataframe.columns[0]:
                return dataframe
            return dataframe
        except Exception as error:
            last_error = error

    raise ValueError(f"Impossible de lire le CSV brut: {file_path}") from last_error


def rename_columns(dataframe):
    normalized_columns = {}
    for column in dataframe.columns:
        clean_name = (
            str(column)
            .strip()
            .lower()
            .replace(" ", "_")
            .replace("-", "_")
            .replace("(", "")
            .replace(")", "")
            .replace("/", "_")
        )
        normalized_columns[column] = RENAME_MAPPING.get(clean_name, clean_name)

    renamed_df = dataframe.rename(columns=normalized_columns).copy()
    return renamed_df


def select_training_columns(dataframe):
    essential_columns = {"age", "gender", "height", "weight", "activity_level"}
    missing_columns = [column for column in essential_columns if column not in dataframe.columns]
    if missing_columns:
        raise ValueError(f"Colonnes essentielles manquantes: {', '.join(sorted(missing_columns))}")

    available_columns = [column for column in dataframe.columns if column in set(selected_columns) | {"target_risk"}]
    selected_df = dataframe.loc[:, available_columns].copy()
    return selected_df


def remove_invalid_rows(dataframe):
    cleaned_df = dataframe.copy()
    cleaned_df = cleaned_df.drop_duplicates()

    numeric_columns = ["age", "height", "weight"]
    for column in numeric_columns:
        cleaned_df[column] = pd.to_numeric(cleaned_df[column], errors="coerce")

    if "bmi" in cleaned_df.columns:
        cleaned_df["bmi"] = pd.to_numeric(cleaned_df["bmi"], errors="coerce")

    cleaned_df = cleaned_df.dropna(subset=["age", "height", "weight"])

    height_in_cm_mask = cleaned_df["height"].between(100, 250, inclusive="both")
    cleaned_df.loc[height_in_cm_mask, "height"] = cleaned_df.loc[height_in_cm_mask, "height"] / 100.0

    cleaned_df["age"] = cleaned_df["age"].astype(int)

    cleaned_df["gender"] = cleaned_df["gender"].astype(str).str.strip().str.lower().map(GENDER_MAPPING)
    cleaned_df["activity_level"] = (
        cleaned_df["activity_level"].astype(str).str.strip().str.lower().map(ACTIVITY_MAPPING)
    )

    cleaned_df = cleaned_df.dropna(subset=["gender", "activity_level"])

    cleaned_df = cleaned_df[
        cleaned_df["age"].between(5, 120)
        & cleaned_df["height"].between(1.0, 2.5)
        & cleaned_df["weight"].between(20, 300)
    ].copy()

    recalculated_bmi = cleaned_df["weight"] / (cleaned_df["height"] ** 2)
    if "bmi" not in cleaned_df.columns:
        cleaned_df["bmi"] = recalculated_bmi
    else:
        cleaned_df["bmi"] = cleaned_df["bmi"].fillna(recalculated_bmi)
        bmi_diff_mask = (cleaned_df["bmi"] - recalculated_bmi).abs() > 0.5
        cleaned_df.loc[bmi_diff_mask, "bmi"] = recalculated_bmi.loc[bmi_diff_mask]

    cleaned_df = cleaned_df[cleaned_df["bmi"].between(10, 70)].copy()
    cleaned_df["bmi"] = cleaned_df["bmi"].round(2)

    return cleaned_df.reset_index(drop=True)


def create_target_label(dataframe):
    prepared_df = dataframe.copy()

    if target_column in prepared_df.columns:
        normalized_target = (
            prepared_df[target_column]
            .astype(str)
            .str.strip()
            .str.lower()
            .map(TARGET_MAPPING)
        )
        prepared_df[target_column] = normalized_target

    if target_column not in prepared_df.columns or prepared_df[target_column].isna().any():
        if "bmi" not in prepared_df.columns:
            prepared_df["bmi"] = (prepared_df["weight"] / (prepared_df["height"] ** 2)).round(2)

        bmi_based_target = pd.Series(index=prepared_df.index, dtype="object")
        bmi_based_target.loc[prepared_df["bmi"] < 18.5] = "moderate_risk"
        bmi_based_target.loc[(prepared_df["bmi"] >= 18.5) & (prepared_df["bmi"] < 25)] = "low_risk"
        bmi_based_target.loc[(prepared_df["bmi"] >= 25) & (prepared_df["bmi"] < 30)] = "moderate_risk"
        bmi_based_target.loc[prepared_df["bmi"] >= 30] = "high_risk"

        if target_column not in prepared_df.columns:
            prepared_df[target_column] = bmi_based_target
        else:
            prepared_df[target_column] = prepared_df[target_column].fillna(bmi_based_target)

    allowed_targets = {"low_risk", "moderate_risk", "high_risk"}
    prepared_df = prepared_df[prepared_df[target_column].isin(allowed_targets)].copy()
    return prepared_df.reset_index(drop=True)


def validate_prepared_dataset(dataframe):
    if dataframe.empty:
        raise ValueError("Le dataset prepare est vide.")

    missing_columns = [column for column in selected_columns if column not in dataframe.columns]
    if missing_columns:
        raise ValueError(f"Colonnes finales manquantes: {', '.join(missing_columns)}")

    if dataframe[target_column].isna().any():
        raise ValueError("La colonne target_risk contient encore des valeurs nulles.")

    return dataframe.loc[:, selected_columns].copy()


def save_prepared_dataset(dataframe, output_path):
    output_path = Path(output_path)
    if dataframe.empty:
        raise ValueError("Impossible de sauvegarder un dataset vide.")

    final_df = validate_prepared_dataset(dataframe)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    final_df.to_csv(output_path, index=False, encoding="utf-8")
    return output_path


def prepare_dataset(input_path=raw_dataset_path, output_path=prepared_dataset_path):
    raw_df = load_raw_dataset(input_path)
    standardized_df = rename_columns(raw_df)
    filtered_df = select_training_columns(standardized_df)
    cleaned_df = remove_invalid_rows(filtered_df)
    prepared_df = create_target_label(cleaned_df)
    prepared_df = validate_prepared_dataset(prepared_df)
    saved_path = save_prepared_dataset(prepared_df, output_path)

    summary = {
        "input_path": str(Path(input_path)),
        "output_path": str(saved_path),
        "rows": len(prepared_df),
        "columns": list(prepared_df.columns),
        "target_distribution": prepared_df[target_column].value_counts().to_dict(),
    }
    return prepared_df, summary


def main():
    prepared_df, summary = prepare_dataset()
    print(f"Dataset brut charge depuis: {summary['input_path']}")
    print(f"Dataset prepare sauvegarde dans: {summary['output_path']}")
    print(f"Lignes finales: {summary['rows']}")
    print(f"Colonnes finales: {', '.join(summary['columns'])}")
    print(f"Distribution de la cible: {summary['target_distribution']}")
    print(prepared_df.head().to_string(index=False))


if __name__ == "__main__":
    main()
