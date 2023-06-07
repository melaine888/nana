from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Actor,Movie,Role


engine = create_engine('sqlite:///db/movies.db', echo=True)

Session = sessionmaker(bind=engine)
session = Session()

def create_instances():
    actor1 = Actor(name = "Actor 1")
    actor2 = Actor(name = "Actor 2")
    actor3 = Actor(name = "Actor 3")

    movie1 = Movie(title = "Movie1",
                   box_office_earnings = 100000000)
    movie2 = Movie(title = "Movie2",
                   box_office_earnings = 50000000)
    movie3 = Movie(title = "Movie3",
                   box_office_earnings = 200000000)
    
    role1 = Role(actor=actor1, movie=movie1, character_name="Character 1", salary=1000000)
    role2 = Role(actor=actor2, movie=movie2, character_name="Character 2", salary=500000)
    role3 = Role(actor=actor3, movie=movie3, character_name="Character 3", salary=2000000)


    session.add_all([actor1, actor2, actor3, movie1, movie2, movie3, role1, role2, role3])
    

    # Commit the changes to the database
    session.commit()

    # Close the session
    session.close()

    if __name__ == '__main__':
        create_instances()
    
                  