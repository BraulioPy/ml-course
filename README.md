# ml-course

Introduction to AI: A Machine Learning Approach

## Cómo usar este repo

1. Haz **Fork** de este repo (botón arriba a la derecha) para tener tu propia copia.
2. Clona **tu fork** y trabaja siempre dentro de la carpeta `workspace/`. No modifiques los archivos del curso.
3. Cuando haya contenido nuevo, pulsa **Sync fork** en tu fork y luego haz `git pull`.

👉 **¿Primera vez con GitHub?** Sigue la guía paso a paso: [docs/how-to-use-this-repo.md](docs/how-to-use-this-repo.md)

> Este repositorio no acepta Pull Requests. Si encuentras un error, avisa al profesor.

## Instalación rápida

Requisitos: [Git](https://git-scm.com/) y [uv](https://docs.astral.sh/uv/). uv instala Python 3.12 automáticamente.

```bash
git clone git@github.com:TU-USUARIO/ml-course.git   # tu fork
cd ml-course
uv sync
uv run python scripts/download_data.py
uv run --with jupyter jupyter lab
```

📖 **Guía completa** (macOS, Linux, Windows y Google Colab): [docs/installation.md](docs/installation.md)

## Estructura del repositorio

```
ml-course/
├── data/        # Datasets (no se versionan, se descargan con el script)
├── docs/        # Documentación del curso
├── notebooks/   # Notebooks de las clases
├── projects/    # Proyectos prácticos
├── scripts/     # Utilidades (p. ej. descarga de datos)
└── workspace/   # Tu carpeta de trabajo: aquí resuelves los ejercicios
```

## Licencia

Ver [LICENSE](LICENSE).
