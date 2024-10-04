# Clasificación de Dibujos con Flask y CNN

Este proyecto es una aplicación web en **Flask** que permite a los usuarios dibujar imágenes, asignarles una categoría y un autor, y guardar estas imágenes en una estructura organizada para crear un dataset etiquetado. Este dataset puede luego ser utilizado para entrenar una red neuronal convolucional (CNN) en tareas de clasificación.

## Funcionalidades Principales

1. **Página de Dibujo Interactiva**:
    - Los usuarios pueden dibujar en un lienzo HTML, seleccionar una categoría (gato, árbol, pájaro, bote) y un autor (Guillermo, Bustos, Andrei, Cristina).
    - La imagen se envía y guarda en una carpeta específica organizada por categoría y autor.
2. **Preparación del Dataset**:
    - Una ruta especial (`/prepare`) carga las imágenes almacenadas, genera etiquetas de categoría y autor, y guarda los datos como archivos `.npy` (`X.npy`, `y_categoria.npy`, `y_autor.npy`), listos para el entrenamiento del modelo.
3. **Descarga de Datos**:
    - Se puede acceder a los archivos `X.npy`, `y_categoria.npy`, y `y_autor.npy` mediante rutas específicas, permitiendo descargar los datos procesados.
4. **Visualización del Dataset**:
    - Una ruta de listado (`/listar_archivos`) muestra la cantidad total de archivos y detalla las imágenes guardadas en cada categoría y autor.

## Estructura de Archivos

- **/categoria/autor/**: Carpetas organizadas por categorías y autores, donde se almacenan las imágenes.
- **X.npy, y_categoria.npy, y_autor.npy**: Archivos de dataset que contienen las imágenes y sus etiquetas.

## Cómo Empezar

1. Clona el repositorio y navega al directorio del proyecto:
    
    ```bash
    git clone <URL_DEL_REPOSITORIO>
    cd Clasificacion_Dibujos
    ```
    
2. Instala las dependencias:
    
    ```bash
    pip install -r requirements.txt
    ```
    
3. Ejecuta la aplicación:
    
    ```bash
    python main.py
    ```
    
4. Accede a `http://127.0.0.1:5000/` en tu navegador para comenzar a dibujar y etiquetar imágenes.

Link del stitio web:

[https://web-production-e4e8.up.railway.app/](https://web-production-e4e8.up.railway.app/)

Link del notebook Colab del modelo de red neuronal convolucional

https://colab.research.google.com/drive/1mtiws6ZppgV2r0ZYLp4ReC4_AvhgVxnG?usp=sharing