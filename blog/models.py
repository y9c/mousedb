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

# mouse management


class Genotype(models.Model):
    name = models.CharField(max_length=50, default='C57')

    def __str__(self):
        return self.name


class Mate(models.Model):
    mate_id = models.CharField(max_length=20)
    mate_start_date = models.DateTimeField('Mate Start Date')
    mate_end_date = models.DateTimeField('Mate End Date')

    def __str__(self):
        return self.mate_id

    def how_old(self):
        return datetime.now() - self.mate_start_date


class Mouse(models.Model):
    name = models.CharField(max_length=50, unique=True)
    training_name = models.CharField(max_length=50, blank=True, null=True)
    dob = models.DateField('date of birth', blank=True, null=True)
    tmx = models.CharField(max_length=50, blank=True, null=True)
    sacked = models.BooleanField(default=False)
    headplate_color = models.CharField(max_length=15, blank=True, null=True)
    notes = models.CharField(max_length=50, null=True, blank=True)
    sackDate = models.DateField('sac date', blank=True, null=True)

    # Could imagine derived classes TrainingMouse and BreederMouse
    # Mostly just so that TrainingMouse has a lot more task-specific info
    # But it's possible that BreederMouse become TrainingMouse
    # And there isn't any BreederMouse-specific info
    role = models.IntegerField(
        choices=(
            (0, 'waiting'),
            (1, 'training'),
            (2, 'vacation'),
            (3, 'breeder'),
        ),
        default=0,
    )

    sex = models.IntegerField(
        choices=(
            (0, 'M'),
            (1, 'F'),
            (2, '?'),
        )
    )

    genotype = models.ForeignKey(Genotype)

    def info(self):
        """Returns TRAINING_NAME || NAME (SEX, AGE, GENOTYPE)

        """
        if self.training_name is not None and self.training_name != '':
            return self.training_name

        age = self.age()
        if age is None:
            return "%s (%s %s)" % (
                str(self.name),
                str(self.genotype),
                str(self.get_sex_display()),
            )
        else:
            return "%s (P%d %s %s)" % (
                str(self.name),
                self.age(),
                str(self.genotype),
                str(self.get_sex_display()),
            )

    def age(self):
        if self.dob is None:
            return None
        today = datetime.date.today()
        return (today - self.dob).days

    def __str__(self):
        return str(self.name)


class Country(models.Model):

    '''
    Represents a geographical Country
    '''
    name = models.CharField(max_length=100)
    population = models.PositiveIntegerField(
        verbose_name=ugettext_lazy('population'))
    tz = models.CharField(max_length=50)
    visits = models.PositiveIntegerField()
    commonwealth = models.NullBooleanField()
    flag = models.FileField(upload_to='blog/static/country/flags/')

    class Meta:
        verbose_name_plural = ugettext_lazy('countries')

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return 'country/%d' % self.pk

    @property
    def summary(self):
        return '%s (pop. %s)' % (self.name, self.population)


class Person(models.Model):
    name = models.CharField(max_length=200, verbose_name='Full Name')
    friendly = models.BooleanField(default=True)

    country = models.ForeignKey(Country, null=True)

    class Meta:
        verbose_name_plural = 'people'

    def __str__(self):
        return self.name
