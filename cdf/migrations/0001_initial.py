# Generated by Django 2.0.7 on 2018-12-07 07:35

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import djgeojson.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Boundary',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('objectid_1', models.BigIntegerField()),
                ('objectid', models.FloatField()),
                ('province', models.CharField(max_length=50)),
                ('const_nam', models.CharField(max_length=50)),
                ('elec_area_field', models.CharField(max_length=50)),
                ('local_auth', models.CharField(max_length=50)),
                ('st_area_sh', models.FloatField()),
                ('st_length_field', models.FloatField()),
                ('const_no', models.FloatField()),
                ('county_nam', models.CharField(max_length=50)),
                ('county_no', models.FloatField()),
                ('st_length1', models.FloatField()),
                ('votes', models.BigIntegerField()),
                ('st_lengt_1', models.FloatField()),
                ('globalid', models.CharField(max_length=38)),
                ('shape_leng', models.FloatField()),
                ('shape_area', models.FloatField()),
                ('geom', djgeojson.fields.MultiPolygonField()),
            ],
        ),
        migrations.CreateModel(
            name='CdfProjects',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('project', models.CharField(max_length=254)),
                ('descrition', models.CharField(max_length=254)),
                ('remarks', models.CharField(max_length=254)),
                ('sectors', models.CharField(max_length=254)),
                ('amount', models.BigIntegerField()),
                ('status', models.CharField(choices=[('Complete', 'Complete'), ('Incomplete', 'Incomplete'), ('Onprogress', 'Onprogress'), ('Stopped', 'Stopped')], max_length=254)),
                ('lat', models.FloatField()),
                ('county_nam', models.CharField(max_length=50)),
                ('location', models.CharField(max_length=100)),
                ('lon', models.FloatField()),
                ('geom', djgeojson.fields.MultiPointField()),
            ],
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('author', models.CharField(max_length=200)),
                ('text', models.TextField()),
                ('created_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('approved_comment', models.BooleanField(default=False)),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='cdf.CdfProjects')),
            ],
            options={
                'ordering': ['-created_date'],
            },
        ),
        migrations.CreateModel(
            name='Events',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=150)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('description', models.TextField()),
                ('mdate', models.DateField()),
                ('mtime', models.TimeField()),
                ('venue', models.CharField(max_length=200)),
            ],
            options={
                'verbose_name_plural': 'Events',
                'ordering': ['-created'],
            },
        ),
        migrations.CreateModel(
            name='FroudReports',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=150)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('photo', models.ImageField(blank=True, upload_to='reportmedia/%y/%m/%d')),
                ('description', models.TextField()),
                ('geom', djgeojson.fields.PointField()),
            ],
            options={
                'verbose_name_plural': 'FroudReports',
                'ordering': ['-created'],
            },
        ),
        migrations.CreateModel(
            name='Report',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(blank=True, upload_to='reportImages/%y/%m/%d')),
                ('description', models.TextField()),
                ('geom', djgeojson.fields.PointField()),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('opinion', models.CharField(choices=[('Comment', 'Comment'), ('Complain', 'Complain')], max_length=200)),
                ('modified', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name_plural': 'Reports',
                'ordering': ['-created'],
            },
        ),
        migrations.CreateModel(
            name='SecurityEvent',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('description', models.TextField()),
                ('mdate', models.DateField()),
                ('mtime', models.TimeField()),
                ('geom', djgeojson.fields.PointField()),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name_plural': 'SecurityEvent',
                'ordering': ['-created'],
            },
        ),
        migrations.CreateModel(
            name='Suggestions',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('suggestion', models.CharField(choices=[('Comment', 'Comment'), ('Complain', 'Complain')], max_length=200)),
                ('body', models.TextField()),
                ('status', models.CharField(choices=[('Complete', 'Complete'), ('Incomplete', 'Incomplete'), ('Onprogress', 'Onprogress'), ('Stopped', 'Stopped')], max_length=200)),
                ('name', models.CharField(max_length=300)),
                ('email', models.EmailField(max_length=254)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name_plural': 'Suggestions',
                'ordering': ['-created'],
            },
        ),
    ]
