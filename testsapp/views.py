from django.shortcuts import render, get_object_or_404
from .models import Test

def test_list(request):
    tests = Test.objects.all()
    return render(request, 'testsapp/test_list.html', {'tests': tests})

def test_detail(request, test_id):
    test = get_object_or_404(Test, id=test_id)
    return render(request, 'testsapp/test_detail.html', {'test': test})