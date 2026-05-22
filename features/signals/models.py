from django.db import models
from config.constants import SIGNAL_STATUSES, SIGNAL_STATUS_NEW

class Signal(models.Model):
    """
    Signal representation in the database.
    Tracks marketing, intent, or transaction signals.
    """
    title = models.CharField(max_length=255, help_text="Short description or title of the signal")
    source = models.CharField(max_length=100, help_text="Origin of the signal (e.g. EMAIL, LINKEDIN, SCRAPE)")
    score = models.IntegerField(default=50, help_text="Priority or confidence score between 0 and 100")
    payload = models.JSONField(default=dict, blank=True, help_text="Dynamic metadata properties associated with the signal event")
    status = models.CharField(
        max_length=50,
        choices=SIGNAL_STATUSES,
        default=SIGNAL_STATUS_NEW,
        help_text="Processing stage of the signal"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "signals"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.title} ({self.source}) - {self.status}"
