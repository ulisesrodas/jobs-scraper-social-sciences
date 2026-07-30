import pandas as pd
from jobspy import scrape_jobs

# Lista de carreras o términos exactos que deseas buscar
carreras = [
    "Sociologia", 
    "Antropologia", 
    "Ciencia Politica", 
    "Ciencias Sociales", 
    "Relaciones Internacionales"
]

# Lista vacía para ir guardando los resultados de cada iteración
todos_los_empleos = []

print("Iniciando extracción por carrera en Perú...\n")

for carrera in carreras:
    print(f"Buscando convocatorias para: {carrera}")
    try:
        # Ejecutamos el scraper para cada término
        empleos = scrape_jobs(
            site_name=["linkedin", "indeed"],
            search_term=carrera,
            location="Peru",
            results_wanted=100,  
            country_indeed="peru", 
            hours_old=720,         
            linkedin_fetch_description=True # indeed viene habilitada por defecto la descripción
        )
        
        # Verificamos si se encontraron datos
        if not empleos.empty:
            # Agregamos una columna para identificar qué término generó este resultado
            empleos['termino_de_busqueda'] = carrera
            todos_los_empleos.append(empleos)
            print(f"-> {len(empleos)} ofertas encontradas.\n")
        else:
            print("-> 0 ofertas encontradas en este periodo.\n")
            
    except Exception as e:
        print(f"-> Ocurrió un error al buscar {carrera}: {e}\n")

# Consolidación y limpieza de la base de datos
if todos_los_empleos:
    # Unir todos los DataFrames individuales en uno solo
    df_final = pd.concat(todos_los_empleos, ignore_index=True)
    
    # Es muy probable que una misma oferta pida "Sociología" y "Ciencia Política"
    # Aquí eliminamos los duplicados usando la URL del trabajo como identificador único
    df_final = df_final.drop_duplicates(subset=['job_url'])
    
    print("=========================================")
    print(f"Extracción completada. Total de ofertas únicas: {len(df_final)}")
    
    # Guardar en CSV para tu posterior análisis
    df_final.to_csv("convocatorias_sociales_pe.csv", index=False)
    print("Archivo 'convocatorias_sociales_pe.csv' guardado con éxito.")
else:
    print("No se logró extraer ninguna oferta laboral con los parámetros dados.")