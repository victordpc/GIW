<html lang="es">

<head>
    <title>Mostrar resultados</title>
    <meta charset="utf-8">
</head> 

<body>
    <header>
       <h1>Resultados encontrados</h1>
    </header>
    <div class="contenido">
        <table>

            % for elemento in datos:
            <li>{{elemento}}</li>
            % end
        </table>
    </div>
</body>

</html>
