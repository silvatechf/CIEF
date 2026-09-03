"""Serializers for the quizz_app REST API."""
from rest_framework import serializers
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

# Tenta importar o model Question caso exista na aplicação
try:
    from quizz_app.models import Question
    class QuestionSerializer(serializers.ModelSerializer):
        class Meta:
            model = Question
            fields = '__all__'
except ImportError:
    class QuestionSerializer(serializers.Serializer):
        id = serializers.IntegerField(required=False)
        question = serializers.CharField(required=False)
        options = serializers.ListField(child=serializers.CharField(), required=False)
        correct_answer = serializers.CharField(required=False)


class SkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skill
        fields = '__all__'


class LearningPathSerializer(serializers.ModelSerializer):
    skills = SkillSerializer(many=True, read_only=True)

    class Meta:
        model = LearningPath
        fields = '__all__'


class ModuleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Module
        fields = '__all__'


class InteractiveLabSerializer(serializers.ModelSerializer):
    class Meta:
        model = InteractiveLab
        fields = '__all__'


class LabExecutionSerializer(serializers.Serializer):
    code = serializers.CharField(required=True, allow_blank=False)


class QuizSerializer(serializers.ModelSerializer):
    class Meta:
        model = Quiz
        fields = '__all__'


class QuizResultSerializer(serializers.ModelSerializer):
    student = serializers.ReadOnlyField(source='student.username')

    class Meta:
        model = QuizResult
        fields = '__all__'
        read_only_fields = ['student']


class UserProgressSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = UserProgress
        fields = '__all__'
        read_only_fields = ['user']


class UserSkillMasterySerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = UserSkillMastery
        fields = '__all__'
        read_only_fields = ['user']