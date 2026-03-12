import os
import subprocess

if os.getenv("CI"):
    commands = [
        [
            "rendercv",
            "render",
            "JuanFranMartin_English_CV.yaml",
            "--pdf-path",
            "./rendercv_output_prod/JuanFranMartin_English_CV.pdf",
        ],
        [
            "rendercv",
            "render",
            "JuanFranMartin_Spanish_CV.yaml",
            "--pdf-path",
            "./rendercv_output_prod/JuanFranMartin_Spanish_CV.pdf",
        ],
    ]
else:
    commands = [
        [
            "rendercv",
            "render",
            "JuanFranMartin_English_CV.yaml",
            "--pdf-path",
            "./rendercv_output_local/JuanFranMartin_English_CV.pdf",
        ],
        [
            "rendercv",
            "render",
            "JuanFranMartin_Spanish_CV.yaml",
            "--pdf-path",
            "./rendercv_output_local/JuanFranMartin_Spanish_CV.pdf",
        ],
    ]


for cmd in commands:
    print(f"Ejecutando: {' '.join(cmd)}")
    result = subprocess.run(cmd)
    if result.returncode == 0:
        print("✅ Completado\n")
    else:
        print(f"❌ Error (código {result.returncode})\n")
