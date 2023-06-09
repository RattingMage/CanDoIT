from django.db import models
from users.models import User
from users.models import Skill


class Vacancy(models.Model):
    STATUS = [("draft", "Черновик"), ("open", "Открыта"), ("closed", "Закрыта")]

    employer = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    executor = models.ManyToManyField(User, related_name="final_executor", blank=True)
    executors = models.ManyToManyField(User, related_name="list_executors", blank=True)
    name = models.CharField(max_length=50)
    text = models.CharField(max_length=1000)
    status = models.CharField(max_length=10, choices=STATUS, default="draft")
    created = models.DateField(auto_now_add=True)
    is_archived = models.BooleanField(default=False)
    skills = models.ManyToManyField(Skill, blank=True)
    min_experience = models.IntegerField(null=True, blank=True)
    price = models.PositiveBigIntegerField(default=0, null=True, blank=True)

    @property
    def username(self):
        return self.employer.company if self.employer.company else None

    class Meta:
        verbose_name = "Вакансия"
        verbose_name_plural = "Вакансии"
