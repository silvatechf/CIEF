# 🔐 CyberSecLearn Platform - Guia Completo de Desenvolvimento

## 📋 Implementação Realizada (Fase 1)

### ✅ Modelos de Dados (13 Novos Modelos)

```
✓ Skill - Competências de segurança/python
✓ LearningPath - Caminhos estruturados de aprendizado
✓ Module - Módulos de conteúdo (LECTURE, LAB, SCENARIO, etc)
✓ InteractiveLab - Labs práticos com execução de código
✓ RealWorldScenario - Desafios CTF-style
✓ Question - Questões com suporte a Interleaving
✓ UserProgress - Rastreamento de progresso
✓ UserSkillMastery - Domínio de skills com Spaced Repetition
✓ Achievement - Sistema de badges/achievements
✓ UserAchievement - Achievements desbloqueados por usuário
✓ UserGamification - Stats de gamificação (level, points, streaks)
✓ AdaptiveQuiz - Quizzes adaptativos com ajuste de dificuldade
✓ LabSubmission - Submissões de labs (com pontuação automática)
✓ ScenarioSubmission - Submissões de cenários
```

### ✅ Algoritmos de Aprendizado Implementados

```
✓ Interleaving Algorithm
  - Mistura tópicos relacionados para melhor retenção (+43%)
  - Evita blocos sequenciais que criam retenção falsa

✓ Spaced Repetition (SM-2)
  - Revisão em intervalos ótimos
  - Algoritmo científico com ease_factor adaptativo
  - Schedule automático de próxima revisão

✓ Adaptive Difficulty
  - Ajusta dificuldade baseado em últimas 5 respostas
  - Mantém usuário na "zona ótima de aprendizado"
  - Bônus/malus de pontos pela dificuldade

✓ Retrieval Practice
  - Mini-quizzes após completar módulos
  - Fortalecem memória de longo prazo

✓ Learning Path Recommendation
  - Sugere próximo caminho baseado em pré-requisitos
  - Respeita progresso e performance

✓ Streak Management
  - Gamificação com sequências de dias consecutivos
  - Recompensas por manter streak
```

### ✅ Lab Executor (Sandbox Python Seguro)

```
✓ Execução segura de código com:
  - Timeout de 5 segundos
  - Whitelist de módulos permitidos
  - Blacklist de operações perigosas

✓ Validação de código:
  - Detecta imports proibidos (os, sys, subprocess)
  - Detecta funções perigosas (eval, exec)
  - Validação de sintaxe

✓ Execução de testes:
  - Múltiplos test cases
  - Captura de output/erro
  - Validação automática

✓ Análise de estilo:
  - Detecta linhas longas
  - Verifica comentários
  - Sugere melhorias

✓ Pontuação:
  - Score baseado em testes (80%) + estilo (20%)
  - Feedback detalhado
```

### ✅ Integração Django Admin

```
✓ Admin para todos os 13 novos modelos
✓ Customizações avançadas:
  - Filter horizontals para M2M
  - Inlines para relacionamentos
  - Read-only fields para auditoria
```

### ✅ Conteúdo Inicial Carregado

```
✓ 10 Skills:
  - 3 de Python Basics
  - 3 de Web Security
  - 2 de Cryptography
  - 1 de Log Analysis
  - 1 de Incident Response

✓ 3 Learning Paths:
  - Python Foundations for Security (beginner)
  - Web Security & Secure Coding (intermediate)
  - Advanced Defense & Incident Response (advanced)

✓ 1 Lab Prático:
  - Calcular Hash MD5 com testes automáticos

✓ 1 Cenário Real:
  - SQL Injection Detection em logs

✓ 3 Achievements:
  - First Steps
  - Lab Master
  - 7-Day Warrior
```

---

## 🚀 Próximos Passos (Fase 2)

### 1. **REST API Endpoints**

Criar endpoints para consumir a plataforma:

```python
# quizz_app/api/views.py

# Learning Paths
GET /api/learning-paths/                 # Listar caminhos
POST /api/learning-paths/<id>/start/     # Iniciar trilha
GET /api/learning-paths/<id>/progress/   # Progresso

# Modules & Content
GET /api/modules/<id>/                   # Conteúdo do módulo
POST /api/modules/<id>/complete/         # Marcar completo

# Adaptive Quiz
GET /api/quiz/next/                      # Próxima questão adaptativa
POST /api/quiz/answer/                   # Responder (atualiza dificuldade)
GET /api/quiz/stats/                     # Stats do quiz

# Labs
POST /api/labs/<id>/submit/              # Submeter código
GET /api/labs/<id>/results/              # Resultados

# Scenarios
POST /api/scenarios/<id>/submit/         # Submeter análise
GET /api/scenarios/<id>/feedback/        # Feedback

# User Progress
GET /api/user/progress/                  # Progresso geral
GET /api/user/skills/                    # Mastery de skills
GET /api/user/achievements/              # Badges
GET /api/user/stats/                     # Stats detalhadas

# Leaderboard
GET /api/leaderboard/                    # Top players
GET /api/leaderboard/friends/            # Entre amigos
```

### 2. **Frontend - Dashboard do Usuário**

```html
<!-- templates/learning/dashboard.html -->

Componentes: - 📊 Progress Overview (caminho atual) - 🎯 Skills Radar
(visualização de competências) - 📅 Spaced Repetition Queue (próximas a revisar)
- 🏆 Achievement Showcase (badges desbloqueados) - 📈 Learning Analytics
(gráficos de progresso) - 🔥 Streak Counter (dias consecutivos) - 👥 Mini
Leaderboard (top 5 amigos)
```

### 3. **Frontend - Learning Path Player**

```html
<!-- templates/learning/path-player.html -->

Componentes: - 📚 Sidebar com módulos (checklist de progresso) - 🎬 Content
Player (vídeos, texto, código) - 💻 Lab Editor (Monaco editor + sandbox) - 📋
Scenario Viewer (dados, logs, análise) - ✅ Quiz Interativo (com Interleaving) -
📝 Feedback & Hints (progressivo)
```

### 4. **Celery Tasks - Background Processing**

```python
# quizz_app/tasks.py

@periodic_task(run_every=crontab(hour=20))  # Diário às 20h
def notify_due_for_review():
    """Notificar usuários sobre skills vencidas para revisão."""
    pass

@task
def check_streaks():
    """Verificar e atualizar streaks dos usuários."""
    pass

@task
def award_achievements():
    """Verificar e conceder achievements."""
    pass

@task
def generate_recommendation():
    """Gerar recomendações de próximo caminho."""
    pass
```

### 5. **WebSocket para Labs Interativos**

```python
# quizz_app/consumers.py

class LabExecutor(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()

    async def execute_code(self, event):
        # Executar código em real-time
        # Enviar output para frontend
        pass
```

### 6. **Analytics & Reporting**

```python
# quizz_app/analytics.py

class LearningAnalytics:
    @staticmethod
    def get_user_insights(user):
        """Gerar insights sobre aprendizado do usuário."""
        return {
            'learning_velocity': '...',
            'weakness_areas': '...',
            'recommended_focus': '...',
            'estimated_mastery': '...',
        }

    @staticmethod
    def predict_mastery_date(user_skill_mastery):
        """Prever quando usuário dominará skill."""
        pass
```

### 7. **Conteúdo Expandido**

Expandir para 50+ skills:

- Python avançado (decorators, async, etc)
- Segurança de Network (nmap, wireshark)
- Malware Analysis
- Threat Intelligence
- Cloud Security
- Container Security
- Blockchain Security

### 8. **Integração com Ferramentas Reais**

```python
# quizz_app/tool_integrations.py

# Simular ferramentas reais:
class NmapSimulator:
    @staticmethod
    def scan(target, options):
        """Simular scan nmap educacional."""
        pass

class WiresharkSimulator:
    @staticmethod
    def parse_pcap(pcap_data):
        """Análise de pacotes educacional."""
        pass

class OpenSSLSimulator:
    @staticmethod
    def generate_cert():
        """Gerar certificados."""
        pass
```

### 9. **Social Features**

```python
# Gamificação social:
- Amigos (follow/unfollow)
- Mensagens privadas
- Discussões por skill/path
- Forum de problemas
- Mentorship (mais experiente ajuda iniciante)
```

### 10. **Mobile App (React Native)**

```javascript
// Versão mobile com:
- Offline mode
- Push notifications
- Streaks reminder
- Quick quizzes
```

---

## 📊 Estrutura de Pontuação

### Points por Atividade

```
Lab completado: 50 pontos
- Bônus se perfeito: +20
- Bônus se rápido (<10min): +10

Cenário completado: 100-200 pontos (baseado em dificuldade)

Quiz adaptativo: 10-50 pontos por questão
- Baseado em dificuldade atual
- Bônus se acertou difícil: +5

Skill dominada (100%): 200 pontos

Achievement desbloqueado: 50-500 pontos (por rarity)
```

### Level Progression

```
Level 1: 0 pontos
Level 2: 1,000 pontos
Level 3: 1,100 pontos (cada nível requer 10% mais)
...
Level 100: ~15 milhões de pontos
```

### Ranks

```
NOVICE:      Level 1-9
LEARNER:     Level 10-24
PRACTITIONER: Level 25-49
EXPERT:      Level 50-74
MASTER:      Level 75+
```

---

## 🔐 Segurança

### SQL Injection Prevention

```python
# Usar Django ORM (proteção automática)
questions = Question.objects.filter(
    skill=skill,
    difficulty=user_difficulty
)
```

### Code Execution Safety

```python
# Whitelist approach
ALLOWED_IMPORTS = {'hashlib', 'json', 're', 'math', ...}
FORBIDDEN_IMPORTS = {'os', 'subprocess', 'socket', ...}

# Validação antes de executar
LabExecutor.validate_code(user_code)
```

### Authentication

```python
# Django permission system
@login_required
@permission_required('quizz_app.view_lab')
def view_lab(request, lab_id):
    pass
```

---

## 🧪 Testing

### Unit Tests

```python
# tests/test_algorithms.py
def test_interleaving():
    """Testar algoritmo de interleaving."""
    pass

def test_spaced_repetition():
    """Testar SM-2 algoritmo."""
    pass

def test_lab_executor():
    """Testar execução segura de código."""
    pass
```

### Integration Tests

```python
# tests/test_api.py
def test_adaptive_quiz_flow():
    """Testar fluxo completo de quiz adaptativo."""
    pass
```

---

## 📦 Dependências Adicionais

```
djangorestframework==3.14.0      # REST API
django-cors-headers==4.3.1       # CORS
celery==5.4.0                    # Async tasks
redis==5.0.0                     # Cache/Broker
psutil==5.9.0                    # System monitoring
websockets==12.0                 # Real-time
pyyaml==6.0                      # Config
```

---

## 🎓 Exemplo de Fluxo de Usuário

```
1. Usuário inicia "Python Foundations for Security"
   ↓
2. Vê progresso: 0% (0/5 módulos)
   ↓
3. Inicia módulo 1: "Python Basics & Setup"
   ↓
4. Completa leitura (LECTURE)
   ↓
5. Faz mini-quiz (Retrieval Practice)
   - Performance: 80% → Skills mastery +2
   ↓
6. Faz Lab: "Calcular Hash MD5"
   - Submete código
   - Testes passam 100%
   - Score: 100 pontos
   - Bônus: +10 (perfeito) +5 (rápido)
   → Ganha achievement "First Steps"
   ↓
7. Dashboard atualiza:
   - Level: 1 → 2
   - Points: 115/1000 para próximo nível
   - Streak: 1 dia 🔥
   - Skills: Variables & Data Types 50/100
   ↓
8. Sistema agenda próxima revisão:
   - "Variables & Data Types" revisado em 1 dia
   - Notificação agendada
   ↓
9. Continue para próximo módulo...
```

---

## 📚 Documentação para Criar Conteúdo

### Para Professores Criarem Novo Caminho

1. Ir para `/admin/quizz_app/learningpath/`
2. Criar Learning Path
3. Adicionar skills pré-existentes ou criar novas
4. Criar módulos ligados ao path
5. Para cada módulo, criar:
   - Conteúdo (texto/markdown)
   - Lab (se prático)
   - Questões interleaved
6. Publicar quando pronto

### Para Criar Labs

1. Ir para `/admin/quizz_app/interactivelab/`
2. Definir:
   - Setup code (imports, fixtures)
   - Solution code (código esperado)
   - Test cases (validação)
   - Hints (progressivos)
3. Testar com `LabExecutor.execute_code()`

### Para Criar Cenários

1. Ir para `/admin/quizz_app/realworldscenario/`
2. Definir:
   - Story (narrativa do desafio)
   - Sample data (logs, arquivos, dados)
   - Expected findings (o que descobrir)
   - Skills covered (quais skills são testadas)

---

## 🔗 URLs Principais

```
/admin/                              # Django Admin
/api/learning-paths/                 # API
/dashboard/                          # Dashboard do usuário
/path/<id>/play/                     # Player do caminho
/lab/<id>/                           # Lab interativo
/scenario/<id>/                      # Cenário do mundo real
/leaderboard/                        # Ranking global
/profile/                            # Perfil do usuário
```

---

## 📞 Suporte & Debugging

### Verificar dados no shell Django

```bash
python manage.py shell
>>> from quizz_app.learning_models import *
>>> skills = Skill.objects.all()
>>> paths = LearningPath.objects.all()
>>> UserProgress.objects.filter(user__username='alice')
```

### Testar Lab Executor

```bash
python manage.py shell
>>> from quizz_app.lab_executor import LabExecutor
>>> code = "print('Hello')"
>>> LabExecutor.execute_code(code)
```

### Ver logs de Spaced Repetition

```bash
python manage.py shell
>>> from quizz_app.learning_models import UserSkillMastery
>>> mastery = UserSkillMastery.objects.get(user__username='alice', skill__name='...')
>>> mastery.next_review_date
>>> mastery.times_reviewed
```

---

## ✨ Dicas de Performance

1. **Usar select_related para ForeignKeys**

   ```python
   Questions.objects.select_related('skill').all()
   ```

2. **Usar prefetch_related para ManyToMany**

   ```python
   Paths.objects.prefetch_related('skills').all()
   ```

3. **Cachear Skills em Redis**

   ```python
   from django.core.cache import cache
   skills = cache.get_or_set('all_skills', Skill.objects.all, 3600)
   ```

4. **Usar indexes** (já criados nas migrations)

---

## 🎯 Métricas de Sucesso

- [ ] 10+ usuários ativos
- [ ] Retenção de 7 dias: >60%
- [ ] Média de 3+ horas por semana por usuário
- [ ] Pelo menos 1 skill dominada por usuário (mastery ≥80%)
- [ ] Streak médio: 5+ dias
- [ ] Satisfação: >4/5 ⭐

---

**Versão**: 2.0 - Learning Platform  
**Data**: Setembro 2026  
**Status**: 🔧 Em Desenvolvimento  
**Próxima Revisão**: Fim de Outubro
