from app.db import get_all
import csv
import io

def generar_csv_estadisticas():
    elecciones = get_all("SELECT id_eleccion, tipo FROM Eleccion WHERE status = FALSE")

    output = io.StringIO()
    writer = csv.writer(output)

    writer.writerow(["id_lista", "tipo", "candidato", "votos", "porcentaje"])

    for eleccion in elecciones:
        tipo_eleccion = eleccion['tipo'].lower()

        if tipo_eleccion == "presidencial":
            listas = get_all("SELECT id, presidente as candidato FROM Lista_Presidencial")
        elif tipo_eleccion == "ballotage":
            listas = get_all("SELECT id, candidato FROM Lista_Ballotage")
        elif tipo_eleccion == "municipal":
            listas = get_all("SELECT id, candidato FROM Lista_Municipal")
        elif tipo_eleccion in ["plebiscito", "referendum"]:
            listas = get_all("SELECT id, opcion as candidato FROM Papeleta")
        else:
            listas = []

        lista_ids = [l['id'] for l in listas]

        if not lista_ids:
            continue

        placeholders = ','.join(['%s'] * len(lista_ids))
        total_votos_result = get_all(f"""
            SELECT COUNT(*) as total
            FROM Voto
            WHERE id_lista IN ({placeholders})
        """, lista_ids)
        total_votos = total_votos_result[0]['total'] if total_votos_result else 0

        votos_por_lista = get_all(f"""
            SELECT id_lista, COUNT(*) as votos
            FROM Voto
            WHERE id_lista IN ({placeholders})
            GROUP BY id_lista
        """, lista_ids)

        candidato_map = {l['id']: l['candidato'] for l in listas}

        for v in votos_por_lista:
            lista_id = v['id_lista']
            cant_votos = v['votos']
            porcentaje = f"{(cant_votos / total_votos * 100):.0f}%" if total_votos > 0 else "0%"

            candidato = candidato_map.get(lista_id, "N/A")

            writer.writerow([
                lista_id,
                eleccion['tipo'],
                candidato,
                cant_votos,
                porcentaje
            ])

    return output.getvalue()
