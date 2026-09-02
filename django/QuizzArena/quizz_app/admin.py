"""Admin configuration for quizz_app."""

from django.contrib import admin
from .models import Category, UserProfile, Quiz, QuizEnrollment, QuizResult
from .learning_models import (
    Skill,
    LearningPath,
    Module,
    InteractiveLab,
    RealWorldScenario,
    Question,
    UserProgress,
    UserSkillMastery,
    Achievement,
    UserAchievement,
    UserGamification,
    AdaptiveQuiz,
    LabSubmission,
    ScenarioSubmission,
)


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ["user", "role", "created_at"]
    list_filter = ["role", "created_at"]
    search_fields = ["user__username"]

    def has_change_permission(self, request, obj=None):
        return request.user.is_superuser

    def has_add_permission(self, request):
        return request.user.is_superuser

    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ["name", "teacher", "created_at"]
    search_fields = ["name", "teacher__username"]


@admin.register(Quiz)
class QuizAdmin(admin.ModelAdmin):
    list_display = [
        "title",
        "category",
        "difficulty",
        "creator",
        "access_code",
        "is_active",
        "created_at",
    ]
    list_filter = ["category", "difficulty", "is_active", "created_at"]
    search_fields = ["title", "description"]
    readonly_fields = ["access_code"]


@admin.register(QuizEnrollment)
class QuizEnrollmentAdmin(admin.ModelAdmin):
    list_display = ["student", "quiz", "completed", "enrolled_at"]
    list_filter = ["quiz", "completed", "enrolled_at"]
    search_fields = ["student__username", "quiz__title"]


@admin.register(QuizResult)
class QuizResultAdmin(admin.ModelAdmin):
    list_display = [
        "player_name",
        "quiz",
        "student",
        "score",
        "percentage",
        "time_taken",
        "created_at",
    ]
    list_filter = ["quiz", "created_at"]
    search_fields = ["player_name", "student__username"]
    readonly_fields = ["created_at", "updated_at"]


# ==================== LEARNING PLATFORM ADMIN ====================


@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ["name", "category", "difficulty", "order", "created_at"]
    list_filter = ["category", "difficulty", "created_at"]
    search_fields = ["name", "description"]
    ordering = ["category", "order"]


@admin.register(LearningPath)
class LearningPathAdmin(admin.ModelAdmin):
    list_display = [
        "title",
        "difficulty_level",
        "is_structured",
        "is_published",
        "creator",
        "created_at",
    ]
    list_filter = ["difficulty_level", "is_structured", "is_published", "created_at"]
    search_fields = ["title", "description"]
    filter_horizontal = ["skills", "prerequisites"]
    readonly_fields = ["created_at", "updated_at"]


class ModuleInline(admin.TabularInline):
    model = Module
    extra = 0
    fields = ["title", "content_type", "skill", "order", "duration_minutes"]


@admin.register(Module)
class ModuleAdmin(admin.ModelAdmin):
    list_display = [
        "title",
        "learning_path",
        "content_type",
        "skill",
        "order",
        "duration_minutes",
    ]
    list_filter = ["learning_path", "content_type", "created_at"]
    search_fields = ["title", "content"]
    ordering = ["learning_path", "order"]


@admin.register(InteractiveLab)
class InteractiveLabAdmin(admin.ModelAdmin):
    list_display = [
        "title",
        "difficulty",
        "max_points",
        "time_limit_minutes",
        "created_at",
    ]
    list_filter = ["difficulty", "created_at"]
    search_fields = ["title", "description"]
    readonly_fields = ["created_at", "updated_at"]


@admin.register(RealWorldScenario)
class RealWorldScenarioAdmin(admin.ModelAdmin):
    list_display = [
        "title",
        "scenario_type",
        "difficulty",
        "points_max",
        "time_limit_minutes",
    ]
    list_filter = ["scenario_type", "difficulty", "created_at"]
    search_fields = ["title", "description", "story"]
    filter_horizontal = ["skills_covered"]
    readonly_fields = ["created_at", "updated_at"]


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = [
        "content",
        "skill",
        "question_type",
        "difficulty",
        "interleaving_group",
        "points",
    ]
    list_filter = ["skill", "question_type", "difficulty", "interleaving_group"]
    search_fields = ["content", "explanation"]
    readonly_fields = ["created_at", "updated_at"]


@admin.register(UserProgress)
class UserProgressAdmin(admin.ModelAdmin):
    list_display = [
        "user",
        "learning_path",
        "status",
        "progress_percentage",
        "started_at",
        "completed_at",
    ]
    list_filter = ["status", "learning_path", "completed_at"]
    search_fields = ["user__username", "learning_path__title"]
    readonly_fields = ["created_at", "updated_at"]


@admin.register(UserSkillMastery)
class UserSkillMasteryAdmin(admin.ModelAdmin):
    list_display = [
        "user",
        "skill",
        "mastery_level",
        "times_reviewed",
        "next_review_date",
    ]
    list_filter = ["skill", "mastery_level", "next_review_date"]
    search_fields = ["user__username", "skill__name"]
    readonly_fields = ["created_at", "updated_at"]


@admin.register(Achievement)
class AchievementAdmin(admin.ModelAdmin):
    list_display = [
        "title",
        "achievement_type",
        "points_reward",
        "rarity",
        "created_at",
    ]
    list_filter = ["achievement_type", "rarity", "created_at"]
    search_fields = ["title", "description"]
    readonly_fields = ["created_at", "updated_at"]


@admin.register(UserAchievement)
class UserAchievementAdmin(admin.ModelAdmin):
    list_display = ["user", "achievement", "unlocked_at", "progress"]
    list_filter = ["achievement", "unlocked_at"]
    search_fields = ["user__username", "achievement__title"]
    readonly_fields = ["unlocked_at"]


@admin.register(UserGamification)
class UserGamificationAdmin(admin.ModelAdmin):
    list_display = [
        "user",
        "level",
        "rank",
        "total_points",
        "current_streak_days",
        "total_achievements",
    ]
    list_filter = ["rank", "level"]
    search_fields = ["user__username"]
    readonly_fields = ["created_at", "updated_at"]


@admin.register(AdaptiveQuiz)
class AdaptiveQuizAdmin(admin.ModelAdmin):
    list_display = [
        "user",
        "learning_path",
        "current_difficulty",
        "status",
        "questions_asked",
        "correct_answers",
    ]
    list_filter = ["status", "current_difficulty", "started_at"]
    search_fields = ["user__username", "learning_path__title"]
    readonly_fields = ["started_at", "created_at", "updated_at"]


@admin.register(LabSubmission)
class LabSubmissionAdmin(admin.ModelAdmin):
    list_display = [
        "user",
        "lab",
        "status",
        "score",
        "hints_used",
        "time_taken_minutes",
        "submitted_at",
    ]
    list_filter = ["status", "lab", "submitted_at"]
    search_fields = ["user__username", "lab__title"]
    readonly_fields = ["submitted_at", "created_at", "updated_at"]


@admin.register(ScenarioSubmission)
class ScenarioSubmissionAdmin(admin.ModelAdmin):
    list_display = [
        "user",
        "scenario",
        "status",
        "score",
        "accuracy",
        "time_taken_minutes",
        "submitted_at",
    ]
    list_filter = ["status", "scenario", "submitted_at"]
    search_fields = ["user__username", "scenario__title"]
    readonly_fields = ["submitted_at", "created_at", "updated_at"]
