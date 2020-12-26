from .models import *

def FirstYearStudent(request):
	if request.user.is_authenticated and hasattr(request.user, 'profile'):
		if StudentFee.objects.filter(profile=request.user.profile, feehead=2).exists():
			return {'first_year': True}
	return {}