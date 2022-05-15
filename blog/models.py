from django.db import models
import os

# Create your models here.
class Post(models.Model):
    title = models.CharField(max_length=30)
    hook_text = models.CharField(max_length=100, blank=True)
    content = models.TextField()

    header_image = models.ImageField(upload_to='blog/images/%Y/%m/%d/', blank=True)
    file_attachment = models.FileField(upload_to='blog/files/%Y/%m/%d/', blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'[{self.pk}]{self.title}'

    def get_absolute_url(self):
        return f'/blog/{self.pk}/'

    def get_filename(self):
        return os.path.basename(self.file_attachment.name)
    
    def get_fileext(self):
        return self.get_filename().split('.')[-1]
