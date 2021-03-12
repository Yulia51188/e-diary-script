# Скрипт для исправления электронного дневника

Этот скрипт поможет исправить в электронном дневнике плохие оценки на пятерки, удалить замечания за ввсе время для указанного ученика и добавить одну похвалу от учителя по указанному предмету к последнему уроку, к которому похвала отсутствовала.

## Подготовка

Для начала необходимы:
- работающий сайт электронного дневника на отдельном сервере, с базой данных
- доступ к серверу, в т.ч. для изменения базы данных
- нужно уметь скачивать и загружать файлы на сервер, открывать консоль и запускать там команды.

При разработке скрипта использовался [прототип сайта электронного дневника](https://github.com/devmanorg/e-diary/tree/master) и тестовая база данных.


## Запуск

Чтобы исправить оценки, цдалить замечания и добавить одну похвалу от учителя, необходимо:

- скачать репозиторий с GitHub (в репозитории находятся два файла: `make_good_score.py` и `README.md`

- загрузить файл `make_good_score.py` на сервер сайта электронного дневника и разместить в той же директории `datacenter`, что и файл `models.py`

- запустить консоль или терминал на сервере

- запустить Django Shell с помощью команды консоли:

```bash
$ python manage.py shell

```
- в Django Shell импортировать функцию `make_good_score`:
```
>>> from make_good_score import make_good_score
```
- запустить функцию `make_good_score` с помощью команды, указав имя для поиска ученика и предмет, по которому нужно добавить похвалу :
```
>>> make_good_score("Фролов Иван", "Литература")
2021-03-12 13:34:34,390 - excellent_student_logger - INFO - Ученик найден: Фролов Иван Григорьевич
2021-03-12 13:34:34,391 - excellent_student_logger - INFO - 0 плохих оценок исправлены для ученика Фролов Иван Григорьевич
2021-03-12 13:34:34,392 - excellent_student_logger - INFO - Замечания удалены для ученика Фролов Иван Григорьевич
2021-03-12 13:34:34,463 - excellent_student_logger - INFO - Добавлена похвала: 2019-05-16, Литература, Фролов Иван Григорьевич
```
- на сайте электронного дневника проверить, что удалены плохие оценки, замечания, добавлена похвала
- при необходимости запустить функцию еще раз, изменив имя ученика и/или предмет:
```
>>> make_good_score("Васильева Полина", "Математика")
2021-03-12 13:42:11,229 - excellent_student_logger - INFO - Ученик найден: Васильева Полина Захаровна
2021-03-12 13:42:12,166 - excellent_student_logger - INFO - 165 плохих оценок исправлены для ученика Васильева Полина Захаровна
2021-03-12 13:42:12,167 - excellent_student_logger - INFO - Замечания удалены для ученика Васильева Полина Захаровна
2021-03-12 13:42:12,231 - excellent_student_logger - INFO - Добавлена похвала: 2019-05-21, Математика, Васильева Полина Захаровна
```

## Ошибки при запуске

При запуске скрипта могут быть допущены ошибки в имени и названии предмета, в таком случае, предусмотрены три ситуации:
- по указанному имени не найдено ни одного ученика в базе:
```
>>> make_good_score("Григорьев Владимир", "Литература")
2021-03-12 13:38:22,003 - excellent_student_logger - ERROR - Ученик с именем "Григорьев Владимир" не найден
```
Проверьте написание имени, фамилии, запустите функцию еще раз. В базе имена записаны в формате `Фамилия Имя Отчество`

- по указанному имени найдено много учеников:
```
>>> make_good_score("Григорьев", "Литература")
2021-03-12 13:38:13,431 - excellent_student_logger - ERROR - Уточните имя "Григорьев": в базе обнаружено слишком много учеников с таким именем
```
Добавьте фамилию, запустите функцию еще раз.

- не найден указанный предмет для похвалы:
```
>>> make_good_score("Васильева Полина", "Китайский язык")
2021-03-12 13:50:14,502 - excellent_student_logger - INFO - Ученик найден: Васильева Полина Захаровна
2021-03-12 13:50:14,503 - excellent_student_logger - INFO - 0 плохих оценок исправлены для ученика Васильева Полина Захаровна
2021-03-12 13:50:14,504 - excellent_student_logger - INFO - Замечания удалены для ученика Васильева Полина Захаровна
2021-03-12 13:50:14,505 - excellent_student_logger - ERROR - Ошибка при добавлении похвалы: уроки с названием "Китайский язык" не найдены
```
Проверьте написание или укажите другой предмет, запустите функцию еще раз.

- по указанному предмету не осталось ни одного урока без похвалы
```
>>> make_good_score("Васильева Полина", "Русскиу язык")
2021-03-12 13:50:14,502 - excellent_student_logger - INFO - Ученик найден: Васильева Полина Захаровна
2021-03-12 13:50:14,503 - excellent_student_logger - INFO - 0 плохих оценок исправлены для ученика Васильева Полина Захаровна
2021-03-12 13:50:14,504 - excellent_student_logger - INFO - Замечания удалены для ученика Васильева Полина Захаровна
2021-03-12 13:50:14,505 - excellent_student_logger - ERROR - Ошибка при добавлении похвалы: не найдено уроков "Русский язык" без похвалы, выберите другой предмет'
```
Укажите название другого предмета и запустите функцию еще раз.

## Цели проекта

Код написан в учебных целях — это урок в курсе по Python и веб-разработке на сайте [Devman](https://dvmn.org).
