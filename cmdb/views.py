from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
import cmdb.models as models
import json
import generateUnittestCode.generateUnittest as generateUnittest


# Create your views here.
def test(request):
    return render(request, 'test.html')


def test2(request):
    text = 'sdfasfas'
    return HttpResponse("<p>" + text + "</p>")


def generateCode(request):
    test_data = json.loads(request.POST.get('data'))
    parameters = {
        'className': request.POST.get('classname'),
        'testCaseList': test_data,
        'report_file_path': request.POST.get('report_file_path', None),
        'report_file_title': request.POST.get('report_file_title', None),
        'report_file_description': request.POST.get('report_file_description', None),
    }
    generateUnittest.modelClassCreate(parameters, 'testCode')
    return JsonResponse({'code': 0, 'msg': 'success'})

