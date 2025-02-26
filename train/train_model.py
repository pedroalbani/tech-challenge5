import subprocess
import data_loader

# TODO
subprocess.run(["python", "primeiro arquivo aqui.py"], check=True)

df = data_loader.load_data()

print(f"Dados carregados: {df.shape}")
