from django.db import models
from config.constants import DEAL_STAGES, DEAL_STAGE_PROSPECTING

class Deal(models.Model):
    """
    Deal representation in the database.
    Tracks active sales cycles, financial metrics, and sales stages.
    """
    name = models.CharField(max_length=255, help_text="Name of the deal opportunity")
    value = models.DecimalField(
        max_digits=15, 
        decimal_places=2, 
        default=0.00,
        help_text="Financial valuation size of the deal"
    )
    stage = models.CharField(
        max_length=50,
        choices=DEAL_STAGES,
        default=DEAL_STAGE_PROSPECTING,
        help_text="Sales pipeline stage of the deal"
    )
    probability = models.IntegerField(
        default=10, 
        help_text="Win probability percentage ranging from 0 to 100"
    )
    close_date = models.DateField(
        null=True, 
        blank=True, 
        help_text="Expected final closing target date"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "deals"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.name} (${self.value}) - {self.stage}"
