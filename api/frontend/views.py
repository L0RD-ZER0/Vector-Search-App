from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponseBadRequest

import libs


def _extract_form_data(request: HttpRequest) -> dict[str]:
    assert 'title' in request.POST
    assert 'text' in request.POST
    assert len(request.POST['title'].encode('utf-8')) < 4096
    return {
        'title': request.POST['title'],
        'authors': _ if (_ := request.POST.get('authors', None)) else None,
        'affiliations': _ if (_ := request.POST.get('affiliations', None)) else None,
        'abstract': _ if (_ := request.POST.get('abstract', None)) else None,
        'text': request.POST['text'],
        'bibliography': _ if (_ := request.POST.get('bibliography', None)) else None,
    }


def home(request):
    """
    Home-Page at `/`
    """
    return render(request, 'home.html')


def add(request: HttpRequest):
    """
    Add-Page at `/add`
    """
    if request.method == 'GET':
        return render(request, 'add.html')
    elif request.method == 'POST':
        try:
            data = _extract_form_data(request)
        except AssertionError:
            return HttpResponseBadRequest("Invalid data sent.")
        else:
            libs.upsert_article(data)
            return redirect('add-report')


def result(request):
    """
    Result-Page at `/result`
    """
    if request.method == 'GET':
        if 'context' in request.session:
            context = request.session['context']

            del request.session['context']
            return render(request, 'result.html', context)
        else:
            return redirect('homepage')
    elif request.method == 'POST':
        try:
            data = _extract_form_data(request)
        except AssertionError:
            return HttpResponseBadRequest("Invalid data sent.")
        else:
            results = libs.analyse_article(data)
            context = {}
            for _ in data:
                context[_] = data[_] if data[_] else "—"
            context['results'] = results
            request.session['context'] = context
            return redirect('result')


def report(request):
    """
    Report-Page at `/report`
    """
    if 'article-id' in request.GET:
        try:
            article_id = int(request.GET['article-id'])
        except ValueError:
            return HttpResponseBadRequest("Invalid data sent.")
        else:
            data = libs.fetch_article(article_id)
            context = {}
            for _ in data:
                context[_] = data[_] if data[_] else "—"
            return render(request, 'report-data.html', context)
    return render(request, 'report.html')
