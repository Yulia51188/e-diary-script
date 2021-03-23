import logging
import random

from datacenter.models import (Chastisement, Commendation, Lesson, Mark,
                               Schoolkid)

logger = logging.getLogger('excellent_student_logger')
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)


COMMENDATIONS = (
    'Молодец!',
    'Отлично!',
    'Хорошо!',
    'Гораздо лучше, чем я ожидал!',
    'Ты меня приятно удивил!',
    'Великолепно!',
    'Прекрасно!',
    'Ты меня очень обрадовал!',
    'Именно этого я давно ждал от тебя!',
    'Сказано здорово – просто и ясно!',
    'Ты, как всегда, точен!',
    'Очень хороший ответ!',
    'Талантливо!',
    'Ты сегодня прыгнул выше головы!',
    'Я поражен!',
    'Уже существенно лучше!',
    'Потрясающе!',
    'Замечательно!',
    'Прекрасное начало!',
    'Так держать!',
    'Ты на верном пути!',
    'Здорово!',
    'Это как раз то, что нужно!',
    'Я тобой горжусь!',
    'С каждым разом у тебя получается всё лучше!',
    'Мы с тобой не зря поработали!',
    'Я вижу, как ты стараешься!',
    'Ты растешь над собой!',
    'Ты многое сделал, я это вижу!',
    'Теперь у тебя точно все получится!',
)


def fix_marks(schoolkid):
    fixed_marks_count = Mark.objects.filter(schoolkid=schoolkid,
        points__in=[2, 3]).update(points=5)
    logger.info(f'{fixed_marks_count} плохих оценок исправлены для ученика '
                f'{schoolkid.full_name}')


def remove_chastisements(schoolkid):
    deleted_items = Chastisement.objects.filter(
        schoolkid=schoolkid).delete()
    logger.info(f'{deleted_items[0]} замечаний(ие) удалено для ученика '
        f'{schoolkid.full_name}')


def make_good_score(name, commendation_subject):
    try:
        child = get_schoolkid(name)
        fix_marks(child)
        remove_chastisements(child)
        create_commendation(child, commendation_subject)
    except Schoolkid.DoesNotExist:
        logger.error(f'Ученик с именем "{name}" не найден')
    except Schoolkid.MultipleObjectsReturned:
        logger.error(f'Уточните имя "{name}": в базе обнаружено слишком много '
            'учеников с таким именем')
    except ValueError as error:
        logger.error(error)


def get_schoolkid(name):
    child = Schoolkid.objects.get(full_name__contains=name)
    logger.info(f'Ученик найден: {child.full_name}')
    return child


def is_commendation_at_lesson(schoolkid, lesson):
    return Commendation.objects.filter(
                schoolkid=schoolkid,
                subject=lesson.subject,
                created=lesson.date
            ).exists()


def get_last_lesson_without_commendation(schoolkid, subject_title):
    lessons = Lesson.objects.filter(
        year_of_study=schoolkid.year_of_study,
        group_letter=schoolkid.group_letter,
        subject__title=subject_title
    ).order_by('date')
    if lessons.count() < 1:
        raise ValueError('Ошибка при добавлении похвалы: уроки с названием '
            f'"{subject_title}" не найдены')
    lessons_without_commendations = [lesson for lesson in lessons
        if not is_commendation_at_lesson(schoolkid, lesson)]
    if len(lessons_without_commendations) < 1:
        raise ValueError('Ошибка при добавлении похвалы: не найдено уроков'
            f'"{subject_title}" без похвалы, выберите другой предмет')
    return lessons_without_commendations[-1]


def create_commendation(schoolkid, subject_title):
    last_lesson = get_last_lesson_without_commendation(schoolkid, subject_title)
    Commendation.objects.create(
        text=random.choice(COMMENDATIONS),
        created=last_lesson.date,
        schoolkid=schoolkid,
        subject=last_lesson.subject,
        teacher=last_lesson.teacher,
    )
    logger.info(f'Добавлена похвала: {last_lesson.date}, '
        f'{last_lesson.subject.title}, {schoolkid.full_name}')