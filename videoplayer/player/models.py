from django.db import models
from django.db.models.signals import pre_save
from django.utils.text import slugify
from markdown_deux import markdown
from django.utils.safestring import mark_safe

# Create your models here.
class Post(models.Model):
    title = models.CharField(max_length=120)
    slug = models.SlugField(unique=True)
    content = models.TextField()
    video_url = models.URLField(max_length = 200, blank= True, null= True)
    image_url = models.URLField(max_length = 200, blank= True, null= True)
    publish = models.DateField(auto_now=False, auto_now_add=False)
    
    def get_markdown(self):
        content = self.content
        markdown_text = markdown(content)  
        return mark_safe(markdown_text)
    
    def __str__(self):
        return self.title
    
def create_slug(instance, new_slug=None):
    slug = slugify(instance.title)
    if new_slug is not None:
        slug = new_slug
    qs = Post.objects.filter(slug=slug).order_by("-id")
    exists = qs.exists()
    if exists:
        new_slug = "%s-%s" %(slug, qs.first().id)
        return create_slug(instance, new_slug = new_slug)
    return slug
    
def pre_save_post_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug= create_slug(instance)
    if instance.content:
        html_string = instance.get_markdown()

pre_save.connect(pre_save_post_receiver, sender=Post)