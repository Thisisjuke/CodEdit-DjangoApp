def last_proj(request):
    if request.user.is_authenticated:
        from django.conf import settings
        from .models import Project

        last_proj = Project.objects.all().filter(user=request.user)[:7]
        return {'last_proj': last_proj}
    else:
        return {'last_proj': 0}