import os
import django
import logging
from django.core.management.base import BaseCommand
from django.db.models.signals import post_save
from django.dispatch import receiver
from wallet.models import A4C_User, UserProfile  # Ensure this import path is correct
from wallet.views import signup  # Ensure this import path is correct
from django.test import RequestFactory  # To simulate a request

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')
logger = logging.getLogger(__name__)

# Signal receiver to log UserProfile creation
@receiver(post_save, sender=UserProfile)
def log_userprofile_creation(sender, instance, created, **kwargs):
    if created:
        logger.info(f"UserProfile created for User ID: {instance.user.id}, Username: {instance.user.username}, Name: {instance.name}, Country: {instance.country}, Phone: {instance.phone}")

# Function to run the signup and track UserProfile creation
def monitor_signup_and_profile_creation():
    # Simulate a request (adjust this based on your actual signup parameters)
    factory = RequestFactory()
    request = factory.post('/signup/', {
        'username': 'testuser',
        'email': 'testuser@example.com',
        'password': 'password123',
        'name': 'John Doe',
        'country': 'Uganda',
        'phone': '+256700123456'
    })

    # Monitor UserProfile creation before running signup
    logger.info("Running signup(request) function...")

    # Call the signup function
    signup_response = signup(request)

    # Monitor UserProfile creation after running signup
    logger.info("Finished running signup(request) function.")

# Django Management Command Class
class Command(BaseCommand):
    help = 'Monitors signup and tracks UserProfile creation'

    def handle(self, *args, **kwargs):
        try:
            monitor_signup_and_profile_creation()
        except Exception as e:
            logger.error(f"An error occurred: {e}")
