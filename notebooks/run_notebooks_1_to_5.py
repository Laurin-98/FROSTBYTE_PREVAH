import subprocess
from datetime import datetime

# Startzeit aufzeichnen
start_time = datetime.now()

# Liste der Jupyter-Notebook-Dateien
notebooks = [
    "1_RegimeClassification.ipynb",
    "2_glac_StreamflowPreprocessing.ipynb",
    #"2_StreamflowPreprocessing.ipynb",
    #"3_SWEPreprocessing.ipynb",
    "3_SWEPreprocessing_without_P_gapfilling.ipynb",
    "4_Forecasting.ipynb",
    "5_HindcastVerification.ipynb"
]

# Funktion zur Ausführung von Notebooks mit --allow-errors
def run_notebook(notebook):
    try:
        # Befehl zum Ausführen des Notebooks, auch wenn Fehler auftreten (--allow-errors)
        command = [
            "jupyter", "nbconvert",
            "--to", "notebook",
            "--execute",
            "--inplace",
            "--allow-errors",  # Fehler werden zugelassen, sodass die Ausführung nicht stoppt
            notebook
        ]
        subprocess.run(command, check=True)
        print(f"Notebook {notebook} wurde erfolgreich ausgeführt.")
    except subprocess.CalledProcessError as e:
        print(f"Fehler beim Ausführen von {notebook}: {e}")
    except Exception as e:
        # Fängt alle anderen Fehler ab, falls subprocess fehlschlägt
        print(f"Ein unerwarteter Fehler trat bei der Ausführung von {notebook} auf: {e}")

# Notebooks nacheinander ausführen
for notebook in notebooks:
    run_notebook(notebook)
# Endzeit aufzeichnen
end_time = datetime.now()
# Laufzeit berechnen und anzeigen
elapsed_time = end_time - start_time
print(f"Laufzeit: {elapsed_time}")