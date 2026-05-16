"""
Django management command to auto-update Business Lens evaluations.

Usage:
    python manage.py update_business_lens --once
    python manage.py update_business_lens --interval 900
"""
import time
from django.core.management.base import BaseCommand
from testing.models import BugTicket, BusinessEvaluation


class Command(BaseCommand):
    help = 'Auto-update Business Lens evaluations based on bug ticket data'

    def add_arguments(self, parser):
        parser.add_argument(
            '--once',
            action='store_true',
            help='Create one evaluation and exit',
        )
        parser.add_argument(
            '--interval',
            type=int,
            default=900,
            help='Interval in seconds between updates (default: 900)',
        )

    def handle(self, *args, **options):
        once = options['once']
        interval = options['interval']

        if once:
            self.stdout.write(self.style.SUCCESS('Creating single Business Lens evaluation...'))
            self.create_evaluation()
            self.stdout.write(self.style.SUCCESS('[OK] Evaluation created successfully'))
        else:
            self.stdout.write(self.style.SUCCESS(
                f'Starting Business Lens auto-update (interval: {interval}s)'
            ))
            self.stdout.write(self.style.WARNING('Press Ctrl+C to stop'))
            
            try:
                while True:
                    self.create_evaluation()
                    self.stdout.write(self.style.SUCCESS(
                        f'[OK] Evaluation created. Next update in {interval}s...'
                    ))
                    time.sleep(interval)
            except KeyboardInterrupt:
                self.stdout.write(self.style.WARNING('\nStopping Business Lens auto-update'))

    def create_evaluation(self):
        """Create a new BusinessEvaluation based on current bug ticket data"""
        # Get bug ticket statistics
        total_tickets = BugTicket.objects.count()
        fixed_tickets = BugTicket.objects.filter(status='fixed').count()
        open_tickets = BugTicket.objects.exclude(status='fixed').count()

        # Calculate score using deterministic logic
        score = self.calculate_score(total_tickets, fixed_tickets, open_tickets)
        
        # Generate verdict based on score
        verdict = self.generate_verdict(score)

        # Create the evaluation
        evaluation = BusinessEvaluation.objects.create(
            score=score,
            verdict=verdict
        )

        self.stdout.write(
            f'Created evaluation #{evaluation.id}: Score={score}, '
            f'Tickets={total_tickets} (Fixed={fixed_tickets}, Open={open_tickets})'
        )

        return evaluation

    def calculate_score(self, total_tickets, fixed_tickets, open_tickets):
        """
        Calculate business viability score based on bug ticket data.
        
        Logic:
        - Start at 55
        - Add up to 25 points based on fix ratio
        - Add 10 points if at least one ticket is fixed
        - Subtract 10 points if there are open tickets
        - Clamp between 0 and 100
        """
        score = 55

        # Add points based on fix ratio
        if total_tickets > 0:
            fix_ratio = fixed_tickets / total_tickets
            score += int(fix_ratio * 25)

        # Bonus for having at least one fix
        if fixed_tickets > 0:
            score += 10

        # Penalty for open tickets
        if open_tickets > 0:
            score -= 10

        # Clamp between 0 and 100
        score = max(0, min(100, score))

        return score

    def generate_verdict(self, score):
        """Generate verdict text based on score"""
        if score < 50:
            return (
                "Business viability is weak right now. The demo needs clearer target "
                "customers, pricing, and proof that the product solves an urgent problem."
            )
        elif score < 75:
            return (
                "Business viability is promising but not fully investor-ready. BuildCheck AI "
                "shows a useful readiness workflow, but should sharpen customer segmentation, "
                "pricing, and enterprise adoption story."
            )
        else:
            return (
                "Business viability is strong for a hackathon demo. BuildCheck AI connects "
                "code readiness, bug fixing, security signals, and product evaluation into a "
                "clear software readiness command center."
            )

# Made with Bob
