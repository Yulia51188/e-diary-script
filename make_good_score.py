import logging
import random

from datacenter.models import Chastisement
from datacenter.models import Commendation
from datacenter.models import Lesson
from datacenter.models import Mark
from datacenter.models import Schoolkid
from django.core.exceptions import MultipleObjectsReturned
from django.core.exceptions import ObjectDoesNotExist

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
    bad_marks = Mark.objects.filter(schoolkid=schoolkid, points__in=[2, 3])
    for bad_mark in bad_marks:
        bad_mark.points = 5
        bad_mark.save()
    logger.info(f'{len(bad_marks)} bad marks are fixed for {schoolkid.full_name}')


def remove_chastisements(schoolkid):
    Chastisement.objects.filter(schoolkid=schoolkid).delete()
    logger.info(f'Chastisements deleted for {schoolkid.full_name}')


def correct_bad_marks_and_chartisements(name):
    try:
        child = get_schoolkid(name)
        fix_marks(child)
        remove_chastisements(child)
    except ObjectDoesNotExist:
        logger.error(f'No schoolkid with name "{name}" was found')
    except MultipleObjectsReturned:
        logger.error(f'Clarify name "{name}": too many schoolkids was found')


def get_schoolkid(name):
    child = Schoolkid.objects.get(full_name__contains=name)
    logger.info(f'Pupil is found: {child.full_name}')
    return child


def is_commendation_at_lesson(schoolkid, lesson):
    commendations = Commendation.objects.filter(
        schoolkid=schoolkid,
        subject=lesson.subject,
        created=lesson.date
    )
    if not any(commendations):
        logging.debug(f'No commendations at {lesson.subject.title}, {lesson.date}')
        return
    logging.debug(f'Found {len(commendations)} commendations at '
                    f'{lesson.subject.title}, {lesson.date}')
    return True


def get_last_lesson_without_commendation(schoolkid, subject_title):
    lessons = Lesson.objects.filter(
        year_of_study=schoolkid.year_of_study,
        group_letter=schoolkid.group_letter,
        subject__title=subject_title
    ).order_by('date')
    lessons_without_commendations = [lesson for lesson in lessons
        if not is_commendation_at_lesson(schoolkid, lesson)]
    return lessons_without_commendations[-1]


def create_commendation(name, subject_title):
    try:
        child = get_schoolkid(name)
        last_lesson = get_last_lesson_without_commendation(child, subject_title)
        Commendation.objects.create(
            text=random.choice(COMMENDATIONS),
            created=last_lesson.date,
            schoolkid=child,
            subject=last_lesson.subject,
            teacher=last_lesson.teacher,
        )
        logger.info(f'Commendation created: {last_lesson.date}, '
                    f'{last_lesson.subject.title}, {child.full_name}')
    except ObjectDoesNotExist:
        logger.error(f'No schoolkid with name "{name}" was found')
    except MultipleObjectsReturned:
        logger.error(f'Clarify name "{name}": too many schoolkids was found')