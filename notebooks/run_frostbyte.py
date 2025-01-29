import nbformat
import subprocess
import time
from datetime import timedelta
## IMPORTANT: if you run FROSTBYTE with this file uncomment in each notebook the definition "test_basin_id = 'some_id". the definition "test_basin_id = settings['domain']" can be used if you only want to run one testbasin manually.
# Liste der IDs

ids = [
    'V8', 'V31', 'V52', 'V85', 'V99', 'V192', 'V200', 'V208', 'V234', 'V250',
    'V286', 'V316', 'V353', 'V365', 'V408', 'V458', 'V459', 'V482', 'V483',
    'V499', 'V500', 'V509', 'V514', 'V520', 'V539', 'V557', 'V566', 'V588',
    'V597', 'V633', 'V663', 'V670', 'V672', 'V685', 'V703', 'V713', 'V736',
    'V747', 'V756', 'V775', 'V780', 'V815', 'V878', 'V880', 'V884', 'V912',
    'V913', 'V941', 'V942', 'V971', 'V976', 'V1010', 'V1040', 'V1061',
    'V1079', 'V1127', 'V1161'
]

# Liste der Jupyter-Notebook-Dateien
## if only nival uncomment this definition of "notebooks" (and comment the nivo-glacial part)
"""
notebooks = [
    "1_RegimeClassification.ipynb",
    "2_StreamflowPreprocessing.ipynb",
    "3_SWEPreprocessing_without_P_gapfilling.ipynb",
    "4_Forecasting.ipynb",
    "5_HindcastVerification.ipynb"
]
"""
## if nival and nivo-glacial basins uncomment this definition of "notebooks" (and comment the nival part)
notebooks = [
    "1_RegimeClassification.ipynb",
    "2_glac_StreamflowPreprocessing.ipynb",
    "3_SWEPreprocessing_without_P_gapfilling.ipynb",
    "4_glac_Forecasting.ipynb",
    "5_glac_HindcastVerification.ipynb"
]

# Funktion, um die test_basin_id in einem Notebook zu ersetzen
def set_basin_id(notebook_path, basin_id):
    try:
        with open(notebook_path, 'r') as f:
            nb = nbformat.read(f, as_version=4)

        replacement_done = False
        for cell in nb.cells:
            if cell.cell_type == 'code' and not replacement_done:
                if 'test_basin_id' in cell.source:
                    cell_lines = cell.source.split('\n')
                    for i, line in enumerate(cell_lines):
                        if 'test_basin_id' in line:
                            cell_lines[i] = f"test_basin_id = '{basin_id}'  # Set basin_id for testing"
                            replacement_done = True
                            break
                    cell.source = '\n'.join(cell_lines)

        with open(notebook_path, 'w') as f:
            nbformat.write(nb, f)
        print(f"test_basin_id erfolgreich auf {basin_id} in {notebook_path} gesetzt.")
    except Exception as e:
        print(f"Fehler beim Setzen der test_basin_id in {notebook_path}: {e}")

# Funktion zur Ausführung von Notebooks mit --allow-errors
def run_notebook(notebook_path):
    try:
        # Befehl zum Ausführen des Notebooks, auch wenn Fehler auftreten (--allow-errors)
        command = [
            "jupyter", "nbconvert",
            "--to", "notebook",
            "--execute",
            "--inplace",
            "--allow-errors",  # Fehler werden zugelassen, sodass die Ausführung nicht stoppt
            notebook_path
        ]
        subprocess.run(command, check=True)
        print(f"Notebook {notebook_path} wurde erfolgreich ausgeführt.")
    except subprocess.CalledProcessError as e:
        print(f"Fehler beim Ausführen von {notebook_path}: {e}")
    except Exception as e:
        print(f"Ein unerwarteter Fehler trat bei der Ausführung von {notebook_path} auf: {e}")

# Startzeit messen
start_time = time.time()

# Schleife durch alle IDs und Notebooks
for basin_id in ids:
    print(f"\n--- Starte Verarbeitung für Basin ID {basin_id} ---\n")
    for notebook_path in notebooks:
        # Setze die test_basin_id im aktuellen Notebook
        set_basin_id(notebook_path, basin_id)
        # Führe das Notebook aus
        run_notebook(notebook_path)

# Endzeit messen
end_time = time.time()

total_time = timedelta(seconds=end_time - start_time)
print(f"\nGesamtlaufzeit: {total_time}")
