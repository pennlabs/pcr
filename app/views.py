from django.shortcuts import get_object_or_404, render_to_response, redirect
from django.http import HttpResponseRedirect, HttpResponse
from django.template import Context, loader, RequestContext

def index(request):
  return render_to_response('index.html')

def instructor(request):
  return render_to_response('instructor.html')

def course(request):
  return render_to_response('course.html')

def department(request):
  return render_to_response('department.html')

def browse(request):
  return render_to_response('browse.html')
