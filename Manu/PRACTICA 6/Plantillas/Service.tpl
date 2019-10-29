<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>{{dict["serviceNameToShow"]}}</title>
    <link rel="stylesheet" href="/Recursos/Styles.css">
</head>
<body>

    <header>
        <h1>BIENVENIDO AL {{dict["serviceNameToShow"]}}</h1>
    </header>

    <main>
	
        %if(dict["serviceName"] == 'SERVICIO 1'):
        
            <div>
                <span>Selecciona un grupo de plantas medicinales</span>
                <form action="/Servicio1Bis" method="post">
                    %for grupo in  dict["groupsOfPlants"].keys():
                        <input type="radio" name="grupo" value="{{grupo}}" checked>
                        {{grupo}}
                        <span>({{dict["webs"][grupo-1]}})</span>
                        <br> 
                    %end
                    <input type="submit" value="Terminar la seleccion de grupo">
                </form>
            </div>

        %elif(dict["serviceName"] == 'SERVICIO 1 BIS'):

            <div>
                <span>Selecciona una planta medicinal del grupo</span>
                <br>
                <form action="/Service1Results" method="post">
                    %for plant in dict["selectedGroup"].items():
                        <input type="radio" name="group:plant" value="{{dict["selectedGroupIndex"]}}:{{plant[0]}}" checked>
                        {{plant[1]['nombre']}}
                        ({{plant[1]['nombre_cientifico']}})
                        <br> 
                    %end
                    <input type="submit" value="Terminar la seleccion de plantas">
                </form>
            </div>

        %elif(dict["serviceName"] == 'SERVICIO 2'):
            
            <div>
                <form action="/Servicio2Bis" method="post">
                    Introduce la palabra o palabras asociadas a la descripcion de una planta:
                    <input type="text" name="palabras">
                    <br>
                    <input type="submit" value="Enviar palabras">
                </form>
            </div>

        %elif(dict["serviceName"] == 'SERVICIO 2 BIS'):

            <div>
                ¿ Que tipo de busqueda desea realizar ?
                <form action="/Service2Results" method="post">
                    <input type="radio" name="tipoBusqueda" value="AND">Quiero que coincidan exactamente las palabras introducidas<br>
                    <input type="radio" name="tipoBusqueda" value="OR" checked>Quiero que se busque cualquier coincidencia con las palabras introducidas<br>
                    <input type="submit" value="Enviar palabras">
                </form>
            </div>

        %elif(dict["serviceName"] == 'SERVICIO 3'):

            <div>
                %import csv
                %csvFile = open('Recursos/Enfermedades.csv',encoding="utf-8",errors='ignore')
                %reader = csv.reader(csvFile, delimiter=";")
                <form action="/Service3Results" method="post">
                    %for data in reader:
                        <input type="checkbox" name="{{"".join(data)}}">{{"".join(data)}}<br>
                    %end
                    %csvFile.close();
                    <input type="submit" value="Obtener Plantas">
                </form>
            </div>

        %end

        <a href="/Recursos/Main.html">Volver al menu principal</a>
    
    </main>

</body>
</html>