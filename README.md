# LibreOffice-Format-Converter

Programa de conversión de archivos por lote que usa LibreOffice para convertirlos y recrea la carpeta principal con todos sus subdirectorios y sus archivos si los tuviera.

Probado en Debian 12:

1. **Requisitos previos**:
   - Asegúrate de tener instalado Python 3, chardet y Tkinter:
     ```
     sudo apt install python3 python3-chardet python3-tk
     ```
   - También necesitarás tener instalado LibreOffice. Puedes instalarlo con el siguiente comando:
     ```
     sudo apt install libreoffice
     ```

2. **Descargar el script**:
   - Puedes clonar el repositorio o sio sólo descarga el script `LibreOffice_Format_Converter.py`

3. **Ejecutar el programa**:
   - Abre una terminal en el directorio donde descargaste el script.
   - Ejecuta el script con el siguiente comando:
     ```
     python3 LibreOffice_Format_Converter.py
     ```
   - Esto abrirá la interfaz gráfica de usuario del programa.

4. **Usar la interfaz de usuario**:
   - Debes poner al lado del script dos carpetas, la carpeta de entrada con sus sub-carpetas si las tuviere y los archivos de texto que contenga, y la otra una carpeta vacía donde se reconstruirán toda la estructura original
   - En la ventana principal, verás los siguientes campos:
     - **Directorio de entrada**: Haz clic en el botón "Seleccionar" para elegir el directorio donde se encuentran los archivos que deseas convertir, entra en el directorio y da clic en "Ok".
     - **Formato de entrada**: Selecciona el formato de archivo actual de los archivos que deseas convertir (por ejemplo, ".txt", ".odt", ".docx", ".fodt").
     - **Directorio de salida**: Haz clic en el botón "Seleccionar" y da clic arriba en la carpeta que tiene una flecha verde hacia arriba para ir atrás un directorio, para elegir el directorio donde se guardarán los archivos convertidos.
     - **Formato de salida**: Selecciona el formato de archivo deseado para los archivos convertidos (por ejemplo, ".txt", ".odt", ".docx", ".fodt").
   - Una vez que hayas completado todos los campos, haz clic en el botón "Convertir" para iniciar el proceso de conversión.
   - Puedes ver el progreso de la conversión en la barra de progreso de la interfaz.

5. **Consideraciones adicionales**:
   - Asegúrate de que los directorios de entrada y salida sean diferentes para evitar sobrescribir los archivos originales.
   - Si el programa encuentra problemas con la codificación de los archivos de texto, intentará convertirlos a UTF-8 antes de enviarlos a LibreOffice.
   - El programa utiliza LibreOffice en modo "headless" (sin interfaz de usuario) para llevar a cabo las conversiones.
