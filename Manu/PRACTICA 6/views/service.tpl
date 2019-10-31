<!DOCTYPE html>
<html lang="en">
<head>
    <!-- Required meta tags -->
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">

    <title>{{dict["serviceNameToShow"]}}</title>
    <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css" integrity="sha384-ggOyR0iXCbMQv3Xipma34MD+dH/1fQ784/j6cY/iJTQUOhcWr7x9JvoRxT2MZw1T" crossorigin="anonymous">
    <link rel="stylesheet" href="/css/styles.css">
</head>
<body>

  <!-- Navigation -->
  <nav class="navbar navbar-expand-lg navbar-dark bg-dark static-top">
    <div class="container">
      <a class="navbar-brand" href="/">{{dict["serviceNameToShow"]}}</a>
      <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarResponsive" aria-controls="navbarResponsive" aria-expanded="false" aria-label="Toggle navigation">
        <span class="navbar-toggler-icon"></span>
      </button>
        <div class="collapse navbar-collapse" id="navbarResponsive">
        <ul class="navbar-nav ml-auto">
          <li class="nav-item">
            <a class="nav-link" href="/">Home</a>
          </li>
          <li class="nav-item {{!'active' if dict["serviceName"] == 'SERVICIO 1' else ""}}">
            <a class="nav-link" href="/Servicio1">Mostrar información sobre plantas</a>
          </li>
          <li class="nav-item {{!'active' if dict["serviceName"] == 'SERVICIO 2' or dict["serviceName"] == 'SERVICIO 2 BIS' else ""}}">
            <a class="nav-link" href="/Servicio2">Buscar por palabra clave</a>
          </li>
          <li class="nav-item {{!'active' if dict["serviceName"] == 'SERVICIO 3' else ""}}">
            <a class="nav-link" href="/Servicio3">Buscar por enfermedades</a>
          </li>
        </ul>
      </div>
    </div>
  </nav>

  <!-- Page Content -->
  <div class="jumbotron vertical-center">
  <div class="container">
    <div class="row">
      <div class="col-lg-12 text-center">
           %if(dict["serviceName"] == 'SERVICIO 1'):
            <div class="form-check">
                <h3>Selecciona un grupo de plantas medicinales</h3>
                <form action="/Servicio1Bis" method="post">
                    %for grupo in  dict["groupsOfPlants"].keys():
                        <input type="radio" name="grupo" value="{{grupo}}" checked>
                        {{grupo}}
                        <span>({{dict["webs"][grupo-1]}})</span>
                        <br>
                    %end
                    <br>
                    <input type="submit" class="btn btn-primary" value="Terminar la seleccion de grupo">
                </form>
            </div>



        %elif(dict["serviceName"] == 'SERVICIO 1 BIS'):

            <div>
                <h3>Selecciona una planta medicinal del grupo</h3>
                <br>
                <form action="/Service1Results" method="post">
                    %for plant in dict["selectedGroup"].items():
                        <input type="radio" name="group:plant" value="{{dict["selectedGroupIndex"]}}:{{plant[0]}}" checked>
                        {{plant[1]['nombre']}}
                        ({{plant[1]['nombre_cientifico']}})
                        <br>
                    %end
                    <br>
                    <input type="submit" class="btn btn-primary" value="Terminar la seleccion de plantas">
                </form>
            </div>

        %elif(dict["serviceName"] == 'SERVICIO 2'):

            <div class="row">
                <div class="offset-md-3 col-lg-6">
                <form action="/Servicio2Bis" method="post">
                    <h3>Introduce la palabra o palabras asociadas a la descripcion de una planta:</h3>
                    <input type="text" class="form-control mb-2 mr-sm-2" name="palabras" id="inlineFormInputName2" placeholder="Ej. gripe">
                    <button type="submit" class="btn btn-primary mb-2">Buscar</button>
                </form>
                </div>
            </div>

        %elif(dict["serviceName"] == 'SERVICIO 2 BIS'):

            <div>
                <h3>¿ Que tipo de busqueda desea realizar ?</h3>
                <form action="/Service2Results" method="post">
                    <input type="radio" name="tipoBusqueda" value="AND"> Quiero que coincidan exactamente las palabras introducidas<br>
                    <input type="radio" name="tipoBusqueda" value="OR" checked> Quiero que se busque cualquier coincidencia con las palabras introducidas<br>
                    <br>
                    <input type="submit" class="btn btn-primary" value="Enviar palabras">
                </form>
            </div>

        %elif(dict["serviceName"] == 'SERVICIO 3'):

            <div>
                <h3>Marque las enfermedades por las que desea buscar:</h3>
                <form action="/Service3Results" method="post">
                    %for disease in dict['diseases']:
                        <input type="checkbox" name="{{disease}}"> {{disease}}<br>
                    %end
                    <br>
                    <input type="submit" class="btn btn-primary" value="Obtener Plantas">
                </form>
            </div>

        %end
      </div>
    </div>
  </div>
  </div>


<script src="https://code.jquery.com/jquery-3.3.1.slim.min.js" integrity="sha384-q8i/X+965DzO0rT7abK41JStQIAqVgRVzpbzo5smXKp4YfRvH+8abtTE1Pi6jizo" crossorigin="anonymous"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.14.7/umd/popper.min.js" integrity="sha384-UO2eT0CpHqdSJQ6hJty5KVphtPhzWj9WO1clHTMGa3JDZwrnQq4sF86dIHNDz0W1" crossorigin="anonymous"></script>
<script src="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/js/bootstrap.min.js" integrity="sha384-JjSmVgyd0p3pXB1rRibZUAYoIIy6OrQ6VrjIEaFf/nJGzIxFDsf4x0xIM+B07jRM" crossorigin="anonymous"></script>
</body>
</html>