from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from multiselectfield import MultiSelectField


class Base(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)


class Role(Base):
    name = models.CharField(max_length=255)


class User(Base):
    role = models.ForeignKey('Role', on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    course = models.IntegerField(default=1, validators=[MinValueValidator(1), MaxValueValidator(4)])


class UserSkills(Base):
    user = models.ForeignKey('User', on_delete=models.CASCADE)
    skill = models.ForeignKey('Skill', on_delete=models.CASCADE)
    confirmed = models.ManyToManyField('User', blank=True)


class Cluster(Base):
    name = models.CharField(max_length=255)
    description = models.TextField()


class Project(Base):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    cluster = models.ForeignKey('Cluster', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='project_image')
    contact = models.CharField(max_length=255)
    teacher = models.ForeignKey('User', on_delete=models.CASCADE)
    curator = models.ForeignKey('User', on_delete=models.CASCADE, blank=True)
    students = models.ManyToManyField('User', blank=True)


class Goal(Base):
    goals_after = models.ManyToManyField('self', blank=True)
    project = models.ForeignKey('Project', on_delete=models.CASCADE)
    is_done = models.BooleanField(default=False)
    name = models.CharField(max_length=255)


class CheckList(Base):
    name = models.CharField(max_length=255)
    description = models.TextField()
    is_done = models.BooleanField(default=False)
    goal = models.ForeignKey('Goal', on_delete=models.CASCADE)


class Skill(Base):
    name = models.CharField(max_length=255)


class Vacancy(Base):
    COURSES = [
        (1, '1 курс'),
        (2, '2 курс'),
        (3, '3 курс'),
        (4, '4 курс')
    ]
    name = models.CharField(max_length=255)
    need_course = MultiSelectField(choices=COURSES)
    description = models.TextField()
    project = models.ForeignKey('Project', on_delete=models.CASCADE)
    skills = models.ManyToManyField('Skill')


class ApplicationVacation(Base):
    user = models.ForeignKey('User', on_delete=models.CASCADE)
    vacancy = models.ForeignKey('Vacancy', on_delete=models.CASCADE)
    chat = models.ForeignKey('Chat', on_delete=models.CASCADE)
    accept_last_project = models.BooleanField(null=True, default=None)
    accept_future_project = models.BooleanField(null=True, default=None)


class ApplicationProject(Base):
    user = models.ForeignKey('User', on_delete=models.CASCADE)
    employer = models.ForeignKey('User', on_delete=models.CASCADE)
    chat = models.ForeignKey('Chat', on_delete=models.CASCADE)
    accept_employer = models.BooleanField(null=True, default=None)


class RatingProject(Base):
    rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    user = models.ForeignKey('User', on_delete=models.CASCADE)
    project_to_rating = models.ForeignKey('Project', on_delete=models.CASCADE)


class RatingUser(Base):
    rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    user = models.ForeignKey('User', on_delete=models.CASCADE)
    user_to_rating = models.ForeignKey('User', on_delete=models.CASCADE)


class Message(Base):
    text_message = models.CharField(max_length=255)
    who_write = models.ForeignKey('User', on_delete=models.CASCADE)
    attached_file = models.ImageField(upload_to='message_attached')
    chat = models.ForeignKey('Chat', on_delete=models.CASCADE)


class Chat(Base):
    user_rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])