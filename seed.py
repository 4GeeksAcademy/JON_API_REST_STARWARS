# seed.py

from src.app import create_app
from src.models import db, User, Person, Planet

def run_seed():
    app = create_app()
    with app.app_context():
        # 1) (Opcional) Eliminar todas las tablas existentes y volver a crearlas
        db.drop_all()
        db.create_all()

        # 2) Crear un usuario de ejemplo
        u = User(
            username='luke_skywalker',
            email='luke@tatooine.com',
            password='secreto',      # En un caso real lo hashearías
            first_name='Luke',
            last_name='Skywalker'
        )
        db.session.add(u)

        # 3) Crear algunos planetas de ejemplo
        p1 = Planet(name='Tatooine', climate='arid', terrain='desert', population=200000)
        p2 = Planet(name='Alderaan', climate='temperate', terrain='grasslands, mountains', population=2000000000)
        p3 = Planet(name='Hoth', climate='frozen', terrain='tundra, ice caves', population=0)
        db.session.add_all([p1, p2, p3])

        # 4) Crear algunos personajes (people) de ejemplo
        c1 = Person(name='Luke Skywalker',   birth_year='19BBY', gender='male',   eye_color='blue')
        c2 = Person(name='Leia Organa',      birth_year='19BBY', gender='female', eye_color='brown')
        c3 = Person(name='Han Solo',         birth_year='29BBY', gender='male',   eye_color='brown')
        c4 = Person(name='Darth Vader',      birth_year='41.9BBY', gender='male', eye_color='yellow')
        db.session.add_all([c1, c2, c3, c4])

        # 5) Confirmar inserciones iniciales
        db.session.commit()

        # 6) Asociar favoritos para el usuario creado (u.id será 1)
        user = User.query.filter_by(username='luke_skywalker').first()
        if user:
            # Añadir un planeta y un personaje a sus favoritos
            tatooine = Planet.query.filter_by(name='Tatooine').first()
            leia     = Person.query.filter_by(name='Leia Organa').first()

            if tatooine and tatooine not in user.favorite_planets:
                user.favorite_planets.append(tatooine)
            if leia and leia not in user.favorite_characters:
                user.favorite_characters.append(leia)

            # También, por ejemplo, asociar Hoth y Han Solo
            hoth = Planet.query.filter_by(name='Hoth').first()
            han  = Person.query.filter_by(name='Han Solo').first()

            if hoth and hoth not in user.favorite_planets:
                user.favorite_planets.append(hoth)
            if han and han not in user.favorite_characters:
                user.favorite_characters.append(han)

            db.session.commit()

        print("✅ Base de datos reiniciada y poblada con datos de ejemplo.")

if __name__ == '__main__':
    run_seed()
