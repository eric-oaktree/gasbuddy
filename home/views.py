from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse

# Create your views here.
from .models import Gas, Region, Station, Site, Ship, Harvester, Setup

def home(request):
    return render(request, "home/home.html")

def sites(request):
    return render(request, "home/sites.html")

def site_an(request):
    return render(request, "home/site_an.html")

def pull_prices(request):
    gs = Gas.objects.all()
    id_str = ''
    for g in gs:
        gid = g.item_id
        id_str = id_str+'&typeid='+gid
    r = Region.objects.get(id=1)
    r = r.region_id
    url = 'http://api.eve-central.com/api/marketstat?'+id_str+'&regionlimit='+r

    return render(request, "home/home.html")

def wipe_db(request):
    s = Site.objects.all()
    s.delete()
    g = Gas.objects.all()
    g.delete()
    r = Region.objects.all()
    r.delete()
    s = Station.objects.all()
    s.delete()
    s = Ship.objects.all()
    s.delete()
    h = Harvester.objects.all()
    h.delete()
    s = Setup.objects.all()
    s.delete()
    return HttpResponseRedirect(reverse('home:home'))

def setup_site(request):
    try:
        s = Setup.objects.get(id=1)
        if s==1:
            return HttpResponseRedirect(reverse('home:home'))
    except:
        g = Gas(name='Fullerite-C28',item_id='30375', volume='2')
        g.save()
        g = Gas(name='Fullerite-C32',item_id='30376', volume='5')
        g.save()
        g = Gas(name='Fullerite-C320',item_id='30377', volume='5')
        g.save()
        g = Gas(name='Fullerite-C50',item_id='30370', volume='1')
        g.save()
        g = Gas(name='Fullerite-C540',item_id='30378', volume='10')
        g.save()
        g = Gas(name='Fullerite-C60',item_id='30371', volume='1')
        g.save()
        g = Gas(name='Fullerite-C70',item_id='30372', volume='1')
        g.save()
        g = Gas(name='Fullerite-C72',item_id='30373', volume='2')
        g.save()
        g = Gas(name='Fullerite-C84',item_id='30374', volume='2')
        g.save()
        r = Region(name='The Forge', region_id='10000002')
        r.save()
        s = Station(name='Jita IV - Moon 4 - Caldari Navy Assembly Plant ( Caldari Administrative Station )',station_id='60003760')
        s.save()
        s = Ship(name='Venture',cargo=5000,cycle_bonus=0.05,yld_bonus=1.00)
        s.save()
        s = Ship(name='Prospect',cargo=10000,cycle_bonus=0.05,yld_bonus=1.00)
        s.save()
        h = Harvester(name='Gas Cloud Harvester I',harv_id='25266',cycle=30,yld=20)
        h.save()
        h = Harvester(name='\'Crop\' Gas Cloud Harvester',harv_id='25540',cycle=30,yld=20)
        h.save()
        h = Harvester(name='\'Plow\' Gas Cloud Harvester',harv_id='25542',cycle=30,yld=20)
        h.save()
        h = Harvester(name='Gas Cloud Harvester II',harv_id='25812',cycle=40,yld=30)
        h.save()
        h = Harvester(name='Syndicate Gas Cloud Harvester',harv_id='28788',cycle=30,yld=20)
        h.save()
        c50 = Gas.objects.get(name='Fullerite-C50')
        c60 = Gas.objects.get(name='Fullerite-C60')
        c70 = Gas.objects.get(name='Fullerite-C70')
        c72 = Gas.objects.get(name='Fullerite-C72')
        c84 = Gas.objects.get(name='Fullerite-C84')
        c28 = Gas.objects.get(name='Fullerite-C28')
        c32 = Gas.objects.get(name='Fullerite-C32')
        c320 = Gas.objects.get(name='Fullerite-C320')
        c540 = Gas.objects.get(name='Fullerite-C540')
        s = Site(name='Barren Perimeter Reservoir',p_gas=c50,s_gas=c60,p_qty=3000,s_qty=1500)
        s.save()
        s = Site(name='Token Perimeter Reservoir',p_gas=c60,s_gas=c70,p_qty=3000,s_qty=1500)
        s.save()
        s = Site(name='Ordinary Perimeter Reservoir',p_gas=c72,s_gas=c84,p_qty=3000,s_qty=1500)
        s.save()
        s = Site(name='Sizable Perimeter Reservoir',p_gas=c84,s_gas=c50,p_qty=3000,s_qty=1500)
        s.save()
        s = Site(name='Minor Perimeter Reservoir',p_gas=c70,s_gas=c72,p_qty=3000,s_qty=1500)
        s.save()
        s = Site(name='Bountiful Frontier Reservoir',p_gas=c28,s_gas=c32,p_qty=5000,s_qty=1000)
        s.save()
        s = Site(name='Vast Frontier Reservoir',p_gas=c32,s_gas=c28,p_qty=5000,s_qty=1000)
        s.save()
        s = Site(name='Instrumental Core Reservoir',p_gas=c320,s_gas=c540,p_qty=6000,s_qty=500)
        s.save()
        s = Site(name='Vital Core Reservoir',p_gas=c540,s_gas=c320,p_qty=6000,s_qty=500)
        s.save()
        s = Setup(setup=1)
        s.save()
        return HttpResponseRedirect(reverse('home:home'))
