# Models for Learning Platform
# Este arquivo será importado em models/__init__.py

from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
import uuid
from datetime import timedelta


class Skill(models.Model):
    """Competency/Topic model for structured learning."""

    CATEGORY_CHOICES = [
        ("PYTHON_BASICS", "Python Basics"),
        ("NETWORK_SECURITY", "Network Security"),
        ("CRYPTOGRAPHY", "Cryptography"),
        ("LOG_ANALYSIS", "Log Analysis"),
        ("INCIDENT_RESPONSE", "Incident Response"),
        ("WEB_SECURITY", "Web Security"),
        ("MALWARE_ANALYSIS", "Malware Analysis"),
        ("THREAT_INTEL", "Threat Intelligence"),
        ("SECURE_CODING", "Secure Coding"),
        ("API_SECURITY", "API Security"),
    ]

    DIFFICULTY_CHOICES = [
        ("beginner", "Beginner"),
        ("intermediate", "Intermediate"),
        ("advanced", "Advanced"),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=200)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    description = models.TextField()
    difficulty = models.CharField(
        max_length=20, choices=DIFFICULTY_CHOICES, default="beginner"
    )
    parent_skill = models.ForeignKey(
        "self",
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name="child_skills",
    )
    order = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["category", "order"]
        verbose_name_plural = "Skills"
        indexes = [
            models.Index(fields=["category", "difficulty"]),
            models.Index(fields=["created_at"]),
        ]

    def __str__(self):
        return f"{self.name} ({self.get_category_display()})"


class LearningPath(models.Model):
    """Structured learning path with prerequisites."""

    LEVEL_CHOICES = [
        ("beginner", "Beginner"),
        ("intermediate", "Intermediate"),
        ("advanced", "Advanced"),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=300)
    description = models.TextField()
    difficulty_level = models.CharField(
        max_length=20, choices=LEVEL_CHOICES, default="beginner"
    )
    skills = models.ManyToManyField(Skill, related_name="learning_paths")
    prerequisites = models.ManyToManyField(
        "self", symmetrical=False, blank=True, related_name="required_for"
    )
    order = models.IntegerField(default=0)
    is_structured = models.BooleanField(
        default=True, help_text="True=obrigatório, False=trilha"
    )
    duration_minutes = models.IntegerField(default=120)
    learning_objectives = models.JSONField(default=list)
    creator = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="created_learning_paths",
    )
    is_published = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["difficulty_level", "order"]
        indexes = [
            models.Index(fields=["is_published", "difficulty_level"]),
        ]

    def __str__(self):
        return f"{self.title} ({self.get_difficulty_level_display()})"


class Module(models.Model):
    """Content module within a learning path."""

    CONTENT_TYPE_CHOICES = [
        ("LECTURE", "Lecture"),
        ("INTERACTIVE", "Interactive"),
        ("LAB", "Hands-on Lab"),
        ("SCENARIO", "Real-world Scenario"),
        ("ASSESSMENT", "Assessment/Quiz"),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    learning_path = models.ForeignKey(
        LearningPath, on_delete=models.CASCADE, related_name="modules"
    )
    skill = models.ForeignKey(
        Skill, on_delete=models.SET_NULL, null=True, related_name="modules"
    )
    title = models.CharField(max_length=300)
    content_type = models.CharField(max_length=50, choices=CONTENT_TYPE_CHOICES)
    order = models.IntegerField(default=0)
    duration_minutes = models.IntegerField(default=30)
    content = models.TextField()
    resources = models.JSONField(default=dict)  # {links, pdfs, videos}
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["learning_path", "order"]
        indexes = [
            models.Index(fields=["learning_path", "order"]),
        ]

    def __str__(self):
        return f"{self.title} ({self.get_content_type_display()})"


class InteractiveLab(models.Model):
    """Practical lab with code execution."""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    module = models.OneToOneField(
        Module,
        on_delete=models.CASCADE,
        related_name="interactive_lab",
        null=True,
        blank=True,
    )
    title = models.CharField(max_length=300)
    description = models.TextField()
    difficulty = models.CharField(
        max_length=20,
        choices=[
            ("beginner", "Beginner"),
            ("intermediate", "Intermediate"),
            ("advanced", "Advanced"),
        ],
        default="beginner",
    )
    setup_code = models.TextField(help_text="Código de setup do ambiente")
    solution_code = models.TextField(help_text="Solução esperada")
    test_cases = models.JSONField(
        default=list
    )  # [{name, input, expected_output, points}]
    hints = models.JSONField(default=list)  # [hint1, hint2, hint3]
    time_limit_minutes = models.IntegerField(default=30)
    max_points = models.IntegerField(default=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Interactive Labs"
        indexes = [
            models.Index(fields=["difficulty", "created_at"]),
        ]

    def __str__(self):
        return f"Lab: {self.title}"


class RealWorldScenario(models.Model):
    """CTF-style challenges for practical learning."""

    SCENARIO_TYPE_CHOICES = [
        ("INCIDENT_RESPONSE", "Incident Response"),
        ("MALWARE_ANALYSIS", "Malware Analysis"),
        ("LOG_FORENSICS", "Log Forensics"),
        ("PENETRATION_TEST_DEFENSE", "Penetration Test Defense"),
        ("THREAT_DETECTION", "Threat Detection"),
        ("SECURE_CODE_REVIEW", "Secure Code Review"),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=300)
    description = models.TextField()
    difficulty = models.CharField(
        max_length=20,
        choices=[
            ("beginner", "Beginner"),
            ("intermediate", "Intermediate"),
            ("advanced", "Advanced"),
        ],
        default="beginner",
    )
    scenario_type = models.CharField(max_length=50, choices=SCENARIO_TYPE_CHOICES)
    story = models.TextField(help_text="Contexto narrativo do desafio")
    sample_data = models.JSONField(default=dict)  # logs, arquivos, dados
    expected_findings = models.JSONField(default=list)  # [finding1, finding2, ...]
    points_max = models.IntegerField(default=200)
    time_limit_minutes = models.IntegerField(default=60)
    skills_covered = models.ManyToManyField(Skill, related_name="scenarios")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Real World Scenarios"
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["scenario_type", "difficulty"]),
        ]

    def __str__(self):
        return f"{self.title} ({self.get_scenario_type_display()})"


class Question(models.Model):
    """Questions with interleaving support."""

    QUESTION_TYPE_CHOICES = [
        ("MULTIPLE_CHOICE", "Multiple Choice"),
        ("CODE_SNIPPET", "Code Snippet"),
        ("COMMAND_LINE", "Command Line"),
        ("LOG_ANALYSIS", "Log Analysis"),
        ("FILL_IN_BLANK", "Fill in the Blank"),
        ("TRUE_FALSE", "True/False"),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    skill = models.ForeignKey(Skill, on_delete=models.CASCADE, related_name="questions")
    content = models.TextField()
    question_type = models.CharField(max_length=50, choices=QUESTION_TYPE_CHOICES)
    difficulty = models.CharField(
        max_length=20,
        choices=[
            ("beginner", "Beginner"),
            ("intermediate", "Intermediate"),
            ("advanced", "Advanced"),
        ],
        default="beginner",
    )
    options = models.JSONField(default=list)  # Para múltipla escolha
    correct_answer = models.TextField()
    explanation = models.TextField(help_text="Feedback detalhado")
    code_context = models.TextField(blank=True, help_text="Para code snippets")
    points = models.IntegerField(default=10)
    interleaving_group = models.IntegerField(
        default=0, help_text="Para misturar tópicos"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Questions"
        ordering = ["interleaving_group", "difficulty"]
        indexes = [
            models.Index(fields=["skill", "difficulty"]),
            models.Index(fields=["interleaving_group"]),
        ]

    def __str__(self):
        return f"Q: {self.content[:50]}..."


class UserProgress(models.Model):
    """Track user progress in learning paths."""

    STATUS_CHOICES = [
        ("NOT_STARTED", "Not Started"),
        ("IN_PROGRESS", "In Progress"),
        ("COMPLETED", "Completed"),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="learning_progress"
    )
    learning_path = models.ForeignKey(
        LearningPath, on_delete=models.CASCADE, related_name="user_progress"
    )
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default="NOT_STARTED"
    )
    progress_percentage = models.FloatField(default=0)
    modules_completed = models.IntegerField(default=0)
    started_at = models.DateTimeField(null=True, blank=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ("user", "learning_path")
        indexes = [
            models.Index(fields=["user", "status"]),
            models.Index(fields=["completed_at"]),
        ]

    def __str__(self):
        return f"{self.user.username} - {self.learning_path.title}"

    @property
    def total_modules(self):
        return self.learning_path.modules.count()

    def update_progress(self):
        """Atualizar percentual de progresso."""
        total = self.total_modules
        if total == 0:
            self.progress_percentage = 0
        else:
            self.progress_percentage = (self.modules_completed / total) * 100
        self.save()


class UserSkillMastery(models.Model):
    """Track mastery level of each skill with spaced repetition."""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="skill_mastery"
    )
    skill = models.ForeignKey(
        Skill, on_delete=models.CASCADE, related_name="user_mastery"
    )
    mastery_level = models.FloatField(default=0)  # 0-100
    times_reviewed = models.IntegerField(default=0)
    last_reviewed_at = models.DateTimeField(null=True, blank=True)
    next_review_date = models.DateTimeField(default=timezone.now)
    strength = models.FloatField(default=0)  # Baseado em acertos
    weakness = models.FloatField(default=0)  # Baseado em erros
    review_interval = models.IntegerField(default=1)  # Dias até próxima revisão
    ease_factor = models.FloatField(default=2.5)  # SM-2 algoritmo
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ("user", "skill")
        indexes = [
            models.Index(fields=["user", "next_review_date"]),
            models.Index(fields=["mastery_level"]),
        ]

    def __str__(self):
        return f"{self.user.username} - {self.skill.name}: {self.mastery_level}%"

    def update_spaced_repetition(self, performance_score):
        """
        Atualizar intervalo de repetição baseado em performance (SM-2).
        performance_score: 0-5 (0=falhou, 5=perfeito)
        """
        self.times_reviewed += 1
        self.last_reviewed_at = timezone.now()

        if performance_score >= 4:  # Bom desempenho
            self.review_interval = max(1, int(self.review_interval * self.ease_factor))
            self.mastery_level = min(100, self.mastery_level + 5)
        elif performance_score >= 3:  # Desempenho médio
            self.review_interval = max(1, int(self.review_interval * 1.5))
            self.mastery_level = max(0, self.mastery_level - 2)
        else:  # Desempenho ruim
            self.review_interval = 1
            self.mastery_level = max(0, self.mastery_level - 10)

        # Atualizar próxima data de revisão
        self.next_review_date = timezone.now() + timedelta(days=self.review_interval)
        self.save()


class Achievement(models.Model):
    """Achievement/Badge system."""

    ACHIEVEMENT_TYPE_CHOICES = [
        ("SKILL_MASTERY", "Skill Mastery"),
        ("STREAK", "Learning Streak"),
        ("SPEED_RUN", "Speed Run"),
        ("PERFECT_SCORE", "Perfect Score"),
        ("HELPING_OTHERS", "Helping Others"),
        ("DISCOVERY", "Discovery"),
        ("COMPLETION", "Path Completion"),
    ]

    RARITY_CHOICES = [
        ("COMMON", "Common"),
        ("RARE", "Rare"),
        ("EPIC", "Epic"),
        ("LEGENDARY", "Legendary"),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=200)
    description = models.TextField()
    badge_icon = models.ImageField(upload_to="badges/", null=True, blank=True)
    achievement_type = models.CharField(max_length=50, choices=ACHIEVEMENT_TYPE_CHOICES)
    points_reward = models.IntegerField(default=50)
    criteria = models.JSONField(default=dict)  # Como conquistar
    rarity = models.CharField(max_length=20, choices=RARITY_CHOICES, default="COMMON")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Achievements"
        ordering = ["rarity", "title"]

    def __str__(self):
        return f"🏆 {self.title}"


class UserAchievement(models.Model):
    """Track unlocked achievements per user."""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="achievements"
    )
    achievement = models.ForeignKey(Achievement, on_delete=models.CASCADE)
    unlocked_at = models.DateTimeField(auto_now_add=True)
    progress = models.FloatField(default=100)  # Para badges progressivos

    class Meta:
        unique_together = ("user", "achievement")
        ordering = ["-unlocked_at"]
        indexes = [
            models.Index(fields=["user", "unlocked_at"]),
        ]

    def __str__(self):
        return f"{self.user.username} - {self.achievement.title}"


class UserGamification(models.Model):
    """Gamification profile for each user."""

    RANK_CHOICES = [
        ("NOVICE", "Novice"),
        ("LEARNER", "Learner"),
        ("PRACTITIONER", "Practitioner"),
        ("EXPERT", "Expert"),
        ("MASTER", "Master"),
    ]

    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="gamification"
    )
    level = models.IntegerField(default=1)  # 1-100
    total_points = models.IntegerField(default=0)
    points_next_level = models.IntegerField(default=1000)
    current_streak_days = models.IntegerField(default=0)
    max_streak_days = models.IntegerField(default=0)
    total_achievements = models.IntegerField(default=0)
    total_labs_completed = models.IntegerField(default=0)
    total_scenarios_completed = models.IntegerField(default=0)
    total_skills_mastered = models.IntegerField(default=0)
    rank = models.CharField(max_length=20, choices=RANK_CHOICES, default="NOVICE")
    last_activity_date = models.DateField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "User Gamification"
        indexes = [
            models.Index(fields=["level", "-total_points"]),
            models.Index(fields=["rank"]),
        ]

    def __str__(self):
        return f"{self.user.username} - Level {self.level} ({self.rank})"

    def add_points(self, points):
        """Add points and check for level up."""
        self.total_points += points
        while self.total_points >= self.points_next_level:
            self.level_up()

    def level_up(self):
        """Level up user."""
        self.level += 1
        self.total_points -= self.points_next_level
        self.points_next_level = int(
            self.points_next_level * 1.1
        )  # 10% mais pontos por nível
        self.update_rank()

    def update_rank(self):
        """Update rank based on level."""
        if self.level < 10:
            self.rank = "NOVICE"
        elif self.level < 25:
            self.rank = "LEARNER"
        elif self.level < 50:
            self.rank = "PRACTITIONER"
        elif self.level < 75:
            self.rank = "EXPERT"
        else:
            self.rank = "MASTER"


class AdaptiveQuiz(models.Model):
    """Adaptive quiz that adjusts difficulty based on performance."""

    STATUS_CHOICES = [
        ("NOT_STARTED", "Not Started"),
        ("IN_PROGRESS", "In Progress"),
        ("COMPLETED", "Completed"),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="adaptive_quizzes"
    )
    learning_path = models.ForeignKey(
        LearningPath,
        on_delete=models.CASCADE,
        related_name="adaptive_quizzes",
        null=True,
        blank=True,
    )
    skill = models.ForeignKey(Skill, on_delete=models.CASCADE, null=True, blank=True)
    current_difficulty = models.CharField(
        max_length=20,
        choices=[
            ("beginner", "Beginner"),
            ("intermediate", "Intermediate"),
            ("advanced", "Advanced"),
        ],
        default="beginner",
    )
    questions_asked = models.IntegerField(default=0)
    correct_answers = models.IntegerField(default=0)
    last_performance = models.FloatField(default=0)  # Percentual %
    should_increase_difficulty = models.BooleanField(default=False)
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default="NOT_STARTED"
    )
    state = models.JSONField(default=dict)  # Histórico de respostas
    started_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-started_at"]
        indexes = [
            models.Index(fields=["user", "status"]),
        ]

    def __str__(self):
        return f"Adaptive Quiz - {self.user.username} ({self.current_difficulty})"

    def calculate_performance(self):
        """Calculate current performance percentage."""
        if self.questions_asked == 0:
            return 0
        return (self.correct_answers / self.questions_asked) * 100

    def should_adjust_difficulty(self):
        """
        Determine if difficulty should be adjusted.
        Algorithm: usar last 5 questions
        """
        self.last_performance = self.calculate_performance()

        if self.last_performance >= 80:
            self.should_increase_difficulty = True
        elif self.last_performance < 50:
            self.should_increase_difficulty = False

        return self.should_increase_difficulty


class LabSubmission(models.Model):
    """Track submissions for interactive labs."""

    STATUS_CHOICES = [
        ("PENDING", "Pending Review"),
        ("PASSED", "Passed"),
        ("FAILED", "Failed"),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="lab_submissions"
    )
    lab = models.ForeignKey(
        InteractiveLab, on_delete=models.CASCADE, related_name="submissions"
    )
    submitted_code = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="PENDING")
    score = models.IntegerField(default=0)
    test_results = models.JSONField(default=list)  # [{test_name, passed, error}]
    hints_used = models.IntegerField(default=0)
    time_taken_minutes = models.IntegerField(default=0)
    submitted_at = models.DateTimeField(auto_now_add=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-submitted_at"]
        indexes = [
            models.Index(fields=["user", "lab", "-submitted_at"]),
        ]

    def __str__(self):
        return f"{self.user.username} - {self.lab.title}: {self.status}"


class ScenarioSubmission(models.Model):
    """Track submissions for real-world scenarios."""

    STATUS_CHOICES = [
        ("PENDING", "Pending Review"),
        ("PARTIAL", "Partially Correct"),
        ("COMPLETE", "Complete"),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="scenario_submissions"
    )
    scenario = models.ForeignKey(
        RealWorldScenario, on_delete=models.CASCADE, related_name="submissions"
    )
    findings = models.JSONField(default=list)  # Lista de achados identificados
    analysis = models.TextField(help_text="Análise detalhada")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="PENDING")
    score = models.IntegerField(default=0)
    accuracy = models.FloatField(default=0)  # % de acertos
    time_taken_minutes = models.IntegerField(default=0)
    submitted_at = models.DateTimeField(auto_now_add=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-submitted_at"]
        indexes = [
            models.Index(fields=["user", "scenario", "-submitted_at"]),
        ]

    def __str__(self):
        return f"{self.user.username} - {self.scenario.title}"
