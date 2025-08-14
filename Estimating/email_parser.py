import requests
import datetime
import logging
from msal import ConfidentialClientApplication
from django.conf import settings
from django.utils.timezone import make_aware
from .models import TenderList, Customer, TenderListCustomers

# Setup logging
logger = logging.getLogger(__name__)

# Azure App Settings from settings.py
CLIENT_ID = settings.CLIENT_ID
CLIENT_SECRET = settings.CLIENT_SECRET
TENANT_ID = settings.TENANT_ID
USER_EMAIL = 'paulson@paulsonsunny.com.au'

AUTHORITY = f'https://login.microsoftonline.com/{TENANT_ID}'
SCOPE = ['https://graph.microsoft.com/.default']


def get_access_token():
    app = ConfidentialClientApplication(
        CLIENT_ID,
        authority=AUTHORITY,
        client_credential=CLIENT_SECRET,
    )

    result = app.acquire_token_silent(SCOPE, account=None)
    if not result:
        result = app.acquire_token_for_client(scopes=SCOPE)

    if 'access_token' not in result:
        logger.error("Failed to acquire access token: %s", result.get("error_description"))
        return None

    return result['access_token']


def fetch_invitation_emails():
    token = get_access_token()
    if not token:
        logger.error("Access token not available. Aborting fetch.")
        return

    headers = {
        'Authorization': f'Bearer {token}',
        'Prefer': 'outlook.body-content-type="text"',
    }

    endpoint = f'https://graph.microsoft.com/v1.0/users/{USER_EMAIL}/mailFolders/inbox/messages'
    params = {
        '$search': '"Invitation to Tender"',
        '$top': 10,
    }

    response = requests.get(endpoint, headers=headers, params=params)
    if response.status_code != 200:
        logger.error("Failed to fetch emails: %s", response.text)
        return

    for msg in response.json().get('value', []):
        process_email(msg)


def process_email(msg):
    subject = msg.get('subject')
    sender_email = msg.get('from', {}).get('emailAddress', {}).get('address')
    received = msg.get('receivedDateTime')
    body = msg.get('body', {}).get('content')
    email_id = msg.get('id')

    if not subject or 'Invitation to Tender' not in subject:
        return

    project_name = extract_project_name(subject, body)
    builder_name = extract_builder_name(sender_email, body)

    if TenderList.objects.filter(email_id=email_id).exists():
        logger.info(f"Email {email_id} already processed.")
        return

    try:
        customer, _ = Customer.objects.get_or_create(name=builder_name)
        tender = TenderList.objects.create(
            tender_name=project_name,
            tender_received_date=make_aware(datetime.datetime.strptime(received, "%Y-%m-%dT%H:%M:%SZ")),
            tender_due_date=None,
            remarks=None,
            added_by=sender_email,
            email_id=email_id,
            is_quoting=True,         # Explicitly set these
            is_completed=False,
        )
        TenderListCustomers.objects.create(tender=tender, customer=customer)
        mark_email_as_read(email_id)
        logger.info(f"Added new tender: {project_name} from {builder_name}")
    except Exception as e:
        logger.error(f"Failed to process email {email_id}: {str(e)}")


def extract_project_name(subject, body):
    if "Invitation to Tender - " in subject:
        return subject.replace("Invitation to Tender - ", "").strip()
    return subject.strip()


def extract_builder_name(sender_email, body):
    return sender_email.split('@')[0].capitalize()


def mark_email_as_read(email_id):
    token = get_access_token()
    if not token:
        logger.warning("Token missing while marking email as read.")
        return

    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }

    patch_url = f'https://graph.microsoft.com/v1.0/users/{USER_EMAIL}/messages/{email_id}'
    patch_body = {
        "isRead": True
    }

    response = requests.patch(patch_url, headers=headers, json=patch_body)
    if response.status_code != 200:
        logger.warning(f"Failed to mark email as read: {response.status_code} {response.text}")
    else:
        logger.info(f"Marked email {email_id} as read.")
