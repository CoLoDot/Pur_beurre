from django.contrib.auth.forms import forms


class Connexion(forms.Form):
    username = forms.CharField(label="Nom d'utilisateur", max_length=30)
    email = forms.CharField(label="Mail", max_length=100)
    password = forms.CharField(label="Mot de passe", widget=forms.PasswordInput)
