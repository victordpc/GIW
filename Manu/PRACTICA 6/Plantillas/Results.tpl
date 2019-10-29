<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="utf-8">
    <title>{{dict["serviceNameToShow"]}}</title>
    <link rel="stylesheet" href="/Recursos/Styles.css">
</head>
<body>

    <header>
        <h1>RESULTADOS DEL SERVICIO {{dict["serviceNameToShow"]}}</h1>
    </header>

    <main>
        
        %if(dict["serviceName"] == "SERVICIO 1"):
            
            <div>
                %for property in dict["selectedGroup"][dict["plant"]].items():
                    <span> {{property[0]}} : {{property[1]}} </span>
                    <br><br>
                %end
            </div>            

        %elif(dict["serviceName"] == "SERVICIO 2"):

            <div>
                %if(len(dict["plants"]) == 0):
                    
                    <span>No se encontro ningun resultado</span>

                %else:

                    %for plant in dict["plants"].items():
                        <span>{{plant[0]}}</span>
                        <br>
                        <span>{{plant[1]}}</span>
                        <br><br>
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

                        <span>Planta: {{element[0]}}</span>
                        <div>{{element[1]}}</div>
                        <br>
                        
                    %end

                %end

            </div>

        %end

        <a href="/Recursos/Main.html">Volver al menu principal</a>

    </main>

</body>
</html>