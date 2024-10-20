from .models import UserProfile

def user_points(request):
    if request.user.is_authenticated:
        try:
            profile = UserProfile.objects.get(user=request.user)
            points = profile.points
        except UserProfile.DoesNotExist:
            points = 0
        return {'user_points': points}
    return {}
