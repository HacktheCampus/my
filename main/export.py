import csv
from hackers.models import Hacker, Application, Team
from staff.models import Staff
from django.http import HttpResponse


def basic(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=basic.csv'
    writer = csv.writer(response, csv.excel)
    writer.writerow([
        "First Name",
        "Last Name",
        "Email",
        "Token",
    ])
    for obj in Hacker.objects.all():
        writer.writerow([
            obj.first_name,
            obj.last_name,
            obj.email,
            obj.token
        ])
    return response


def basic_staff(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=basic_staff.csv'
    writer = csv.writer(response, csv.excel)
    writer.writerow([
        "First Name",
        "Last Name",
        "Email",
        "Token",
    ])
    for obj in Staff.objects.all():
        writer.writerow([
            obj.first_name,
            obj.last_name,
            obj.email,
            obj.token
        ])
    return response


def basic_confirmed(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=basic_confirmed.csv'
    writer = csv.writer(response, csv.excel)
    writer.writerow([
        "First Name",
        "Last Name",
        "Email",
        "Token",
    ])
    for obj in Hacker.objects.all():
        if obj.finished_application:
            writer.writerow([
                obj.first_name,
                obj.last_name,
                obj.email,
                obj.token
            ])
    return response


def basic_unconfirmed(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=basic_unconfirmed.csv'
    writer = csv.writer(response, csv.excel)
    writer.writerow([
        "First Name",
        "Last Name",
        "Email",
        "Token",
    ])
    for obj in Hacker.objects.all():
        if not obj.finished_application:
            writer.writerow([
                obj.first_name,
                obj.last_name,
                obj.email,
                obj.token
            ])
    return response


def advanced(request, exclude_hacker=[], exclude_application=[]):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=advanced.csv'
    writer = csv.writer(response, csv.excel)
    fields = [k for k, v in Hacker.objects.first().export_fields(exclude_hacker).items()]
    fields.extend([k for k, v in Application.objects.first().export_fields(exclude_application).items()])
    writer.writerow(fields)
    for hacker in Hacker.objects.all():
        if hacker.finished_application:
            row = [v for k, v in hacker.export_fields(exclude_hacker).items()]
            row.extend([v for k, v in hacker.application.export_fields(exclude_application).items()])
            writer.writerow(row)
    return response


def advanced_attended(request, exclude_hacker=[], exclude_application=[]):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=advanced.csv'
    writer = csv.writer(response, csv.excel)
    fields = [k for k, v in Hacker.objects.first().export_fields(exclude_hacker).items()]
    fields.extend([k for k, v in Application.objects.first().export_fields(exclude_application).items()])
    writer.writerow(fields)
    for hacker in Hacker.objects.filter(checked_in=True):
        if hacker.finished_application:
            row = [v for k, v in hacker.export_fields(exclude_hacker).items()]
            row.extend([v for k, v in hacker.application.export_fields(exclude_application).items()])
            writer.writerow(row)
    return response


def teams(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=teams.csv'
    writer = csv.writer(response, csv.excel)
    for obj in Team.objects.exclude(project__isnull=True).exclude(project__exact='').exclude(location__isnull=True).exclude(location__exact='').exclude(github_url=None).exclude(github_url__iexact=''):
        if obj.hackers.all().count() > 0:
            writer.writerow([
                obj.name,
                obj.location,
                obj.project
            ])
    return response


def teams_after(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=teams.csv'
    writer = csv.writer(response, csv.excel)
    writer.writerow(["Nome", "Local", "Descrição", "Github", "Participantes"])
    for obj in Team.objects.exclude(project__isnull=True).exclude(project__exact='').exclude(location__isnull=True).exclude(location__exact='').exclude(github_url=None).exclude(github_url__iexact=''):
        if obj.hackers.all().count() > 0:
            writer.writerow([
                obj.name,
                obj.location,
                obj.project,
                obj.github_url,
                str([hacker.name for hacker in obj.hackers.all()])
            ])
    return response
