"""Views for the quizz application."""
import json
import base64
from io import BytesIO
from urllib.parse import urlencode
from functools import wraps

from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse, HttpResponse, Http404
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.db.models import Avg, Count, Q
from django.views.decorators.csrf import csrf_exempt
from django.urls import reverse
from django.utils import timezone
import qrcode

from .models import Category, Quiz, QuizResult, QuizEnrollment, UserProfile, LiveSession, LiveParticipant


# ==========================================
# Decorators Customizados
# ==========================================

def teacher_required(view_func):
    """Decorator que garante que o usuário autenticado é um professor."""
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('quizz_app:login')
        profile = getattr(request.user, 'profile', None)
        if not profile or profile.role != 'profesor':
            return redirect('quizz_app:index')
        return view_func(request, *args, **kwargs)
    return _wrapped_view


# ==========================================
# Autenticação e Conta
# ==========================================

def login_view(request):
    """Display login page."""
    error = None
    if request.method == 'POST':
        identifier = request.POST.get('username', '').strip()
        password = request.POST.get('password', '')

        if not identifier or not password:
            error = 'Por favor completa todos los campos'
        else:
            username = identifier
            if '@' in identifier:
                try:
                    username = User.objects.get(email__iexact=identifier).username
                except User.DoesNotExist:
                    username = ''

            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect(request.POST.get('next') or 'quizz_app:index')
            error = 'Usuario o contraseña incorrectos'

    context = {'error': error, 'next': request.GET.get('next', '')}
    return render(request, 'login.html', context)


def register_view(request):
    """Register a new student account."""
    error = None
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        email = request.POST.get('email', '').strip().lower()
        password = request.POST.get('password', '')
        password_confirmation = request.POST.get('password_confirmation', '')

        if not username or not email or not password or not password_confirmation:
            error = 'Por favor completa todos los campos'
        else:
            try:
                validate_email(email)
            except ValidationError:
                error = 'Ingresa un correo electrónico válido'

        if error is None and password != password_confirmation:
            error = 'Las contraseñas no coinciden'
        elif error is None and User.objects.filter(username=username).exists():
            error = 'Este nombre de usuario ya está registrado'
        elif error is None and User.objects.filter(email__iexact=email).exists():
            error = 'Este correo electrónico ya está registrado'
        elif error is None:
            user = User.objects.create_user(username=username, email=email, password=password)
            UserProfile.objects.get_or_create(user=user, defaults={'role': 'estudiante'})
            return redirect('quizz_app:login')

    return render(request, 'register.html', {'error': error})


def logout_view(request):
    """Logout the user."""
    logout(request)
    return redirect('quizz_app:login')


# ==========================================
# Quizzes - Alunos
# ==========================================

def index(request):
    """Display list of available quizzes."""
    quizzes = Quiz.objects.all().order_by('-created_at')
    return render(request, 'index.html', {'quizzes': quizzes})


@login_required
def quiz_detail(request, quiz_id):
    """Display a specific quiz."""
    quiz = get_object_or_404(Quiz, id=quiz_id)
    context = {
        'quiz': quiz,
        'questions': quiz.get_questions(),
    }
    return render(request, 'quiz.html', context)


@login_required
@require_http_methods(["POST"])
def submit_quiz(request, quiz_id):
    """Handle quiz submission and calculate score."""
    quiz = get_object_or_404(Quiz, id=quiz_id)
    
    try:
        data = json.loads(request.body)
        answers = data.get('answers', {})
        question_times = data.get('question_times', {})
        if not isinstance(question_times, dict):
            question_times = {}

        questions = quiz.get_questions()
        normalized_question_times = {
            str(index): max(0, int(question_times.get(str(index), 0)))
            for index in range(len(questions))
        }
        time_taken = sum(normalized_question_times.values())
        average_time_per_question = time_taken / len(questions) if questions else 0
        
        score = 0
        total = len(questions)
        
        for idx, question in enumerate(questions):
            question_idx = str(idx)
            user_ans = answers.get(question_idx)
            correct_ans = question.get('correct_answer')
            
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
            answers=answers,
            question_times=normalized_question_times,
            time_taken=time_taken,
            average_time_per_question=average_time_per_question,
        )
        
        return JsonResponse({
            'success': True,
            'score': score,
            'total': total,
            'percentage': round(percentage, 2),
            'time_taken': time_taken,
            'average_time_per_question': round(average_time_per_question, 2),
            'result_id': result.id
        })
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=400)


def results(request, result_id):
    """Display quiz results."""
    result = get_object_or_404(QuizResult, id=result_id)
    questions = result.quiz.get_questions()
    
    detailed_results = []
    for idx, question in enumerate(questions):
        question_idx = str(idx)
        user_answer = result.answers.get(question_idx)
        correct_answer = question.get('correct_answer')
        
        is_correct = (
            user_answer is not None and 
            str(user_answer).strip() == str(correct_answer).strip()
        )
        
        detailed_results.append({
            'question': question.get('question'),
            'options': question.get('options', []),
            'correct_answer': correct_answer,
            'user_answer': user_answer,
            'is_correct': is_correct,
        })
    
    context = {
        'result': result,
        'detailed_results': detailed_results,
    }
    return render(request, 'results.html', context)


@login_required
def my_scores(request):
    """Display the authenticated user's completed quiz results."""
    results = QuizResult.objects.filter(student=request.user).order_by('-created_at')
    return render(request, 'my_scores.html', {'results': results})


def leaderboard(request, quiz_id):
    """Display leaderboard for a specific quiz."""
    quiz = get_object_or_404(Quiz, id=quiz_id)
    results = QuizResult.objects.filter(quiz=quiz).order_by('-score', '-percentage')[:10]
    return render(request, 'leaderboard.html', {'quiz': quiz, 'results': results})


def generate_qr_code(request, quiz_id):
    """Generate QR code for quiz enrollment."""
    quiz = get_object_or_404(Quiz, id=quiz_id)
    enrollment_path = reverse('quizz_app:enroll_quiz', kwargs={'access_code': quiz.access_code})
    enrollment_url = request.build_absolute_uri(enrollment_path)
    
    qr = qrcode.QRCode(version=1, box_size=10, border=2)
    qr.add_data(enrollment_url)
    qr.make(fit=True)
    
    img = qr.make_image(fill_color="black", back_color="white")
    buffer = BytesIO()
    img.save(buffer, format='PNG')
    
    return HttpResponse(buffer.getvalue(), content_type='image/png')


def enroll_quiz(request, access_code):
    """Enroll student in quiz via access code."""
    quiz = get_object_or_404(Quiz, access_code=access_code, is_active=True)
    
    if request.user.is_authenticated:
        QuizEnrollment.objects.get_or_create(student=request.user, quiz=quiz)
        return redirect('quizz_app:quiz_detail', quiz_id=quiz.id)
    else:
        next_url = reverse('quizz_app:quiz_detail', kwargs={'quiz_id': quiz.id})
        login_url = reverse('quizz_app:login')
        return redirect(f'{login_url}?{urlencode({"next": next_url})}')


# ==========================================
# Área do Professor
# ==========================================

@login_required
@teacher_required
def teacher_dashboard(request):
    """Teacher dashboard to manage quizzes (Otimizado via ORM)."""
    quizzes = Quiz.objects.filter(creator=request.user).annotate(
        enrollments_count=Count('quizenrollment', distinct=True),
        attempts_count=Count('results', distinct=True),
        avg_score=Avg('results__percentage')
    ).order_by('-created_at')
    
    quiz_stats = [
        {
            'quiz': quiz,
            'enrollments': quiz.enrollments_count,
            'attempts': quiz.attempts_count,
            'avg_score': round(quiz.avg_score or 0, 2),
        }
        for quiz in quizzes
    ]
    
    return render(request, 'teacher_dashboard.html', {'quiz_stats': quiz_stats})


@login_required
@teacher_required
def teacher_statistics(request):
    """Display aggregate performance statistics for the teacher's quizzes."""
    quizzes = Quiz.objects.filter(creator=request.user)
    results = QuizResult.objects.filter(quiz__creator=request.user)
    
    aggregate = results.aggregate(
        total_attempts=Count('id'),
        total_students=Count('student', distinct=True),
        average_score=Avg('percentage'),
        average_time=Avg('time_taken'),
    )
    
    category_stats = quizzes.values('category').annotate(
        quizzes=Count('id'),
        attempts=Count('results'),
        average_score=Avg('results__percentage'),
    ).order_by('category')

    context = {
        'total_quizzes': quizzes.count(),
        'active_quizzes': quizzes.filter(is_active=True).count(),
        'total_attempts': aggregate['total_attempts'],
        'total_students': aggregate['total_students'],
        'average_score': round(aggregate['average_score'] or 0, 2),
        'average_time': round(aggregate['average_time'] or 0, 2),
        'category_stats': category_stats,
    }
    return render(request, 'teacher_statistics.html', context)


@login_required
@teacher_required
def manage_categories(request):
    """Create, rename, and delete quiz categories owned by the teacher."""
    if request.method == 'POST':
        action = request.POST.get('action')
        name = request.POST.get('name', '').strip()

        if action == 'create' and name:
            Category.objects.get_or_create(teacher=request.user, name=name)
        elif action == 'rename' and name:
            category = get_object_or_404(Category, id=request.POST.get('category_id'), teacher=request.user)
            category.name = name
            category.save()
        elif action == 'delete':
            category = get_object_or_404(Category, id=request.POST.get('category_id'), teacher=request.user)
            category.delete()

        return redirect('quizz_app:manage_categories')

    categories = Category.objects.filter(teacher=request.user)
    return render(request, 'manage_categories.html', {'categories': categories})


@login_required
@teacher_required
def create_quiz(request):
    """Create a new quiz."""
    if request.method == 'POST':
        try:
            title = request.POST.get('title', '').strip()
            description = request.POST.get('description', '').strip()
            category = request.POST.get('category', 'General').strip()
            difficulty = request.POST.get('difficulty', 'medio')
            time_limit = int(request.POST.get('time_limit', 0))
            questions_json = request.POST.get('questions', '[]')
            
            if not title:
                raise ValueError('El título es requerido')
            if not difficulty:
                raise ValueError('La dificultad es requerida')
            
            try:
                questions = json.loads(questions_json)
            except json.JSONDecodeError as e:
                raise ValueError(f'Error en el JSON de las preguntas: {str(e)}')
            
            if not questions or not isinstance(questions, list):
                raise ValueError('Las preguntas deben ser una lista JSON válida')
            
            for idx, q in enumerate(questions):
                if not isinstance(q, dict):
                    raise ValueError(f'Pregunta {idx + 1}: debe ser un objeto')
                if 'question' not in q or 'options' not in q or 'correct_answer' not in q:
                    raise ValueError(f'Pregunta {idx + 1}: debe tener "question", "options" y "correct_answer"')
                if not isinstance(q['options'], list) or len(q['options']) < 2:
                    raise ValueError(f'Pregunta {idx + 1}: debe tener al menos 2 opciones')
                try:
                    correct_idx = int(q['correct_answer'])
                    if correct_idx < 0 or correct_idx >= len(q['options']):
                        raise ValueError()
                except (ValueError, TypeError):
                    raise ValueError(f'Pregunta {idx + 1}: "correct_answer" es inválido')
            
            Quiz.objects.create(
                creator=request.user,
                title=title,
                description=description,
                category=category,
                difficulty=difficulty,
                time_limit=time_limit,
                questions_data=questions,
                is_active=True
            )
            return redirect('quizz_app:teacher_dashboard')
            
        except (ValueError, KeyError) as e:
            context = {'error': str(e), 'form_data': request.POST}
            return render(request, 'create_quiz.html', context, status=400)
    
    return render(request, 'create_quiz.html', {
        'categories': Category.objects.filter(teacher=request.user),
    })


@login_required
@teacher_required
def edit_quiz(request, quiz_id):
    """Edit an existing quiz."""
    quiz = get_object_or_404(Quiz, id=quiz_id, creator=request.user)
    
    if request.method == 'POST':
        try:
            title = request.POST.get('title', '').strip()
            description = request.POST.get('description', '').strip()
            category = request.POST.get('category', 'General').strip()
            difficulty = request.POST.get('difficulty', 'medio')
            time_limit = int(request.POST.get('time_limit', 0))
            questions_json = request.POST.get('questions', '[]')
            
            if not title or not difficulty:
                raise ValueError('Título e Dificuldade são obrigatórios')
            
            questions = json.loads(questions_json)
            if not questions or not isinstance(questions, list):
                raise ValueError('Las preguntas deben ser una lista JSON válida')
            
            quiz.title = title
            quiz.description = description
            quiz.category = category
            quiz.difficulty = difficulty
            quiz.time_limit = time_limit
            quiz.questions_data = questions
            quiz.save()
            
            return redirect('quizz_app:teacher_dashboard')
            
        except (ValueError, json.JSONDecodeError) as e:
            context = {'error': str(e), 'quiz': quiz, 'form_data': request.POST}
            return render(request, 'edit_quiz.html', context, status=400)
    
    context = {
        'quiz': quiz,
        'categories': Category.objects.filter(teacher=request.user),
        'form_data': {
            'title': quiz.title,
            'description': quiz.description,
            'category': quiz.category,
            'difficulty': quiz.difficulty,
            'time_limit': quiz.time_limit,
            'questions': json.dumps(quiz.questions_data, ensure_ascii=False, indent=2)
        }
    }
    return render(request, 'edit_quiz.html', context)


@login_required
@teacher_required
def delete_quiz(request, quiz_id):
    """Delete a quiz."""
    quiz = get_object_or_404(Quiz, id=quiz_id, creator=request.user)
    if request.method == 'POST':
        quiz.delete()
        return redirect('quizz_app:teacher_dashboard')
    
    return render(request, 'delete_quiz.html', {'quiz': quiz})


@login_required
@teacher_required
def quiz_students(request, quiz_id):
    """View all students who took a specific quiz (Otimizado via ORM)."""
    quiz = get_object_or_404(Quiz, id=quiz_id, creator=request.user)
    results = QuizResult.objects.filter(quiz=quiz).order_by('-percentage', '-score')
    
    stats = results.aggregate(avg_score=Avg('percentage'), total_attempts=Count('id'))
    
    context = {
        'quiz': quiz,
        'results': results,
        'total_attempts': stats['total_attempts'],
        'avg_score': round(stats['avg_score'] or 0, 2),
    }
    return render(request, 'quiz_students.html', context)


# ==========================================
# Sessões Ao Vivo
# ==========================================

@login_required
@teacher_required
def start_live_session(request, quiz_id):
    """Start a live session for a quiz."""
    quiz = get_object_or_404(Quiz, id=quiz_id, creator=request.user)
    session = LiveSession.objects.create(quiz=quiz, teacher=request.user, status='waiting')
    return redirect('quizz_app:manage_live_session', session_id=session.id)


@login_required
@teacher_required
def manage_live_session(request, session_id):
    """Manage a live session (teacher view)."""
    session = get_object_or_404(LiveSession, id=session_id, teacher=request.user)
    
    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'start':
            session.status = 'active'
            session.started_at = timezone.now()
        elif action == 'pause':
            session.status = 'paused'
        elif action == 'resume':
            session.status = 'active'
        elif action == 'finish':
            session.status = 'finished'
            session.ended_at = timezone.now()
            session.allow_join = False
        
        session.save()
        return redirect('quizz_app:manage_live_session', session_id=session_id)
    
    participants = session.live_participants.all()
    total_questions = len(session.quiz.questions_data or [])

    for participant in participants:
        participant.score_percentage = (participant.score / total_questions * 100) if total_questions > 0 else 0

    context = {
        'session': session,
        'quiz': session.quiz,
        'participants': participants,
        'total_participants': participants.count(),
        'completed_count': participants.filter(completed=True).count(),
    }
    return render(request, 'live_session_manage.html', context)


@login_required
def join_live_session(request):
    """Join a live session (student view)."""
    if request.method == 'POST':
        session_code = request.POST.get('session_code', '').strip().upper()
        student_name = request.POST.get('student_name', '').strip()
        
        try:
            session = LiveSession.objects.get(
                session_code=session_code, 
                allow_join=True, 
                status__in=['waiting', 'active']
            )
        except LiveSession.DoesNotExist:
            return render(request, 'join_live_session.html', {'error': 'Código de sesión no válido o sesión no disponible'})
        
        participant, created = LiveParticipant.objects.get_or_create(
            session=session,
            student_name=student_name,
            defaults={'student': request.user if request.user.is_authenticated else None}
        )
        
        if not created and participant.completed:
            return render(request, 'join_live_session.html', {'error': 'Ya has completado esta sesión'})
        
        return redirect('quizz_app:live_quiz', session_id=session.id, participant_id=participant.id)
    
    return render(request, 'join_live_session.html')


@login_required
def live_quiz(request, session_id, participant_id):
    """Take the live quiz (student view)."""
    session = get_object_or_404(LiveSession, id=session_id)
    participant = get_object_or_404(LiveParticipant, id=participant_id, session=session)
    
    if participant.completed:
        return redirect('quizz_app:live_results', session_id=session_id, participant_id=participant_id)
    
    quiz = session.quiz
    questions = quiz.get_questions()
    
    if request.method == 'POST':
        answers = {}
        for i in range(len(questions)):
            answer = request.POST.get(f'question_{i}')
            if answer is not None:
                try:
                    answers[str(i)] = int(answer)
                except ValueError:
                    continue
        
        score = sum(
            1 for i, q in enumerate(questions)
            if str(i) in answers and str(answers[str(i)]).strip() == str(q.get('correct_answer')).strip()
        )
        
        participant.answers = answers
        participant.score = score
        participant.completed = True
        participant.submitted_at = timezone.now()
        participant.save()
        
        return redirect('quizz_app:live_results', session_id=session_id, participant_id=participant_id)
    
    context = {
        'session': session,
        'quiz': quiz,
        'questions': questions,
        'participant': participant,
    }
    return render(request, 'live_quiz.html', context)


@login_required
def live_results(request, session_id, participant_id):
    """View live quiz results (student view)."""
    session = get_object_or_404(LiveSession, id=session_id)
    participant = get_object_or_404(LiveParticipant, id=participant_id, session=session)
    
    questions = session.quiz.get_questions()
    detailed_results = []
    
    for i, question in enumerate(questions):
        user_answer = participant.answers.get(str(i))
        correct_answer = question.get('correct_answer')
        
        is_correct = (
            user_answer is not None and 
            str(user_answer).strip() == str(correct_answer).strip()
        )
        
        detailed_results.append({
            'question': question.get('question'),
            'options': question.get('options', []),
            'user_answer': user_answer,
            'correct_answer': correct_answer,
            'is_correct': is_correct,
        })
    
    percentage = (participant.score / len(questions) * 100) if questions else 0
    
    context = {
        'session': session,
        'quiz': session.quiz,
        'participant': participant,
        'score': participant.score,
        'total': len(questions),
        'percentage': round(percentage, 1),
        'detailed_results': detailed_results,
    }
    return render(request, 'live_results.html', context)


def api_session_status(request, session_id):
    """API endpoint to get live session status."""
    session = get_object_or_404(LiveSession, id=session_id)
    participants = session.live_participants.all()
    
    return JsonResponse({
        'status': session.status,
        'current_question': getattr(session, 'current_question', 0),
        'total_participants': participants.count(),
        'completed': participants.filter(completed=True).count(),
        'participants': [
            {
                'name': p.student_name,
                'completed': p.completed,
                'score': p.score if p.completed else None,
            }
            for p in participants
        ]
    })


@login_required
def cybersecurity_quiz_view(request):
    """Exibe o quiz de Cibersegurança."""
    quiz = Quiz.objects.filter(
        Q(category__icontains='cybersecurity') | 
        Q(category__icontains='ciberseguran') |
        Q(title__icontains='cybersecurity') |
        Q(title__icontains='ciberseguran')
    ).first()

    if not quiz:
        quiz = Quiz.objects.first()

    if not quiz:
        raise Http404("Nenhum quiz foi encontrado no banco de dados.")
    
    context = {
        'quiz': quiz,
        'questions': quiz.get_questions(),
    }
    return render(request, 'quiz.html', context)