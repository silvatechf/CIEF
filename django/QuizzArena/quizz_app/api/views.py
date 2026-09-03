from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly

from quizz_app.models import (
    LearningPath,
    Skill,
    Module,
    InteractiveLab,
    UserProgress,
    UserSkillMastery,
    Quiz,
    QuizResult
)

try:
    from quizz_app.models import Question
except ImportError:
    Question = None

from quizz_app.api.serializers import (
    LearningPathSerializer,
    SkillSerializer,
    ModuleSerializer,
    InteractiveLabSerializer,
    LabExecutionSerializer,
    UserProgressSerializer,
    UserSkillMasterySerializer,
    QuizSerializer,
    QuestionSerializer,
    QuizResultSerializer
)

try:
    from quizz_app.services.lab_executor import LabExecutor
except ImportError:
    from quizz_app.lab_executor import LabExecutor


class QuizViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Quiz.objects.all()
    serializer_class = QuizSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def submit_answers(self, request, pk=None):
        """Valida las respuestas enviadas en JSON: {"answers": {"0": 1}}"""
        quiz = self.get_object()
        user_answers = request.data.get('answers', {})
        questions = quiz.get_questions() if hasattr(quiz, 'get_questions') else []

        score = 0
        total = len(questions)

        for idx, q in enumerate(questions):
            user_ans = user_answers.get(str(idx))
            correct_ans = q.get('correct_answer')
            if user_ans is not None and str(user_ans).strip() == str(correct_ans).strip():
                score += 1

        percentage = (score / total * 100) if total > 0 else 0

        result = QuizResult.objects.create(
            quiz=quiz,
            quiz_name=quiz.title,
            student=request.user,
            player_name=request.user.username,
            score=score,
            total_questions=total,
            percentage=percentage,
            answers=user_answers
        )

        return Response({
            'success': True,
            'score': score,
            'total': total,
            'percentage': round(percentage, 2),
            'result_id': result.id
        }, status=status.HTTP_200_OK)


if Question:
    class QuestionViewSet(viewsets.ReadOnlyModelViewSet):
        queryset = Question.objects.all()
        serializer_class = QuestionSerializer
        permission_classes = [IsAuthenticatedOrReadOnly]


class LearningPathViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = LearningPath.objects.all()
    serializer_class = LearningPathSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class SkillViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Skill.objects.all()
    serializer_class = SkillSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class ModuleViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Module.objects.all()
    serializer_class = ModuleSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class InteractiveLabViewSet(viewsets.ModelViewSet):
    queryset = InteractiveLab.objects.all()
    serializer_class = InteractiveLabSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def run_lab(self, request, pk=None):
        lab = self.get_object()
        serializer = LabExecutionSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        user_code = serializer.validated_data['code']
        executor = LabExecutor(user_code=user_code, lab_context=lab)
        result = executor.run()

        if result.get('success'):
            UserProgress.objects.update_or_create(
                user=request.user,
                lab=lab,
                defaults={'completed': True, 'score': result.get('score', 100)}
            )

        return Response(result, status=status.HTTP_200_OK)


class UserProgressViewSet(viewsets.ModelViewSet):
    serializer_class = UserProgressSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return UserProgress.objects.filter(user=self.request.user)


class UserSkillMasteryViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = UserSkillMasterySerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return UserSkillMastery.objects.filter(user=self.request.user)