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
            clicks=0,
            landing_page_title=data.get('landing_page_title'),
            landing_page_subtitle=data.get('landing_page_subtitle'),
            cover_image_url=data.get('cover_image_url'),
            embed_url=data.get('embed_url'),
            long_description=data.get('long_description'),
            social_sharing_enabled=data.get('social_sharing_enabled', True)
        )
        
        # Gérer les plateformes
        platforms = data.get('platforms', [])
        if platforms:
            smartlink.set_platforms(platforms)
        
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
        
        # Mettre à jour les champs de base
        if 'title' in data:
            smartlink.title = data['title']
        if 'description' in data:
            smartlink.description = data['description']
        if 'url' in data:
            smartlink.url = data['url']
        
        # Mettre à jour les champs de la page de destination
        if 'landing_page_title' in data:
            smartlink.landing_page_title = data['landing_page_title']
        if 'landing_page_subtitle' in data:
            smartlink.landing_page_subtitle = data['landing_page_subtitle']
        if 'cover_image_url' in data:
            smartlink.cover_image_url = data['cover_image_url']
        if 'embed_url' in data:
            smartlink.embed_url = data['embed_url']
        if 'long_description' in data:
            smartlink.long_description = data['long_description']
        if 'social_sharing_enabled' in data:
            smartlink.social_sharing_enabled = data['social_sharing_enabled']
        
        # Mettre à jour les plateformes
        if 'platforms' in data:
            smartlink.set_platforms(data['platforms'])
        
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


@smartlink_bp.route('/smartlinks/<string:smartlink_id>/landing', methods=['GET'])
def get_smartlink_landing_page(smartlink_id):
    """Récupérer les données complètes d'une page de destination"""
    try:
        smartlink = Smartlink.query.get(smartlink_id)
        if not smartlink:
            return jsonify({'error': 'Smartlink not found'}), 404
        
        # Incrémenter le nombre de vues
        smartlink.views += 1
        db.session.commit()
        
        # Retourner toutes les données nécessaires pour la page de destination
        landing_data = {
            'id': smartlink.id,
            'landing_page_title': smartlink.landing_page_title or smartlink.title,
            'landing_page_subtitle': smartlink.landing_page_subtitle,
            'cover_image_url': smartlink.cover_image_url,
            'platforms': smartlink.get_platforms(),
            'embed_url': smartlink.embed_url,
            'long_description': smartlink.long_description or smartlink.description,
            'social_sharing_enabled': smartlink.social_sharing_enabled,
            'views': smartlink.views,
            'clicks': smartlink.clicks
        }
        
        return jsonify(landing_data), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@smartlink_bp.route('/smartlinks/<string:smartlink_id>/platforms/<int:platform_index>/click', methods=['POST'])
def track_platform_click(smartlink_id, platform_index):
    """Enregistrer un clic sur une plateforme spécifique"""
    try:
        smartlink = Smartlink.query.get(smartlink_id)
        if not smartlink:
            return jsonify({'error': 'Smartlink not found'}), 404
        
        platforms = smartlink.get_platforms()
        if platform_index >= len(platforms):
            return jsonify({'error': 'Platform index out of range'}), 400
        
        # Incrémenter le nombre de clics global
        smartlink.clicks += 1
        
        # Optionnel : incrémenter le compteur de clics pour cette plateforme spécifique
        if 'clicks' not in platforms[platform_index]:
            platforms[platform_index]['clicks'] = 0
        platforms[platform_index]['clicks'] += 1
        smartlink.set_platforms(platforms)
        
        db.session.commit()
        
        return jsonify({
            'message': 'Platform click tracked successfully',
            'total_clicks': smartlink.clicks,
            'platform_clicks': platforms[platform_index]['clicks'],
            'redirect_url': platforms[platform_index].get('url')
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

