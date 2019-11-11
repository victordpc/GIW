<html lang="es">

<head>
    <title>Error</title>
    <meta charset="utf-8">
</head> 

<body>
    <header>
       <h1>Se ha producido un error en su petición</h1>
    </header>
    <div class="contenido">
        <p>Al realizar la petición se han pasado incorrectamente los parámetros, esperaba {{numero}} parametros, se han recibido {{actual}} :</p>
        <ul>
            % for elemento in msg:
            <li>{{elemento}}</li>
            % end
        </ul>
    </div>
</body>

</html>