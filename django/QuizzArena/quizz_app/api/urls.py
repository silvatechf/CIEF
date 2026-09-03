"""URL routing for quizz_app REST API."""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from quizz_app.api.views import (
    LearningPathViewSet,
    SkillViewSet,
    ModuleViewSet,
    InteractiveLabViewSet,
    UserProgressViewSet,
    UserSkillMasteryViewSet,
    QuizViewSet,
)

app_name = 'quizz_app_api'

router = DefaultRouter()
router.register(r'paths', LearningPathViewSet, basename='learningpath')
router.register(r'skills', SkillViewSet, basename='skill')
router.register(r'modules', ModuleViewSet, basename='module')
router.register(r'labs', InteractiveLabViewSet, basename='interactivelab')
router.register(r'progress', UserProgressViewSet, basename='userprogress')
router.register(r'mastery', UserSkillMasteryViewSet, basename='userskillmastery')
router.register(r'quizzes', QuizViewSet, basename='quiz')

urlpatterns = [
    path('', include(router.urls)),
]