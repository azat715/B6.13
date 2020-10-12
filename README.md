# B6.13
Примеры использования
- http -f GET http://localhost:8081/api/artist
- http -f GET 'http://localhost:8081/api/artist?type=year&value=1966'
- http -f GET 'http://localhost:8081/api/artist?type=genre&value=Rhythm%20and%20blues'
- http -f GET 'http://localhost:8081/api/artist?type=artist&value=Beatles'
- http -f GET 'http://localhost:8081/api/artist?type=album&value=Please%20Please%20Me'
- http --form POST http://localhost:8081/new_artist artist="Metallica" album="Kill ’Em All" year=1983 genre="thrash metal"

- http://localhost:8081/new_artist можно зайти через браузер и с помощью формы добавить запись артиста
- http://localhost:8081/artist можно зайти через браузер и с помощью формы выполнить запрос к базе

Валидация 
- http --form POST http://localhost:8081/new_artist artist="" album="" year=l genre="" 
- http --form POST http://localhost:8081/new_artist artist="" album="" year=sss genre="" 


обязательно установить SQLAlchemy bottle-sqlalchemy WTForms 
