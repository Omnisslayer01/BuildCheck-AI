from django.shortcuts import render
from testing.models import BugTicket

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
    
    return render(request, 'dashboard.html', context)

def bug_list_partial(request):
    """HTMX endpoint for auto-refreshing bug ticket rows"""
    tickets = BugTicket.objects.all()
    context = {
        'tickets': tickets,
    }
    return render(request, 'partials/bug_rows.html', context)
