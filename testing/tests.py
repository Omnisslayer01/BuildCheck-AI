from django.test import TestCase, Client
from django.urls import reverse
import json
from .models import BugTicket, BusinessEvaluation


class BusinessLensAPITestCase(TestCase):
    """Tests for the Business Lens API endpoint"""

    def setUp(self):
        self.client = Client()
        self.url = reverse('api_business_lens')

    def test_api_business_lens_creates_evaluation_with_valid_json(self):
        """Test that api_business_lens creates a BusinessEvaluation with valid JSON"""
        data = {
            'score': 85,
            'verdict': 'Good business potential'
        }
        response = self.client.post(
            self.url,
            data=json.dumps(data),
            content_type='application/json'
        )
        
        self.assertEqual(response.status_code, 200)
        response_data = response.json()
        self.assertTrue(response_data['success'])
        self.assertEqual(response_data['evaluation']['score'], 85)
        self.assertEqual(response_data['evaluation']['verdict'], 'Good business potential')
        
        # Verify it was saved to database
        self.assertEqual(BusinessEvaluation.objects.count(), 1)
        evaluation = BusinessEvaluation.objects.first()
        self.assertEqual(evaluation.score, 85)
        self.assertEqual(evaluation.verdict, 'Good business potential')

    def test_api_business_lens_rejects_score_above_100(self):
        """Test that api_business_lens rejects score above 100"""
        data = {
            'score': 150,
            'verdict': 'Too high'
        }
        response = self.client.post(
            self.url,
            data=json.dumps(data),
            content_type='application/json'
        )
        
        self.assertEqual(response.status_code, 400)
        response_data = response.json()
        self.assertFalse(response_data['success'])
        self.assertIn('between 0 and 100', response_data['error'])
        
        # Verify nothing was saved
        self.assertEqual(BusinessEvaluation.objects.count(), 0)

    def test_api_business_lens_rejects_score_below_0(self):
        """Test that api_business_lens rejects score below 0"""
        data = {
            'score': -10,
            'verdict': 'Negative score'
        }
        response = self.client.post(
            self.url,
            data=json.dumps(data),
            content_type='application/json'
        )
        
        self.assertEqual(response.status_code, 400)
        response_data = response.json()
        self.assertFalse(response_data['success'])
        self.assertIn('between 0 and 100', response_data['error'])

    def test_api_business_lens_rejects_missing_verdict(self):
        """Test that api_business_lens rejects missing verdict"""
        data = {
            'score': 75
        }
        response = self.client.post(
            self.url,
            data=json.dumps(data),
            content_type='application/json'
        )
        
        self.assertEqual(response.status_code, 400)
        response_data = response.json()
        self.assertFalse(response_data['success'])
        self.assertIn('verdict', response_data['error'].lower())

    def test_api_business_lens_rejects_empty_verdict(self):
        """Test that api_business_lens rejects empty verdict"""
        data = {
            'score': 75,
            'verdict': '   '
        }
        response = self.client.post(
            self.url,
            data=json.dumps(data),
            content_type='application/json'
        )
        
        self.assertEqual(response.status_code, 400)
        response_data = response.json()
        self.assertFalse(response_data['success'])

    def test_api_business_lens_rejects_missing_score(self):
        """Test that api_business_lens rejects missing score"""
        data = {
            'verdict': 'No score provided'
        }
        response = self.client.post(
            self.url,
            data=json.dumps(data),
            content_type='application/json'
        )
        
        self.assertEqual(response.status_code, 400)
        response_data = response.json()
        self.assertFalse(response_data['success'])
        self.assertIn('score', response_data['error'].lower())

    def test_api_business_lens_converts_score_to_int(self):
        """Test that api_business_lens converts string score to int"""
        data = {
            'score': '90',
            'verdict': 'String score'
        }
        response = self.client.post(
            self.url,
            data=json.dumps(data),
            content_type='application/json'
        )
        
        self.assertEqual(response.status_code, 200)
        response_data = response.json()
        self.assertTrue(response_data['success'])
        self.assertEqual(response_data['evaluation']['score'], 90)


class DashboardTestCase(TestCase):
    """Tests for the dashboard views"""

    def setUp(self):
        self.client = Client()

    def test_dashboard_renders_when_business_evaluation_exists(self):
        """Test that dashboard renders successfully when a BusinessEvaluation exists"""
        # Create a business evaluation
        BusinessEvaluation.objects.create(
            score=88,
            verdict='Strong business case'
        )
        
        response = self.client.get(reverse('dashboard_home'))
        
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'BuildCheck AI')
        self.assertContains(response, 'Business Lens')

    def test_dashboard_renders_when_no_business_evaluation_exists(self):
        """Test that dashboard renders successfully when no BusinessEvaluation exists"""
        response = self.client.get(reverse('dashboard_home'))
        
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'BuildCheck AI')

    def test_business_lens_html_endpoint_renders_successfully(self):
        """Test that /api/business-lens-html/ renders successfully"""
        # Create a business evaluation
        BusinessEvaluation.objects.create(
            score=75,
            verdict='Promising demo'
        )
        
        response = self.client.get(reverse('business_lens_partial'))
        
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Business Lens')
        self.assertContains(response, '75')
        self.assertContains(response, 'Promising demo')

    def test_business_lens_html_endpoint_shows_fallback_when_no_data(self):
        """Test that /api/business-lens-html/ shows fallback when no data exists"""
        response = self.client.get(reverse('business_lens_partial'))
        
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Business Lens')
        self.assertContains(response, '62')
        self.assertContains(response, 'BuildCheck AI has a strong technical demo')


class LatestBusinessEvaluationTestCase(TestCase):
    """Tests to ensure latest BusinessEvaluation is used, not oldest"""

    def test_latest_business_evaluation_is_used_not_oldest(self):
        """Test that dashboard uses the newest evaluation, not the oldest"""
        # Create multiple evaluations
        old_eval = BusinessEvaluation.objects.create(
            score=50,
            verdict='Old evaluation'
        )
        
        # Wait a moment to ensure different timestamps
        import time
        time.sleep(0.1)
        
        new_eval = BusinessEvaluation.objects.create(
            score=90,
            verdict='New evaluation'
        )
        
        # Get dashboard
        response = self.client.get(reverse('dashboard_home'))
        
        # Should show the new evaluation, not the old one
        self.assertContains(response, '90')
        self.assertContains(response, 'New evaluation')
        self.assertNotContains(response, 'Old evaluation')

    def test_business_lens_partial_uses_latest_evaluation(self):
        """Test that business_lens_partial uses the newest evaluation"""
        # Create multiple evaluations
        BusinessEvaluation.objects.create(
            score=40,
            verdict='First evaluation'
        )
        
        import time
        time.sleep(0.1)
        
        BusinessEvaluation.objects.create(
            score=95,
            verdict='Latest evaluation'
        )
        
        # Get partial
        response = self.client.get(reverse('business_lens_partial'))
        
        # Should show the latest evaluation
        self.assertContains(response, '95')
        self.assertContains(response, 'Latest evaluation')
        self.assertNotContains(response, 'First evaluation')


class BugTicketIntegrationTestCase(TestCase):
    """Tests to ensure BugTicket functionality is not broken"""

    def test_bug_ticket_model_still_works(self):
        """Test that BugTicket model still functions correctly"""
        ticket = BugTicket.objects.create(
            title='Test Bug',
            bug_description='This is a test bug',
            status='analyzing'
        )
        
        self.assertEqual(ticket.title, 'Test Bug')
        self.assertEqual(ticket.status, 'analyzing')

    def test_update_bug_status_api_still_works(self):
        """Test that /api/update-status/ still works"""
        ticket = BugTicket.objects.create(
            title='Test Bug',
            bug_description='Test',
            status='analyzing'
        )
        
        response = self.client.post(
            reverse('update_bug_status'),
            data=json.dumps({
                'ticket_id': ticket.id,
                'status': 'fixed'
            }),
            content_type='application/json'
        )
        
        self.assertEqual(response.status_code, 200)
        response_data = response.json()
        self.assertTrue(response_data['success'])
        
        # Verify status was updated
        ticket.refresh_from_db()
        self.assertEqual(ticket.status, 'fixed')

    def test_bug_list_html_endpoint_still_works(self):
        """Test that /api/bug-list-html/ still works"""
        BugTicket.objects.create(
            title='Test Bug 1',
            bug_description='Test',
            status='analyzing'
        )
        
        response = self.client.get(reverse('bug_list_partial'))
        
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Bug 1')

# Made with Bob
