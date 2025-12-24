"""
Contacts and Email Templates Tool
Manages contacts database and email templates for quick access.
"""

import json
from pathlib import Path
from typing import Dict, List, Optional, Any
from config.settings import settings

CONTACTS_FILE = settings.data_dir / 'contacts.json'

def load_contacts_data() -> Dict[str, Any]:
    """Load contacts and templates from JSON file."""
    if CONTACTS_FILE.exists():
        try:
            with open(CONTACTS_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"Error loading contacts: {e}")
    
    return {"contacts": {}, "email_templates": {}}

def find_contact(name_or_role: str) -> Dict[str, Any]:
    """
    Find contact by name or role.
    
    Args:
        name_or_role: Contact name, role, or identifier
        
    Returns:
        Contact information or error
    """
    data = load_contacts_data()
    contacts = data.get('contacts', {})
    
    name_or_role = name_or_role.lower().strip()
    
    # Direct key match
    if name_or_role in contacts:
        contact = contacts[name_or_role]
        return {
            'success': True,
            'contact': contact,
            'identifier': name_or_role,
            'message': f"Found contact: {contact['name']} ({contact['role']})"
        }
    
    # Search by role
    for key, contact in contacts.items():
        if contact.get('role', '').lower() == name_or_role:
            return {
                'success': True,
                'contact': contact,
                'identifier': key,
                'message': f"Found contact: {contact['name']} ({contact['role']})"
            }
    
    # Search by name (partial match)
    for key, contact in contacts.items():
        if name_or_role in contact.get('name', '').lower():
            return {
                'success': True,
                'contact': contact,
                'identifier': key,
                'message': f"Found contact: {contact['name']} ({contact['role']})"
            }
    
    return {
        'success': False,
        'message': f"Contact '{name_or_role}' not found. Available contacts: {', '.join(contacts.keys())}"
    }

def get_email_template(template_name: str) -> Dict[str, Any]:
    """
    Get email template by name.
    
    Args:
        template_name: Template identifier
        
    Returns:
        Template information or error
    """
    data = load_contacts_data()
    templates = data.get('email_templates', {})
    
    template_name = template_name.lower().replace(' ', '_')
    
    if template_name in templates:
        return {
            'success': True,
            'template': templates[template_name],
            'name': template_name,
            'message': f"Found template: {template_name}"
        }
    
    # Partial match
    for key, template in templates.items():
        if template_name in key:
            return {
                'success': True,
                'template': template,
                'name': key,
                'message': f"Found template: {key}"
            }
    
    return {
        'success': False,
        'message': f"Template '{template_name}' not found. Available: {', '.join(templates.keys())}"
    }

def list_contacts() -> Dict[str, Any]:
    """List all available contacts."""
    data = load_contacts_data()
    contacts = data.get('contacts', {})
    
    contact_list = []
    for key, contact in contacts.items():
        contact_list.append({
            'identifier': key,
            'name': contact.get('name', ''),
            'role': contact.get('role', ''),
            'email': contact.get('email', ''),
            'whatsapp': contact.get('whatsapp', '')
        })
    
    return {
        'success': True,
        'contacts': contact_list,
        'count': len(contact_list),
        'message': f"Found {len(contact_list)} contacts"
    }

def list_email_templates() -> Dict[str, Any]:
    """List all available email templates."""
    data = load_contacts_data()
    templates = data.get('email_templates', {})
    
    template_list = []
    for key, template in templates.items():
        template_list.append({
            'name': key,
            'subject': template.get('subject', ''),
            'description': f"Template for {key.replace('_', ' ')}"
        })
    
    return {
        'success': True,
        'templates': template_list,
        'count': len(template_list),
        'message': f"Found {len(template_list)} email templates"
    }

def prepare_email_with_template(recipient: str, template_name: str, **kwargs) -> Dict[str, Any]:
    """
    Prepare an email using a template and contact information.
    
    Args:
        recipient: Contact name/role to send to
        template_name: Email template to use
        **kwargs: Template variables (dates, reason, etc.)
        
    Returns:
        Prepared email details
    """
    # Find recipient contact
    contact_result = find_contact(recipient)
    if not contact_result['success']:
        return contact_result
    
    contact = contact_result['contact']
    
    # Get email template
    template_result = get_email_template(template_name)
    if not template_result['success']:
        return template_result
    
    template = template_result['template']
    
    # Prepare template variables
    template_vars = {
        'recipient_name': contact.get('name', recipient),
        'sender_name': kwargs.get('sender_name', 'Your Name'),
        **kwargs
    }
    
    # Fill template
    try:
        subject = template['subject'].format(**template_vars)
        body = template['body'].format(**template_vars)
        
        return {
            'success': True,
            'email_details': {
                'to': contact.get('email', ''),
                'subject': subject,
                'body': body,
                'recipient_name': contact.get('name', ''),
                'template_used': template_result['name']
            },
            'message': f"Email prepared for {contact['name']} using {template_result['name']} template"
        }
        
    except KeyError as e:
        return {
            'success': False,
            'message': f"Missing template variable: {e}. Available variables: {list(template_vars.keys())}"
        }

def smart_email_lookup(query: str) -> Dict[str, Any]:
    """
    Smart lookup for email preparation based on natural language.
    
    Args:
        query: Natural language query like "send leave letter to manager"
        
    Returns:
        Suggested email preparation
    """
    query_lower = query.lower()
    
    # Detect template type
    template_mapping = {
        'leave': 'leave_request',
        'sick': 'sick_leave', 
        'meeting': 'meeting_request',
        'follow up': 'follow_up',
        'followup': 'follow_up'
    }
    
    detected_template = None
    for keyword, template in template_mapping.items():
        if keyword in query_lower:
            detected_template = template
            break
    
    # Detect recipient
    data = load_contacts_data()
    contacts = data.get('contacts', {})
    
    detected_recipient = None
    for key, contact in contacts.items():
        if key in query_lower or contact.get('role', '').lower() in query_lower:
            detected_recipient = key
            break
    
    if detected_template and detected_recipient:
        return {
            'success': True,
            'suggestion': {
                'recipient': detected_recipient,
                'template': detected_template,
                'query': query
            },
            'message': f"Detected: {detected_template} template for {detected_recipient}"
        }
    
    return {
        'success': False,
        'message': f"Could not parse email request: '{query}'. Try 'send [template] to [recipient]'",
        'available_templates': list(template_mapping.values()),
        'available_recipients': list(contacts.keys())
    }