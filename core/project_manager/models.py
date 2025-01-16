from django.db import models


class Project(models.Model):
    class ProjectType(models.TextChoices):
        TRAINING = "train", "Training"
        DIACRITIZATION = "dicr", "Diacritization"

    name = models.CharField(max_length=200)
    project_type = models.CharField(
        max_length=5, choices=ProjectType.choices, default=ProjectType.DIACRITIZATION
    )
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)


class Document(models.Model):
    project = models.ForeignKey(
        Project, on_delete=models.CASCADE, related_name="documents"
    )
    name = models.CharField(max_length=200)
    file = models.FileField(upload_to="documents/")
    file_size = models.IntegerField(null=True, blank=True)  # Size in KB
    uploaded_at = models.DateTimeField(auto_now_add=True)


class Verse(models.Model):
    class Status(models.TextChoices):
        NEW = "NEW", "New"
        IN_PROGRESS = "IN_PROGRESS", "In Progress"
        COMPLETED = "COMPLETED", "Completed"
        REVIEWED = "REVIEWED", "Reviewed"

    document = models.ForeignKey(
        Document, on_delete=models.CASCADE, related_name="verses"
    )
    content = models.TextField()
    position = models.IntegerField()
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.NEW)
