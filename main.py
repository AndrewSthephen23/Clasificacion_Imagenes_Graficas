import tempfile
import os
from flask import Flask, request, redirect, send_file, url_for
from skimage import io
import base64
import glob
import numpy as np

app = Flask(__name__)

def render_main_html(selected_categoria=None, selected_autor=None):
    return f"""
<html>
<head></head>
<script>
  var mousePressed = false;
  var lastX, lastY;
  var ctx;

  function InitThis() {{
      ctx = document.getElementById('myCanvas').getContext("2d");

      $('#myCanvas').mousedown(function (e) {{
          mousePressed = true;
          Draw(e.pageX - $(this).offset().left, e.pageY - $(this).offset().top, false);
      }});

      $('#myCanvas').mousemove(function (e) {{
          if (mousePressed) {{
              Draw(e.pageX - $(this).offset().left, e.pageY - $(this).offset().top, true);
          }}
      }});

      $('#myCanvas').mouseup(function (e) {{
          mousePressed = false;
      }});
  	    $('#myCanvas').mouseleave(function (e) {{
          mousePressed = false;
      }});
  }}

  function Draw(x, y, isDown) {{
      if (isDown) {{
          ctx.beginPath();
          ctx.strokeStyle = 'black';
          ctx.lineWidth = 11;
          ctx.lineJoin = "round";
          ctx.moveTo(lastX, lastY);
          ctx.lineTo(x, y);
          ctx.closePath();
          ctx.stroke();
      }}
      lastX = x; lastY = y;
  }}

  function clearArea() {{
      ctx.setTransform(1, 0, 0, 1, 0, 0);
      ctx.clearRect(0, 0, ctx.canvas.width, ctx.canvas.height);
  }}

  // Enviar imagen y datos al servidor
  function prepareImg() {{
     var canvas = document.getElementById('myCanvas');
     document.getElementById('myImage').value = canvas.toDataURL();
  }}

</script>
<body onload="InitThis();">
    <script src="https://ajax.googleapis.com/ajax/libs/jquery/1.7.1/jquery.min.js" type="text/javascript"></script>
    <div align="center">
        <h1>Dibuja y selecciona la categoría y el autor</h1>
        <canvas id="myCanvas" width="200" height="200" style="border:2px solid black"></canvas>
        <br/>
        <br/>
        <button onclick="javascript:clearArea();return false;">Borrar</button>
    </div>
    
    <div align="center">
      <form method="post" action="upload" onsubmit="javascript:prepareImg();" enctype="multipart/form-data">
          <select id="categoria" name="categoria">
              <option value="gato" {"selected" if selected_categoria == "gato" else ""}>Gato</option>
              <option value="arbol" {"selected" if selected_categoria == "arbol" else ""}>Árbol</option>
              <option value="pajaro" {"selected" if selected_categoria == "pajaro" else ""}>Pájaro</option>
              <option value="bote" {"selected" if selected_categoria == "bote" else ""}>Bote</option>
          </select>
          
          <select id="autor" name="autor">
              <option value="Guillermo" {"selected" if selected_autor == "Guillermo" else ""}>Guillermo</option>
              <option value="Bustos" {"selected" if selected_autor == "Bustos" else ""}>Bustos</option>
              <option value="Andrei" {"selected" if selected_autor == "Andrei" else ""}>Andrei</option>
              <option value="Cristina" {"selected" if selected_autor == "Cristina" else ""}>Cristina</option>
          </select>
          
          <input id="myImage" name="myImage" type="hidden" value="">
          <input id="bt_upload" type="submit" value="Enviar">
      </form>
    </div>
</body>
</html>
"""

@app.route("/")
def main():
    # Capturar las selecciones de la URL, si están disponibles
    selected_categoria = request.args.get('categoria')
    selected_autor = request.args.get('autor')
    return render_main_html(selected_categoria, selected_autor)

@app.route('/upload', methods=['POST'])
def upload():
    try:
        # Procesar imagen
        img_data = request.form.get('myImage').replace("data:image/png;base64,", "")
        categoria = request.form.get('categoria')
        autor = request.form.get('autor')
        
        # Crear carpetas si no existen
        if not os.path.exists(categoria):
            os.mkdir(categoria)
        if not os.path.exists(f"{categoria}/{autor}"):
            os.mkdir(f"{categoria}/{autor}")
        
        # Guardar imagen en la carpeta correspondiente a la categoría y autor
        with tempfile.NamedTemporaryFile(delete=False, mode="w+b", suffix='.png', dir=f"{categoria}/{autor}") as fh:
            fh.write(base64.b64decode(img_data))
        
        print(f"Imagen de {categoria} hecha por autor {autor} subida con exito.")
    except Exception as e:
        print("Error al subir la imagen:", e)

    # Redirigir a la página principal con las selecciones mantenidas
    return redirect(url_for('main', categoria=categoria, autor=autor))

@app.route('/prepare', methods=['GET'])
def prepare_dataset():
    images = []
    categorias = ["gato", "arbol", "pajaro", "bote"]
    autores = ["Guillermo", "Bustos", "Andrei", "Cristina"]
    
    categoria_labels = []
    autor_labels = []
    
    # Cargar imágenes de cada categoría y autor
    for categoria in categorias:
        for autor in autores:
            path = f"{categoria}/{autor}/*.png"
            filelist = glob.glob(path)
            
            if filelist:
                images_read = io.concatenate_images(io.imread_collection(filelist))
                images_read = images_read[:, :, :, 3]  # Extraer la cuarta capa (alfa) si la imagen tiene transparencia
                
                # Etiquetas
                categoria_labels += [categorias.index(categoria)] * len(images_read)
                autor_labels += [autores.index(autor)] * len(images_read)
                
                images.append(images_read)
    
    images = np.vstack(images)  # Combinar todas las imágenes en un solo array
    categoria_labels = np.array(categoria_labels)
    autor_labels = np.array(autor_labels)
    
    # Guardar el dataset y las etiquetas
    np.save('X.npy', images)
    np.save('y_categoria.npy', categoria_labels)
    np.save('y_autor.npy', autor_labels)
    
    return "Dataset preparado y guardado como X.npy, y_categoria.npy, y_autor.npy."

@app.route('/X.npy', methods=['GET'])
def download_X():
    return send_file('./X.npy')

@app.route('/y_categoria.npy', methods=['GET'])
def download_y_categoria():
    return send_file('./y_categoria.npy')

@app.route('/y_autor.npy', methods=['GET'])
def download_y_autor():
    return send_file('./y_autor.npy')

@app.route('/listar_archivos', methods=['GET'])
def listar_archivos():
    categorias = ["gato", "arbol", "pajaro", "bote"]
    autores = ["Guillermo", "Bustos", "Andrei", "Cristina"]
    
    archivos_por_autor = {autor: {categoria: [] for categoria in categorias} for autor in autores}
    
    for categoria in categorias:
        for autor in autores:
            path = f"{categoria}/{autor}/*.png"
            filelist = glob.glob(path)
            archivos_por_autor[autor][categoria].extend(filelist)

    # Contar el total de archivos
    total_archivos = sum(len(archivos_por_autor[autor][categoria]) for autor in autores for categoria in categorias)
    
    response = f"<h1>Listado de Archivos</h1>"
    response += f"<p>Total de archivos: {total_archivos}</p>"
    
    for autor in autores:
        response += f"<h2>Autor: {autor}</h2>"
        for categoria in categorias:
            archivos = archivos_por_autor[autor][categoria]
            response += f"<h3>Categoría: {categoria}</h3>"
            response += "<ul>"
            for archivo in archivos:
                response += f"<li>{os.path.basename(archivo)}</li>"
            response += "</ul>"
    
    response += '<a href="/">Volver a la página principal</a>'
    return response



if __name__ == "__main__":
    categorias = ['gato', 'arbol', 'pajaro', 'bote']
    autores = ["Guillermo", "Bustos", "Andrei", "Cristina"]
    
    for categoria in categorias:
        for autor in autores:
            if not os.path.exists(f"{categoria}/{autor}"):
                os.makedirs(f"{categoria}/{autor}")
    app.run()
