from flask import Blueprint, request, jsonify
from src.models.user import db, Smartlink
from datetime import datetime
import string
import random

smartlink_bp = Blueprint('smartlink', __name__)

def generate_smartlink_id():
    """Génère un ID unique pour un smartlink"""
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(8))

@smartlink_bp.route('/smartlinks', methods=['POST'])
def create_smartlink():
    """Créer un nouveau smartlink"""
    try:
        data = request.get_json()
        
        # Générer un ID unique
        smartlink_id = generate_smartlink_id()
        while Smartlink.query.get(smartlink_id):
            smartlink_id = generate_smartlink_id()
        
        # Créer le nouveau smartlink
        smartlink = Smartlink(
            id=smartlink_id,
            title=data.get('title'),
            description=data.get('description'),
            url=data.get('url'),
            views=0,
            clicks=0
        )
        
        db.session.add(smartlink)
        db.session.commit()
        
        return jsonify(smartlink.to_dict()), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@smartlink_bp.route('/smartlinks', methods=['GET'])
def get_all_smartlinks():
    """Récupérer tous les smartlinks"""
    try:
        smartlinks = Smartlink.query.all()
        return jsonify([smartlink.to_dict() for smartlink in smartlinks]), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@smartlink_bp.route('/smartlinks/<string:smartlink_id>', methods=['GET'])
def get_smartlink(smartlink_id):
    """Récupérer un smartlink spécifique"""
    try:
        smartlink = Smartlink.query.get(smartlink_id)
        if not smartlink:
            return jsonify({'error': 'Smartlink not found'}), 404
        
        # Incrémenter le nombre de vues
        smartlink.views += 1
        db.session.commit()
        
        return jsonify(smartlink.to_dict()), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@smartlink_bp.route('/smartlinks/<string:smartlink_id>', methods=['PUT'])
def update_smartlink(smartlink_id):
    """Mettre à jour un smartlink"""
    try:
        smartlink = Smartlink.query.get(smartlink_id)
        if not smartlink:
            return jsonify({'error': 'Smartlink not found'}), 404
        
        data = request.get_json()
        
        # Mettre à jour les champs
        if 'title' in data:
            smartlink.title = data['title']
        if 'description' in data:
            smartlink.description = data['description']
        if 'url' in data:
            smartlink.url = data['url']
        
        smartlink.updated_at = datetime.utcnow()
        db.session.commit()
        
        return jsonify(smartlink.to_dict()), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@smartlink_bp.route('/smartlinks/<string:smartlink_id>', methods=['DELETE'])
def delete_smartlink(smartlink_id):
    """Supprimer un smartlink"""
    try:
        smartlink = Smartlink.query.get(smartlink_id)
        if not smartlink:
            return jsonify({'error': 'Smartlink not found'}), 404
        
        db.session.delete(smartlink)
        db.session.commit()
        
        return jsonify({'message': 'Smartlink deleted successfully'}), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@smartlink_bp.route('/smartlinks/<string:smartlink_id>/click', methods=['POST'])
def track_click(smartlink_id):
    """Enregistrer un clic sur un smartlink"""
    try:
        smartlink = Smartlink.query.get(smartlink_id)
        if not smartlink:
            return jsonify({'error': 'Smartlink not found'}), 404
        
        # Incrémenter le nombre de clics
        smartlink.clicks += 1
        db.session.commit()
        
        return jsonify({
            'message': 'Click tracked successfully',
            'clicks': smartlink.clicks
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

