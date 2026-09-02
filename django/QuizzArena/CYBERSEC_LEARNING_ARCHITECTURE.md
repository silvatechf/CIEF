# 🔐 CyberSecLearn - Arquitetura de Plataforma Educativa

## Python + Cybersecurity com Técnicas Avançadas de Aprendizado

---

## 🎯 Visão Geral

Transformação do QuizzMaster em uma plataforma educativa sofisticada focada em **Segurança Defensiva (Hardening, Detection, Response)** com técnicas cognitivas comprovadas:

- ✅ **Interleaving**: Misturar tópicos em sequências ótimas
- ✅ **Spaced Repetition**: Revisitar conceitos em intervalos científicos
- ✅ **Retrieval Practice**: Testes frequentes para fortalecer memória
- ✅ **Variabilidade**: Mesmo conceito em múltiplos contextos
- ✅ **Caminhos Adaptativos**: Ajusta dificuldade baseado em performance

---

## 🏗️ Novos Modelos de Dados

### 1. **LearningPath** (Caminho de Aprendizado)

```python
LearningPath
├── id: UUID
├── title: str (ex: "Python Basics for Secure Coding")
├── description: str
├── difficulty_level: enum (beginner, intermediate, advanced)
├── skills: ManyToMany [Skill]
├── prerequisites: ManyToMany [LearningPath]
├── order: int (sequência dentro de um nível)
├── is_structured: bool (True = caminho obrigatório, False = trilha)
├── duration_minutes: int
├── learning_objectives: JSONField (lista de objetivos)
├── created_at, updated_at
```

### 2. **Skill** (Competência/Tópico)

```python
Skill
├── id: UUID
├── name: str (ex: "SQL Injection Detection")
├── category: enum
│   ├── PYTHON_BASICS
│   ├── NETWORK_SECURITY
│   ├── CRYPTOGRAPHY
│   ├── LOG_ANALYSIS
│   ├── INCIDENT_RESPONSE
│   ├── WEB_SECURITY
│   ├── MALWARE_ANALYSIS
│   └── THREAT_INTEL
├── description: str
├── difficulty: enum (beginner, intermediate, advanced)
├── parent_skill: ForeignKey (para hierarquias)
├── created_at, updated_at
```

### 3. **Module** (Módulo de Conteúdo)

```python
Module
├── id: UUID
├── learning_path: ForeignKey
├── skill: ForeignKey
├── title: str
├── content_type: enum (LECTURE, INTERACTIVE, LAB, SCENARIO, ASSESSMENT)
├── order: int (ordem dentro do caminho)
├── duration_minutes: int
├── content: TextField (markdown)
├── resources: JSONField (links, PDFs, vídeos)
├── created_at, updated_at
```

### 4. **InteractiveLab** (Lab Prático com Execução)

```python
InteractiveLab
├── id: UUID
├── module: ForeignKey
├── title: str
├── description: str
├── difficulty: enum
├── setup_code: str (código de setup do ambiente)
├── solution_code: str (código esperado)
├── test_cases: JSONField
│   ├── test_name: str
│   ├── input: str
│   ├── expected_output: str
│   └── points: int
├── hints: JSONField (dicas progressivas)
├── time_limit_minutes: int
├── created_at, updated_at
```

### 5. **RealWorldScenario** (Desafios CTF-Style)

```python
RealWorldScenario
├── id: UUID
├── title: str (ex: "Detect SQL Injection Attack")
├── description: str
├── difficulty: enum
├── scenario_type: enum
│   ├── INCIDENT_RESPONSE
│   ├── MALWARE_ANALYSIS
│   ├── LOG_FORENSICS
│   ├── PENETRATION_TEST_DEFENSE
│   └── THREAT_DETECTION
├── story: str (contexto narrativo)
├── sample_data: JSONField (logs, arquivos, etc)
├── expected_findings: JSONField (o que descobrir)
├── points_max: int
├── time_limit_minutes: int
├── skills_covered: ManyToMany [Skill]
├── created_at, updated_at
```

### 6. **Question** (Questão com Interleaving)

```python
Question
├── id: UUID
├── skill: ForeignKey
├── content: str
├── question_type: enum
│   ├── MULTIPLE_CHOICE
│   ├── CODE_SNIPPET
│   ├── COMMAND_LINE
│   ├── LOG_ANALYSIS
│   └── FILL_IN_BLANK
├── difficulty: enum
├── options: JSONField (para múltipla escolha)
├── correct_answer: str
├── explanation: str (feedback detalhado)
├── code_context: str (para code snippets)
├── points: int
├── interleaving_group: int (para misturar tópicos)
├── created_at, updated_at
```

### 7. **UserProgress** (Rastreamento de Progresso)

```python
UserProgress
├── id: UUID
├── user: ForeignKey
├── learning_path: ForeignKey
├── status: enum (NOT_STARTED, IN_PROGRESS, COMPLETED)
├── progress_percentage: float
├── modules_completed: int
├── total_modules: int
├── estimated_completion_date: DateTime
├── started_at: DateTime
├── completed_at: DateTime (nullable)
├── created_at, updated_at
```

### 8. **UserSkillMastery** (Domínio de Competências)

```python
UserSkillMastery
├── id: UUID
├── user: ForeignKey
├── skill: ForeignKey
├── mastery_level: float (0-100)
├── times_reviewed: int
├── last_reviewed_at: DateTime
├── next_review_date: DateTime (spaced repetition)
├── strength: float (baseado em acertos históricos)
├── weakness: float (baseado em erros históricos)
├── created_at, updated_at
```

### 9. **Achievement & Badge** (Gamificação)

```python
Achievement
├── id: UUID
├── title: str
├── description: str
├── badge_icon: ImageField
├── achievement_type: enum
│   ├── SKILL_MASTERY (dominou uma competência)
│   ├── STREAK (X dias consecutivos)
│   ├── SPEED_RUN (completou rápido)
│   ├── PERFECT_SCORE (100% em avaliação)
│   ├── HELPING_OTHERS (ajudou X pessoas)
│   └── DISCOVERY (descobriu conceito difícil)
├── points_reward: int
├── criteria: JSONField (como conquistar)
├── rarity: enum (COMMON, RARE, EPIC, LEGENDARY)
├── created_at, updated_at

UserAchievement
├── id: UUID
├── user: ForeignKey
├── achievement: ForeignKey
├── unlocked_at: DateTime
├── progress: float (para badges progressivos)
```

### 10. **UserGamification** (Stats de Jogador)

```python
UserGamification
├── id: UUID
├── user: OneToOneField
├── level: int (1-100)
├── total_points: int
├── current_streak_days: int
├── max_streak_days: int
├── total_achievements: int
├── total_labs_completed: int
├── total_scenarios_completed: int
├── rank: enum (NOVICE, LEARNER, PRACTITIONER, EXPERT, MASTER)
├── friends: ManyToMany [User]
├── created_at, updated_at
```

### 11. **AdaptiveQuiz** (Quiz Adaptativo)

```python
AdaptiveQuiz
├── id: UUID
├── user: ForeignKey
├── learning_path: ForeignKey
├── current_difficulty: enum
├── questions_asked: int
├── correct_answers: int
├── last_performance: float (%)
├── should_increase_difficulty: bool
├── state: JSONField (histórico de respostas)
├── started_at: DateTime
├── completed_at: DateTime (nullable)
├── created_at, updated_at
```

---

## 🧠 Algoritmos de Aprendizado

### 1. **Interleaving Algorithm**

```
Para cada módulo de prática:
  1. Identificar 3-5 skills relacionadas
  2. Selecionar questões de cada skill (não sequencial)
  3. Padrão: SKILL_A → SKILL_B → SKILL_C → SKILL_A → SKILL_B
  4. Variação: misturar dificuldades também
  5. Resultado: melhor retenção que blocos sequenciais
```

### 2. **Spaced Repetition (SM-2 Algorithm)**

```
Interval Schedule:
  - Primeira revisão: 1 dia
  - Segunda: 3 dias
  - Terceira: 7 dias
  - Quarta: 14 dias
  - Quinta: 30 dias

Fator adaptativo:
  IF performance_score >= 4/5:
    interval = previous_interval * 2.5
  ELSE IF performance_score >= 3/5:
    interval = previous_interval * 1.5
  ELSE:
    interval = 1 (reset)
```

### 3. **Adaptive Difficulty**

```
Algoritmo:
  1. Iniciar em dificuldade BEGINNER
  2. Rastrear last_5_questions performance
  3. IF avg_performance >= 80%:
       → increase_difficulty()
  4. IF avg_performance < 50%:
       → decrease_difficulty()
  5. Aplicar +/- 10% pontos baseado na dificuldade
```

### 4. **Contextualized Learning**

```
Para cada skill, fornecer em contextos:
  1. ISOLATED: Questão teórica pura
  2. CODE_CONTEXT: Reconhecer em snippet de código
  3. REAL_WORLD: Aplicar em scenario prático
  4. TOOL_USAGE: Usar ferramenta real (Python, logs, etc)

Objetivo: Variabilidade contextual
```

---

## 🔌 Integração de Ferramentas Reais

### 1. **Python Code Execution**

```python
# Usar Docker ou exec() controlado
- Segurança: sandbox com timeout (5s)
- Feedback: stdout + stderr
- Testes: assertions automáticas
- Exemplo: Escrever script de hash com hashlib
```

### 2. **CLI Simulation**

```bash
# Ferramentas simuladas ou reais:
- nmap simulations
- wireshark log parsing
- grep/awk log analysis
- openssl certificate inspection
```

### 3. **Log Analysis Labs**

```
Dados reais de:
- Apache/Nginx access logs (detecção de ataques)
- Syslog (incidentes de segurança)
- Firewall logs (padrões de tráfego suspeito)
```

---

## 🗂️ Estrutura de Conteúdo: Cybersecurity Defensivo

### **Nível 1: Python para Segurança** (Beginner)

```
├── Module: Python Basics
│   ├── Topic: Variables & Data Types
│   ├── Topic: Functions & Imports
│   ├── Topic: File I/O
│   └── Lab: Script básico de hash
├── Module: Bibliotecas de Segurança
│   ├── Topic: hashlib (MD5, SHA, etc)
│   ├── Topic: ssl/tls
│   ├── Topic: secrets (random tokens)
│   └── Lab: Gerar certificados SSL
└── Module: Criptografia Básica
    ├── Topic: Symmetric encryption (AES)
    ├── Topic: Asymmetric encryption (RSA)
    └── Lab: Encriptar/Decriptar mensagens
```

### **Nível 2: Defesa Web** (Intermediate)

```
├── Module: Web Security Fundamentals
│   ├── Topic: OWASP Top 10
│   ├── Topic: Input Validation
│   ├── Topic: Output Encoding
│   └── Scenario: Detectar SQL Injection em logs
├── Module: Secure Coding Practices
│   ├── Topic: SQL Injection Prevention
│   ├── Topic: XSS Prevention
│   ├── Topic: CSRF Protection
│   └── Lab: Escrever formulário seguro
└── Module: API Security
    ├── Topic: Authentication (JWT, OAuth)
    ├── Topic: Authorization (RBAC)
    └── Lab: Proteger endpoint com tokens
```

### **Nível 3: Análise e Resposta** (Advanced)

```
├── Module: Log Analysis & Forensics
│   ├── Topic: Log Parsing com Python
│   ├── Topic: Pattern Recognition
│   ├── Topic: Timeline Construction
│   └── Lab: Analisar breach scenario
├── Module: Incident Response
│   ├── Topic: Detection (YARA, Sigma)
│   ├── Topic: Containment Strategies
│   ├── Topic: Eradication Techniques
│   └── Scenario: Responder a ransomware
└── Module: Threat Intelligence
    ├── Topic: IOC Collection
    ├── Topic: MITRE ATT&CK Framework
    └── Lab: Mapear ataque a técnicas
```

---

## 📊 Dashboard do Usuário

```
┌─────────────────────────────────────┐
│ 🎮 Seu Perfil de Aprendizado        │
├─────────────────────────────────────┤
│ Level: 15 | Points: 3,450           │
│ Streak: 7 dias 🔥 | Skills: 12/50   │
│                                     │
│ 📈 Caminho: Python + Web Security   │
│ Progress: 45% [████░░░░░]           │
│ Próximo módulo: XSS Prevention      │
│                                     │
│ 🎯 Próximas a Revisar (Spaced Rep) │
│  • SQL Injection Detection (2 dias) │
│  • XSS Payloads (5 dias)            │
│  • JWT Token Validation (7 dias)    │
│                                     │
│ 🏆 Achievements Recentes            │
│  ⭐ Quick Learner (completou em 15m)│
│  ⭐ SQL Expert (dominou skill)      │
│  ⭐ 7-Day Streak                    │
└─────────────────────────────────────┘
```

---

## 🚀 API/Endpoints Principais

| Método | URL                               | Função                           |
| ------ | --------------------------------- | -------------------------------- |
| GET    | `/api/learning-paths/`            | Listar caminhos                  |
| POST   | `/api/learning-paths/<id>/start/` | Iniciar trilha                   |
| GET    | `/api/modules/<id>/content/`      | Conteúdo do módulo               |
| POST   | `/api/labs/<id>/run/`             | Executar lab                     |
| POST   | `/api/scenarios/<id>/submit/`     | Submeter resposta                |
| GET    | `/api/adaptive-quiz/next/`        | Próxima questão (adaptive)       |
| POST   | `/api/adaptive-quiz/answer/`      | Responder (atualiza dificuldade) |
| GET    | `/api/user/progress/`             | Progresso do usuário             |
| GET    | `/api/user/skills/`               | Mastery de skills                |
| GET    | `/api/user/achievements/`         | Badges conquistadas              |
| GET    | `/api/leaderboard/`               | Ranking global                   |

---

## 🎨 UI/UX Componentes Novos

1. **Skill Visualizer** - Mapa visual de competências (grafo)
2. **Progress Timeline** - Histórico de aprendizado
3. **Code Editor** - Monaco com syntax highlighting
4. **Lab Terminal** - Simulador de CLI
5. **Scenario Viewer** - Painel de dados (logs, arquivos)
6. **Spaced Repetition Queue** - Cards para revisar
7. **Achievement Showcase** - Wall de badges
8. **Performance Analytics** - Gráficos de crescimento

---

## 📦 Dependências Novas Necessárias

```
django-extensions==3.2.3
django-cors-headers==4.3.1
djangorestframework==3.14.0
celery==5.4.0  # Para tarefas async (spaced rep)
redis==5.0.0   # Cache e broker
docker==7.0.0  # Para labs em sandbox
psutil==5.9.0  # Monitoramento de sistema
```

---

## ✅ Roadmap de Implementação

**Fase 1 (Esta semana)**

- [ ] Migrations: Novos modelos
- [ ] Algoritmos: Interleaving + Spaced Rep
- [ ] Conteúdo: Módulos base + 20 skills

**Fase 2**

- [ ] Labs: Python execution engine
- [ ] Scenarios: 5 desafios reais
- [ ] Gamification: Points + Achievements

**Fase 3**

- [ ] Dashboard: Visualizações
- [ ] Analytics: Tracking avançado
- [ ] Teacher tools: Criar conteúdo

**Fase 4**

- [ ] Mobile: App React Native
- [ ] Community: Forums + mentorship
- [ ] Marketplace: Compartilhar conteúdo

---

**Status**: 🔧 Planejado  
**Versão**: 2.0 Learning Platform  
**Data**: Setembro 2026
