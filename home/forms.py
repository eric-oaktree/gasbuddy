from django import forms

from .models import Gas, Region, Station, Site, Ship, Harvester, Setup

class GasForm(forms.Form):
    ship = forms.ModelChoiceField(queryset=Ship.objects.all(), initial=Ship.objects.get(name='Prospect'), label='Ship: ')
    harvester = forms.ModelChoiceField(queryset=Harvester.objects.all(), initial=Harvester.objects.get(harv_id='25812'), label='Harvester: ')
    skill = forms.IntegerField(initial=5, label='Mining Frigates Skill: ', max_value=5, min_value=1)

class SiteForm(forms.Form):
    num = forms.IntegerField(initial=1, label='Number of Ships:', widget=forms.NumberInput(attrs={'class': 'form-control'}) )
    ship = forms.ModelChoiceField(queryset=Ship.objects.all(), initial=Ship.objects.get(name='Prospect'), label='Ship: ', widget=forms.Select(attrs={'class': 'form-control'}))
    harvester = forms.ModelChoiceField(queryset=Harvester.objects.all(), initial=Harvester.objects.get(harv_id='25812'), label='Harvester: ', widget=forms.Select(attrs={'class': 'form-control'}))
    skill = forms.IntegerField(initial=5, label='Mining Frigates Skill: ', max_value=5, min_value=1, widget=forms.NumberInput(attrs={'class': 'form-control'}))
    extra_data = forms.BooleanField(required=False, label='Extra Data:', widget=forms.CheckboxInput(attrs={'class': 'form-control'}))

class SiteAnalyzer(forms.Form):
    scan = forms.CharField(label='Paste Scan Here: ', widget=forms.Textarea(attrs={'class': 'form-control'}))
    num = forms.IntegerField(initial=1, label='Number of Ships:', widget=forms.NumberInput(attrs={'class': 'form-control'}))
    ship = forms.ModelChoiceField(queryset=Ship.objects.all(), initial=Ship.objects.get(name='Prospect'), label='Ship: ', widget=forms.Select(attrs={'class': 'form-control'}))
    harvester = forms.ModelChoiceField(queryset=Harvester.objects.all(), initial=Harvester.objects.get(harv_id='25812'), label='Harvester: ', widget=forms.Select(attrs={'class': 'form-control'}))
    skill = forms.IntegerField(initial=5, label='Mining Frigates Skill: ', max_value=5, min_value=1, widget=forms.NumberInput(attrs={'class': 'form-control'}))
