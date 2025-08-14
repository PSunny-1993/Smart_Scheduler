from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import TenderList
from .models import Door
from .email_parser import fetch_invitation_emails
from .serializers import DoorSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status


@csrf_exempt
def run_email_parser(request):
    """
    Trigger the email parser when a POST request is made.
    """
    if request.method == 'POST':
        try:
            fetch_invitation_emails()
            return JsonResponse({'status': 'success'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)
    return JsonResponse({'status': 'invalid request'}, status=400)

def estimating_list_view(request):
    """
    Display the list of tenders.
    """
    tenders = TenderList.objects.all().order_by('-created_at')
    return render(request, 'Estimating/estimating_list.html', {'tenders': tenders})

from .email_parser import fetch_invitation_emails


def fetch_emails_view(request):
    try:
        fetch_invitation_emails()
        return JsonResponse({'status': 'emails fetched'})
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=500)


def create_project_view(request, tender_id):
    from .forms import ProjectForm
    tender = get_object_or_404(TenderList, pk=tender_id)
    if request.method == 'POST':
        form = ProjectForm(request.POST)
        if form.is_valid():
            project = form.save(commit=False)
            project.created_from = tender
            project.save()
            return redirect('create_package', project_id=project.id)
    else:
        form = ProjectForm(initial={
            'name': tender.project_name,
            'builder': tender.builder,
            'estimator': tender.estimator
        })
    return render(request, 'projects/create_project.html', {'form': form})

@api_view(['POST'])
def save_doors(request):
    doors_data = request.data.get('doors', [])

    # Save each door
    for row in doors_data:
        if len(row) >= 4:
            Door.objects.create(
                name=row[0],
                material=row[1],
                type=row[2],
                rating=row[3]
            )

    return Response({"message": "Doors saved successfully."}, status=status.HTTP_201_CREATED)


