<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="utf-8">
    <title>Resultados</title>
    <link rel="stylesheet" href="Styles.css">
    <!-- GOOGLE-FONTS
    <link rel="stylesheet" href="https://fonts.googleapis.com/css?family=">
    -->
    <!-- PRINTER-VIEW
    <link rel="stylesheet" href="*.css" media="print">
    -->
    <!-- LOAD JAVASCRIPT 
    <script src="*.js"></script> 
    -->
</head>
<body>

    <header>
        <h1>RESULTADOS DEL SERVICIO {{dict["serviceName"]}}</h1>
    </header>

    <main>
        
        %if(dict["serviceName"] == "SERVICIO 1"):
            
            <div>RESULTADOS DEL SERVICIO 1</div>            

        %elif(dict["serviceName"] == "SERVICIO 2"):

            <div>RESULTADOS DEL SERVICIO 2</div>

        %elif(dict["serviceName"] == "SERVICIO 3"):

            %for element in dict["plantsForDiseases"].items():

                <span>Planta: {{element[0]}}</span>
                <div>{{element[1]}}</div>
                <br>
                
            %end

        %end

        <a href="/MainMenu">Volver al menu principal</a>

    </main>

</body>
</html>