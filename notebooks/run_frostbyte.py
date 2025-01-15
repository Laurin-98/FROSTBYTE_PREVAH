import nbformat
from nbconvert.preprocessors import ExecutePreprocessor
import time
from datetime import timedelta

# Liste der IDs
ids = ['V135', 'V1010']

# Liste der Jupyter-Notebook-Dateien
notebooks = [
    "1_RegimeClassification.ipynb",
    "2_StreamflowPreprocessing.ipynb",
    "3_SWEPreprocessing_without_P_gapfilling.ipynb",
    "4_Forecasting.ipynb",
    "5_HindcastVerification.ipynb"
]

# Funktion, um die test_basin_id in einem Notebook zu ersetzen
def set_basin_id(notebook, basin_id):
    replacement_done = False
    for cell in notebook.cells:
        if cell.cell_type == 'code' and not replacement_done:
            if 'test_basin_id' in cell.source:
                cell_lines = cell.source.split('\n')
                for i, line in enumerate(cell_lines):
                    if 'test_basin_id' in line:
                        cell_lines[i] = f"test_basin_id = '{basin_id}'  # Set basin_id for testing"
                        replacement_done = True
                        break
                cell.source = '\n'.join(cell_lines)
    return notebook

# Funktion, um ein Notebook auszuführen
def run_notebook(notebook_path, basin_id):
    try:
        with open(notebook_path) as f:
            nb = nbformat.read(f, as_version=4)

        # Setze die test_basin_id im Notebook
        nb = set_basin_id(nb, basin_id)

        # Notebook ausführen
        ep = ExecutePreprocessor(timeout=600, kernel_name='python3')
        ep.preprocess(nb, {'metadata': {'path': './'}})
        print(f"Notebook {notebook_path} erfolgreich ausgeführt für Basin ID {basin_id}.")

    except Exception as e:
        print(f"Fehler beim Ausführen von {notebook_path} für Basin ID {basin_id}: {e}")

# Startzeit messen
start_time = time.time()

# Schleife durch alle IDs und Notebooks
for basin_id in ids:
    print(f"\n--- Starte Verarbeitung für Basin ID {basin_id} ---\n")
    for notebook_path in notebooks:
        run_notebook(notebook_path, basin_id)

# Endzeit messen
end_time = time.time()

total_time = timedelta(seconds=end_time - start_time)
print(f"\nGesamtlaufzeit: {total_time}")
