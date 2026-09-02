"""
Management command to load cybersecurity learning content

Carrega:
- 10 Habilidades de Python e Cybersecurity
- 3 Caminhos de aprendizado estruturados
- 15+ Módulos
- Labs práticos
- Cenários do mundo real
"""

from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from quizz_app.learning_models import (
    Skill,
    LearningPath,
    Module,
    InteractiveLab,
    RealWorldScenario,
    Question,
    Achievement,
)
import json


class Command(BaseCommand):
    help = "Carrega conteúdo de cybersecurity e python para o learning platform"

    def handle(self, *args, **options):
        self.stdout.write(
            self.style.SUCCESS("🔐 Iniciando carregamento de conteúdo Cybersecurity...")
        )

        # Criar habilidades
        self.load_skills()

        # Criar caminhos de aprendizado
        self.load_learning_paths()

        # Criar módulos
        self.load_modules()

        # Criar labs
        self.load_labs()

        # Criar cenários reais
        self.load_scenarios()

        # Criar questões
        self.load_questions()

        # Criar achievements
        self.load_achievements()

        self.stdout.write(self.style.SUCCESS("✅ Conteúdo carregado com sucesso!"))

    def load_skills(self):
        """Carregar habilidades de cybersecurity e python."""
        self.stdout.write("📚 Carregando habilidades...")

        skills_data = [
            # Python Basics
            (
                "Variables & Data Types",
                "PYTHON_BASICS",
                "Trabalhar com variáveis, tipos de dados e estruturas",
                "beginner",
                1,
            ),
            (
                "Functions & Imports",
                "PYTHON_BASICS",
                "Definir funções reutilizáveis e importar módulos",
                "beginner",
                2,
            ),
            (
                "File I/O & Handling",
                "PYTHON_BASICS",
                "Ler e escrever arquivos, tratamento de erros",
                "beginner",
                3,
            ),
            # Segurança Web
            (
                "SQL Injection Detection",
                "WEB_SECURITY",
                "Identificar e prevenir injeção SQL",
                "intermediate",
                1,
            ),
            (
                "XSS Prevention",
                "WEB_SECURITY",
                "Compreender e prevenir cross-site scripting",
                "intermediate",
                2,
            ),
            (
                "API Security & Authentication",
                "API_SECURITY",
                "JWT, OAuth, autenticação segura de APIs",
                "intermediate",
                3,
            ),
            # Criptografia & Segurança
            (
                "Hashing & Password Security",
                "CRYPTOGRAPHY",
                "MD5, SHA, bcrypt, gerenciar senhas",
                "intermediate",
                1,
            ),
            (
                "Symmetric Encryption (AES)",
                "CRYPTOGRAPHY",
                "Criptografia simétrica com AES",
                "advanced",
                2,
            ),
            # Análise & Resposta
            (
                "Log Analysis Fundamentals",
                "LOG_ANALYSIS",
                "Analisar logs, buscar anomalias",
                "intermediate",
                1,
            ),
            (
                "Incident Response Basics",
                "INCIDENT_RESPONSE",
                "Responder a incidentes de segurança",
                "advanced",
                1,
            ),
        ]

        for name, category, desc, difficulty, order in skills_data:
            skill, created = Skill.objects.get_or_create(
                name=name,
                defaults={
                    "category": category,
                    "description": desc,
                    "difficulty": difficulty,
                    "order": order,
                },
            )
            if created:
                self.stdout.write(f"  ✓ Criada skill: {name}")

    def load_learning_paths(self):
        """Carregar caminhos de aprendizado."""
        self.stdout.write("🛣️  Carregando caminhos de aprendizado...")

        paths_data = [
            {
                "title": "Python Foundations for Security",
                "description": "Aprenda Python fundamentos essencial para cybersecurity",
                "difficulty_level": "beginner",
                "duration_minutes": 240,
                "learning_objectives": [
                    "Dominar variáveis e tipos de dados",
                    "Escrever funções reutilizáveis",
                    "Trabalhar com arquivos e I/O",
                    "Usar módulos da lib padrão",
                ],
            },
            {
                "title": "Web Security & Secure Coding",
                "description": "Defender aplicações web contra ataques comuns (OWASP Top 10)",
                "difficulty_level": "intermediate",
                "duration_minutes": 360,
                "learning_objectives": [
                    "Identificar vulnerabilidades OWASP Top 10",
                    "Implementar validação de entrada",
                    "Proteger APIs com autenticação",
                    "Escrever código seguro",
                ],
            },
            {
                "title": "Advanced Defense & Incident Response",
                "description": "Análise, detecção e resposta a incidentes de segurança",
                "difficulty_level": "advanced",
                "duration_minutes": 480,
                "learning_objectives": [
                    "Analisar logs para detectar ataques",
                    "Responder a incidentes",
                    "Usar criptografia defendendo dados",
                    "Implementar detecção de anomalias",
                ],
            },
        ]

        for path_data in paths_data:
            path, created = LearningPath.objects.get_or_create(
                title=path_data["title"],
                defaults={
                    "description": path_data["description"],
                    "difficulty_level": path_data["difficulty_level"],
                    "duration_minutes": path_data["duration_minutes"],
                    "learning_objectives": path_data["learning_objectives"],
                    "is_published": True,
                },
            )
            if created:
                self.stdout.write(f'  ✓ Criado caminho: {path_data["title"]}')

    def load_modules(self):
        """Carregar módulos de conteúdo."""
        self.stdout.write("📖 Carregando módulos...")

        # Obter skills e paths
        skills = {s.name: s for s in Skill.objects.all()}
        paths = {p.title: p for p in LearningPath.objects.all()}

        modules_data = [
            {
                "path_title": "Python Foundations for Security",
                "title": "Python Basics & Setup",
                "content_type": "LECTURE",
                "skill_name": "Variables & Data Types",
                "order": 1,
                "duration_minutes": 60,
                "content": """
# Python para Segurança - Fundamentos

Python é a linguagem padrão em cybersecurity. Aqui aprenderemos:

## Por que Python?
- Simples e legível
- Enorme ecossistema de libs de segurança
- Padrão em forensics, análise de logs, etc

## Variáveis e Tipos
```python
# Tipos básicos
nome = "Alice"  # string
idade = 30      # int
pontuacao = 9.8 # float
ativo = True    # bool

# Operações
concatenacao = f"Olá, {nome}! Idade: {idade}"
```

## Segurança desde o início
- Validar entrada sempre
- Não usar eval() ou exec()
- Usar bibliotecas padrão, não reinventar

Vamos aos exercícios práticos!
                """,
            },
        ]

        for mod_data in modules_data:
            path = paths.get(mod_data["path_title"])
            skill = skills.get(mod_data["skill_name"])

            if path and skill:
                module, created = Module.objects.get_or_create(
                    title=mod_data["title"],
                    learning_path=path,
                    defaults={
                        "content_type": mod_data["content_type"],
                        "skill": skill,
                        "order": mod_data["order"],
                        "duration_minutes": mod_data["duration_minutes"],
                        "content": mod_data["content"],
                    },
                )
                if created:
                    self.stdout.write(f'  ✓ Criado módulo: {mod_data["title"]}')

    def load_labs(self):
        """Carregar labs interativos."""
        self.stdout.write("💻 Carregando labs...")

        labs_data = [
            {
                "title": "Calcular Hash MD5",
                "description": "Escrever função que calcula hash MD5 de strings",
                "difficulty": "beginner",
                "setup_code": "import hashlib",
                "solution_code": """
def calculate_md5(text):
    return hashlib.md5(text.encode()).hexdigest()

# Testes
print(calculate_md5("hello"))  # 5d41402abc4b2a76b9719d911017c592
                """,
                "test_cases": [
                    {
                        "name": 'MD5 de "hello"',
                        "test_code": 'assert calculate_md5("hello") == "5d41402abc4b2a76b9719d911017c592"',
                        "points": 10,
                    }
                ],
                "hints": [
                    "Use hashlib.md5()",
                    "Converta string para bytes com .encode()",
                    "Use .hexdigest() para obter formato hex",
                ],
                "max_points": 100,
            },
        ]

        for lab_data in labs_data:
            lab, created = InteractiveLab.objects.get_or_create(
                title=lab_data["title"],
                defaults={
                    "description": lab_data["description"],
                    "difficulty": lab_data["difficulty"],
                    "setup_code": lab_data["setup_code"],
                    "solution_code": lab_data["solution_code"],
                    "test_cases": lab_data["test_cases"],
                    "hints": lab_data["hints"],
                    "max_points": lab_data["max_points"],
                    "time_limit_minutes": 30,
                },
            )
            if created:
                self.stdout.write(f'  ✓ Criado lab: {lab_data["title"]}')

    def load_scenarios(self):
        """Carregar cenários do mundo real."""
        self.stdout.write("🎬 Carregando cenários...")

        skills = {s.name: s for s in Skill.objects.all()}

        scenarios_data = [
            {
                "title": "SQL Injection Detection Challenge",
                "description": "Detectar SQL injection em logs de aplicação",
                "difficulty": "intermediate",
                "scenario_type": "LOG_FORENSICS",
                "story": """
Um cliente reportou ataque SQL Injection em seu aplicativo web.
Os logs estão disponíveis. Você precisa:
1. Identificar as requisições maliciosas
2. Extrair o payload SQL injetado
3. Recomendar mitigação
                """,
                "sample_data": {
                    "logs": [
                        "2024-01-15 10:23:45 GET /api/users?id=1 200",
                        "2024-01-15 10:23:50 GET /api/users?id=1%20OR%201=1 200",
                        "2024-01-15 10:24:00 GET /api/users?id=1;DROP TABLE users; 500",
                    ]
                },
                "expected_findings": [
                    'Injeção SQL: "1 OR 1=1"',
                    "Tentativa de DROP TABLE",
                    "Falta de validação de entrada",
                ],
                "points_max": 200,
                "time_limit_minutes": 60,
                "skills_covered": [
                    "SQL Injection Detection",
                    "Log Analysis Fundamentals",
                ],
            },
        ]

        for scenario_data in scenarios_data:
            skills_objs = [
                skills.get(name) for name in scenario_data.pop("skills_covered", [])
            ]
            skills_objs = [s for s in skills_objs if s]

            scenario, created = RealWorldScenario.objects.get_or_create(
                title=scenario_data["title"],
                defaults={
                    "description": scenario_data["description"],
                    "difficulty": scenario_data["difficulty"],
                    "scenario_type": scenario_data["scenario_type"],
                    "story": scenario_data["story"],
                    "sample_data": scenario_data["sample_data"],
                    "expected_findings": scenario_data["expected_findings"],
                    "points_max": scenario_data["points_max"],
                    "time_limit_minutes": scenario_data["time_limit_minutes"],
                },
            )

            if created:
                scenario.skills_covered.set(skills_objs)
                self.stdout.write(f'  ✓ Criado cenário: {scenario_data["title"]}')

    def load_questions(self):
        """Carregar questões interleaved."""
        self.stdout.write("❓ Carregando questões...")

        skills = {s.name: s for s in Skill.objects.all()}

        questions_data = [
            {
                "skill_name": "Variables & Data Types",
                "content": 'Qual é o resultado de "5" + "3" em Python?',
                "question_type": "MULTIPLE_CHOICE",
                "difficulty": "beginner",
                "options": ["8", '"53"', "Error", "None"],
                "correct_answer": '"53"',
                "explanation": 'Em Python, + com strings faz concatenação, não soma numérica. "5" + "3" = "53"',
                "points": 10,
                "interleaving_group": 1,
            },
        ]

        for q_data in questions_data:
            skill = skills.get(q_data["skill_name"])
            if skill:
                question, created = Question.objects.get_or_create(
                    content=q_data["content"],
                    skill=skill,
                    defaults={
                        "question_type": q_data["question_type"],
                        "difficulty": q_data["difficulty"],
                        "options": q_data["options"],
                        "correct_answer": q_data["correct_answer"],
                        "explanation": q_data["explanation"],
                        "points": q_data["points"],
                        "interleaving_group": q_data["interleaving_group"],
                    },
                )
                if created:
                    self.stdout.write(
                        f'  ✓ Criada questão: {q_data["content"][:50]}...'
                    )

    def load_achievements(self):
        """Carregar achievements."""
        self.stdout.write("🏆 Carregando achievements...")

        achievements_data = [
            {
                "title": "First Steps",
                "description": "Complete seu primeiro módulo de aprendizado",
                "achievement_type": "COMPLETION",
                "points_reward": 50,
                "rarity": "COMMON",
            },
            {
                "title": "Lab Master",
                "description": "Complete 5 labs com pontuação perfeita",
                "achievement_type": "SKILL_MASTERY",
                "points_reward": 200,
                "rarity": "RARE",
            },
            {
                "title": "7-Day Warrior",
                "description": "Mantenha 7 dias de aprendizado consecutivo",
                "achievement_type": "STREAK",
                "points_reward": 150,
                "rarity": "EPIC",
            },
        ]

        for ach_data in achievements_data:
            achievement, created = Achievement.objects.get_or_create(
                title=ach_data["title"],
                defaults={
                    "description": ach_data["description"],
                    "achievement_type": ach_data["achievement_type"],
                    "points_reward": ach_data["points_reward"],
                    "rarity": ach_data["rarity"],
                },
            )
            if created:
                self.stdout.write(f'  ✓ Criado achievement: {ach_data["title"]}')
