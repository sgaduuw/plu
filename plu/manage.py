from plu.database import Base, engine, SessionLocal
from plu.models import Group, User, Transactions
from passlib.context import CryptContext
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

db = SessionLocal()


def create_tables():
    Base.metadata.create_all(bind=engine)


def ensure_groups():
    group_names = ['admin', 'managers', 'sellers']
    for group_name in group_names:
        q = db.query(Group).filter(Group.name == group_name).first() is not None
        if not q:
            add_this = Group(name=group_name)
            db.add(add_this)
    db.commit()


def ensure_eelco():
    q = db.query(User).filter(User.username == 'eelco').first() is not None
    print(q)
    if not q:
        print('Adding user eelco')
        eelco = User(
            username='eelco',
            password='qqq',
            email='eelco@init1.nl',
            group_id=1
        )
        print(eelco)
        db.add(eelco)
        db.commit()
        print(pwd_context.hash(eelco.password))


if __name__ == "__main__":
    create_tables()
    ensure_groups()
    ensure_eelco()
    