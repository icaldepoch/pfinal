from django.db import models

class Alumne(models.Model):
    CURS_ESCOLAR = [
        ('1ESO', '1r ESO'),
        ('2ESO', '2n ESO'),
        ('3ESO', '3r ESO'),
        ('4ESO', '4t ESO'),
        ('1BAT', '1r Batxillerat'),
        ('2BAT', '2n Batxillerat'),
    ]

    codiAlumne = models.CharField(max_length=100)
    nom = models.CharField(max_length=100)
    curs = models.CharField(max_length=5, choices=CURS_ESCOLAR)
    correuElectronicAlumne = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return f"{self.nom} ({self.get_curs_display()})"
    
    def save(self):
        if not self.correuElectronicAlumne:
            self.correuElectronicAlumne = f"{self.codiAlumne}@institut.cat"
        super(Alumne, self).save()

class Conte(models.Model):
    portada = models.ImageField(null=True, blank=True)
    titol = models.CharField(max_length=200)
    text = models.TextField()
    autor = models.OneToOneField(Alumne, on_delete=models.CASCADE, related_name='conte')

    def __str__(self):
        return self.titol


# class Vot(models.Model):
#     conte = models.ForeignKey(Conte, on_delete=models.CASCADE, related_name='vots')
#     ip_votant = models.GenericIPAddressField()
#     data = models.DateTimeField(auto_now_add=True)

#     class Meta:
#         unique_together = ('conte', 'ip_votant')  # Evita múltiples vots d'una mateixa IP

#     def __str__(self):
#         return f"Vot per {self.conte.titol}"

