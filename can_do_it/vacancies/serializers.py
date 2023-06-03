from rest_framework import serializers
from rest_framework.relations import PrimaryKeyRelatedField

from vacancies.models import Vacancy

from users.models import User


class VacancySerializer(serializers.ModelSerializer):
    employer = serializers.SlugRelatedField(
        read_only=True,
        slug_field='email'
    )

    class Meta:
        model = Vacancy
        fields = '__all__'
