# Create your models here.
import datetime

from django.db import models


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
    color = models.CharField(max_length=50, default='black',
                             choices=(('Black', 'Black'),
                                      ('White', 'White'),
                                      ('Nake', 'Nake'))
                             )
    note = models.CharField(max_length=200, null=True)

    def __str__(self):
        return "{}:{}".format(self.color, self.note)


# genotype group
class Genotype(models.Model):
    strain = models.CharField(max_length=50, default='C57BL/6')
    line = models.CharField(max_length=50, default='WT')
    locus = models.CharField(max_length=50, null=True)

    def line_id(self):
        mapper = {"WT": 1, "CRE": 2, "C": 2, "MSH2": 3, "MSH": 3, "M": 3, "RTTA": 4, "R": 4,
                  "T": 7 , "A": 7 , "MC": 5 , "MR": 6 , "TAH": 7 , "TR": 8 , "TRM": 9 ,
                  "MSH2+CRE": 5 , "MSH2+RTTA": 6 , "TAH+RTTA": 8 , "TAH+RTTA+MSH2": 9 ,
                  "A,R": 8 , "A,R,M": 9 , "M,C": 5 , "M,R": 6}
        return mapper[self.line]

    def sex(self):
        if "S(XY)" in self.locus.upper().strip():
            return "Male"
        if "S(XX)" in self.locus.upper().strip():
            return "Female"
        else:
            return "Unknow"

    def __str__(self):
        return "{}:{}:{}".format(self.strain, self.line, self.locus)


class Health(models.Model):
    date = models.DateField('Weighting Date')
    health = models.CharField(max_length=50, null=True)

    def __str__(self):
        return "{}:{}".format(self.date, self.health)


class Weight(models.Model):
    date = models.DateField('Weighting Date')
    weight = models.FloatField('Weight')

    def __str__(self):
        return "{}:{}".format(self.date, self.weight)


# breed
class Breed(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50, unique=True)
    mate_start_date = models.DateField('date of mate start', blank=False, null=False)
    mate_end_date = models.DateField('date of mate end', blank=True, null=True)
    pregnant = models.NullBooleanField(default=None)
    infanticide = models.NullBooleanField(default=None)
    born_date = models.DateField('date of born', blank=False, null=True)
    wean_start_date = models.DateField('date of wean start', blank=True, null=True)
    wean_end_date = models.DateField('date of wean end', blank=True, null=True)
    litter_count = models.IntegerField(null=True)
    genotyped = models.BooleanField(default=False)

    # paternal_id = models.ManyToManyField(
    #     Mouse, related_name='paternal', verbose_name='paternal mouse object')
    # maternal_id = models.ManyToManyField(
    #     Mouse, related_name='maternal', verbose_name='maternal mouse object')
    def status(self):
        if self.mate_end_date is None:
            return "mating"
        elif self.pregnant is None:
            return "observing"
        elif self.pregnant is False:
            # 未怀孕
            return "unpregnant"
        elif self.born_date is None:
            return "pregnanting"
        elif self.infanticide is True:
            # 吃仔
            return "infanticided"
        elif self.wean_end_date is None:
            return "weaning"
        else:
            # 断奶
            return "finish"

    def mate_days(self):
        return datetime.datetime.now() - self.mate_start_date

    def __str__(self):
        return self.name


# feed(chow drink bedding)
class Feed(models.Model):
    date = models.DateField('Chow Added Date')
    chow = models.CharField(max_length=200, default="Normal")
    drink = models.CharField(max_length=200, default="Normal")
    amount = models.FloatField('Chow Added Amount')

    def __str__(self):
        return str(self.date) + ': ' + ' / '.join(
            mouse.mouse_id for mouse in self.mouse.all())


# experiment
class InjectVirus(models.Model):
    category = models.CharField(max_length=200, null=True)
    date = models.DateField('Bedding Added Date')
    time = models.TimeField('Bedding Added Time')
    note = models.CharField(max_length=200)

    def __str__(self):
        return self.category + ': ' + ' / '.join(
            mouse.mouse_id for mouse in self.mouse.all())

# # # # # # # #
# 1 # Individual
# # # # # # # #


class Mouse(models.Model):
    mouse_id = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=50, blank=True, null=True)

    # property
    # one-to-one
    source = models.CharField(max_length=50, default='饲养产生后代',
                              choices=(('饲养产生后代', '饲养产生后代'),
                                       ('广东省实验动物中心', '广东省实验动物中心'),
                                       ('南京模式生物中心', '南京模式生物中心'),
                                       ('unknown', 'unknown'), )
                              )

    status = models.CharField(max_length=50, default='idle',
                              choices=(('idle', 'idle'),
                                       ('suckling', 'suckling'),
                                       ('mating', 'mating'),
                                       ('lactating', 'lactating'),
                                       ('dead', 'dead'),
                                       ('unknown', 'unknown'), ),
                              )

    dob = models.DateField('date of birth', blank=True, null=True)
    dod = models.DateField('date of death', blank=True, null=True)
    notes = models.CharField(max_length=200, null=True, blank=True)
    corpse = models.CharField(max_length=50, default='丢弃',
                              choices=(('丢弃', '丢弃'),
                                       ('实验', '实验'),
                                       ('送出', '送出'), ))

    born_order = models.IntegerField('the order in Breed', blank=True, null=True)

    # many-to-one
    genotype = models.ForeignKey(Genotype,
                                 related_name='mouse',
                                 verbose_name='genotype that this mouse is',
                                 blank=True, null=True)
    phenotype = models.ForeignKey(Phenotype,
                                  related_name='mouse',
                                  verbose_name='phenotype that this mouse is',
                                  blank=True, null=True)
    born = models.ForeignKey(
        Breed,
        related_name='litter',
        verbose_name='born breed',
        blank=True, null=True)

    # many-to-many
    breed = models.ManyToManyField(
        Breed,
        related_name='parent',
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
# class Show_MouseDetails(models.Model):
#    id = Mouse.mouse_id
#    mouse = Mouse.objects.get(mouse_id = id)
#    genotype = mouse.genotype.all()
