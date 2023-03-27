from django.shortcuts import render
from rest_framework import viewsets, pagination

from users.models import Skill
from users.serializers import SkillSerializer


class SkillPagination(pagination.PageNumberPagination):
    page_size = 5


class SkillViewSet(viewsets.ModelViewSet):
    queryset = Skill.objects.all()
    pagination_class = SkillPagination
    serializer_class = SkillSerializer
