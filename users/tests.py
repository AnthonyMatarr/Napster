from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Locations, Profile
from django.http import JsonResponse, HttpResponseRedirect

def create_location(name):
    """
    Create a location with the given `name`.
    """
    return Locations.objects.create(name=name)

class LocationsTestCase(TestCase):
    def setUp(self):
        # Create an admin user
        self.admin_user = User.objects.create_superuser(
            username="adminuser",
            password="adminpassword"
        )

    def test_user_can_submit_location(self):
        """
        Test that a user can submit a location.
        """
        # Log in a regular user
        self.client.login(username="testuser", password="testpassword")

        # Create a location
        response = self.client.post(reverse("add_location"), {
            "name": "Test Location",
            "rating": 5,
            "description": "Test description",
        })

        self.assertEqual(response.status_code, 200)  # Check for a 200 status code after submission
        self.assertEqual(Locations.objects.count(), 1)  # Check that a location was created

    def test_admin_can_approve_location(self):
        """
        Test that an admin can approve a location.
        """
        # Create a location
        location = create_location(
            name="Test Location"
        )

        # Log in the admin user
        self.client.login(username="adminuser", password="adminpassword")

        # Approve the location
        response = self.client.post(reverse("admin_dashboard"), {
            "location_id": location.id,
            "action": "approve",
        })

        self.assertEqual(response.status_code, 302)  # Check for a redirect after approval
        location.refresh_from_db()  # Refresh the object from the database
        self.assertTrue(location.approved)  # Check that the location is approved

    def test_admin_can_delete_location(self):
        """
        Test that an admin can delete a location.
        """
        # Create a location
        location = create_location(
            name="Test Location"
        )

        # Log in the admin user
        self.client.login(username="adminuser", password="adminpassword")

        # Delete the location
        response = self.client.post(reverse("admin_dashboard"), {
            "location_id": location.id,
            "action": "delete",
        })

        self.assertEqual(response.status_code, 302)  # Check for a redirect after deletion
        self.assertEqual(Locations.objects.count(), 0)  # Check that the location is deleted