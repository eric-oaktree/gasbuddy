from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
import datetime, time, requests, re, os
import bs4
from django.contrib.admin.views.decorators import staff_member_required
from decimal import *

# Create your views here.
from .models import Gas, Region, Station, Site, Ship, Harvester, Setup, APICheck
from .forms import GasForm, SiteForm, SiteAnalyzer

def about(request):
    return render(request, 'home/about.html')

def home(request):
    if request.method == "POST":
        form = GasForm(data=request.POST)
        if form.is_valid():
            data = form.cleaned_data
            harv = data['harvester']
            cycle = harv.cycle
            yld = harv.yld
            ship = data['ship']
            yld_bonus = ship.yld_bonus
            if data['skill'] > 5:
                skill = 5
            if data['skill'] < 1:
                skill = 1
            else:
                skill = data['skill']
            cycle_bonus = skill * .05
    else:
        form = GasForm()
        cycle = 40
        yld = 20
        cycle_bonus = 0.25
        yld_bonus = 1

    if cycle_bonus > .25:
        cycle_bonus = Decimal(0.25)
    c = cycle * (1 - cycle_bonus)
    y = yld * (1 + yld_bonus)

    gases = Gas.objects.all()
    isk_min = {}
    for gas in gases:
        g = gas.name
        vol = gas.volume
        isk_min_val = ((Decimal(y) / Decimal(gas.volume)) * 2) * (60 / Decimal(c)) * Decimal(gas.last_price)
        isk_mthree = Decimal(gas.last_price) / Decimal(gas.volume)
        isk_min[g] = [isk_min_val, isk_mthree]

    u = APICheck.objects.get(id=1)

    context = {'isk_min': isk_min, 'form': form, 'updated': str(u.updated)}
    return render(request, "home/home.html", context)

def sites(request):
    if request.method == "POST":
        form = SiteForm(data=request.POST)
        if form.is_valid():
            data = form.cleaned_data
            harv = data['harvester']
            cycle = Decimal(harv.cycle)
            yld = Decimal(harv.yld)
            ship = data['ship']
            yld_bonus = Decimal(ship.yld_bonus)
            cargo = Decimal(ship.cargo)
            num = Decimal(data['num'])
            if data['skill'] > 5:
                skill = 5
            if data['skill'] < 1:
                skill = 1
            else:
                skill = data['skill']
            cycle_bonus = skill * .05

            extra_data = data['extra_data']



    else:
        form = SiteForm()
        cycle = Decimal(40)
        yld = Decimal(20)
        cycle_bonus = Decimal(0.25)
        yld_bonus = Decimal(1)
        num = Decimal(1)
        cargo = 10000
        extra_data = False

    c = cycle * (Decimal(1) - Decimal(cycle_bonus))
    y = yld * (Decimal(1) + Decimal(yld_bonus))

    sites = Site.objects.all()
    sites_calc = {}
    for site in sites:
        p_price = site.p_gas.last_price
        s_price = site.s_gas.last_price
        p_vol = site.p_gas.volume
        s_vol = site.s_gas.volume

        p_isk_min = ((Decimal(y) / Decimal(p_vol)) * 2) * (60 / Decimal(c)) * Decimal(p_price) * num
        s_isk_min = ((Decimal(y) / Decimal(s_vol)) * 2) * (60 / Decimal(c)) * Decimal(s_price) * num

        if p_isk_min < s_isk_min:
            best_gas = site.s_gas
            best_gas_isk_min = s_isk_min
            best_qty = site.s_qty
            other_gas = site.p_gas
            other_gas_isk_min = p_isk_min
            other_qty = site.p_qty
        else:
            best_gas = site.p_gas
            best_gas_isk_min = p_isk_min
            best_qty = site.p_qty
            other_gas = site.s_gas
            other_gas_isk_min = s_isk_min
            other_qty = site.s_qty

        p_units_min = ((y / best_gas.volume) * 2) * (60 / c) * num
        s_units_min = ((y / other_gas.volume) * 2) * (60 / c) * num
        time_to_clear = (best_qty / p_units_min) + (other_qty / s_units_min)
        isk_pres = (p_price * site.p_qty) + (s_price * site.s_qty)

        site_isk_min = Decimal(isk_pres) / Decimal(time_to_clear)

        #extra data calculations
        primary_time_to_clear = (best_qty / p_units_min)
        secondary_time_to_clear = (other_qty / s_units_min)
        #blue_loot_isk
        #time to kill site
        ships_needed = ((site.p_qty * p_vol) + (site.s_qty * s_vol)) / (cargo)

        sites_calc[site.name] = [isk_pres, best_gas, best_gas_isk_min, other_gas, other_gas_isk_min, site_isk_min, time_to_clear, primary_time_to_clear, secondary_time_to_clear, ships_needed]

    u = APICheck.objects.get(id=1)
    context = {'form': form, 'sites_calc': sites_calc, 'updated': str(u.updated), 'extra_data': extra_data}
    return render(request, "home/sites.html", context)

def site_an(request):
    if request.method == 'POST':
        form = SiteAnalyzer(data=request.POST)
        if form.is_valid():
            data = form.cleaned_data
            scan = data['scan']
            num = Decimal(data['num'])
            ship = data['ship']
            harvester = data['harvester']
            skill = Decimal(data['skill'])
            show_data = True
    else:
        form = SiteAnalyzer()
        show_data = False
        skill = 0
        yld = 0
        num = 1
        ship = Ship.objects.get(id=1)
        harvester = Harvester.objects.get(id=1)

    cycle_bonus = skill * Decimal(0.05)
    yld = harvester.yld
    c = harvester.cycle * (1 - cycle_bonus)
    y = yld * (1 + ship.yld_bonus) * num
    #parse Dscan
    sites = []
    proc_sites = []
    if show_data == True:
        #print(scan)
        scan_re = re.compile(r'Gas Site	*(\S* \S* \S*)	*')
        scan_re_b = re.compile(r'(Instrumental Core Reservoir|Ordinary Perimeter Reservoir|Minor Perimeter Reservoir|Bountiful Frontier Reservoir|Barren Perimeter Reservoir|Token Perimeter Reservoir|Sizable Perimeter Reservoir|Vast Frontier Reservoir|Vital Core Reservoir)')
        scan_results = scan_re.findall(scan)
        if scan_results == []:
            scan_results = scan_re_b.findall(scan)
        print(scan_results)
        for res in scan_results:
            sites.append(res)


        for s in sites:
            site = Site.objects.get(name=s)
            site_name = site.name
            site_isk = (site.p_gas.last_price * site.p_qty) + (site.s_gas.last_price * site.s_qty)

            #ninja scanning
            #determine best gas
            p_isk_min = ((Decimal(y) / Decimal(site.p_gas.volume)) * 2) * (60 / Decimal(c)) * Decimal(site.p_gas.last_price)
            s_isk_min = ((Decimal(y) / Decimal(site.s_gas.volume)) * 2) * (60 / Decimal(c)) * Decimal(site.s_gas.last_price)
            if p_isk_min >= s_isk_min:
                first_cloud = site.p_gas
                first_qty = site.p_qty
                sec_cloud = site.s_gas
                sec_qty = site.s_qty
            if p_isk_min <= s_isk_min:
                first_cloud = site.s_gas
                first_qty = site.s_qty
                sec_cloud = site.p_gas
                sec_qty = site.p_qty
            #calculate how much you can get in 15 minutes
            units_15 = ((Decimal(y) / Decimal(first_cloud.volume)) * 2) * (60 / Decimal(c)) * 15
            if units_15 <= first_qty:
                ninja_isk = units_15 * first_cloud.last_price
                if ninja_isk > site_isk:
                    ninja_isk = site_isk
                m_per_s = (units_15 / num) * first_cloud.volume

            #if it is more than the qty in the best cloud, calculate the remaining time
            if units_15 > first_qty:
                min_left = 15 - (first_qty / (units_15 / 15))
                sec_units_min = ((Decimal(y) / Decimal(sec_cloud.volume)) * 2) * (60 / Decimal(c))
                rem_units = sec_units_min * min_left
                ninja_isk = (rem_units * sec_cloud.last_price) + (first_qty * first_cloud.last_price)
                if ninja_isk > site_isk:
                    ninja_isk = site_isk
                m_per_s = ((units_15 / num) * first_cloud.volume) + ((rem_units / num) * sec_cloud.volume)
                if m_per_s * num > (site.p_qty * site.p_gas.volume) + (site.s_qty * site.s_gas.volume):
                    m_per_s = ((site.p_qty * site.p_gas.volume) + (site.s_qty * site.s_gas.volume)) / num

            sipm = ninja_isk / 15 / num
            nips = ninja_isk / num
            if site_name == 'Ordinary Perimeter Reservoir':
                sipm = 0
                m_per_s = 0
                nips = 0
                ninja_isk = 0
            ninja_si = (site_name, site_isk, sipm, first_cloud.name, m_per_s, nips, ninja_isk)
            #print(ninja_si)
            proc_sites.append(ninja_si)

    t_site_isk = 0
    t_sipm = 0
    t_sipm_c = 0
    t_m_per_s = 0
    t_nips = 0
    t_ninja_isk = 0
    for s in proc_sites:
        t_site_isk = t_site_isk + s[1]
        t_sipm = t_sipm + s[2]
        if s[0] != "Ordinary Perimeter Reservoir":
            t_sipm_c = t_sipm_c + 1
        t_m_per_s = t_m_per_s + s[4]
        t_nips = t_nips + s[5]
        t_ninja_isk = t_ninja_isk + s[6]

    ships = t_m_per_s / ship.cargo
    if t_sipm_c == 0:
        t_sipm_c = 1
    if t_site_isk == 0:
        t_site_isk = 1
    percent = (t_ninja_isk / t_site_isk) * 100
    totals = (t_site_isk, t_sipm / t_sipm_c, t_m_per_s, t_nips, t_ninja_isk, ships, percent)
    t_min = t_sipm_c * 15
    u = APICheck.objects.get(id=1)

    #site clearing

    #take sites
    #isk present, blue loot isk present, time to fully clear site, rat dps, rat ehp 

    context = {'show_data': show_data, 'form': form, 'sites': sites, 'proc_sites': proc_sites, 'totals': totals, 't_min': t_min, 'updated': str(u.updated)}
    return render(request, "home/site_an.html", context)

def pull_prices(request):
    tag_re = re.compile(r'<.*>(.*)</.*>')
    gs = Gas.objects.all()
    id_str = ''
    for g in gs:
        gid = g.item_id
        id_str = id_str+'&typeid='+gid
    #r = Region.objects.get(id=1)
    #r = r.region_id
    r = '10000002'
    url = 'http://api.eve-central.com/api/marketstat?'+id_str+'&regionlimit='+r
    xml_raw = requests.get(url)
    if xml_raw.status_code == requests.codes.ok:
        path = 'data/prices.xml'
        xml = open(path, 'w')
        xml.write(xml_raw.text)
        xml.close()
        status = 'OK'
    else:
        status = 'Error'
    xml_file = open(path, 'r')
    xml = xml_file.read()
    soup = bs4.BeautifulSoup(xml, 'xml')
    types = soup.find_all('type')
    for t in types:
        t_dict = dict(t.attrs)
        type_id = t_dict['id']
        buy = t.buy
        avg = buy.find_all('max')
        avg_in = tag_re.search(str(avg))
        avg_in = avg_in.group(1)
        avg_price = Decimal(avg_in)
        avg_price = round(avg_price, 2)
        g = Gas.objects.get(item_id=type_id)
        g.last_price = avg_price
        g.save()
    gases = Gas.objects.all()
    a, c = APICheck.objects.get_or_create(id=1)
    a.save()
    context = {'status': status, 'gases': gases}
    return render(request, "home/pull_prices.html", context)

@staff_member_required
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

@staff_member_required
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
        s = Ship(name='Venture',cargo=5000,yld_bonus=1.00)
        s.save()
        s = Ship(name='Prospect',cargo=10000,yld_bonus=1.00)
        s.save()
        h = Harvester(name='Gas Cloud Harvester I',harv_id='25266',cycle=30,yld=10)
        h.save()
        h = Harvester(name='\'Crop\' Gas Cloud Harvester',harv_id='25540',cycle=30,yld=10)
        h.save()
        h = Harvester(name='\'Plow\' Gas Cloud Harvester',harv_id='25542',cycle=30,yld=10)
        h.save()
        h = Harvester(name='Gas Cloud Harvester II',harv_id='25812',cycle=40,yld=20)
        h.save()
        h = Harvester(name='Syndicate Gas Cloud Harvester',harv_id='28788',cycle=30,yld=10)
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
        try:
            os.mkdir('data/')
        except:
            pass
        s = Setup(setup=1)
        s.save()
        return HttpResponseRedirect(reverse('home:home'))
