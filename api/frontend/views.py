from django.http import HttpResponse


def home(request):
    """
    Home-Page at `/`
    """
    return HttpResponse("It Works!")


def add(request):
    """
    Add-Page at `/add`
    """


def result(request):
    """
    Result-Page at `/result`
    """


def report(request):
    """
    Report-Page at `/report`
    """


def view_report(request, report_id: int):
    """
    Individual-Report-Pages at `/report/<int:id>`
    """
