from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.urls import reverse
from django.shortcuts import render, get_object_or_404
import markdown
from django.utils.html import strip_tags

# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '文章分類'
        verbose_name_plural = verbose_name


class Tag(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '文章標籤'
        verbose_name_plural = verbose_name


class Post(models.Model):
    title = models.CharField('標題', max_length=100) # 標題
    body = models.TextField('正文') # 正文
    created_time = models.DateTimeField('創建時間', default=timezone.now) # 創建時間
    modified_time = models.DateTimeField('修改時間') # 最新的修改時間
    excerpt = models.CharField('摘要', max_length=70, blank=True) # 摘要，且允許爲空
    category = models.ForeignKey(Category, verbose_name='分類', on_delete=models.CASCADE) # 分類
    tags = models.ManyToManyField(Tag, verbose_name='標籤', blank=True) # 標籤
    # 分類只能有一個，而標籤可以有很多個，所以非類是一對一的，而標籤是一對多的
    author = models.ForeignKey(User, verbose_name='作者', on_delete=models.CASCADE) # 作者（一對一）
    views = models.PositiveIntegerField(default=0)

    def increase_views(self):
        self.views += 1
        self.save(update_fields=['views'])

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = '文章'
        verbose_name_plural = verbose_name
        ordering = ['-created_time']

    def save(self, *args, **kwargs):
        self.modified_time = timezone.now()

        # 首先实例化一个 Markdown 类，用于渲染 body 的文本。
        # 由于摘要并不需要生成文章目录，所以去掉了目录拓展。
        md = markdown.Markdown(extensions=[
            'markdown.extensions.extra',
            'markdown.extensions.codehilite',
        ])

        # 先将 Markdown 文本渲染成 HTML 文本
        # strip_tags 去掉 HTML 文本的全部 HTML 标签
        # 从文本摘取前 54 个字符赋给 excerpt
        self.excerpt = strip_tags(md.convert(self.body))[:54]

        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('blog:detail', kwargs={'pk': self.pk})
