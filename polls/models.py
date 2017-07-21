# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import datetime
import os
import random
import string

from django.db import models
from django.utils.timezone import now as timezone_now

# Create your models here.


class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')

    def was_published_recently(self):
    	return self.pub_date >= timezone.now() - datetime.timedelta(days=1)

    def __str__(self):
    	return self.question_text


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)
    
    def __str__(self):
    	return self.choice_text


def create_random_string(length=30):
    if length <= 0:
        length = 30

    symbols = string.ascii_lowercase + string.ascii_uppercase + string.digits
    return ''.join([random.choice(symbols) for x in range(length)])


def upload_to(instance, filename):
    now = timezone_now()
    filename_base, filename_ext = os.path.splitext(filename)
    return 'images/{}_{}{}'.format(
        now.strftime("%Y/%m/%d/%Y%m%d%H%M%S"),
        create_random_string(),
        filename_ext.lower()
    )

class CSVFile(models.Model):
    name_of = models.CharField(max_length=20, blank = False)


class SubFile(models.Model):
    pid = models.ForeignKey(CSVFile)
    my_file = models.FileField(upload_to=upload_to)
    description = models.CharField(max_length=200, blank = True)
    uploaded_at = models.DateTimeField(auto_now_add=True)