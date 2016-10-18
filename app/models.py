# Create your models here.
import datetime
import random
import string

from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy


class BlogsPost(models.Model):
    title = models.CharField(max_length=150)
    body = models.TextField()
    timestamp = models.DateTimeField()

    def __str__(self):
        return self.title

# mouse management


# 0 # mouse property
# Phenotype group
class Phenotype(models.Model):
    date = models.DateField('Weighting Date')
    time = models.TimeField('Weighting Time')
    weight = models.FloatField('Weight')
    health = models.CharField(max_length=50, null=True)

    color = models.IntegerField(
        choices=((0, 'Black'),
                 (1, 'White'),
                 (2, 'Nake'), ), default=0)

    #def __str__(self):
    #    return "{}:{}".format(self.date, self.check_point)


# genotype group
class Genotype(models.Model):
    strain = models.CharField(max_length=50, default='C57BL/6')
    line = models.CharField(max_length=50, default='WT')
    locus = models.CharField(max_length=50, null=True)

    def sex(self):
        if "S(XY)" in self.locus.upper().strip():
            return "Female"
        if "S(XX)" in self.locus.upper().strip():
            return "Male"
        else:
            return "Unknow"

    def __str__(self):
        return "{}:{}:{}".format(self.strain, self.line, self.locus)


class Weight(models.Model):
    date = models.DateField('Weighting Date')
    time = models.TimeField('Weighting Time')
    weight = models.FloatField('Weight')

    def __str__(self):
        return "{}:{}:{}".format(self.date, self.time, self.weight)


# breed
class Breed(models.Model):
    id = models.AutoField(primary_key=True)
    mate_start_date = models.DateField(
        'date of mate start', blank=True, null=True)
    mate_end_date = models.DateField('date of mate end', blank=True, null=True)
    born_date = models.DateField('date of born', null=True)
    wean_start_date = models.DateField(
        'date of wean start', blank=True, null=True)
    wean_end_date = models.DateField('date of wean end', blank=True, null=True)
    litter = models.IntegerField(null=True)
    genotyped = models.BooleanField(default=False)

    # paternal_id = models.ManyToManyField(
    #     Mouse, related_name='paternal', verbose_name='paternal mouse object')
    # maternal_id = models.ManyToManyField(
    #     Mouse, related_name='maternal', verbose_name='maternal mouse object')

    def mate_days(self):
        return datetime.now() - self.mate_start_date

    def __str__(self):
        return self.id


# feed(chow drink bedding)
class Feed(models.Model):
    date = models.DateField('Chow Added Date')
    time = models.TimeField('Chow Added Time')
    chow = models.CharField(max_length=200, default="Normal")
    drink = models.CharField(max_length=200, default="Normal")
    amount = models.FloatField('Chow Added Amount')

    def __str__(self):
        return self.category + ': ' + ' / '.join(
            mouse.mouse_id for mouse in self.to_mouse.all())


# experiment
class InjectVirus(models.Model):
    category = models.CharField(max_length=200, null=True)
    date = models.DateField('Bedding Added Date')
    time = models.TimeField('Bedding Added Time')
    note = models.CharField(max_length=200)

    def __str__(self):
        return self.category + ': ' + ' / '.join(
            mouse.mouse_id for mouse in self.to_mouse.all())

# # # # # # # #
# 1 # Individual
# # # # # # # #


class Mouse(models.Model):
    mouse_id = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=50, default='?')

    # property
    # one-to-one
    source = models.IntegerField(
        choices=((0, '饲养产生后代'),
                 (1, '广东省实验动物中心'),
                 (2, '南京模式生物中心'),
                 (9, 'unknown'), ),
        default=0)

    status = models.IntegerField(
        choices=((0, 'idle'),
                 (1, 'suckling'),
                 (2, 'mating'),
                 (3, 'lactating'),
                 (4, 'dead'),
                 (9, 'unknown'), ),
        default=0, )

    dob = models.DateField('date of birth', blank=True, null=True)
    dod = models.DateField('date of death', blank=True, null=True)
    notes = models.CharField(max_length=200, null=True, blank=True)
    corpse = models.IntegerField(
        choices=((0, '丢弃'),
                 (1, '实验'),
                 (2, '送出'), ), default=0)

    # many-to-one
    genotype = models.ForeignKey(Genotype, blank=True, null=True)
    phenotype = models.ForeignKey(Phenotype, blank=True, null=True)

    # many-to-many
    breed = models.ManyToManyField(
        Breed,
        related_name='paternal',
        verbose_name='breed that this mouse engage',
        blank=True)

    # one-to-many
    feed = models.ManyToManyField(
        Feed,
        related_name='mouse',
        verbose_name='feed that this mouse engage',
        blank=True)

    weight = models.ManyToManyField(
        Weight,
        related_name='mouse',
        verbose_name='weight record for this mouse',
        blank=True)

    injectvirus = models.ManyToManyField(
        InjectVirus,
        related_name='mouse',
        verbose_name='virus record for this mouse',
        blank=True)

    def age(self):
        if self.dob is None:
            return None
        else:
            today = datetime.date.today()
            return (today - self.dob).days

    def info(self):
        return "{},{}".format(str(self.mouse_id),
                              self.age(), )

    def __str__(self):
        return str(self.mouse_id)

# 3 # show
# 3.1 # mouse details
#class Show_MouseDetails(models.Model):
#    id = Mouse.mouse_id
#    mouse = Mouse.objects.get(mouse_id = id)
#    genotype = mouse.genotype.all()
