#musis si naintalovat nasledujici baliky popmoci prikazu , je to ta alchemy, ten driver a nejake extensions a pytest pak pro testovani
#pip(pip3) install SQLAlchemy mysql-connector-python sqlalchemy-utils alembic pytest
from Cviceni2.menu import Menu

def main():
    # udelal jsem si zvlast tridu pro menu aby se dalo nahradit jinym, treba GUI, nebo jinaci volby atd...
    menu = Menu()
    menu.show()

if __name__ == '__main__':
    #tohle je jen ujisteni, ze se to spousti primo z hlavniho modulu
    main()