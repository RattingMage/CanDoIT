from rest_framework import pagination, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from vacancies.models import Vacancy
from users.models import User

from vacancies.serializers import VacancySerializer


class VacancyPagination(pagination.PageNumberPagination):
    page_size = 5


class VacancyViewSet(viewsets.ModelViewSet):
    queryset = Vacancy.objects.all()
    pagination_class = VacancyPagination
    serializer_class = VacancySerializer

    def perform_create(self, serializer):
        user_pk = self.request.user.pk
        if user_pk is None:
            return Response("Unauthorized", status=401)
        serializer.save(employer=self.request.user)

    @action(detail=True, methods=["get"], permission_classes=[IsAuthenticated])
    def list_executors(self, request, pk=None):
        vacancy = Vacancy.objects.get(pk=pk)
        executors = vacancy.executors.all()
        response = []
        for executor in executors:
            skills_list = []
            for skill in executor.skills.all():
                skills_list.append(skill.name)
            response.append({
                "pk": executor.id,
                "email": executor.email,
                "first_name": executor.first_name,
                "last_name": executor.last_name,
                "experience": executor.experience,
                "skills": skills_list
            })

        return Response(response)

    @action(detail=True, methods=["post"], permission_classes=[IsAuthenticated])
    def add_executor_to_list(self, request, pk=None):
        vacancy = Vacancy.objects.get(pk=pk)
        vacancy.executors.add(self.request.user)
        executors = vacancy.executors.all()
        response = []
        for executor in executors:
            skills_list = []
            for skill in executor.skills.all():
                skills_list.append(skill.name)
            response.append({
                "pk": executor.id,
                "email": executor.email,
                "first_name": executor.first_name,
                "last_name": executor.last_name,
                "experience": executor.experience,
                "skills": skills_list
            })

        return Response(response)

    @action(detail=True, methods=["post"], permission_classes=[IsAuthenticated])
    def add_executor(self, request, pk=None):
        try:
            vacancy = Vacancy.objects.get(pk=pk)
            vacancy.executor = User.objects.get(pk=self.request.data.get("exec_pk"))
            vacancy.save()
            return Response("No content", 204)
        except:
            return Response("Error", 503)
