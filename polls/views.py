import datetime
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from .models import Goal
from .forms import GoalForm
from django.utils import timezone

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('polls:goal_list')
    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('polls:goal_list')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

@login_required
def goal_list(request):
    if request.method == 'POST':
        form = GoalForm(request.POST)
        if form.is_valid():
            goal = form.save(commit=False)
            goal.user = request.user
            goal.save()
            return redirect('polls:goal_list')
    else:
        form = GoalForm()

    today = datetime.date.today()
    current_year, current_week, _ = today.isocalendar()
    goals = Goal.objects.filter(user=request.user, created_at__year=current_year, created_at__week=current_week)

    weekdays = ['월', '화', '수', '목', '금', '토', '일']
    weekday_goals = {weekday: [] for weekday in weekdays}
    for goal in goals:
        weekday_index = goal.day_of_week
        weekday_goals[weekdays[weekday_index]].append(goal)

    return render(request, 'goal_list.html', {'form': form, 'weekday_goals': weekday_goals})

@login_required
def delete_goal(request, goal_id):
    goal = get_object_or_404(Goal, id=goal_id, user=request.user)
    goal.delete()
    return redirect('polls:goal_list')

@login_required
def complete_goal(request, goal_id):
    goal = get_object_or_404(Goal, id=goal_id, user=request.user)
    goal.completed = not goal.completed
    goal.save()
    return redirect('polls:goal_list')

@login_required
def history(request):
    current_week = timezone.now().isocalendar()[1]
    goals = Goal.objects.filter(user=request.user)
    weeks = goals.dates('created_at', 'week')

    weekly_goals = {}
    for week in weeks:
        week_goals = goals.filter(created_at__week=week.isocalendar()[1])
        completed_goals = week_goals.filter(completed=True).count()
        total_goals = week_goals.count()
        weekly_goals[week] = {
            'goals': week_goals,
            'completed_goals': completed_goals,
            'total_goals': total_goals,
        }

    current_week_goals = goals.filter(created_at__week=current_week)
    weekly_goals[timezone.now().date()] = {
        'goals': current_week_goals,
        'completed_goals': current_week_goals.filter(completed=True).count(),
        'total_goals': current_week_goals.count(),
    }

    sorted_weekly_goals = sorted(weekly_goals.items(), reverse=True)
    current_date = timezone.now().date()

    return render(request, 'history.html', {'weekly_goals': sorted_weekly_goals, 'current_date': current_date})

@login_required
def add_reflection(request, goal_id):
    goal = get_object_or_404(Goal, id=goal_id, user=request.user)
    if request.method == 'POST':
        goal.reflection = request.POST['reflection']
        if 'image' in request.FILES:
            goal.image = request.FILES['image']
        goal.save()
        return redirect('polls:goal_list')
    return render(request, 'add_reflection.html', {'goal': goal})