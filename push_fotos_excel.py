import subprocess

subprocess.run(["git", "add", "-A"], cwd=r"E:\sitios web\pc-custom-lab")
subprocess.run(["git", "commit", "-m", "feat(ml-fotos-excel): inclusion de Modificar_Fotos_180_HD.xlsx para subida directa"], cwd=r"E:\sitios web\pc-custom-lab")
subprocess.run(["git", "-c", "gc.auto=0", "push", "origin", "main"], cwd=r"E:\sitios web\pc-custom-lab")

subprocess.run(["git", "add", "-A"], cwd=r"E:\sitios web")
subprocess.run(["git", "commit", "-m", "feat(ml-fotos-excel): sincronizacion de Modificar_Fotos_180_HD.xlsx"], cwd=r"E:\sitios web")
subprocess.run(["git", "-c", "gc.auto=0", "push", "origin", "main"], cwd=r"E:\sitios web")
