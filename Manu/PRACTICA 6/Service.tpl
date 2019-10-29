<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>{{dict["serviceName"]}}</title>
    <link rel="stylesheet" href="Styles.css">
</head>
<body>

    <header>
        <h1>BIEN VENIDO AL {{dict["serviceName"]}}</h1>
    </header>

    <main>
	
        %if(dict["serviceName"] == 'SERVICIO 1'):
        
            <div>
                <span>Selecciona un grupo de plantas medicinales</span>
                <form action="/Servicio1Bis" method="post">
                    %for grupo in  dict["groupsOfPlants"].keys():
                        <input type="radio" name="grupo" value="{{grupo}}">{{grupo}}<br> 
                    %end
                    <input type="submit" value="Terminar la seleccion de grupo">
                </form>
            </div>

        %elif(dict["serviceName"] == 'SERVICIO 1 BIS'):

            <div>
                <span>Selecciona una planta medicinal del grupo</span>
                <br>
                <form action="/Service1Results" method="post">
                    %for i in dict["selectedGroup"]:
                        <input type="radio" name=""> {{i}} 
                    %end
                    <input type="submit" value="Terminar la seleccion de plantas">
                </form>
            </div>

        %elif(dict["serviceName"] == 'SERVICIO 2'):
            
            <div>
                Cuerpo del servicio 2
            </div>

        %elif(dict["serviceName"] == 'SERVICIO 3'):

            <div>
                %import csv
                %csvFile = open('Enfermedades.csv',encoding="utf-8",errors='ignore')
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

        <a href="/MainMenu">Volver al menu principal</a>
    
    </main>

</body>
</html>