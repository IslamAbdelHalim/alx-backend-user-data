from user import User


print(User.__tablename__)


for column in User.__table__.columns:
    print(column, column.type)