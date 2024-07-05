from django.db import models


class Message(models.Model):
    user_name = models.CharField(max_length=25, verbose_name="author")
    email = models.EmailField(max_length=254)
    home_page = models.URLField(max_length=200, blank=True)
    text = models.TextField(max_length=2000)
    raiting = models.SmallIntegerField(default=0)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    reply = models.ForeignKey("self", on_delete=models.CASCADE, blank=True, null=True, related_name="responses")

    class Meta:
        ordering = ('-created', "user_name", "email")
    
    def __str__(self):
        return f"{self.user_name} - {self.created.strftime('%Y-%m-%d %H:%M')} ({self.pk})"
    
    @property
    def is_response(self):
        return self.reply is not None
