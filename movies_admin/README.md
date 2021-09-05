# How to run

- клонируем репозиторий на локальную машину и перейдите в рабочую директорию:
  
  ```git clone https://github.com/TheZavitaev/Admin_panel_sprint_2 && cd Admin_panel_sprint_2```

- в корневой папке находим файл `.env.template`. 
  
- по образу и подобию необходимо создать файл `.env` и заполнить его своими значениями.

- запускаем процесс сборки и запуска контейнеров:
  
  ```docker-compose up -d```
- запускаем терминал внутри контейнера (на вин системах используйте winpty docker-compose exec admin_panel bash):

  ```docker-compose exec admin_panel bash```
- применяем миграции:
  
  ```./manage.py migrate```

- собираем статику:

  ```./manage.py collectstatic --no-input```

- запускаем генерацию данных:
  
  ```./manage.py generate_test_data```
- создаем суперпользователя:
  
  ```./manage.py createsuperuser```

- поднимаем вебсервер для разработки:
  
  ```./manage.py runserver```
- переходим по адресу:
  
  ```http://localhost/api/v1/movies/```