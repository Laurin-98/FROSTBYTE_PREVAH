import nbformat
import subprocess
import time
from datetime import timedelta

# Liste der IDs

ids = [  'V1085', 'V388',
    'V375', 'V775', 'V942', 'V36', 'V8', 'V672', 'V1116', 'V1158', 'V459', 'V1040',
    'V598', 'V482', 'V475', 'V670', 'V989', 'V192', 'V293', 'V945', 'V685', 'V492',
    'V885', 'V597', 'V514', 'V932', 'V1061', 'V736', 'V165', 'V85', 'V971', 'V478',
    'V250', 'V1046', 'V508', 'V398', 'V715', 'V588', 'V1074', 'V703', 'V663', 'V557',
    'V880', 'V52', 'V436', 'V1043', 'V17', 'V941', 'V419', 'V1143', 'V655', 'V223',
    'V550', 'V901', 'V912', 'V918', 'V1128', 'V1125', 'V201', 'V12', 'V234', 'V1161',
    'V881', 'V1127', 'V884', 'V1028', 'V861', 'V157', 'V99', 'V34', 'V403', 'V607',
    'V1072', 'V683', 'V913', 'V660', 'V909', 'V935', 'V870', 'V756', 'V976', 'V353',
    'V852', 'V618', 'V509', 'V1118', 'V821', 'V539', 'V602', 'V680', 'V780', 'V747',
    'V380', 'V483', 'V878', 'V332', 'V964', 'V227', 'V286', 'V457']

# Liste der Jupyter-Notebook-Dateien
notebooks = [
    "1_RegimeClassification.ipynb",
    "2_StreamflowPreprocessing.ipynb",
    "3_SWEPreprocessing_without_P_gapfilling.ipynb",
    "4_Forecasting.ipynb",
    "5_HindcastVerification.ipynb"
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
