from flask import Blueprint, request, jsonify
from app.controllers.voto_controller import emitir_voto_completo

voto_bp = Blueprint('voto', __name__, url_prefix='/voto')

@voto_bp.route('/emitir', methods=['POST'])
def emitir():
    data = request.json
    try:
        resultado = emitir_voto_completo(data)
        if resultado == 'CIRCUITO_CERRADO':
            return jsonify({'error': 'El circuito electoral está cerrado'}), 400
        if resultado == 'YA_VOTO':
            return jsonify({'error': 'El ciudadano ya votó en esta elección'}), 400
        elif resultado:
            return jsonify({'mensaje': 'Voto registrado correctamente'}), 201
        else:
            return jsonify({'error': 'No se pudo registrar el voto'}), 500
    except Exception as e:
        print(f"❌ Error al emitir voto: {e}")
        return jsonify({'error': 'Error interno en el servidor'}), 500
