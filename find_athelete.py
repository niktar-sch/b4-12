import sqlalchemy as sa
from sqlalchemy.sql import func
import users

class Athelete(users.Base):
    """
    Описывает структуру таблицы athelete для хранения данных по спортсменам
    """
    # задаем название таблицы
    __tablename__ = 'athelete'
    # идентификатор пользователя, первичный ключ
    id = sa.Column(sa.Integer, primary_key=True)
    # возраст
    age = sa.Column(sa.Integer)
    # дата рождения
    birthdate = sa.Column(sa.Text)
    # пол
    gender = sa.Column(sa.Text)
    # рост
    height = sa.Column(sa.Float)
    # вес
    weight = sa.Column(sa.Integer)
    # имя
    name = sa.Column(sa.Text)
    # количество золотых медалей
    gold_medals = sa.Column(sa.Integer)
    # количество серебряных медалей
    silver_medals = sa.Column(sa.Integer)
    # количество бронзовых медалей
    bronze_medals = sa.Column(sa.Integer)
    # общее количество медалей
    total_medals = sa.Column(sa.Integer)
    # вид спорта
    sport = sa.Column(sa.Text)
    # страна
    country = sa.Column(sa.Text)


def request_data():
    """
    Запрашивает у пользователя user_id
    """
    print("Поиск атлетов, похожих на одного из пользователей.")
    user_id = input("Ввети идентификатор пользователя: ")
    return int(user_id)

def main():
    session = users.connect_db()
    user_id = request_data()
    user = session.query(users.User).filter(users.User.id == user_id).first()
    if user:
        nearest_birth_athelete = session.query(Athelete)\
                                 .filter(Athelete.birthdate.isnot(None))\
                                 .order_by(func.abs(func.julianday(Athelete.birthdate) - func.julianday(user.birthdate))).first()
        nearest_height_athelete = session.query(Athelete)\
                                  .filter(Athelete.height.isnot(None))\
                                  .order_by(func.abs(Athelete.height - user.height)).first()
        print(f'Ближайший по дате рождения атлет: id: {nearest_birth_athelete.id}, имя: {nearest_birth_athelete.name}, дата рождения: {nearest_birth_athelete.birthdate}')
        print(f'Ближайший по росту атлет: id: {nearest_height_athelete.id}, имя: {nearest_height_athelete.name}, рост: {nearest_height_athelete.height}')
    else:
        print('Пользовалель с таким id не найден')

if __name__ == "__main__":
    main()
