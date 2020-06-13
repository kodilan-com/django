# Kodilan Backend (Django)

### Eksikler

- [X] Firmaların ilanları eklenecek
- [X] Etiketlerin ilanları eklenecek
- [X] Ilan gönderme eklenecek
- [X] Lokasyona göre ilan arama eklenecek
- [X] Search eklenecek (Pozisyon adı, şehir, type/örn: tam zamanlı)

### Gereksinimler

- postgresql
- python 3.6+

### Kurulum

paketlerin yüklenilmesi
```console
$ pip install -r requirements.txt
```

migration oluşturma
```console
$ python manage.py makemigrations
```

migrate 
```console
$ python manage.py migrate
```

superuser oluşturma
```console
$ python manage.py createsuperuser
```