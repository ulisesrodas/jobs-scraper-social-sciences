import pandas as pd

df = pd.read_csv('convocatorias_sociales_pe_filtrado.csv', encoding='utf-8')

# Filtrar solo Sociología (el valor en el CSV tiene comillas dobles)
mask = df['termino_de_busqueda'].str.contains('Sociologia', na=False)
socio = df[mask][['company', 'title', 'job_url', 'description', 'termino_de_busqueda']].copy()
socio.columns = ['Empresa', 'Titulo del puesto', 'Link', 'Descripcion', 'Carrera']
socio['Carrera'] = 'Sociologia'

print(f'Total convocatorias de Sociologia: {len(socio)}')

socio.to_excel('convocatorias_sociologia.xlsx', index=False)
print('Archivo guardado: convocatorias_sociologia.xlsx')
