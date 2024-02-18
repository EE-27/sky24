from datetime import timedelta
from django.utils import timezone
today = timezone.now()
thirty_days_ago = today - timedelta(days=30)

print(today)
print(thirty_days_ago)