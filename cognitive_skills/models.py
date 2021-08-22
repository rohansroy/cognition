import uuid
from functools import reduce
from django.db import models

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
    turk_id = models.CharField(max_length=255)

    def __str__(self):
        return self.turk_id

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
        return f"Worker: {self.worker.turk_id} {self.test.name} {self.correct}/{self.total}"

    @property
    def pctCorrect(self):
        try:
            return "{:.2f}".format(self.correct / self.total)
        except ZeroDivisionError as e:
            return "{:.2f}".format(0.0)
    
    @property
    def incorrect(self):
        return self.total - self.correct