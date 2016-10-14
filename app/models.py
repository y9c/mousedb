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
    organization = models.ForeignKey(
        Organization, null=True, blank=True, on_delete=models.CASCADE)
    married = models.BooleanField(verbose_name="married", default=False)


# mouse management
# 0 # mouse property
# Phenotype
class Phenotype(models.Model):
    check_point = models.DateField('check_point', unique=True)
    date = models.DateField('Weighting Date')
    time = models.TimeField('Weighting Time')
    weight = models.FloatField('Weight')
    health = models.CharField(max_length=50, null=True)

    sex = models.IntegerField(
        choices=((0, 'M'),
                 (1, 'F'),
                 (2, '?'), ), default=2)

    def __str__(self):
        return "{}:{}".format(self.weight, self.health)


# genotype
class Genotype(models.Model):
    strain = models.CharField(max_length=50, default='C57BL/6')
    line = models.CharField(max_length=50, default='WT')
    locus = models.CharField(max_length=50, null=True)
    sex = models.IntegerField(
        choices=((0, 'M'),
                 (1, 'F'),
                 (2, '?'), ), default=2)

    def __str__(self):
        return "{}:{}:{}".format(self.strain, self.line, self.locus)


# 1 # Individual
class Mouse(models.Model):
    mouse_id = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=50, default='?')
    source = models.IntegerField(
        choices=((0, '饲养产生后代'),
                 (1, '广东省实验动物中心'),
                 (2, '南京模式生物中心'), ),
        default=0)

    status = models.IntegerField(
        choices=((0, 'idle'),
                 (1, 'nuring'),
                 (2, 'mating'),
                 (3, 'weaning'),
                 (4, 'sacked'),
                 (5, 'dead'), ),
        default=0, )

    # property
    dob = models.DateField('date of birth', blank=True, null=True)
    dod = models.DateField('date of death', blank=True, null=True)

    notes = models.CharField(max_length=200, null=True, blank=True)

    # 要关联的！！！
    # Phenotype
    # mate id
    # litter order
    # day of beath
    # day of sacked
    # Genotype
    #genotype = models.ForeignKey(Genotype)
    # genealogy
    # mate many to many

    def age(self):
        if self.dob is None:
            return None
        today = datetime.date.today()
        return (today - self.dob).days

    def info(self):
        return "{},{}".format(str(self.mouse_id),
                              self.age(), )

    def __str__(self):
        return str(self.mouse_id)


# 2 # Event
# 2.1 # Phenotyping
class Get_Weight(models.Model):
    date = models.DateField('Weighting Date')
    time = models.TimeField('Weighting Time')
    weight = models.FloatField('Weight')

    def __str__(self):
        return self.category


# 2.2 # Genotyping
class Get_Genotype(models.Model):
    date = models.DateField('Genotyping Date')
    time = models.TimeField('Genotyping Time')


# 2.3 # Sack
class Do_Sack(models.Model):
    date = models.DateField('Sacked Date')
    time = models.TimeField('Sacked Time')
    sacked = models.BooleanField(default=False)
    sackDate = models.DateField('sac date', blank=True, null=True)


# 2.4 # Mating
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
