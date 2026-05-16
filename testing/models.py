from django.db import models

# Create your models here.

class BugTicket(models.Model):
    STATUS_CHOICES = [
        ('analyzing', 'Analyzing'),
        ('test_failed', 'Test Failed'),
        ('fixed', 'Fixed'),
    ]
    
    title = models.CharField(max_length=200)
    bug_description = models.TextField()
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='analyzing'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.title
    
    class Meta:
        ordering = ['-created_at']

# Made with Bob
