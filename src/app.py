# src/app.py

from flask import Flask, request, jsonify, redirect, url_for
from flask_migrate import Migrate
from flasgger import Swagger, swag_from
from src.models import db, User, Person, Planet, favorite_planets, favorite_characters

# ----------------------------------------------------------
# Usuario “hardcodeado” (mientras no implementemos autenticación)
CURRENT_USER_ID = 1
# ----------------------------------------------------------

def create_app():
    app = Flask(__name__)

    # ------------------------------------------------------
    # Configuración de la base de datos (SQLite en este ejemplo)
    # ------------------------------------------------------
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///starwars_blog_api.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # ------------------------------------------------------
    # Plantilla de Swagger/OpenAPI (ahora usando swagger: "2.0")
    # para forzar el orden de los tags y evitar conflicto
    # ------------------------------------------------------
    swagger_template = {
        "swagger": "2.0",
        "info": {
            "title": "StarWars Blog API",
            "version": "1.0.0",
            "description": "API REST para listar planetas, personajes y manejar favoritos en el StarWars Blog",
            "contact": {
                "responsibleOrganization": "4Geeks Academy",
                "responsibleDeveloper": "Tu Nombre",
                "email": "tu.email@ejemplo.com",
                "url": "https://github.com/4GeeksAcademy"
            }
        },
        # <-- Declaramos los cuatro tags EN EL ORDEN EXACTO que queremos -->
        "tags": [
            {
                "name": "people",
                "description": "Operaciones sobre personajes"
            },
            {
                "name": "planets",
                "description": "Operaciones sobre planetas"
            },
            {
                "name": "users",
                "description": "Operaciones sobre usuarios y favoritos"
            },
            {
                "name": "favorite",
                "description": "Añadir/Eliminar favoritos"
            }
        ],
        # Servidor base para Swagger
        "schemes": ["http"],
        "basePath": "/",
    }

    # ------------------------------------------------------
    # Configuración de Flasgger (Swagger UI + ReDoc)
    # ------------------------------------------------------
    app.config['SWAGGER'] = {
        'uiversion': 3,
        'specs_route': '/apidocs/'
    }
    # Inicializamos Flasgger pasándole el template corregido
    Swagger(app, template=swagger_template)

    # ------------------------------------------------------
    # Inicialización de extensiones
    # ------------------------------------------------------
    db.init_app(app)
    Migrate(app, db)

    # ------------------------------------------------------
    # Ruta raíz (“/”) redirige directamente a Swagger UI (/apidocs/)
    # ------------------------------------------------------
    @app.route('/')
    def index():
        return redirect(url_for('flasgger.apidocs'))

    # ======================================================
    # 1) BLOQUE “people” – Operaciones sobre personajes (/people)
    # ======================================================

    @app.route('/people', methods=['GET'])
    @swag_from({
        'tags': ['people'],
        'summary': 'Listar todos los personajes',
        'responses': {
            200: {
                'description': 'Lista de todos los personajes disponibles',
                'schema': {
                    'type': 'array',
                    'items': {
                        'type': 'object',
                        'properties': {
                            'id':         {'type': 'integer', 'example': 1},
                            'name':       {'type': 'string',  'example': 'Luke Skywalker'},
                            'birth_year': {'type': 'string',  'example': '19BBY'},
                            'gender':     {'type': 'string',  'example': 'male'},
                            'eye_color':  {'type': 'string',  'example': 'blue'}
                        }
                    }
                }
            }
        }
    })
    def get_all_people():
        people = Person.query.all()
        result = [{
            'id': p.id,
            'name': p.name,
            'birth_year': p.birth_year,
            'gender': p.gender,
            'eye_color': p.eye_color
        } for p in people]
        return jsonify(result), 200

    @app.route('/people/<int:people_id>', methods=['GET'])
    @swag_from({
        'tags': ['people'],
        'summary': 'Obtener un personaje por su ID',
        'parameters': [
            {
                'name': 'people_id',
                'in': 'path',
                'description': 'ID del personaje a buscar',
                'required': True,
                'type': 'integer'
            }
        ],
        'responses': {
            200: {
                'description': 'Datos detallados del personaje',
                'schema': {
                    'type': 'object',
                    'properties': {
                        'id':         {'type': 'integer', 'example': 1},
                        'name':       {'type': 'string',  'example': 'Luke Skywalker'},
                        'birth_year': {'type': 'string',  'example': '19BBY'},
                        'gender':     {'type': 'string',  'example': 'male'},
                        'eye_color':  {'type': 'string',  'example': 'blue'}
                    }
                }
            },
            404: {
                'description': 'Personaje no encontrado',
                'schema': {
                    'type': 'object',
                    'properties': {
                        'error': {'type': 'string', 'example': 'Person not found'}
                    }
                }
            }
        }
    })
    def get_person(people_id):
        p = Person.query.get(people_id)
        if not p:
            return jsonify({'error': 'Person not found'}), 404
        data = {
            'id': p.id,
            'name': p.name,
            'birth_year': p.birth_year,
            'gender': p.gender,
            'eye_color': p.eye_color
        }
        return jsonify(data), 200

    # ======================================================
    # 2) BLOQUE “planets” – Operaciones sobre planetas (/planets)
    # ======================================================

    @app.route('/planets', methods=['GET'])
    @swag_from({
        'tags': ['planets'],
        'summary': 'Listar todos los planetas',
        'responses': {
            200: {
                'description': 'Lista de todos los planetas disponibles',
                'schema': {
                    'type': 'array',
                    'items': {
                        'type': 'object',
                        'properties': {
                            'id':         {'type': 'integer', 'example': 1},
                            'name':       {'type': 'string',  'example': 'Tatooine'},
                            'climate':    {'type': 'string',  'example': 'arid'},
                            'terrain':    {'type': 'string',  'example': 'desert'},
                            'population': {'type': 'integer', 'example': 200000}
                        }
                    }
                }
            }
        }
    })
    def get_all_planets():
        planets = Planet.query.all()
        result = [{
            'id': pl.id,
            'name': pl.name,
            'climate': pl.climate,
            'terrain': pl.terrain,
            'population': pl.population
        } for pl in planets]
        return jsonify(result), 200

    @app.route('/planets/<int:planet_id>', methods=['GET'])
    @swag_from({
        'tags': ['planets'],
        'summary': 'Obtener un planeta por su ID',
        'parameters': [
            {
                'name': 'planet_id',
                'in': 'path',
                'description': 'ID del planeta a buscar',
                'required': True,
                'type': 'integer'
            }
        ],
        'responses': {
            200: {
                'description': 'Datos detallados del planeta',
                'schema': {
                    'type': 'object',
                    'properties': {
                        'id':         {'type': 'integer', 'example': 1},
                        'name':       {'type': 'string',  'example': 'Tatooine'},
                        'climate':    {'type': 'string',  'example': 'arid'},
                        'terrain':    {'type': 'string',  'example': 'desert'},
                        'population': {'type': 'integer', 'example': 200000}
                    }
                }
            },
            404: {
                'description': 'Planeta no encontrado',
                'schema': {
                    'type': 'object',
                    'properties': {
                        'error': {'type': 'string', 'example': 'Planet not found'}
                    }
                }
            }
        }
    })
    def get_planet(planet_id):
        pl = Planet.query.get(planet_id)
        if not pl:
            return jsonify({'error': 'Planet not found'}), 404
        data = {
            'id': pl.id,
            'name': pl.name,
            'climate': pl.climate,
            'terrain': pl.terrain,
            'population': pl.population
        }
        return jsonify(data), 200

    # ======================================================
    # 3) BLOQUE “users” – Operaciones sobre usuarios (/users)
    # ======================================================

    @app.route('/users', methods=['GET'])
    @swag_from({
        'tags': ['users'],
        'summary': 'Listar todos los usuarios',
        'responses': {
            200: {
                'description': 'Lista de todos los usuarios',
                'schema': {
                    'type': 'array',
                    'items': {
                        'type': 'object',
                        'properties': {
                            'id':         {'type': 'integer', 'example': 1},
                            'username':   {'type': 'string',  'example': 'luke_skywalker'},
                            'email':      {'type': 'string',  'example': 'luke@tatooine.com'},
                            'first_name': {'type': 'string',  'example': 'Luke'},
                            'last_name':  {'type': 'string',  'example': 'Skywalker'},
                            'joined_at':  {'type': 'string',  'example': '2025-06-01T12:34:56'}
                        }
                    }
                }
            }
        }
    })
    def get_all_users():
        users = User.query.all()
        result = [{
            'id': u.id,
            'username': u.username,
            'email': u.email,
            'first_name': u.first_name,
            'last_name': u.last_name,
            'joined_at': u.joined_at.isoformat()
        } for u in users]
        return jsonify(result), 200

    @app.route('/users/favorites', methods=['GET'])
    @swag_from({
        'tags': ['users'],
        'summary': 'Listar favoritos del usuario actual',
        'responses': {
            200: {
                'description': 'Favoritos del usuario',
                'schema': {
                    'type': 'object',
                    'properties': {
                        'user_id': {'type': 'integer', 'example': 1},
                        'favorite_planets': {
                            'type': 'array',
                            'items': {
                                'type': 'object',
                                'properties': {
                                    'id':         {'type': 'integer', 'example': 1},
                                    'name':       {'type': 'string',  'example': 'Tatooine'},
                                    'climate':    {'type': 'string',  'example': 'arid'},
                                    'terrain':    {'type': 'string',  'example': 'desert'},
                                    'population': {'type': 'integer', 'example': 200000}
                                }
                            }
                        },
                        'favorite_characters': {
                            'type': 'array',
                            'items': {
                                'type': 'object',
                                'properties': {
                                    'id':         {'type': 'integer', 'example': 1},
                                    'name':       {'type': 'string',  'example': 'Luke Skywalker'},
                                    'birth_year': {'type': 'string',  'example': '19BBY'},
                                    'gender':     {'type': 'string',  'example': 'male'},
                                    'eye_color':  {'type': 'string',  'example': 'blue'}
                                }
                            }
                        }
                    }
                }
            },
            404: {
                'description': 'Usuario no encontrado',
                'schema': {
                    'type': 'object',
                    'properties': {
                        'error': {'type': 'string', 'example': 'Current user not found'}
                    }
                }
            }
        }
    })
    def get_user_favorites():
        user = User.query.get(CURRENT_USER_ID)
        if not user:
            return jsonify({'error': 'Current user not found'}), 404

        fav_planets = [{
            'id': pl.id,
            'name': pl.name,
            'climate': pl.climate,
            'terrain': pl.terrain,
            'population': pl.population
        } for pl in user.favorite_planets]

        fav_people = [{
            'id': p.id,
            'name': p.name,
            'birth_year': p.birth_year,
            'gender': p.gender,
            'eye_color': p.eye_color
        } for p in user.favorite_characters]

        return jsonify({
            'user_id': user.id,
            'favorite_planets': fav_planets,
            'favorite_characters': fav_people
        }), 200

    # ======================================================
    # 4) BLOQUE “favorite” – Añadir y eliminar favoritos
    # ======================================================

    @app.route('/favorite/planet/<int:planet_id>', methods=['POST'])
    @swag_from({
        'tags': ['favorite'],
        'summary': 'Añadir un planeta a favoritos',
        'parameters': [
            {
                'name': 'planet_id',
                'in': 'path',
                'description': 'ID del planeta a agregar a favoritos',
                'required': True,
                'type': 'integer'
            }
        ],
        'responses': {
            201: {
                'description': 'Planeta añadido a favoritos',
                'schema': {
                    'type': 'object',
                    'properties': {
                        'message': {'type': 'string', 'example': 'Planet Tatooine added to favorites'}
                    }
                }
            },
            404: {
                'description': 'Usuario o planeta no encontrado',
                'schema': {
                    'type': 'object',
                    'properties': {
                        'error': {'type': 'string', 'example': 'Planet not found'}
                    }
                }
            },
            409: {
                'description': 'Planeta ya estaba en favoritos',
                'schema': {
                    'type': 'object',
                    'properties': {
                        'message': {'type': 'string', 'example': 'Planet already in favorites'}
                    }
                }
            }
        }
    })
    def add_favorite_planet(planet_id):
        user = User.query.get(CURRENT_USER_ID)
        if not user:
            return jsonify({'error': 'Current user not found'}), 404

        planet = Planet.query.get(planet_id)
        if not planet:
            return jsonify({'error': 'Planet not found'}), 404

        if planet in user.favorite_planets:
            return jsonify({'message': 'Planet already in favorites'}), 409

        user.favorite_planets.append(planet)
        db.session.commit()
        return jsonify({'message': f'Planet {planet.name} added to favorites'}), 201

    @app.route('/favorite/planet/<int:planet_id>', methods=['DELETE'])
    @swag_from({
        'tags': ['favorite'],
        'summary': 'Eliminar un planeta de favoritos',
        'parameters': [
            {
                'name': 'planet_id',
                'in': 'path',
                'description': 'ID del planeta a eliminar de favoritos',
                'required': True,
                'type': 'integer'
            }
        ],
        'responses': {
            200: {
                'description': 'Planeta eliminado de favoritos',
                'schema': {
                    'type': 'object',
                    'properties': {
                        'message': {'type': 'string', 'example': 'Planet Tatooine removed from favorites'}
                    }
                }
            },
            404: {
                'description': 'Usuario, planeta o favorito no encontrado',
                'schema': {
                    'type': 'object',
                    'properties': {
                        'message': {'type': 'string', 'example': 'Planet not in favorites'}
                    }
                }
            }
        }
    })
    def delete_favorite_planet(planet_id):
        user = User.query.get(CURRENT_USER_ID)
        if not user:
            return jsonify({'error': 'Current user not found'}), 404

        planet = Planet.query.get(planet_id)
        if not planet:
            return jsonify({'error': 'Planet not found'}), 404

        if planet not in user.favorite_planets:
            return jsonify({'message': 'Planet not in favorites'}), 404

        user.favorite_planets.remove(planet)
        db.session.commit()
        return jsonify({'message': f'Planet {planet.name} removed from favorites'}), 200

    @app.route('/favorite/people/<int:people_id>', methods=['POST'])
    @swag_from({
        'tags': ['favorite'],
        'summary': 'Añadir un personaje a favoritos',
        'parameters': [
            {
                'name': 'people_id',
                'in': 'path',
                'description': 'ID del personaje a agregar a favoritos',
                'required': True,
                'type': 'integer'
            }
        ],
        'responses': {
            201: {
                'description': 'Personaje añadido a favoritos',
                'schema': {
                    'type': 'object',
                    'properties': {
                        'message': {'type': 'string', 'example': 'Person Luke Skywalker added to favorites'}
                    }
                }
            },
            404: {
                'description': 'Usuario o personaje no encontrado',
                'schema': {
                    'type': 'object',
                    'properties': {
                        'error': {'type': 'string', 'example': 'Person not found'}
                    }
                }
            },
            409: {
                'description': 'Personaje ya estaba en favoritos',
                'schema': {
                    'type': 'object',
                    'properties': {
                        'message': {'type': 'string', 'example': 'Person already in favorites'}
                    }
                }
            }
        }
    })
    def add_favorite_person(people_id):
        user = User.query.get(CURRENT_USER_ID)
        if not user:
            return jsonify({'error': 'Current user not found'}), 404

        person = Person.query.get(people_id)
        if not person:
            return jsonify({'error': 'Person not found'}), 404

        if person in user.favorite_characters:
            return jsonify({'message': 'Person already in favorites'}), 409

        user.favorite_characters.append(person)
        db.session.commit()
        return jsonify({'message': f'Person {person.name} added to favorites'}), 201

    @app.route('/favorite/people/<int:people_id>', methods=['DELETE'])
    @swag_from({
        'tags': ['favorite'],
        'summary': 'Eliminar un personaje de favoritos',
        'parameters': [
            {
                'name': 'people_id',
                'in': 'path',
                'description': 'ID del personaje a eliminar de favoritos',
                'required': True,
                'type': 'integer'
            }
        ],
        'responses': {
            200: {
                'description': 'Personaje eliminado de favoritos',
                'schema': {
                    'type': 'object',
                    'properties': {
                        'message': {'type': 'string', 'example': 'Person Luke Skywalker removed from favorites'}
                    }
                }
            },
            404: {
                'description': 'Usuario, personaje o favorito no encontrado',
                'schema': {
                    'type': 'object',
                    'properties': {
                        'message': {'type': 'string', 'example': 'Person not in favorites'}
                    }
                }
            }
        }
    })
    def delete_favorite_person(people_id):
        user = User.query.get(CURRENT_USER_ID)
        if not user:
            return jsonify({'error': 'Current user not found'}), 404

        person = Person.query.get(people_id)
        if not person:
            return jsonify({'error': 'Person not found'}), 404

        if person not in user.favorite_characters:
            return jsonify({'message': 'Person not in favorites'}), 404

        user.favorite_characters.remove(person)
        db.session.commit()
        return jsonify({'message': f'Person {person.name} removed from favorites'}), 200

    # --------------------------------------------------
    # 404 por defecto para rutas no encontradas
    # --------------------------------------------------
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({'error': 'Not found'}), 404

    return app


if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0', port=5000, debug=True)
