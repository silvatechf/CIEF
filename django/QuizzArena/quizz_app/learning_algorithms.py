"""
Learning Algorithms Module
Implementação de técnicas científicas de aprendizado baseadas em evidências cognitivas.

Técnicas implementadas:
1. Interleaving: Misturar tópicos relacionados
2. Spaced Repetition (SM-2): Revisão em intervalos ótimos
3. Adaptive Difficulty: Ajustar dificuldade baseado em performance
4. Retrieval Practice: Teste frequente para fortalecer memória
"""

from datetime import timedelta, datetime
from django.utils import timezone
from typing import List, Dict, Tuple
import random
import math


class InterleavingAlgorithm:
    """
    Interleaving Algorithm: Misturar tópicos relacionados

    Evidência: Estudos mostram que aprender tópicos relacionados
    em sequência misturada (não em blocos) melhora retenção em 43%.

    Exemplo:
    - Sequencial (ruim): Q1 SQL → Q2 SQL → Q3 SQL → Q4 XSS → Q5 XSS
    - Interleaving (bom): Q1 SQL → Q2 XSS → Q3 SQL → Q4 CSRF → Q5 XSS
    """

    @staticmethod
    def generate_interleaved_sequence(
        questions: List, num_questions: int = 10, difficulty: str = "mixed"
    ) -> List:
        """
        Gerar sequência interleaving de questões.

        Args:
            questions: Lista de questões com skill_id
            num_questions: Número de questões a selecionar
            difficulty: 'mixed' para misturar, ou específica

        Returns:
            Lista de questões em ordem interleading
        """
        if not questions or len(questions) == 0:
            return []

        # Agrupar questões por skill
        skills_map = {}
        for q in questions:
            skill_id = q.skill_id
            if skill_id not in skills_map:
                skills_map[skill_id] = []
            skills_map[skill_id].append(q)

        # Converter em lista de skills
        skills_list = list(skills_map.values())
        if len(skills_list) == 0:
            return questions[:num_questions]

        # Embaralhar cada grupo
        for skill_questions in skills_list:
            random.shuffle(skill_questions)

        # Gerar sequência interleading: pega uma questão de cada skill alternadamente
        interleaved = []
        skill_indices = [0] * len(skills_list)
        skill_cycle = 0

        while len(interleaved) < num_questions:
            skill_idx = skill_cycle % len(skills_list)

            if skill_indices[skill_idx] < len(skills_list[skill_idx]):
                interleaved.append(skills_list[skill_idx][skill_indices[skill_idx]])
                skill_indices[skill_idx] += 1

            skill_cycle += 1

            # Evitar loop infinito se não há questões suficientes
            if skill_cycle > num_questions * 3:
                break

        return interleaved[:num_questions]

    @staticmethod
    def calculate_interleaving_group(skill_position: int, total_skills: int) -> int:
        """
        Calcular grupo de interleaving para uma skill.
        Usado para organizar questões.
        """
        return (skill_position % max(3, total_skills // 2)) + 1


class SpacedRepetitionSM2:
    """
    SuperMemo-2 Algorithm: Spaced Repetition

    Algoritmo científico que otimiza revisão baseado em:
    - Intervalo de tempo entre revisões
    - Performance em cada revisão
    - Fatores de dificuldade

    Referência: https://www.supermemo.com/en/archives1990-2015/english/ol/2rep.htm
    """

    # Configuração do algoritmo
    INITIAL_EASE = 2.5
    MIN_INTERVAL = 1
    MAX_INTERVAL = 36500  # ~100 anos

    @staticmethod
    def calculate_next_interval(
        current_interval: int,
        ease_factor: float,
        performance_score: int,  # 0-5
        times_reviewed: int,
    ) -> Tuple[int, float]:
        """
        Calcular próximo intervalo de revisão usando SM-2.

        Args:
            current_interval: Intervalo atual em dias
            ease_factor: Fator de facilidade (padrão 2.5)
            performance_score: 0-5 (0=falhou, 3=aceitável, 5=perfeito)
            times_reviewed: Número de vezes revisado

        Returns:
            Tuple: (novo_intervalo_dias, novo_ease_factor)
        """

        # Validar performance_score
        performance_score = max(0, min(5, int(performance_score)))

        # Atualizar ease factor
        new_ease = ease_factor + (
            0.1 - (5 - performance_score) * (0.08 + (5 - performance_score) * 0.02)
        )
        new_ease = max(1.3, new_ease)  # Ease factor mínimo

        # Calcular novo intervalo baseado em performance
        if performance_score < 3:
            # Performance ruim: resetar intervalo
            new_interval = 1
        elif times_reviewed == 1:
            # Primeira revisão bem-sucedida: 1 dia
            new_interval = 1
        elif times_reviewed == 2:
            # Segunda revisão bem-sucedida: 3 dias
            new_interval = 3
        else:
            # Revisões seguintes: multiplicar por ease_factor
            new_interval = int(current_interval * new_ease)

        # Garantir limites
        new_interval = max(SpacedRepetitionSM2.MIN_INTERVAL, new_interval)
        new_interval = min(SpacedRepetitionSM2.MAX_INTERVAL, new_interval)

        return new_interval, new_ease

    @staticmethod
    def get_due_for_review(user_skill_mastery_qs) -> List:
        """
        Obter skills que estão vencidas para revisão.

        Args:
            user_skill_mastery_qs: QuerySet de UserSkillMastery

        Returns:
            List de skills vencidas para revisão
        """
        now = timezone.now()
        return list(
            user_skill_mastery_qs.filter(next_review_date__lte=now).order_by(
                "next_review_date"
            )[:10]
        )

    @staticmethod
    def schedule_next_review(user_skill_mastery, performance_score: int):
        """
        Agendar próxima revisão para uma skill.

        Args:
            user_skill_mastery: Instância de UserSkillMastery
            performance_score: 0-5
        """
        new_interval, new_ease = SpacedRepetitionSM2.calculate_next_interval(
            current_interval=user_skill_mastery.review_interval,
            ease_factor=user_skill_mastery.ease_factor,
            performance_score=performance_score,
            times_reviewed=user_skill_mastery.times_reviewed,
        )

        user_skill_mastery.review_interval = new_interval
        user_skill_mastery.ease_factor = new_ease
        user_skill_mastery.next_review_date = timezone.now() + timedelta(
            days=new_interval
        )
        user_skill_mastery.update_spaced_repetition(performance_score)


class AdaptiveDifficultyAlgorithm:
    """
    Adaptive Difficulty: Ajustar dificuldade dinamicamente

    Baseado em:
    - Performance nas últimas questões
    - Tempo de resposta
    - Padrão de erros

    Objetivo: Manter usuário na "zona de aprendizado ótima" (nem fácil, nem impossível)
    """

    DIFFICULTY_LEVELS = ["beginner", "intermediate", "advanced"]
    PERFORMANCE_WINDOW = 5  # Usar últimas 5 questões

    @staticmethod
    def get_next_difficulty(
        adaptive_quiz, last_n_performance: List[bool]  # True = acerto, False = erro
    ) -> str:
        """
        Determinar próxima dificuldade baseada em performance.

        Args:
            adaptive_quiz: Instância de AdaptiveQuiz
            last_n_performance: Últimas N respostas (True/False)

        Returns:
            str: Nova dificuldade ('beginner', 'intermediate', 'advanced')
        """

        if not last_n_performance:
            return "beginner"

        # Calcular percentual de acertos
        accuracy = sum(last_n_performance) / len(last_n_performance)
        current_idx = AdaptiveDifficultyAlgorithm.DIFFICULTY_LEVELS.index(
            adaptive_quiz.current_difficulty
        )

        # Ajustar dificuldade
        if accuracy >= 0.80:
            # Performance excelente: aumentar dificuldade
            new_idx = min(
                current_idx + 1, len(AdaptiveDifficultyAlgorithm.DIFFICULTY_LEVELS) - 1
            )
        elif accuracy >= 0.60:
            # Performance boa: manter ou aumentar levemente
            new_idx = current_idx
        elif accuracy >= 0.40:
            # Performance intermediária: manter
            new_idx = current_idx
        else:
            # Performance ruim: diminuir dificuldade
            new_idx = max(current_idx - 1, 0)

        return AdaptiveDifficultyAlgorithm.DIFFICULTY_LEVELS[new_idx]

    @staticmethod
    def adjust_points_by_difficulty(base_points: int, difficulty: str) -> int:
        """
        Ajustar pontos baseado na dificuldade.

        Mais difícil = mais pontos
        """
        multipliers = {
            "beginner": 0.5,
            "intermediate": 1.0,
            "advanced": 2.0,
        }
        return int(base_points * multipliers.get(difficulty, 1.0))


class RetrievalPracticeAlgorithm:
    """
    Retrieval Practice: Teste frequente para fortalecer memória

    Baseado em evidências que testes frequentes:
    - Fortalecem memória de longo prazo
    - Aumentam retenção em 50%+ vs lectura passiva
    - Reduzem esquecimento (curva do esquecimento)
    """

    @staticmethod
    def should_quiz_user(user_progress) -> bool:
        """
        Determinar se usuário deveria fazer um mini-quiz.

        Regra: Após completar um módulo, fazer quiz de recuperação.
        """
        return user_progress.status == "IN_PROGRESS"

    @staticmethod
    def generate_retrieval_quiz(learning_path, num_questions: int = 5) -> List:
        """
        Gerar quiz de recuperação com questões do caminho aprendido.

        Estratégia: Misturar questões de diferentes módulos já completos.
        """
        # Obter todas as questões de skills no caminho
        skills = learning_path.skills.all()
        questions = []

        for skill in skills:
            questions.extend(list(skill.questions.all()))

        # Embaralhar e selecionar
        random.shuffle(questions)
        return questions[:num_questions]


class LearningPathRecommendation:
    """
    Recomendação de Caminhos de Aprendizado

    Baseado em:
    - Performance histórica do usuário
    - Habilidades já dominadas
    - Objetivos de aprendizado
    - Tempo disponível
    """

    @staticmethod
    def recommend_next_path(user) -> "LearningPath":
        """
        Recomendar próximo caminho de aprendizado.
        """
        from .models import LearningPath, UserProgress

        # Obter caminhos completados
        completed_paths = UserProgress.objects.filter(
            user=user, status="COMPLETED"
        ).values_list("learning_path_id", flat=True)

        # Obter caminhos em progresso
        in_progress = UserProgress.objects.filter(
            user=user, status="IN_PROGRESS"
        ).first()

        if in_progress:
            return in_progress.learning_path

        # Recomendar caminho não iniciado com pré-requisitos satisfeitos
        all_paths = (
            LearningPath.objects.filter(is_published=True)
            .exclude(id__in=completed_paths)
            .order_by("difficulty_level")
        )

        for path in all_paths:
            # Verificar pré-requisitos
            prerequisites = path.prerequisites.all()
            if all(p.id in completed_paths for p in prerequisites):
                return path

        # Se nenhum com pré-requisitos, recomendar mais fácil
        return all_paths.filter(difficulty_level="beginner").first()


class StreakManager:
    """
    Gerenciar Learning Streaks (sequência de atividades)

    Gamificação: Manter usuário engajado com sistemas de streak.
    """

    @staticmethod
    def update_streak(user_gamification) -> int:
        """
        Atualizar streak do usuário.

        Regra: atividade no mesmo dia não quebra streak,
               falta de atividade por 1 dia quebra streak.
        """
        last_activity = user_gamification.last_activity_date
        today = timezone.now().date()

        if last_activity == today:
            # Já fez atividade hoje
            return user_gamification.current_streak_days

        days_since = (today - last_activity).days

        if days_since == 1:
            # Atividade ontem: aumentar streak
            user_gamification.current_streak_days += 1
            user_gamification.max_streak_days = max(
                user_gamification.max_streak_days, user_gamification.current_streak_days
            )
        elif days_since > 1:
            # Falta de atividade: resetar streak
            user_gamification.current_streak_days = 1

        user_gamification.save()
        return user_gamification.current_streak_days
