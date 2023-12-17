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

    # def __str__(self):
    #     return self.email
    
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
    price = models.IntegerField(default=0)

    trending = models.BooleanField(default=False)
    def __str__(self) -> str:
        return self.name
    
    class Meta:
        verbose_name_plural = "Treks/Expedition Lists"
        ordering = ["-created_at"]


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

            self.main_iamge = InMemoryUploadedFile(output, 
            'ImageField', "%s.jpg" % self.main_iamge.name.split('.')[0], 'image/jpeg', file_size, None)
        if self.rating == 0 and self.rate_total == 0:

            random_rating = random.uniform(4.4, 5)
            random_rating = round(random_rating, 1)

            self.rating = random_rating
            self.rate_total = random.randint(200, 1000)



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
        

    def get_location(self):
        if PeeksLocation.objects.filter(peek_info = self).exists():
            return PeeksLocation.objects.filter(peek_info = self).first().location_frame
        else:
            return None 
        
    def get_included(self):
        if PeeekIncludeExclude.objects.filter(peek_info=self,inc_type = "Included").exists():
            return PeeekIncludeExclude.objects.filter(peek_info=self,inc_type = "Included")
        else:
            return None 
        

    def get_notincluded(self):
        if PeeekIncludeExclude.objects.filter(peek_info=self,inc_type = "NotIncluded").exists():
            return PeeekIncludeExclude.objects.filter(peek_info=self,inc_type = "NotIncluded")
        else:
            return None 


class PeeksLocation(AuditFields):
    peek_info = models.ForeignKey(PeeksLists, on_delete=models.CASCADE, related_name="peek_location")
    location_frame = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.peek_info.name


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
        ordering = ["-created_at"]
    

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


class PeeekIncludeExclude(AuditFields):

    choices = (
        ("Included","Included"),
        ("NotIncluded","NotIncluded")
    )
    inc_type = models.CharField(max_length=200, choices=choices, default="Included")
    peek_info = models.ForeignKey(PeeksLists, on_delete=models.CASCADE, related_name="peek_inc_exe")
    
    name=models.CharField(max_length=250)


    def __str__(self) -> str:
        return self.peek_info.name

    class Meta:
        verbose_name_plural = "Peeks Included/Excluded Lists"
        ordering = ["-created_at"]



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
        ordering = ["-created_at"]


class CommentsTours(AuditFields):
    peek_info = models.ForeignKey(PeeksLists, on_delete=models.CASCADE,null=True, blank=True)
    blogs = models.ForeignKey("Blogs", on_delete=models.CASCADE,null=True, blank=True)
    name = models.CharField(max_length=50,null=True, blank=True)
    email = models.EmailField(max_length=254,null=True, blank=True)
    title = models.CharField(max_length=250,null=True, blank=True)

    message = models.TextField(null=True, blank=True)

    def get_avatar(self):
        url="https://ui-avatars.com/api/?background=0D8ABC&color=fff&name={0}&size=256&format=png".format(self.name)
        return url

    class Meta:
        verbose_name_plural = "Comments"
        ordering = ["-created_at"]

class ContactUsModel(AuditFields):
    name = models.CharField(max_length=50)
    email = models.EmailField(max_length=254)
    phone = models.CharField(max_length=50)
    subject = models.CharField(max_length=50)
    message = models.TextField(null=True, blank=True)

    class Meta:
        verbose_name_plural = "Contacted Lists"
        ordering = ["-created_at"]

class DealsLists(AuditFields):
    peek_info = models.ForeignKey(PeeksLists, on_delete=models.CASCADE)
    till = models.DateField(null=True, blank=True)
    percentage = models.DecimalField(max_digits=5, decimal_places=2)

    class Meta:
        verbose_name_plural = "Deal Lists"

class FAQLists(AuditFields):

    questions = models.CharField((""), max_length=255, null=True, blank=True)
    answers = RichTextField(null=True, blank=True)


class BlogCategory(models.Model):

    name = models.CharField(max_length=50, null=True, blank=True)

    class Meta:
        verbose_name = ("BlogCategory")
        verbose_name_plural = ("BlogCategorys")

    def __str__(self):
        return self.name



class Blogs(AuditFields):

    category = models.ForeignKey(BlogCategory, on_delete=models.SET_NULL, null=True, blank=True)

    thumbnail = models.FileField(upload_to="thumbnail", 
        validators=[FileExtensionValidator(allowed_extensions=["jpg","png", "jpeg"])], null=True)
    
    title = models.CharField(max_length=255)
    description = RichTextField(null=True, blank=True)
    user = models.CharField(max_length=255)

    def get_comments(self):
        if CommentsTours.objects.filter(blogs = self).exists():
            return CommentsTours.objects.filter(blogs = self)
        else:
            return None 
        

    class Meta:
        ordering = ["-created_at"]


class Certificates(AuditFields):

    name = models.CharField(max_length=255, null=True, blank=True)

    certificates = models.FileField(upload_to="certificates", 
        validators=[FileExtensionValidator(allowed_extensions=["jpg","png", "jpeg"])], null=True)
    