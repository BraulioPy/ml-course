# Guía de instalación

Esta guía explica cómo preparar tu entorno para el curso en **macOS**, **Linux**, **Windows (PowerShell)** o **Google Colab**.

Usamos [**uv**](https://docs.astral.sh/uv/) para gestionar todo: instala Python 3.12, crea el entorno virtual (`.venv`) e instala las dependencias exactas del archivo `uv.lock`. No necesitas instalar Python por separado ni usar `pip`, `venv` o `conda`.

> ¿No quieres instalar nada? Ve directo a [Google Colab](#opción-b-google-colab).

---

## Contenido

- [Opción A: instalación local](#opción-a-instalación-local)
  1. [Instalar Git](#1-instalar-git)
  2. [Instalar uv](#2-instalar-uv)
  3. [Instalar Python 3.12](#3-instalar-python-312)
  4. [Clonar el repositorio](#4-clonar-el-repositorio)
  5. [Crear el entorno e instalar dependencias](#5-crear-el-entorno-e-instalar-dependencias)
  6. [Descargar los datos](#6-descargar-los-datos)
  7. [Abrir los notebooks](#7-abrir-los-notebooks)
- [Opción B: Google Colab](#opción-b-google-colab)
- [Comandos útiles de uv](#comandos-útiles-de-uv)
- [Problemas comunes](#problemas-comunes)

---

## Opción A: instalación local

### 1. Instalar Git

Comprueba si ya lo tienes:

```bash
git --version
```

Si no aparece una versión, instálalo:

| Sistema | Comando |
|---|---|
| macOS | `xcode-select --install` |
| Linux (Debian/Ubuntu) | `sudo apt update && sudo apt install git` |
| Linux (Fedora) | `sudo dnf install git` |
| Windows (PowerShell) | `winget install --id Git.Git -e` |

### 2. Instalar uv

**macOS y Linux**

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

Si no tienes `curl`, usa `wget -qO- https://astral.sh/uv/install.sh | sh`. En macOS también puedes usar Homebrew: `brew install uv`.

**Windows (PowerShell)**

```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

También puedes usar `winget install --id=astral-sh.uv -e`.

**Verifica la instalación.** Cierra y vuelve a abrir la terminal, y luego ejecuta:

```bash
uv --version
```

### 3. Instalar Python 3.12

```bash
uv python install 3.12
```

Puedes ver las versiones disponibles e instaladas con `uv python list`.

> Este paso es opcional: el repositorio incluye un archivo `.python-version` con `3.12`, y `uv sync` (paso 5) descargará Python 3.12 automáticamente si no lo encuentra.

### 4. Clonar el repositorio

Primero haz **fork** del repo y configura SSH. Si nunca has usado GitHub, sigue [docs/how-to-use-this-repo.md](how-to-use-this-repo.md) (pasos 1 y 2) y [docs/github-ssh.md](github-ssh.md).

Luego clona **tu fork**:

```bash
git clone git@github.com:TU-USUARIO/ml-course.git
cd ml-course
```

### 5. Crear el entorno e instalar dependencias

```bash
uv sync
```

Esto crea la carpeta `.venv/` e instala las versiones exactas definidas en `uv.lock`, así que todos trabajamos con el mismo entorno.

Para ejecutar código tienes dos opciones:

**a) Con `uv run`** (recomendado, no hace falta activar nada):

```bash
uv run python scripts/download_data.py
```

**b) Activando el entorno virtual:**

| Sistema | Comando |
|---|---|
| macOS / Linux | `source .venv/bin/activate` |
| Windows (PowerShell) | `.venv\Scripts\Activate.ps1` |

Para salir del entorno: `deactivate`.

### 6. Descargar los datos

Desde la raíz del repo:

```bash
uv run python scripts/download_data.py
```

El script descarga (o genera) los datasets del curso y los guarda como CSV en `data/`:

| Archivo | Origen | Para qué |
|---|---|---|
| `viviendas.csv` | sintético | Introducción a pandas |
| `viviendas_sucio.csv` | sintético | Limpieza de datos (las mismas viviendas, con errores a propósito) |
| `titanic.csv`, `penguins.csv`, `tips.csv` | seaborn | Exploración y limpieza de datos reales |
| `iris.csv`, `breast_cancer.csv` | scikit-learn | Clasificación |
| `california_housing.csv` | scikit-learn | Regresión |

Necesita conexión a internet. Puedes ejecutarlo todas las veces que quieras: vuelve a crear los archivos.

Los datos se guardan en `data/`. Esa carpeta está en el `.gitignore`, así que los datasets **no** se suben al repositorio.

### 7. Abrir los notebooks

**Jupyter Lab**

```bash
uv run --with jupyter jupyter lab
```

**VS Code**

1. Instala las extensiones **Python** y **Jupyter**.
2. Abre la carpeta `ml-course`.
3. Abre un notebook y, en **Select Kernel**, elige el intérprete de `.venv` (`.venv/bin/python` en macOS/Linux, `.venv\Scripts\python.exe` en Windows).

---

## Opción B: Google Colab

[Google Colab](https://colab.research.google.com/) ofrece un entorno de Python en la nube con GPU gratuita, sin instalar nada. Solo necesitas una cuenta de Google.

### Abrir un notebook del repositorio

Sustituye `<ruta>` por la ruta del notebook dentro del repo:

```
https://colab.research.google.com/github/riosinda/ml-course/blob/main/<ruta>.ipynb
```

Por ejemplo: [`.../blob/main/notebooks/lectures/chapter_00/00_intro_to_jupyter.ipynb`](https://colab.research.google.com/github/riosinda/ml-course/blob/main/notebooks/lectures/chapter_00/00_intro_to_jupyter.ipynb)

También puedes ir a **Archivo → Abrir cuaderno → GitHub** y buscar `riosinda/ml-course`.

### Preparar el entorno dentro de Colab

Ejecuta esta celda al inicio del notebook:

```python
!git clone -q https://github.com/riosinda/ml-course.git
%cd ml-course

# Instala las dependencias del proyecto con uv (mucho más rápido que pip)
!pip install -q uv
!uv pip install --system -q -r pyproject.toml

# Descarga los datos
!python scripts/download_data.py
```

### Guardar tu trabajo

Colab **borra todo** lo que hay en `/content` cuando se cierra la sesión. Para conservar datos o resultados, monta tu Google Drive:

```python
from google.colab import drive
drive.mount("/content/drive")
```

Y guarda en `/content/drive/MyDrive/...`. Para guardar el notebook en sí: **Archivo → Guardar una copia en Drive**.

### Activar GPU (opcional)

**Entorno de ejecución → Cambiar tipo de entorno de ejecución → T4 GPU**.

---

## Comandos útiles de uv

| Comando | Qué hace |
|---|---|
| `uv sync` | Crea o actualiza `.venv` según `uv.lock` |
| `uv add <paquete>` | Añade una dependencia (actualiza `pyproject.toml` y `uv.lock`) |
| `uv add --dev <paquete>` | Añade una dependencia solo de desarrollo |
| `uv remove <paquete>` | Elimina una dependencia |
| `uv run <comando>` | Ejecuta un comando dentro del entorno del proyecto |
| `uv lock --upgrade` | Actualiza las versiones del lockfile |
| `uv python list` | Lista las versiones de Python disponibles |

> Si añades dependencias, sube a Git **`pyproject.toml` y `uv.lock`** juntos.

---

## Problemas comunes

**`uv: command not found` / `uv no se reconoce como comando`**
Cierra y vuelve a abrir la terminal. En macOS/Linux también puedes ejecutar `source $HOME/.local/bin/env`.

**Windows: "la ejecución de scripts está deshabilitada en este sistema"** al activar `.venv`
Ejecuta una vez en PowerShell:

```powershell
Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned
```

O usa `uv run`, que no necesita activar el entorno.

**El entorno quedó en mal estado**
Borra `.venv` y vuelve a crearlo:

```bash
rm -rf .venv      # macOS / Linux
# Remove-Item -Recurse -Force .venv   # Windows (PowerShell)
uv sync
```

**Archivos `._*` en un disco externo (macOS)**
Si el repo está en un disco con formato ExFAT, macOS crea archivos `._*`. Ya están en el `.gitignore`; para borrarlos ejecuta `dot_clean -m .`.
