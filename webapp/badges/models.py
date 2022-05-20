from django.db import models


class Student(models.Model):
    intra_id = models.BigIntegerField(primary_key=True, unique=True)
    login = models.CharField(max_length=255)
    email = models.EmailField()
    displayname = models.CharField(max_length=255)
    image_url = models.URLField()
    is_staff = models.BooleanField(default=False)

    def __str__(self) -> str:
        return self.login


class Badge(models.Model):
    class BadgeType(models.TextChoices):
        PISCINEUX = 'PISCINEUX', 'Piscineux'
        STUDENT = 'STUDENT', 'Student'

    serial = models.IntegerField(unique=True)
    uid = models.CharField(max_length=255, null=True, blank=True)
    reference = models.CharField(max_length=255, null=True, blank=True)
    badge_type = models.CharField(
        max_length=255, choices=BadgeType.choices, default=BadgeType.STUDENT,)
    lost = models.BooleanField(default=False)

    def __str__(self) -> str:
        return str(self.serial)


class StudentBadge(models.Model):
    student = models.ForeignKey(
        Student, on_delete=models.DO_NOTHING, related_name='students_badges')
    badge = models.ForeignKey(
        Badge, on_delete=models.DO_NOTHING, related_name='students_badges')
    start_at = models.DateTimeField()
    end_at = models.DateTimeField(null=True, blank=True)
    caution_paid = models.FloatField(default=0.0)
    caution_returned = models.BooleanField(default=False)

    def __str__(self) -> str:
        return str(self.id)