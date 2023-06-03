from django.shortcuts import redirect
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required

from NewsPortal.models import Author


@login_required
def upgrade_me(request):
    user = request.user
    authors_group = Group.objects.get(name='authors')
    if not user.groups.filter(name='authors').exists() :
        authors_group.user_set.add(user)
        author = Author.objects.create(user=user, rating=0)
    return redirect('/')
