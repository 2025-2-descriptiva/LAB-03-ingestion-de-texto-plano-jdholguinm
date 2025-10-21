"""
Escriba el codigo que ejecute la accion solicitada en cada pregunta.
"""

# pylint: disable=import-outside-toplevel


def pregunta_01():
    """
    Construya y retorne un dataframe de Pandas a partir del archivo
    'files/input/clusters_report.txt'. Los requierimientos son los siguientes:

    - El dataframe tiene la misma estructura que el archivo original.
    - Los nombres de las columnas deben ser en minusculas, reemplazando los
      espacios por guiones bajos.
    - Las palabras clave deben estar separadas por coma y con un solo
      espacio entre palabra y palabra.


    """
    import pandas as pd
    import re

    with open("files/input/clusters_report.txt", "r", encoding="utf-8") as f:
        lines = f.readlines()

    columns = ["cluster", "cantidad_de_palabras_clave", "porcentaje_de_palabras_clave", "principales_palabras_clave"]

    clusters_raw = []  # lista donde guardaremos cada cluster completo
    current_cluster = ""  # texto acumulado

    for line in lines[4:]:
        # Si la línea comienza con un número → nuevo cluster
        if re.match(r'^\s*\d+', line):
            # Guardar el cluster anterior si ya teníamos uno
            if current_cluster != "":
                clusters_raw.append(current_cluster.strip())
            # Empezar nuevo cluster
            current_cluster = line.strip()
        else:
            # Continuación del texto anterior → agregarlo
            current_cluster += " " + line.strip()

    # Agregar el último cluster porque al salir del loop no se agrega
    if current_cluster:
        clusters_raw.append(current_cluster.strip())

    # Lista donde guardaremos las filas ya separadas
    filas_limpias = []

    # Expresión regular, cada () representa una columna
    # \S+ : uno o más caracteres que no son espacios
    # \s+ : uno o más espacios

    patron = r'^(\S+)\s+(\S+)\s+(\S+\s*%)\s+(.+)$'

    for fila in clusters_raw:
        match = re.match(patron, fila)
        if match:
            # Extrae los 4 grupos (columnas)
            columnas_match = list(match.groups())
            filas_limpias.append(columnas_match)
        
        else:
            print("No fue posible match para la fila:", fila)

    filas_limpias

    df = pd.DataFrame(filas_limpias, columns=columns)

    df.porcentaje_de_palabras_clave = df.porcentaje_de_palabras_clave.str.replace('%', '')
    df.porcentaje_de_palabras_clave = df.porcentaje_de_palabras_clave.str.replace(',', '.')
    df.porcentaje_de_palabras_clave = df.porcentaje_de_palabras_clave.astype(float)
    df.cantidad_de_palabras_clave = df.cantidad_de_palabras_clave.astype(int)
    df.cluster = df.cluster.astype(int)
    df.principales_palabras_clave = (
    df.principales_palabras_clave
    .apply(lambda x: re.sub(r"\s+", " ", x.strip()))     # normaliza espacios
    .apply(lambda x: re.sub(r"\s*,\s*", ", ", x))        # coma + espacio
    )
    df.principales_palabras_clave = (df.principales_palabras_clave.str.replace(r"\s+", ' ')
                                   .str.replace(', ', ',')
                                   .str.replace(',', ', ')
                                   .str.strip()
                                   .str.replace('.', '')
                                   )

    return df

if __name__ == "__main__":
    resultado = pregunta_01()


