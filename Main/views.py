from django.shortcuts import render
from django.contrib.auth.models import User


def home(request):

    return render(request, 'Placement/placement_index.html')

