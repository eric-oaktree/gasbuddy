from django import forms

from .models import Gas, Region, Station, Site, Ship, Harvester, Setup

class GasForm(forms.Form):
    try:
        ship = forms.ModelChoiceField(queryset=Ship.objects.all(), initial=Ship.objects.get(name='Prospect'), label='Ship: ')
        harvester = forms.ModelChoiceField(queryset=Harvester.objects.all(), initial=Harvester.objects.get(harv_id='25812'), label='Harvester: ')
        skill = forms.IntegerField(initial=5, label='Mining Frigates Skill: ')
    except:
        pass

class SiteForm(forms.Form):
    try:
        ship = forms.ModelChoiceField(queryset=Ship.objects.all(), initial=Ship.objects.get(name='Prospect'), label='Ship: ')
        harvester = forms.ModelChoiceField(queryset=Harvester.objects.all(), initial=Harvester.objects.get(harv_id='25812'), label='Harvester: ')
        skill = forms.IntegerField(initial=5, label='Mining Frigates Skill: ')
    except:
        pass
