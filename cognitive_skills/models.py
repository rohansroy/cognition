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

class Result(models.Model):
    worker_id = models.CharField(max_length=255)
    test = models.ForeignKey(Test, on_delete=models.CASCADE, related_name='results')
    correct = models.PositiveIntegerField()
    total = models.PositiveIntegerField()
    raw = models.JSONField(blank=True, null=True)
    average_response_time = models.PositiveIntegerField(blank=True, null=True)
    fastest_response_time = models.PositiveIntegerField(blank=True, null=True)
    slowest_response_time = models.PositiveIntegerField(blank=True, null=True)
    median_response_time = models.PositiveIntegerField(blank=True, null=True)

    def __str__(self):
        return f"Worker: {self.worker_id} {self.test.name} {self.correct}/{self.total}"

    def pctCorrect(self):
        try:
            return "{:.2f}".format(self.correct / self.total)
        except ZeroDivisionError as e:
            return "{:.2f}".format(0.0)