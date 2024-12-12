from django.test import TestCase, Client
from django.urls import reverse
from .models import Poll

class PollsViewsTestCase(TestCase):

    def setUp(self):
        # Create some sample data for testing
        self.poll = Poll.objects.create(
            question="Sample Question?",
            option_one="Option 1",
            option_two="Option 2",
            option_three="Option 3"
        )
        self.client = Client()

    def test_home_view(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'poll/home.html')
        self.assertContains(response, 'Sample Question?')

    def test_create_view_get(self):
        response = self.client.get(reverse('create'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'poll/create.html')
    
    def test_create_view_post(self):
        response = self.client.post(reverse('create'), {
            'question': 'New Question?',
            'option_one': 'Option 1',
            'option_two': 'Option 2',
            'option_three': 'Option 3'
        })
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('home'))
        self.assertEqual(Poll.objects.count(), 2)

    def test_vote_view_post(self):
        response = self.client.post(reverse('vote', args=[self.poll.id]), {
            'poll': 'option1'
        })
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('results', args=[self.poll.id]))
        self.poll.refresh_from_db()
        self.assertEqual(self.poll.option_one_count, 1)

    def test_results_view(self):
        response = self.client.get(reverse('results', args=[self.poll.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'poll/results.html')
        self.assertContains(response, 'Sample Question?')
