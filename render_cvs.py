import subprocess

commands = [
    [
        "rendercv",
        "render",
        "JuanFranMartin_English_CV.yaml",
        "--pdf-path",
        "JuanFranMartin_English_CV.pdf",
    ],
    [
        "rendercv",
        "render",
        "JuanFranMartin_Spanish_CV.yaml",
        "--pdf-path",
        "JuanFranMartin_Spanish_CV.pdf",
    ],
]

for cmd in commands:
    print(f"Ejecutando: {' '.join(cmd)}")
    result = subprocess.run(cmd)
    if result.returncode == 0:
        print("✅ Completado\n")
    else:
        print(f"❌ Error (código {result.returncode})\n")
