# Create your models here.
import datetime

from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy


class BlogsPost(models.Model):
    title = models.CharField(max_length=150)
    body = models.TextField()
    timestamp = models.DateTimeField()

    def __str__(self):
        return self.title


# demo question and choice
class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')

    def __str__(self):
        return self.question_text

    def was_published_recently(self):
        return self.pub_date >= timezone.now() - datetime.timedelta(days=1)


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def __str__(self):
        return self.choice_text


# demo country and person

class Organization(models.Model):
    name = models.CharField(verbose_name="NAME", max_length=100)


class Person(models.Model):
    name = models.CharField(verbose_name="full name", max_length=100)
    organization = models.ForeignKey(Organization, null=True, blank=True, on_delete=models.CASCADE)
    married = models.BooleanField(verbose_name="married", default=False)




# mouse management
# 1 # mouse recording
# 1.1 # Phenotyping
class Weighting(models.Model):
    date = models.DateField('Weighting Date')
    time = models.TimeField('Weighting Time')
    weight = models.FloatField('Weight')

    def __str__(self):
        return self.category


# 1.2 # Genotyping
class Genotype(models.Model):
    strain = models.CharField(max_length=50, default='C57BL/6')
    line = models.CharField(max_length=50, default='WT')

    def __str__(self):
        return "{}:{}".format(self.strain,self.line)


# 1 # Individual
class Mouse(models.Model):
    mouse_id = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=50, default='?')

    # Genotype
    genotype = models.ForeignKey(Genotype)

    # Phenotype
    health = models.CharField(max_length=50, null=True)

    # property
    dob = models.DateField('date of birth', blank=True, null=True)
    dod = models.DateField('date of death', blank=True, null=True)

    sacked = models.BooleanField(default=False)
    sackDate = models.DateField('sac date', blank=True, null=True)

    sex = models.IntegerField(
        choices=(
            (0, 'M'),
            (1, 'F'),
            (2, '?'),
        ),
    default=2)

    status = models.IntegerField(
        choices=(
            (0, 'idle'),
            (1, 'nuring'),
            (2, 'mating'),
            (3, 'weaning'),
        ),
        default=0,
    )

    notes = models.CharField(max_length=200, null=True, blank=True)


    def age(self):
        if self.dob is None:
            return None
        today = datetime.date.today()
        return (today - self.dob).days

    def info(self):
        return "%s (P%d %s %s)" % (
            str(self.mouse_id),
            self.age(),
            str(self.genotype),
            str(self.sex()),
        )

    def __str__(self):
        return str(self.mouse_id)


# 2 # Event

# 2.1 # Mating
class Mate(models.Model):
    mate_id = models.CharField(max_length=20)
    mate_start_date = models.DateTimeField('Mate Start Date')
    mate_end_date = models.DateTimeField('Mate End Date')
    paternal_id = models.ManyToManyField(
        Mouse, related_name='paternal', verbose_name='paternal mouse object')
    maternal_id = models.ManyToManyField(
        Mouse, related_name='maternal', verbose_name='maternal mouse object')
    litter = models.IntegerField(default=0)


    def __str__(self):
        return self.mate_id

    def days(self):
        return datetime.now() - self.mate_start_date

 # 2.2 # Feeding


class AddChow(models.Model):
    category = models.CharField(max_length=200)
    date = models.DateField('Chow Added Date')
    time = models.TimeField('Chow Added Time')
    amount = models.FloatField('Chow Added Amount')

    def __str__(self):
        return self.category


class AddDrink(models.Model):
    category = models.CharField(max_length=200)
    date = models.DateField('Drink Added Date')
    time = models.TimeField('Drink Added Time')
    amount = models.FloatField('Drink Amount')

    def __str__(self):
        return self.category


class AddBedding(models.Model):
    date = models.DateField('Bedding Added Date')
    time = models.TimeField('Bedding Added Time')
    note = models.CharField(max_length=200)
