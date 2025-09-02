from django.db import models

class Report(models.Model):
    REPORT_TYPES = [
        ("sales", "Sales Report"),
        ("purchase", "Purchase Report"),
        ("inventory", "Inventory Report"),
    ]
    name = models.CharField(max_length=100)
    report_type = models.CharField(max_length=20, choices=REPORT_TYPES)
    generated_on = models.DateTimeField(auto_now_add=True)
    file = models.FileField(upload_to="reports/", blank=True, null=True)

    def __str__(self):
        return f"{self.name} ({self.get_report_type_display()})"
