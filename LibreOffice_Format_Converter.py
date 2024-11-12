import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import os
import subprocess
import threading
import chardet

class FileConverterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Conversor de Archivos")
        self.root.geometry("620x350")

        # Variables
        self.input_dir = tk.StringVar()
        self.output_dir = tk.StringVar()
        self.input_format = tk.StringVar(value=".txt")
        self.output_format = tk.StringVar(value=".odt")

        # Widgets de entrada
        tk.Label(root, text="Directorio de entrada:").grid(row=0, column=0, padx=10, pady=10, sticky="e")
        tk.Entry(root, textvariable=self.input_dir, width=40).grid(row=0, column=1, padx=10)
        tk.Button(root, text="Seleccionar", command=self.select_input_dir).grid(row=0, column=2)

        tk.Label(root, text="Formato de entrada:").grid(row=1, column=0, padx=10, pady=10, sticky="e")
        input_format_menu = ttk.Combobox(root, textvariable=self.input_format, values=[".txt", ".odt", ".docx", ".fodt"])
        input_format_menu.grid(row=1, column=1, padx=10, pady=10, sticky="w")

        # Widgets de salida
        tk.Label(root, text="Directorio de salida:").grid(row=2, column=0, padx=10, pady=10, sticky="e")
        tk.Entry(root, textvariable=self.output_dir, width=40).grid(row=2, column=1, padx=10)
        tk.Button(root, text="Seleccionar", command=self.select_output_dir).grid(row=2, column=2)

        tk.Label(root, text="Formato de salida:").grid(row=3, column=0, padx=10, pady=10, sticky="e")
        output_format_menu = ttk.Combobox(root, textvariable=self.output_format, values=[".txt", ".odt", ".docx", ".fodt"])
        output_format_menu.grid(row=3, column=1, padx=10, pady=10, sticky="w")

        # Botón de conversión
        tk.Button(root, text="Convertir", command=self.start_conversion).grid(row=4, column=1, pady=10)

        # Barra de progreso
        self.progress = ttk.Progressbar(root, orient="horizontal", length=400, mode="determinate")
        self.progress.grid(row=5, column=0, columnspan=3, padx=10, pady=20)

    def select_input_dir(self):
        self.input_dir.set(filedialog.askdirectory())

    def select_output_dir(self):
        self.output_dir.set(filedialog.askdirectory())

    def start_conversion(self):
        # Iniciar el proceso de conversión en un hilo separado
        threading.Thread(target=self.convert_files).start()

    def convert_files(self):
        # Verificar entradas
        if not self.input_dir.get() or not self.output_dir.get():
            messagebox.showerror("Error", "Seleccione directorios de entrada y salida.")
            return
        if self.input_format.get() == self.output_format.get():
            messagebox.showerror("Error", "El formato de entrada y salida no pueden ser iguales.")
            return

        # Contar archivos para el progreso
        total_files = sum(len(files) for _, _, files in os.walk(self.input_dir.get()) if any(f.endswith(self.input_format.get()) for f in files))
        processed_files = 0
        self.progress["value"] = 0
        self.progress["maximum"] = total_files

        # Convertir archivos
        for root_dir, _, files in os.walk(self.input_dir.get()):
            relative_path = os.path.relpath(root_dir, self.input_dir.get())
            output_subdir = os.path.join(self.output_dir.get(), relative_path)
            os.makedirs(output_subdir, exist_ok=True)

            for file in files:
                if file.endswith(self.input_format.get()):
                    input_file_path = os.path.join(root_dir, file)
                    output_file_name = os.path.splitext(file)[0] + self.output_format.get()
                    output_file_path = os.path.join(output_subdir, output_file_name)

                    # Detectar y convertir el archivo con la codificación correcta
                    if self.input_format.get() == ".txt":
                        temp_file_path = self.convert_to_utf8(input_file_path)
                        self.convert_with_libreoffice(temp_file_path, output_file_path)
                        os.remove(temp_file_path)  # Eliminar archivo temporal
                    else:
                        self.convert_with_libreoffice(input_file_path, output_file_path)

                    # Actualizar progreso
                    processed_files += 1
                    self.progress["value"] = processed_files
                    self.root.update_idletasks()  # Refrescar la interfaz

        messagebox.showinfo("Éxito", "La conversión ha finalizado.")

    def convert_to_utf8(self, file_path):
        # Detectar la codificación
        with open(file_path, 'rb') as f:
            result = chardet.detect(f.read())
        encoding = result['encoding']

        # Leer el archivo con la codificación detectada y guardarlo en UTF-8
        temp_file_path = os.path.join("/tmp", os.path.basename(file_path))  # Guardar en /tmp
        with open(file_path, 'r', encoding=encoding) as f:
            content = f.read()
        with open(temp_file_path, 'w', encoding='utf-8') as f:
            f.write(content)

        return temp_file_path

    def convert_with_libreoffice(self, input_file, output_file):
        output_dir = os.path.dirname(output_file)
        command = [
            "libreoffice", "--headless", "--convert-to",
            os.path.splitext(output_file)[1][1:],  # Remove dot from extension
            "--outdir", output_dir, input_file
        ]
        subprocess.run(command, check=True)

# Crear la aplicación
root = tk.Tk()
app = FileConverterApp(root)
root.mainloop()

