import uuid
from functools import reduce
from django.db import models

from localflavor.us.models import USStateField

# Create your models here.
class Test(models.Model):
    class Meta:
        ordering = ('name',)
    name = models.CharField(max_length=50)
    slug = models.SlugField()
    introduction = models.TextField()
    description = models.TextField()
    # Add Sort Order Field

    def __str__(self):
        return self.name


class Worker(models.Model):
    id = models.UUIDField(
            primary_key = True,
            default = uuid.uuid4,
            editable = False)
    turk_id = models.CharField(max_length=255, blank=True, null=True)
    age = models.PositiveSmallIntegerField(help_text='You must be 18+ to take this survey')
    gender = models.CharField(max_length=255, help_text='To which gender identity do you most identify?', choices = [
                                    ('male', 'Male'),
                                    ('female', 'Female'),
                                    ('transgender_male', 'Transgender Male'),
                                    ('transgender_female', 'Transgender Female'),
                                    ('gender_nonconforming', 'Gender Variant/Non-Conforming'),
                                    ('prefer_not_to_answer', 'Prefer Not To Answer'),
                                ])
    city = models.CharField(max_length=255)
    state = USStateField()
    ethnicity = models.CharField(max_length=255, help_text="Which of the following ethnic group(s) do you consider yourself a member?",
                                choices = [
                                    ('black', 'African, African American, Black'),
                                    ('indigenous', 'American Indian, Alaska Native'),
                                    ('asian', 'Asian, Asian-American'),
                                    ('hispanic', 'Hispanic, Latino, Latina, LatinX'),
                                    ('middle_eastern', 'Middle Eastern'),
                                    ('pacific_islander', 'Native Hawaiian or Other Pacific Islander'),
                                    ('white', 'Non-Hispanic Caucasian, White'),
                                ])
    education = models.CharField(max_length=255, help_text="What is the highest degree or level of education you have completed?",
                                choices = [
                                    ('none', 'None'),
                                    ('grade_school', 'Grade School (Preschool to 8th Grade)'),
                                    ('some_high_school', 'Some High School, No Diploma'),
                                    ('high_school', 'High School Graduate, Diploma or equivalent (GED)'),
                                    ('some_college', 'Some College Credit, No Degree'),
                                    ('trade', 'Trade/Vocational School'),
                                    ('associates_degree', 'Associates Degree'),
                                    ('bachelors_degree', 'Bachelor’s Degree'),
                                    ('masters_degree', 'Master’s Degree'),
                                    ('some_postgraduate', 'Some Postgraduate Work, No Degree'),
                                    ('postgraduate', 'Ph.D., J.D., M.D., or Other Professional Degree'),
                                ])
    
    marital_status = models.CharField(max_length=255, help_text="What is your marital status?",
                                choices = [
                                    ('single_never_married', 'Single, Never Married'),
                                    ('single_previously_married', 'Single, Previously Married'),
                                    ('married', 'Married'),
                                    ('domestic_partnership', 'Domestic Partnership'),
                                    ('widowed', 'Widowed'),
                                    ('separated', 'Separated'),
                                ])
    
    orientation = models.CharField(max_length=255, help_text="Which of the following do you most strongly identify with?",
                                    choices = [
                                        ('heterosexual', 'Heterosexual'),
                                        ('gay', 'Gay'),
                                        ('lesbian', 'Lesbian'),
                                        ('bisexual', 'Bisexual'),
                                        ('other', 'Other'),
                                    ])
    
    employment = models.CharField(max_length=255, help_text="Please select your current employment status.",
                                    choices=[
                                        ('employed', 'Employed for wages'),
                                        ('self_employed', 'Self Employed'),
                                        ('unemployed_looking', 'Out of work and looking for work'),
                                        ('unemployed_not_looking', 'Out of work but not currently looking for work'),
                                        ('homemaker', 'Homemaker'),
                                        ('student', 'Student'),
                                        ('military', 'Active-Duty Military'),
                                        ('veteran', 'Veteran'),
                                        ('retired', 'Retired'),
                                        ('disabled', 'Unable to work'),
                                    ])

    def __str__(self):
        return str(self.id)

    @property
    def tests_completed(self):
        test_count = Result.objects.filter(worker=self).order_by('test').values('test').annotate(n=models.Count('test')).count()
        return test_count

    @property
    def completed_all_tests(self):
        total_tests = Test.objects.all().count()
        return self.tests_completed == total_tests

    @property
    def total_answers(self):
        queryset = Result.objects.filter(worker=self).order_by('test').values('total').annotate(n=models.Count('total'))
        return reduce(lambda initial, elem: initial + elem['total'], queryset, 0)
    
    @property
    def total_correct_answers(self):
        queryset = Result.objects.filter(worker=self).order_by('test').values('correct').annotate(n=models.Count('correct'))
        return reduce(lambda initial, elem: initial + elem['correct'], queryset, 0)
    
    @property
    def pctCorrect(self):
        try:
            return "{:.2f}".format(self.total_correct_answers / self.total_answers)
        except:
            return 0



class Result(models.Model):
    worker = models.ForeignKey(Worker, on_delete=models.CASCADE, related_name='workers')
    test = models.ForeignKey(Test, on_delete=models.CASCADE, related_name='results')
    correct = models.PositiveIntegerField()
    total = models.PositiveIntegerField()
    raw = models.JSONField(blank=True, null=True)
    average_response_time = models.PositiveIntegerField(blank=True, null=True)
    fastest_response_time = models.PositiveIntegerField(blank=True, null=True)
    slowest_response_time = models.PositiveIntegerField(blank=True, null=True)
    median_response_time = models.PositiveIntegerField(blank=True, null=True)

    def __str__(self):
        return f"Worker: {self.worker.pk} {self.test.name} {self.correct}/{self.total}"

    @property
    def pctCorrect(self):
        try:
            return "{:.2f}".format(self.correct / self.total)
        except ZeroDivisionError as e:
            return "{:.2f}".format(0.0)
    
    @property
    def incorrect(self):
        return self.total - self.correct