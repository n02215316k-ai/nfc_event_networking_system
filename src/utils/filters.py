from datetime import datetime
try:
    from markupsafe import Markup
except ImportError:
    from flask import Markup
import re

def register_filters(app):
    """Register custom template filters"""
    
    @app.template_filter('datetime_format')
    def datetime_format(value, format='%Y-%m-%d %H:%M:%S'):
        """Format a datetime object"""
        if value is None:
            return ''
        if isinstance(value, str):
            try:
                value = datetime.strptime(value, '%Y-%m-%d %H:%M:%S')
            except:
                return value
        return value.strftime(format)
    
    @app.template_filter('timeago')
    def timeago(value):
        """Convert datetime to 'time ago' format"""
        if value is None:
            return ''
        
        if isinstance(value, str):
            try:
                value = datetime.strptime(value, '%Y-%m-%d %H:%M:%S')
            except:
                return value
        
        now = datetime.now()
        diff = now - value
        
        seconds = diff.total_seconds()
        
        if seconds < 60:
            return 'just now'
        elif seconds < 3600:
            minutes = int(seconds / 60)
            return f'{minutes} minute{"s" if minutes != 1 else ""} ago'
        elif seconds < 86400:
            hours = int(seconds / 3600)
            return f'{hours} hour{"s" if hours != 1 else ""} ago'
        elif seconds < 604800:
            days = int(seconds / 86400)
            return f'{days} day{"s" if days != 1 else ""} ago'
        elif seconds < 2592000:
            weeks = int(seconds / 604800)
            return f'{weeks} week{"s" if weeks != 1 else ""} ago'
        elif seconds < 31536000:
            months = int(seconds / 2592000)
            return f'{months} month{"s" if months != 1 else ""} ago'
        else:
            years = int(seconds / 31536000)
            return f'{years} year{"s" if years != 1 else ""} ago'
    
    @app.template_filter('truncate_words')
    def truncate_words(value, length=50):
        """Truncate text to specified number of words"""
        if not value:
            return ''
        
        words = value.split()
        if len(words) <= length:
            return value
        
        return ' '.join(words[:length]) + '...'
    
    @app.template_filter('nl2br')
    def nl2br(value):
        """Convert newlines to <br> tags"""
        if not value:
            return ''
        return Markup(value.replace('\n', '<br>'))
    
    @app.template_filter('format_number')
    def format_number(value):
        """Format number with commas"""
        if value is None:
            return '0'
        try:
            return '{:,}'.format(int(value))
        except:
            return value
    
    @app.template_filter('pluralize')
    def pluralize(count, singular='', plural='s'):
        """Add plural suffix based on count"""
        if count == 1:
            return singular
        return plural
    
    @app.template_filter('filesize')
    def filesize(bytes):
        """Convert bytes to human readable file size"""
        if bytes is None:
            return '0 B'
        
        bytes = float(bytes)
        kb = bytes / 1024
        
        if kb < 1024:
            return f'{kb:.2f} KB'
        
        mb = kb / 1024
        if mb < 1024:
            return f'{mb:.2f} MB'
        
        gb = mb / 1024
        return f'{gb:.2f} GB'
    
    @app.template_filter('status_badge')
    def status_badge(status):
        """Convert status to Bootstrap badge class"""
        status_map = {
            'active': 'success',
            'pending': 'warning',
            'inactive': 'secondary',
            'published': 'success',
            'draft': 'secondary',
            'cancelled': 'danger',
            'completed': 'info',
            'verified': 'success',
            'rejected': 'danger',
            'checked_in': 'success',
            'checked_out': 'info',
            'registered': 'primary'
        }
        return status_map.get(status.lower(), 'secondary')