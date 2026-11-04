"""Pipeline de limpieza y transformación del Titanic.

Resume las decisiones del notebook `proyecto_titanic_trabajo.ipynb`.

Uso rápido:
    from titanic_pipeline import cargar_datos, construir_pipeline
    X_train, X_test, y_train, y_test = cargar_datos()
    pipe = construir_pipeline()
    X_train_t = pipe.fit_transform(X_train)   # aprende SOLO con train
    X_test_t = pipe.transform(X_test)
"""
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn import set_config
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import (FunctionTransformer, OneHotEncoder,
                                   OrdinalEncoder, StandardScaler)

set_config(transform_output="pandas")

# Columnas redundantes (embark_town = embarked, class = pclass, etc.) y deck (74% nulos)
COLUMNAS_A_ELIMINAR = ["embark_town", "adult_male", "class", "alive", "alone", "deck"]


def limpiar(df: pd.DataFrame) -> pd.DataFrame:
    """Limpieza a nivel de filas. No aprende nada de los datos, así que va antes del split."""
    df = df.drop(columns=COLUMNAS_A_ELIMINAR).drop_duplicates()

    error_edad = df["age"] < 1                              # NaN da False: no se elimina
    error_fare = (df["fare"] > 500) | (df["fare"] <= 0)
    error_sibsp = df["sibsp"] >= 8
    return df[~(error_edad | error_fare | error_sibsp)]


class ImputadorEdad(BaseEstimator, TransformerMixin):
    """Rellena `age` con la mediana de cada grupo (sex, who), calculada solo con train."""

    def fit(self, X, y=None):
        self.feature_names_in_ = np.asarray(X.columns, dtype=object)
        self.medianas_ = X.groupby(["sex", "who"])["age"].median()
        self.mediana_global_ = X["age"].median()  # respaldo por si aparece un grupo nuevo
        return self

    def transform(self, X):
        X = X.copy()
        por_grupo = pd.MultiIndex.from_frame(X[["sex", "who"]]).map(self.medianas_)
        relleno = pd.Series(por_grupo, index=X.index).fillna(self.mediana_global_)
        X["age"] = X["age"].fillna(relleno)
        return X

    def get_feature_names_out(self, input_features=None):
        return self.feature_names_in_


def _crear_features(X: pd.DataFrame) -> pd.DataFrame:
    X = X.copy()
    X["fsize"] = X["sibsp"] + X["parch"]
    X["u_fare"] = X["fare"] / (X["fsize"] + 1)
    X["r_age"] = pd.cut(X["age"], bins=[0, 15, 50, np.inf],
                        labels=["child", "adult", "eldery"]).astype(str)
    return X


def _nombres_features(transformer, nombres):
    return [*nombres, "fsize", "u_fare", "r_age"]


def construir_pipeline() -> Pipeline:
    numericas = ["pclass", "age", "sibsp", "parch", "fsize"]
    asimetricas = ["fare", "u_fare"]   # log1p para reducir el sesgo y luego escalar
    binarias = ["sex"]
    nominales = ["embarked", "who"]
    ordinales = ["r_age"]

    asimetrico = Pipeline([
        ("log", FunctionTransformer(np.log1p, feature_names_out="one-to-one")),
        ("escalar", StandardScaler()),
    ])

    columnas = ColumnTransformer([
        ("num", StandardScaler(), numericas),
        ("asim", asimetrico, asimetricas),
        ("bin", OneHotEncoder(drop="if_binary", sparse_output=False), binarias),
        ("nom", OneHotEncoder(drop="first", handle_unknown="ignore", sparse_output=False), nominales),
        ("ord", OrdinalEncoder(categories=[["child", "adult", "eldery"]]), ordinales),
    ], verbose_feature_names_out=False)

    return Pipeline([
        ("imputar_embarked", ColumnTransformer(
            [("moda", SimpleImputer(strategy="most_frequent"), ["embarked"])],
            remainder="passthrough", verbose_feature_names_out=False)),
        ("imputar_edad", ImputadorEdad()),
        ("features", FunctionTransformer(_crear_features, feature_names_out=_nombres_features)),
        ("columnas", columnas),
    ])


def cargar_datos(test_size=0.2, random_state=42):
    """Lee data/titanic.csv, limpia y separa en train/test."""
    raiz = next((p for p in [Path.cwd(), *Path.cwd().parents] if (p / "pyproject.toml").exists()), Path.cwd())
    df = limpiar(pd.read_csv(raiz / "data" / "titanic.csv"))
    X, y = df.drop(columns="survived"), df["survived"]
    return train_test_split(X, y, test_size=test_size, random_state=random_state)


if __name__ == "__main__":
    X_train, X_test, y_train, y_test = cargar_datos()
    pipe = construir_pipeline()
    X_train_t = pipe.fit_transform(X_train)
    X_test_t = pipe.transform(X_test)
    print(X_train_t.shape, X_test_t.shape)
    print("Nulos:", int(X_train_t.isna().sum().sum()), int(X_test_t.isna().sum().sum()))
    print(X_train_t.head())
