from django.http import HttpResponse


def home(request):
    """
    Home-Page at `/`
    """
    return HttpResponse("It Works!")
