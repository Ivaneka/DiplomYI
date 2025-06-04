from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.utils import timezone
from django.db.models import Max
from .models import Test, TestResult, Material, Answer
from .forms import RegisterForm


def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('testsapp:cabinet')
    else:
        form = RegisterForm()
    return render(request, 'testsapp/register.html', {'form': form})


def test_list(request):
    tests = Test.objects.all()
    return render(request, 'testsapp/test_list.html', {'tests': tests})


@login_required
def test_detail(request, test_id):
    test = get_object_or_404(Test, id=test_id)
    materials = Material.objects.filter(related_test=test)

    if request.method == "POST":
        score = 0
        total_questions = test.question_set.count()

        for question in test.question_set.all():
            answer_id = request.POST.get(f'question_{question.id}')
            if answer_id:
                try:
                    selected_answer = Answer.objects.get(id=answer_id)
                    if selected_answer.is_correct:
                        score += 1
                except Answer.DoesNotExist:
                    pass

        TestResult.objects.create(
            user=request.user,
            test=test,
            score=score,
            completed_at=timezone.now()
        )
        return redirect('testsapp:cabinet')

    return render(request, 'testsapp/test_detail.html', {
        'test': test,
        'materials': materials
    })


@login_required
def personal_cabinet(request):
    test_stats = []
    assigned_tests = Test.objects.filter(assigned_to=request.user)

    for test in assigned_tests:
        results = TestResult.objects.filter(user=request.user, test=test)
        attempts = results.count()
        best_score = results.aggregate(Max('score'))['score__max'] if attempts > 0 else 0

        test_stats.append({
            'test': test,
            'attempts': attempts,
            'best_score': best_score,
            'last_attempt': results.last().completed_at if attempts > 0 else None
        })

    materials = Material.objects.filter(related_test__assigned_to=request.user).distinct()

    return render(request, 'testsapp/cabinet.html', {
        'test_stats': test_stats,
        'materials': materials
    })


@login_required
def material_detail(request, material_id):
    material = get_object_or_404(Material, id=material_id)
    return render(request, 'testsapp/material_detail.html', {'material': material})