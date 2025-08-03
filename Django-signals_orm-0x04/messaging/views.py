from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponse

@login_required
def delete_user(request):
    user = get_object_or_404(User, pk=request.user.pk)
    user.delete()
    return HttpResponse("Your account and related data have been deleted.")