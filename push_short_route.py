import subprocess

subprocess.run(["git", "add", "-A"], cwd=r"E:\sitios web\pc-custom-lab")
subprocess.run(["git", "commit", "-m", "feat(img-short): ruta de imagenes ultra-corta /img/ y plantillas oficiales optimizadas"], cwd=r"E:\sitios web\pc-custom-lab")
subprocess.run(["git", "-c", "gc.auto=0", "push", "origin", "main"], cwd=r"E:\sitios web\pc-custom-lab")

subprocess.run(["git", "add", "-A"], cwd=r"E:\sitios web")
subprocess.run(["git", "commit", "-m", "feat(img-short): sincronizacion de plantillas oficiales optimizadas"], cwd=r"E:\sitios web")
subprocess.run(["git", "-c", "gc.auto=0", "push", "origin", "main"], cwd=r"E:\sitios web")
