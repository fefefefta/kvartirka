# 🏰 kvartirka
Тестовое задание

## 🛸 Особенности
Для выполнения задания я пользовался **django-rest-framework** и **postgreSQL**. Чтобы эффективнее работать с деревом комментариев, я использовал стороннюю библиотеку **django-mppt** для хранения графовых структур в базе данных.

## 🛠 Ставим
0. сначала заполучите [докер](https://www.docker.com/get-started/)
1. стяните репозиторий и перейдите в директорию проекта
```
> git clone https://github.com/fefefefta/kvartirka
> cd kvartirka
```
2. запустите докер
```
> docker build .
> docker-compose build
> docker-compose up
```
3. переходим на [0.0.0.0:8000](http://0.0.0.0:8000) <br> <br>
***чтобы остановить работу докера нажмите Ctrl+C***


## 💣 фичиии!!!
### 1. Получить список всех статей:
[**/articles/**](http://0.0.0.0:8000/articles/) - GET-запрос<br><br>
**То же самое из терминала:**
```
curl --request GET http://0.0.0.0:8000/articles/
```
<br><br>
### 2. Добавить статью:
[**/articles/**](http://0.0.0.0:8000/articles/) - POST-запрос
```
{
  "title": "hello world",
  "text": "bla-bla-bla"
}
```
<br><br>
**То же самое из терминала:**
```
curl -H "Content-Type: application/json" --request POST --data '{"title":"hello world", "text":"bla-bla-bla"}' http://0.0.0.0:8000/articles/
```
<br><br>
### 3. Получить статью по id и комментарии на первых трех уровнях вложенности:
[**/articles/1/**](http://0.0.0.0:8000/articles/1/) - GET-запрос<br><br>
**То же самое из терминала:**
```
curl --request GET http://0.0.0.0:8000/articles/1/
```
<br><br>
### 4. Получить все дерево комментариев к статье по id:
[**/articles/1/comments/**](http://0.0.0.0:8000/articles/1/comments/) - GET-запрос<br><br>
**То же самое из терминала:**
```
curl --request GET http://0.0.0.0:8000/articles/1/comments/
```
<br><br>
### 5. Добавить комментарий к статье (на любом уровне вложенности):
[**/articles/1/comments/**](http://0.0.0.0:8000/articles/1/comments/) - POST-запрос <br>
**для комментария первого уровня**
```
{
  "text": "first comment. or not?"
}
```
**для комментариев на остальных уровнях**
```
{
  "text": "mb",
  "answered_to": 1
}
```
<br><br>
**То же самое из терминала:**
```
curl -H "Content-Type: application/json" --request POST --data '{"text": "first comment. or not?"}' http://0.0.0.0:8000/articles/1/comments/
```
```
curl -H "Content-Type: application/json" --request POST --data '{"text": "mb", "answered_to": 1}' http://0.0.0.0:8000/articles/1/comments/
```
<br><br>

### 6. Получить комментарий и все дерево ответов на него (дерево только в том случае, если комментарий на 3-ем уровне вложенности):
[**/articles/1/comments/1/**](http://0.0.0.0:8000/articles/1/comments/1/) - GET-запрос<br><br>
**То же самое из терминала:**
```
curl --request GET http://0.0.0.0:8000/articles/1/comments/1/
```

### 7. Добавить комментарий в ответ на тот, на который указывает URL:
[**/articles/1/comments/1/**](http://0.0.0.0:8000/articles/1/comments/1/) - POST-запрос
```
{
  "text": "may be. dunno how it works"
}
```
<br><br>
**То же самое из терминала:**
```
curl -H "Content-Type: application/json" --request POST --data '{"text": "may be. dunno how it works"}' http://0.0.0.0:8000/articles/1/comments/1/
```
