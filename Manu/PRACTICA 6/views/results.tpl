<!DOCTYPE html>
<html lang="en">
<head>
    <!-- Required meta tags -->
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">

    <title>GIW - {{dict["serviceNameToShow"]}}</title>
    <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css" integrity="sha384-ggOyR0iXCbMQv3Xipma34MD+dH/1fQ784/j6cY/iJTQUOhcWr7x9JvoRxT2MZw1T" crossorigin="anonymous">
    <link rel="stylesheet" href="/css/styles.css">
</head>
<body>


  <!-- Navigation -->
  <nav class="navbar sticky-top navbar-expand-lg navbar-dark bg-dark">
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
           %if(dict["serviceName"] == "SERVICIO 1"):

            <div>
            <div class="card">
  <div class="card-body">
    <h5 class="card-title">{{dict["selectedGroup"][dict["plant"]]['nombre']}}</h5>
    <h6 class="card-subtitle mb-2 text-muted">{{dict["selectedGroup"][dict["plant"]]['nombre_cientifico']}}</h6>
    <p class="card-text">
    {{dict["selectedGroup"][dict["plant"]]['descripcion']}}
    </p>
  </div>
</div>
            </div>

        %elif(dict["serviceName"] == "SERVICIO 2"):
            <h3>Resultados de búsqueda: </h3><br>
            <div class="row">
                %if(len(dict["plants"]) == 0):

                    <span>No se encontro ningun resultado</span>

                %else:

                    %for plant in dict["plants"].items():
                         <div class="card col-md-6">
  <div class="card-body">
    <h5 class="card-title">{{plant[0]}}</h5>
    <p class="card-text">
    {{plant[1]}}
    </p>
  </div>
</div>
    <br>

                    %end

                %end
            </div>

        %elif(dict["serviceName"] == "SERVICIO 3"):

            <div>

                %if(len(dict["diseases"]) == 0 or len(dict["plantsForDiseases"]) == 0):

                    <span>No se encontro ningun resultado</span>
                    <br>

                %else:

                    %for element in dict["plantsForDiseases"].items():

            <div class="card">
  <div class="card-body">
    <h5 class="card-title">{{element[0]}}</h5>
    <p class="card-text">
    {{element[1]}}
    </p>
  </div>
</div>
<br>

                    %end

                %end

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