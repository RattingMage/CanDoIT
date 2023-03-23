from django.urls import path, include
from rest_framework.routers import SimpleRouter

from vacancies.views import VacancyViewSet

vacancy_router = SimpleRouter()
vacancy_router.register("vacancy", VacancyViewSet, basename="vacancy")

urlpatterns = [
    path("", include(vacancy_router.urls))
]
