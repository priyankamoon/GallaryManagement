from django.db import models

# Create your models here.

class GallaryImages(models.Model):
    file = models.FileField(upload_to="",null=True, db_column="FILE")
    is_active = models.BooleanField(db_column='IS_ACTIVE',
                                    default=True)  # Field name made lowercase.
    is_deleted = models.BooleanField(db_column='IS_DELETED',
                                     default=False)  # Field name made lowercase.
    created_date = models.DateTimeField(db_column='CREATED_DATE',
                                        auto_now_add=True,null=True,blank=True )  # Field name made lowercase.
    last_updated_date = models.DateTimeField(db_column='LAST_UPDATED_DATE', auto_now=True,null=True,blank=True)  # Field name made lowercase.

    class Meta(object):
        db_table = 'GallaryImages'
        app_label = 'GallaryApp'

    def __str__(self):
        return str(self.id)