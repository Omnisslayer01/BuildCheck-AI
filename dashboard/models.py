from django.db import models

class BugTicket(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    status = models.CharField(
        max_length=50, 
        choices=[('analyzing', 'Analyzing (Red)'), ('fixed', 'Fixed (Green)')],
        default='analyzing'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Ticket #{self.id}: {self.title}"
# Create your models here.
