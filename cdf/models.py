# from django.db import models
from django.contrib.gis.db import models
from django.utils import timezone
from djgeojson.fields import PolygonField,PointField,MultiPolygonField,MultiPointField
status=(
		('Complete','Complete'),
		('Incomplete','Incomplete'),
		('Onprogress','Onprogress'),
		('Stopped','Stopped')
		)
suggest = (
	('Comment','Comment'),
	('Complain','Complain')
	)
class BaseContent(models.Model):
	title = models.CharField(max_length=150)
	created = models.DateTimeField(auto_now_add=True)
	modified = models.DateTimeField(auto_now=True)

	class Meta:
		abstract = True


class FroudReports(BaseContent):
	photo = models.ImageField(upload_to='reportmedia/%y/%m/%d',blank=True)
	description = models.TextField()
	geom = PointField()

	def __str__(self):
		return self.title

	class Meta:
		verbose_name_plural = 'FroudReports'
		ordering = ['-created']

class Suggestions(models.Model):
	suggestion = models.CharField(max_length=200,choices=suggest)
	body = models.TextField()
	status = models.CharField(max_length=200,choices=status)
	name = models.CharField(max_length=300)
	email = models.EmailField()
	created = models.DateTimeField(auto_now_add=True)
	modified = models.DateTimeField(auto_now=True)

	def __str__(self):
		return self.suggestion

	class Meta:
		verbose_name_plural = 'Suggestions'
		ordering = ['-created']


class Events(BaseContent):
	description = models.TextField()
	mdate = models.DateField()
	mtime = models.TimeField()
	venue = models.CharField(max_length=200)

	def __str__(self):
		return self.title

	class Meta:
		verbose_name_plural = 'Events'
		ordering = ['-created']
class CdfProjects(models.Model): 
	project = models.CharField(max_length=254)
	descrition = models.CharField(max_length=254)
	remarks = models.CharField(max_length=254)
	sectors = models.CharField(max_length=254)
	amount = models.BigIntegerField()
	status = models.CharField(max_length=254,choices=status)
	lat = models.FloatField()
	county_nam = models.CharField(max_length=50)
	location = models.CharField(max_length=100)
	lon = models.FloatField()
	geom = MultiPointField()

	def __str__(self):
		return self.project

	def approved_comments(self):
		return self.comments.filter(approved_comment=True)

class Boundary(models.Model):
    objectid_1 = models.BigIntegerField()
    objectid = models.FloatField()
    province = models.CharField(max_length=50)
    const_nam = models.CharField(max_length=50)
    elec_area_field = models.CharField(max_length=50)
    local_auth = models.CharField(max_length=50)
    st_area_sh = models.FloatField()
    st_length_field = models.FloatField()
    const_no = models.FloatField()
    county_nam = models.CharField(max_length=50)
    county_no = models.FloatField()
    st_length1 = models.FloatField()
    votes = models.BigIntegerField()
    st_lengt_1 = models.FloatField()
    globalid = models.CharField(max_length=38)
    shape_leng = models.FloatField()
    shape_area = models.FloatField()
    geom = MultiPolygonField()



# Comments on CdfProjects
class Comment(models.Model):
    post = models.ForeignKey('CdfProjects', on_delete=models.CASCADE, related_name='comments')
    author = models.CharField(max_length=200)
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    approved_comment = models.BooleanField(default=False)

    def approve(self):
        self.approved_comment = True
        self.save()

    def __str__(self):
        return self.text

    class Meta:
    	ordering = ['-created_date']

class Report(models.Model):
	image = models.ImageField(upload_to='reportImages/%y/%m/%d',blank=True)
	description = models.TextField()
	geom = PointField()
	created = models.DateTimeField(auto_now_add=True)
	opinion = models.CharField(max_length=200,choices=suggest)
	modified = models.DateTimeField(auto_now=True)

	@property
	def image_url(self):
		return self.image.url


	class Meta:
		verbose_name_plural = 'Reports'
		ordering = ['-created']

	def __str__(self):
		return self.description

class SecurityEvent(models.Model):
	title = models.CharField(max_length=200)
	description = models.TextField()
	mdate = models.DateField()
	mtime = models.TimeField()
	geom = PointField()
	created = models.DateTimeField(auto_now_add=True)
	modified = models.DateTimeField(auto_now=True)

	class Meta:
		verbose_name_plural = 'SecurityEvent'
		ordering = ['-created']

	def __str__(self):
		return self.title
