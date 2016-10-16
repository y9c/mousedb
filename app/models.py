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


# genotype
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
                 (1, 'suckling'),
                 (2, 'mating'),
                 (3, 'lactating'),
                 (4, 'dead'), ),
        default=0, )



    dob = models.DateField('date of birth', blank=True, null=True)
    dod = models.DateField('date of death', blank=True, null=True)
    notes = models.CharField(max_length=200, null=True, blank=True)

    # property
    #genotype = models.ForeignKey(Genotype)
    #phenotype = models.ForeignKey(Phenotype)

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
# 2.1 # Mating
class Mate(models.Model):
    mate_id = models.CharField(max_length=20)
    mate_start_date = models.DateTimeField('Mate Start Date')
    mate_end_date = models.DateTimeField('Mate End Date')

    paternal_id = models.ManyToManyField(
        Mouse, related_name='paternal', verbose_name='paternal mouse object')
    maternal_id = models.ManyToManyField(
        Mouse, related_name='maternal', verbose_name='maternal mouse object')

    def __str__(self):
        return self.mate_id

    def days(self):
        return datetime.now() - self.mate_start_date


# 2.2 # Phenotyping
class Get_Phenotype(models.Model):
    check_point = models.CharField('check_point', max_length=50, unique=True)
    date = models.DateField('Weighting Date')
    time = models.TimeField('Weighting Time')
    health = models.CharField(max_length=50, null=True)
    color = models.IntegerField(
        choices=((0, 'Black'),
                 (1, 'White'),
                 (2, 'Nake'), ), default=0)

    to_mouse = models.ManyToManyField(
        Mouse,
        related_name='phenotype',
        verbose_name='get phenotype for mouse object')

    def __str__(self):
        return str(self.date) + ': ' + ' / '.join(
            mouse.mouse_id for mouse in self.to_mouse.all())


class Get_Phenotype_Weight(models.Model):
    check_point = models.CharField('check_point', max_length=50, unique=True)
    date = models.DateField('Weighting Date')
    time = models.TimeField('Weighting Time')
    weight = models.FloatField('Weight')

    to_mouse = models.ManyToManyField(
        Mouse,
        related_name='phenotype_weight',
        verbose_name='get phenotype weight for mouse object')

    def __str__(self):
        return str(self.date) + ': ' + ' / '.join(
            mouse.mouse_id for mouse in self.to_mouse.all())


# 2.3 # Genotyping
class Get_Genotype(models.Model):
    check_point = models.CharField('check_point', max_length=50, unique=True)
    date = models.DateField('Genotyping Date')
    time = models.TimeField('Genotyping Time')
    mate = Mate()
    litter = models.IntegerField(null=True)

    genotype = models.ForeignKey(Genotype, on_delete=models.CASCADE, null=True)

    to_mouse = models.ManyToManyField(
        Mouse,
        related_name='genotype',
        verbose_name='get genotype for mouse object')

    def __str__(self):
        return str(self.date) + ': ' + ' / '.join(
            mouse.mouse_id for mouse in self.to_mouse.all())


# 2.3 # Sack
class Do_Sack(models.Model):
    date = models.DateField('Sacked Date')
    time = models.TimeField('Sacked Time')
    corpse = models.IntegerField(
        choices=((0, '丢弃'),
                 (1, '实验'),
                 (2, '送出'), ), default=0)

    to_mouse = models.ManyToManyField(
        Mouse, related_name='sack', verbose_name='sack event to mouse object')

    def __str__(self):
        return self.date + ': ' + ' / '.join(mouse.mouse_id
                                             for mouse in self.to_mouse.all())



# 2.5 # Weaning
class Wean(models.Model):
    weam_id = models.CharField(max_length=20)
    weam_start_date = models.DateTimeField('weam Start Date')
    weam_end_date = models.DateTimeField('weam End Date')
    litter = models.IntegerField(default=0)

    to_mouse = models.ManyToManyField(
        Mouse, related_name='wean', verbose_name='wean event to mouse object')

    def __str__(self):
        return self.mate_id

    def days(self):
        return datetime.now() - self.mate_start_date


# 2.6 # Feeding
class Do_AddChow(models.Model):
    category = models.CharField(max_length=200)
    date = models.DateField('Chow Added Date')
    time = models.TimeField('Chow Added Time')
    amount = models.FloatField('Chow Added Amount')

    to_mouse = models.ManyToManyField(
        Mouse,
        related_name='add_chow',
        verbose_name='addchow event to mouse object')

    def __str__(self):
        return self.category + ': ' + ' / '.join(
            mouse.mouse_id for mouse in self.to_mouse.all())


class Do_AddDrink(models.Model):
    category = models.CharField(max_length=200)
    date = models.DateField('Drink Added Date')
    time = models.TimeField('Drink Added Time')
    amount = models.FloatField('Drink Amount')

    to_mouse = models.ManyToManyField(
        Mouse,
        related_name='add_drink',
        verbose_name='adddrink event to mouse object')

    def __str__(self):
        return self.category + ': ' + ' / '.join(
            mouse.mouse_id for mouse in self.to_mouse.all())


class Do_AddBedding(models.Model):
    category = models.CharField(max_length=200, null=True)
    date = models.DateField('Bedding Added Date')
    time = models.TimeField('Bedding Added Time')
    note = models.CharField(max_length=200)

    to_mouse = models.ManyToManyField(
        Mouse,
        related_name='add_bedding',
        verbose_name='add bedding event to mouse object')

    def __str__(self):
        return self.category + ': ' + ' / '.join(
            mouse.mouse_id for mouse in self.to_mouse.all())


# 2.7 # experiment
class Do_InjectVirus(models.Model):
    category = models.CharField(max_length=200, null=True)
    date = models.DateField('Bedding Added Date')
    time = models.TimeField('Bedding Added Time')
    note = models.CharField(max_length=200)

    to_mouse = models.ManyToManyField(
        Mouse,
        related_name='inject_virus',
        verbose_name='inject virus event to mouse object')

    def __str__(self):
        return self.category + ': ' + ' / '.join(
            mouse.mouse_id for mouse in self.to_mouse.all())


# 3 # show
# 3.1 # mouse details
#class Show_MouseDetails(models.Model):
#    id = Mouse.mouse_id
#    mouse = Mouse.objects.get(mouse_id = id)
#    genotype = mouse.genotype.all()

