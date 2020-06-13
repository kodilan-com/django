from django.db import models


class Company(models.Model):
    class Meta:
        verbose_name_plural = "companies"

    name = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(null=True)
    email = models.EmailField(unique=True)
    logo = models.ImageField(upload_to='uploads/')
    www = models.URLField()
    twitter = models.CharField(null=True, max_length=15)
    linkedin = models.URLField(null=True,)
    pub_date = models.DateTimeField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = self.name.lower()
        super(Tag, self).save(*args, **kwargs)


class Post(models.Model):

    class TypeEnum(models.IntegerChoices):
        FULLTIME = 1, 'Full Time'
        PARTTIME = 2, 'Part Time'
        TRAINEE = 3, 'Trainee'
        FREELANCER = 4, 'Freelancer'

    class StatusEnum(models.IntegerChoices):
        DISAPPROVED = 0, 'Disapproved'
        APPROVED = 1, 'Approved'
        UNPUBLISHED = 2, 'Unpublished'

    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    tags = models.ManyToManyField(Tag)
    slug = models.SlugField(null=True, unique=True)
    position = models.CharField(max_length=200)
    description = models.TextField()
    apply_url = models.URLField(null=True, blank=True)
    apply_email = models.EmailField(null=True, blank=True)
    location = models.CharField(max_length=200)
    type = models.PositiveSmallIntegerField(choices=TypeEnum.choices)
    status = models.PositiveSmallIntegerField(choices=StatusEnum.choices)
    is_featured = models.BooleanField()
    activation_code = models.CharField(max_length=200, null=True, blank=True)
    renewal_code = models.CharField(max_length=200, null=True, blank=True)
    notes = models.TextField(null=True, blank=True)
    pub_date = models.DateTimeField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.company.name + ' > ' + self.position

    def detail(self):
        return f"{self.company.id} > {self.company.name}"