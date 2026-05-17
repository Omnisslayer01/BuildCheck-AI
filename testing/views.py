from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
import json
from .models import BugTicket


@csrf_exempt
@require_http_methods(["POST"])
def update_bug_status(request):
    """
    API endpoint to update bug ticket status.
    Expects JSON: {"ticket_id": 1, "status": "fixed"}
    """
    try:
        data = json.loads(request.body)
        ticket_id = data.get('ticket_id')
        status = data.get('status')
        
        if not ticket_id or not status:
            return JsonResponse({
                'success': False,
                'error': 'Missing ticket_id or status'
            }, status=400)
        
        # Validate status is one of the allowed choices
        valid_statuses = ['analyzing', 'test_failed', 'fixed']
        if status not in valid_statuses:
            return JsonResponse({
                'success': False,
                'error': f'Invalid status. Must be one of: {", ".join(valid_statuses)}'
            }, status=400)
        
        # Find and update the bug ticket
        try:
            ticket = BugTicket.objects.get(id=ticket_id)
            ticket.status = status
            ticket.save()
            
            return JsonResponse({
                'success': True,
                'message': f'Bug ticket {ticket_id} status updated to {status}',
                'ticket': {
                    'id': ticket.id,
                    'title': ticket.title,
                    'status': ticket.status
                }
            })
        except BugTicket.DoesNotExist:
            return JsonResponse({
                'success': False,
                'error': f'Bug ticket with id {ticket_id} not found'
            }, status=404)
            
    except json.JSONDecodeError:
        return JsonResponse({
            'success': False,
            'error': 'Invalid JSON'
        }, status=400)
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=500)



def dashboard_home(request):
    """Dashboard home view displaying all bug tickets"""
    tickets = BugTicket.objects.all()
    
    # Calculate stats
    total_tickets = tickets.count()
    fixed_tickets = tickets.filter(status='fixed').count()
    analyzing_tickets = tickets.filter(status='analyzing').count()
    
    # Mock stats for demo
    project_readiness = 85
    ai_fixes = fixed_tickets
    threats_blocked = 42
    
    context = {
        'tickets': tickets,
        'project_readiness': project_readiness,
        'ai_fixes': ai_fixes,
        'threats_blocked': threats_blocked,
    }
    
    return render(request, 'index.html', context)

def bug_list_partial(request):
    """HTMX endpoint for auto-refreshing bug ticket rows"""
    tickets = BugTicket.objects.all()
    context = {
        'tickets': tickets,
    }
    return render(request, 'bug_rows.html', context)

# Made with Bob
