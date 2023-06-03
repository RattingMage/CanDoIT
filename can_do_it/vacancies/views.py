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
        if self.request.user.pk is None:
            return Response("Unauthorized", status=401)
        serializer.save(employer_id=self.request.user.pk)

    @action(detail=True, methods=["get"])
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

    @action(detail=True, methods=["post"])
    def add_executor_to_list(self, request, pk=None):
        vacancy = Vacancy.objects.get(pk=pk)
        vacancy.executors.add(User.objects.get(pk=self.request.data["user_pk"]))
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
