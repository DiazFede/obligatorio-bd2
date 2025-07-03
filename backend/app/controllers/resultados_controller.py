from app.db import get_all, get_one

def obtener_resultados_circuito(id_circuito, id_eleccion):
    """
    Obtiene los resultados detallados de una elección en un circuito particular,
    incluyendo votos por lista, en blanco y anulados.
    """
    query_total_votos = """
        SELECT COUNT(id_voto) AS total_votos
        FROM Voto
        WHERE id_circuito = %s AND id_eleccion = %s
    """

    total_votos_data = get_one(query_total_votos, (id_circuito, id_eleccion))
    total_votos = total_votos_data['total_votos'] if total_votos_data and total_votos_data['total_votos'] is not None else 0

    if total_votos == 0:
        return {
            "message": "No se han registrado votos en este circuito para esta elección."
        }

    query_listas = """
        SELECT
            L.numero_lista AS Lista, -- Corregido: usando numero_lista
            PP.nombre AS Partido,
            COUNT(VL.id_voto) AS Cant_Votos
        FROM Voto_Lista VL
        JOIN Voto V ON VL.id_voto = V.id_voto
        JOIN Lista L ON VL.id_lista = L.id
        LEFT JOIN Partido_politico PP ON L.nombre_partido = PP.nombre
        WHERE V.id_circuito = %s AND V.id_eleccion = %s AND V.condicion = 'Válido'
        GROUP BY L.id, L.numero_lista, PP.nombre -- Corregido: usando numero_lista en GROUP BY
        ORDER BY Cant_Votos DESC
    """
    listas_data = get_all(query_listas, (id_circuito, id_eleccion))

    resultados_listas = []
    for row in listas_data:
        porcentaje = (row['Cant_Votos'] / total_votos) * 100 if total_votos > 0 else 0
        resultados_listas.append({
            "Lista": row['Lista'],
            "Partido": row['Partido'],
            "Cant. Votos": row['Cant_Votos'],
            "Porcentaje": f"{porcentaje:.2f}%"
        })

    query_blanco = """
        SELECT COUNT(id_voto) AS Cant_Votos
        FROM Voto
        WHERE id_circuito = %s AND id_eleccion = %s AND condicion = 'En Blanco'
    """
    blanco_data = get_one(query_blanco, (id_circuito, id_eleccion))
    cant_blanco = blanco_data['Cant_Votos'] if blanco_data and blanco_data['Cant_Votos'] is not None else 0
    porcentaje_blanco = (cant_blanco / total_votos) * 100 if total_votos > 0 else 0
    resultados_listas.append({
        "Lista": "En Blanco",
        "Partido": "En Blanco",
        "Cant. Votos": cant_blanco,
        "Porcentaje": f"{porcentaje_blanco:.2f}%"
    })

    query_anulado = """
        SELECT COUNT(id_voto) AS Cant_Votos
        FROM Voto
        WHERE id_circuito = %s AND id_eleccion = %s AND condicion = 'Anulado'
    """
    anulado_data = get_one(query_anulado, (id_circuito, id_eleccion))
    cant_anulado = anulado_data['Cant_Votos'] if anulado_data and anulado_data['Cant_Votos'] is not None else 0
    porcentaje_anulado = (cant_anulado / total_votos) * 100 if total_votos > 0 else 0
    resultados_listas.append({
        "Lista": "Anulado",
        "Partido": "Anulado",
        "Cant. Votos": cant_anulado,
        "Porcentaje": f"{porcentaje_anulado:.2f}%"
    })

    return {
        "resultados_por_lista": resultados_listas,
        "total_votos_emitidos": total_votos
    }

def obtener_resultados_agregados_partido_circuito(id_circuito, id_eleccion):
    """
    Obtiene los resultados agregados por partido en un circuito particular,
    incluyendo votos en blanco y anulados.
    """
    query = """
        SELECT
            CASE
                WHEN V.condicion = 'En Blanco' THEN 'En Blanco'
                WHEN V.condicion = 'Anulado' THEN 'Anulado'
                ELSE PP.nombre
            END AS Partido,
            COUNT(V.id_voto) AS Votos
        FROM Voto V
        LEFT JOIN Voto_Lista VL ON V.id_voto = VL.id_voto
        LEFT JOIN Lista L ON VL.id_lista = L.id
        LEFT JOIN Partido_politico PP ON L.nombre_partido = PP.nombre
        WHERE V.id_circuito = %s AND V.id_eleccion = %s
        GROUP BY Partido
        ORDER BY Votos DESC
    """
    data = get_all(query, (id_circuito, id_eleccion))

    if not data:
        return {"message": "No hay datos para este circuito y elección."}

    total_validos = sum(row['Votos'] for row in data if row['Partido'] not in ('En Blanco', 'Anulado'))
    total_votos_emitidos = sum(row['Votos'] for row in data)

    resultados = []
    for row in data:
        partido = row['Partido']
        votos = row['Votos']
        porcentaje = 0
        if partido in ('En Blanco', 'Anulado'):
            if total_votos_emitidos > 0:
                porcentaje = (votos / total_votos_emitidos) * 100
        else:
            if total_validos > 0:
                porcentaje = (votos / total_validos) * 100

        resultados.append({
            "Partido": partido,
            "Votos": votos,
            "Porcentaje": f"{porcentaje:.2f}%"
        })

    return {"resultados_por_partido": resultados}


def obtener_resultados_finales_candidato_circuito(id_circuito, id_eleccion):
    """
    Obtiene los resultados finales por candidato en un circuito particular,
    incluyendo votos por candidato, en blanco y anulados.
    """
    query_total_votos = """
        SELECT COUNT(id_voto) AS total_votos
        FROM Voto
        WHERE id_circuito = %s AND id_eleccion = %s
    """
    total_votos_data = get_one(query_total_votos, (id_circuito, id_eleccion))
    total_votos = total_votos_data['total_votos'] if total_votos_data and total_votos_data['total_votos'] is not None else 0

    if total_votos == 0:
        return {
            "message": "No se han registrado votos en este circuito para esta elección."
        }

    query = """
        SELECT
            PP.nombre AS Partido,
            CIU.nombre_completo AS Candidato, -- Corregido: Nombre del candidato desde Ciudadano
            COUNT(VL.id_voto) AS Cant_Votos
        FROM Voto_Lista VL
        JOIN Voto V ON VL.id_voto = V.id_voto
        JOIN Lista L ON VL.id_lista = L.id
        LEFT JOIN Candidato_Lista CL ON L.id = CL.id_lista
        LEFT JOIN Candidato C ON CL.numero_credencial_candidato = C.numero_credencial -- Corregido: key de join
        LEFT JOIN Ciudadano CIU ON C.numero_credencial = CIU.numero_credencial -- Agregado: Join a Ciudadano
        LEFT JOIN Partido_politico PP ON L.nombre_partido = PP.nombre
        WHERE V.id_circuito = %s AND V.id_eleccion = %s AND V.condicion = 'Válido'
        GROUP BY PP.nombre, CIU.nombre_completo -- Corregido: Usando nombre_completo
        ORDER BY Cant_Votos DESC
    """
    data = get_all(query, (id_circuito, id_eleccion))

    resultados = []
    for row in data:
        porcentaje = (row['Cant_Votos'] / total_votos) * 100 if total_votos > 0 else 0
        resultados.append({
            "Partido": row['Partido'],
            "Candidato": row['Candidato'],
            "Cant Votos": row['Cant_Votos'],
            "Porcentaje": f"{porcentaje:.2f}%"
        })

    query_blanco = """
        SELECT COUNT(id_voto) AS Cant_Votos
        FROM Voto
        WHERE id_circuito = %s AND id_eleccion = %s AND condicion = 'En Blanco'
    """
    blanco_data = get_one(query_blanco, (id_circuito, id_eleccion))
    cant_blanco = blanco_data['Cant_Votos'] if blanco_data and blanco_data['Cant_Votos'] is not None else 0
    porcentaje_blanco = (cant_blanco / total_votos) * 100 if total_votos > 0 else 0
    resultados.append({
        "Partido": "En blanco",
        "Candidato": "En blanco",
        "Cant Votos": cant_blanco,
        "Porcentaje": f"{porcentaje_blanco:.2f}%"
    })

    query_anulado = """
        SELECT COUNT(id_voto) AS Cant_Votos
        FROM Voto
        WHERE id_circuito = %s AND id_eleccion = %s AND condicion = 'Anulado'
    """
    anulado_data = get_one(query_anulado, (id_circuito, id_eleccion))
    cant_anulado = anulado_data['Cant_Votos'] if anulado_data and anulado_data['Cant_Votos'] is not None else 0
    porcentaje_anulado = (cant_anulado / total_votos) * 100 if total_votos > 0 else 0
    resultados.append({
        "Partido": "Anulado",
        "Candidato": "Anulado",
        "Cant Votos": cant_anulado,
        "Porcentaje": f"{porcentaje_anulado:.2f}%"
    })

    return {"resultados_por_candidato": resultados}


def obtener_resultados_departamento(id_departamento, id_eleccion):
    """
    Obtiene los resultados agregados por partido a nivel de departamento.
    """
    query_total_votos_depto = """
        SELECT COUNT(V.id_voto) AS total_votos
        FROM Voto V
        JOIN Circuito C ON V.id_circuito = C.numero_circuito
        WHERE C.id_departamento = %s AND V.id_eleccion = %s
    """
    total_votos_data = get_one(query_total_votos_depto, (id_departamento, id_eleccion))
    total_votos = total_votos_data['total_votos'] if total_votos_data and total_votos_data['total_votos'] is not None else 0

    if total_votos == 0:
        return {"message": "No se han registrado votos en este departamento para esta elección."}

    query_partidos_depto = """
        SELECT
            CASE
                WHEN V.condicion = 'En Blanco' THEN 'En Blanco'
                WHEN V.condicion = 'Anulado' THEN 'Anulado'
                ELSE PP.nombre
            END AS Partido,
            COUNT(V.id_voto) AS Votos
        FROM Voto V
        LEFT JOIN Voto_Lista VL ON V.id_voto = VL.id_voto
        LEFT JOIN Lista L ON VL.id_lista = L.id
        LEFT JOIN Partido_politico PP ON L.nombre_partido = PP.nombre
        JOIN Circuito CI ON V.id_circuito = CI.numero_circuito
        WHERE CI.id_departamento = %s AND V.id_eleccion = %s
        GROUP BY Partido
        ORDER BY Votos DESC
    """
    data = get_all(query_partidos_depto, (id_departamento, id_eleccion))

    resultados = []
    for row in data:
        porcentaje = (row['Votos'] / total_votos) * 100 if total_votos > 0 else 0
        resultados.append({
            "Partido": row['Partido'],
            "Votos": row['Votos'],
            "Porcentaje": f"{porcentaje:.2f}%"
        })

    return {"resultados_departamento_por_partido": resultados}


def obtener_ganador_departamento(id_departamento, id_eleccion):
    """
    Aplica la "ley de lemas" para determinar el candidato ganador en un departamento
    para una elección municipal.
    """

    query_votos_candidato_partido = """
        SELECT
            PP.nombre AS nombre_partido,
            CIU.nombre_completo AS nombre_candidato, -- Corregido: Nombre del candidato desde Ciudadano
            COUNT(VL.id_voto) AS votos_candidato
        FROM Voto V
        JOIN Voto_Lista VL ON V.id_voto = VL.id_voto
        JOIN Lista L ON VL.id_lista = L.id
        LEFT JOIN Candidato_Lista CL ON L.id = CL.id_lista
        LEFT JOIN Candidato C ON CL.numero_credencial_candidato = C.numero_credencial -- Corregido: key de join
        LEFT JOIN Ciudadano CIU ON C.numero_credencial = CIU.numero_credencial -- Agregado: Join a Ciudadano
        LEFT JOIN Partido_politico PP ON L.nombre_partido = PP.nombre
        JOIN Circuito CI ON V.id_circuito = CI.numero_circuito
        WHERE CI.id_departamento = %s
          AND V.id_eleccion = %s
          AND V.condicion = 'Válido'
          AND L.organo_candidato = 'concejales' -- Asumiendo que 'concejales' es para intendente/alcaldes
        GROUP BY PP.nombre, CIU.nombre_completo -- Corregido: Usando nombre_completo
        ORDER BY nombre_partido, votos_candidato DESC
    """
    votos_data = get_all(query_votos_candidato_partido, (id_departamento, id_eleccion))

    if not votos_data:
        return {"message": "No hay datos de votos válidos para esta elección municipal en el departamento."}

    votos_por_partido = {}
    for row in votos_data:
        partido = row['nombre_partido']
        votos_candidato = row['votos_candidato']

        if partido not in votos_por_partido:
            votos_por_partido[partido] = {
                'total_votos_partido': 0,
                'candidatos': []
            }

        votos_por_partido[partido]['total_votos_partido'] += votos_candidato
        votos_por_partido[partido]['candidatos'].append({
            'nombre': row['nombre_candidato'],
            'votos': votos_candidato
        })

    partido_mas_votado = None
    max_votos_partido = -1

    for partido, data in votos_por_partido.items():
        if data['total_votos_partido'] > max_votos_partido:
            max_votos_partido = data['total_votos_partido']
            partido_mas_votado = partido

    if not partido_mas_votado:
        return {"message": "No se pudo determinar el partido más votado."}

    candidatos_del_partido_ganador = votos_por_partido[partido_mas_votado]['candidatos']
    candidato_ganador_final = None
    max_votos_candidato = -1

    for candidato in candidatos_del_partido_ganador:
        if candidato['votos'] > max_votos_candidato:
            max_votos_candidato = candidato['votos']
            candidato_ganador_final = candidato['nombre']

    return {
        "departamento_id": id_departamento,
        "partido_ganador": partido_mas_votado,
        "candidato_ganador": candidato_ganador_final,
        "total_votos_partido_ganador": max_votos_partido,
        "votos_candidato_ganador": max_votos_candidato
    }


def obtener_resultados_por_circuito(numero_circuito):
    query = """
        SELECT 
            l.id AS lista,
            COUNT(v.id_voto) AS cantidad_votos
        FROM Voto v
        JOIN Lista l ON v.id_lista = l.id
        JOIN Acto_Electoral ae ON v.id_voto = ae.id_eleccion
        JOIN Establecimiento_Eleccion ee ON ae.id_eleccion = ee.id_eleccion
        WHERE ee.numero_circuito = %s
        GROUP BY l.id
        ORDER BY cantidad_votos DESC;
    """
    return get_all(query, (numero_circuito,))
