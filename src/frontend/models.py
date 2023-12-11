from django.db import models
from django.core.validators import FileExtensionValidator, MaxValueValidator
from django.urls import reverse

from ckeditor.fields import RichTextField

import random



# Create your mod9(els here.
class AuditFields(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class NewsLetterModel(AuditFields):
    email = models.EmailField(max_length=254, null=True, blank=True)

    def __str__(self):
        return self.email
    
    class Meta:
        verbose_name_plural = "NewsLEtter Lists"
    

# class ContactUsModel(AuditFields):

class PeeksModel(AuditFields):
    name = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return self.name
    


class Region(AuditFields):
    name = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return self.name
    
from PIL import Image
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile
import sys

class PeeksLists(AuditFields):
    choices = (
        ("expedition", "expedition"),
        ("treks" ,"treks"),
        ("hiking" ,"hiking"),
        ("peek_climbing" ,"peek_climbing"),
        ("tours" ,"tours"),
        ("sightseeing" ,"sightseeing"),
    )

    peeks_catg = models.ForeignKey(PeeksModel, verbose_name=("Peeks Lists"), on_delete=models.CASCADE, null=True, blank=True)
    region_peak = models.ForeignKey(Region, verbose_name=("Peeks Region"), on_delete=models.SET_NULL, null=True, blank=True)
    peek_type = models.CharField(choices=choices, max_length=50, null=True, blank=True)
    name = models.CharField(max_length=150)
    thumbnail = models.FileField(upload_to="thumbnail", 
        validators=[FileExtensionValidator(allowed_extensions=["jpg","png", "jpeg"])], null=True)

    main_iamge = models.FileField(upload_to="main_image", 
        validators=[FileExtensionValidator(allowed_extensions=["jpg","png", "jpeg"])], null=True)
    rating = models.DecimalField(max_digits=5, decimal_places=1)
    rate_total = models.IntegerField(default=0)
    overview = RichTextField(null=True, blank=True)
    duration = models.IntegerField(default=0)
    highest_elevation = models.CharField(max_length=150)
    accomodation = models.CharField(max_length=150)
    season = models.CharField(max_length=150)
    age = models.IntegerField(default=0)
    location = models.CharField(max_length=150)
    popular = models.BooleanField(default=False)
    location_frame = models.TextField(null=True, blank=True)
    price = models.IntegerField(default=0)

    trending = models.BooleanField(default=False)
    def __str__(self) -> str:
        return self.name
    
    class Meta:
        verbose_name_plural = "Treks/Expedition Lists"


    def save(self, *args, **kwargs):
        if self.main_iamge:
            image_temporary = Image.open(self.main_iamge)
            if image_temporary.mode in ("RGBA", "P"):
                image_temporary = image_temporary.convert("RGB")

            output = BytesIO()
            image_quality = 90
            while True:
                output = BytesIO()
                image_temporary.save(output, format='JPEG', quality=image_quality)
                output.seek(0)
                file_size = sys.getsizeof(output)
                if file_size < 5000000:  # 5 MB in bytes
                    break
                else:
                    image_quality -= 10

            self.main_iamge = InMemoryUploadedFile(output, 'ImageField', "%s.jpg" % self.main_iamge.name.split('.')[0], 'image/jpeg', file_size, None)

        super(PeeksLists, self).save(*args, **kwargs)

    def total_booked(self):
        random_number = random.randint(500, 1000)
        if BookaTour.objects.filter(peek_info = self).exists():
            return BookaTour.objects.filter(peek_info = self).count() + random_number
        else:
            return random_number
        
    def get_highlight(self):
        if PeeeksHighlights.objects.filter(peek_info = self).exists():
            return PeeeksHighlights.objects.filter(peek_info = self).first()
        else:
            return None 
        
    def get_itenary(self):
        if PeeeksItenary.objects.filter(peek_info = self).exists():
            return PeeeksItenary.objects.filter(peek_info = self)
        else:
            return None 
        
    def get_comments(self):
        if CommentsTours.objects.filter(peek_info = self).exists():
            return CommentsTours.objects.filter(peek_info = self)
        else:
            return None 


class PopularPeaks(AuditFields):
    peek_info = models.ForeignKey(PeeksLists, on_delete=models.CASCADE, related_name="popular_peek")
    offer = models.CharField(max_length=250,null=True, blank=True)
    price = models.CharField(max_length=250, null=True, blank=True)
    title = models.CharField(max_length=250,null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    popular_last_month = models.BooleanField(default=False)

    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name_plural = "Popular Peaks Lists"
    

class PeeeksHighlights(AuditFields):
    peek_info = models.ForeignKey(PeeksLists, on_delete=models.CASCADE, related_name="peek_highlights")
    highlights = RichTextField(null=True, blank=True)

    def __str__(self) -> str:
        return self.peek_info.name

    class Meta:
        verbose_name_plural = "Peeeks Highlights Lists"

class PeeeksItenary(AuditFields):
    peek_info = models.ForeignKey(PeeksLists, on_delete=models.CASCADE, related_name="peek_itemary")
    day = models.CharField(max_length=250)
    title = models.CharField(max_length=250)
    descriotion = RichTextField(null=True, blank=True)


    def __str__(self) -> str:
        return self.peek_info.name

    class Meta:
        verbose_name_plural = "Peeeks Itenary Lists"

class BookaTour(AuditFields):
    peek_info = models.ForeignKey(PeeksLists, on_delete=models.CASCADE)
    name = models.CharField(max_length=50, null=True, blank=True)
    email = models.EmailField(max_length=254, null=True, blank=True)
    phone = models.CharField(max_length=50, null=True, blank=True)
    country = models.CharField(max_length=50, null=True, blank=True)
    arrival_time =models.CharField(max_length=50, null=True, blank=True)
    departure_date =models.CharField(max_length=50, null=True, blank=True)
    message = models.TextField(null=True,blank=True)

    class Meta:
        verbose_name_plural = "Booked Tour Lists"


class CommentsTours(AuditFields):
    peek_info = models.ForeignKey(PeeksLists, on_delete=models.CASCADE)
    name = models.CharField(max_length=50,null=True, blank=True)
    email = models.EmailField(max_length=254,null=True, blank=True)
    title = models.CharField(max_length=250,null=True, blank=True)

    message = models.TextField(null=True, blank=True)

    def get_avatar(self):
        url="https://ui-avatars.com/api/?background=0D8ABC&color=fff&name={0}&size=256&format=png".format(self.name)
        return url

    class Meta:
        verbose_name_plural = "Comments"

class ContactUsModel(AuditFields):
    name = models.CharField(max_length=50)
    email = models.EmailField(max_length=254)
    phone = models.CharField(max_length=50)
    subject = models.CharField(max_length=50)
    message = models.TextField(null=True, blank=True)

    class Meta:
        verbose_name_plural = "Contacted Lists"

class DealsLists(AuditFields):
    peek_info = models.ForeignKey(PeeksLists, on_delete=models.CASCADE)
    till = models.DateField(null=True, blank=True)
    percentage = models.DecimalField(max_digits=5, decimal_places=2)

    class Meta:
        verbose_name_plural = "Deal Lists"

class FAQLists(AuditFields):

    questions = models.CharField((""), max_length=255, null=True, blank=True)
    answers = RichTextField(null=True, blank=True)



class Blogs(AuditFields):

    thumbnail = models.FileField(upload_to="thumbnail", 
        validators=[FileExtensionValidator(allowed_extensions=["jpg","png", "jpeg"])], null=True)
    
    title = models.CharField(max_length=255)
    description = RichTextField(null=True, blank=True)
    user = models.CharField(max_length=255)