"""Reproduce published radius sensitivity and test a reusable collocation engine."""
from pathlib import Path
import json
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
ROOT=Path(__file__).resolve().parent

def haversine_km(lat,lon,site_lat,site_lon):
    lat,lon=np.radians(np.asarray(lat,float)),np.radians(np.asarray(lon,float))
    slat,slon=np.radians([site_lat,site_lon])
    a=np.sin((lat-slat)/2)**2+np.cos(lat)*np.cos(slat)*np.sin((lon-slon)/2)**2
    return 6371.0088*2*np.arcsin(np.sqrt(np.clip(a,0,1)))

def collocate(soundings,site_lat,site_lon,reference_time,radius_km=300,time_hours=2):
    if radius_km<=0 or time_hours<0:raise ValueError('Invalid collocation limits')
    if not -90<=site_lat<=90 or not -180<=site_lon<=180:raise ValueError('Invalid site coordinates')
    f=soundings.copy()
    if not f.latitude.between(-90,90).all() or not f.longitude.between(-180,180).all():raise ValueError('Invalid sounding coordinates')
    f['distance_km']=haversine_km(f.latitude,f.longitude,site_lat,site_lon)
    t=pd.to_datetime(f.time,utc=True);ref=pd.Timestamp(reference_time)
    if ref.tzinfo is None:raise ValueError('Reference time must include UTC/timezone')
    f['time_difference_hours']=(t-ref).dt.total_seconds().abs()/3600
    return f[(f.distance_km<=radius_km)&(f.time_difference_hours<=time_hours)]

def run():
    out=ROOT/'results';out.mkdir(exist_ok=True)
    d=pd.read_csv(ROOT/'data/published_radius_summary.csv')
    assert len(d)==23 and (d.comparison_days>0).all()
    assert (d.satellite_retrievals>=d.comparison_days).all()
    fig,axes=plt.subplots(2,3,figsize=(13,7))
    for j,gas in enumerate(['CO2','CH4','CO']):
        for mission,g in d[d.gas==gas].groupby('mission'):
            axes[0,j].errorbar(g.radius_km,g.mean_difference,yerr=g.sd_difference,marker='o',capsize=3,label=mission)
            axes[1,j].plot(g.radius_km,g.comparison_days,'o-',label=mission)
        unit=d[d.gas==gas].unit.iloc[0]
        axes[0,j].axhline(0,color='gray',lw=1);axes[0,j].set(title=gas,ylabel=f'Satellite − ground ({unit}); ± SD')
        axes[1,j].set(xlabel='Collocation radius (km)',ylabel='Matched comparison days')
        for ax in axes[:,j]:ax.grid(alpha=.2);ax.legend(fontsize=8)
    fig.suptitle('Published Jinja comparison: more coverage changes estimated differences',fontsize=13)
    fig.tight_layout();fig.savefig(out/'radius_tradeoffs.png',dpi=160);plt.close(fig)
    selected=d[((d.gas=='CO')&(d.radius_km==50))|((d.gas!='CO')&(d.radius_km==300))]
    selected.to_csv(out/'paper_selected_radii.csv',index=False)
    changes=[]
    for (mission,gas),g in d.groupby(['mission','gas']):
        g=g.sort_values('radius_km');lo,hi=g.iloc[0],g.iloc[-1]
        changes.append({'mission':mission,'gas':gas,'unit':lo.unit,'radius_min_km':int(lo.radius_km),'radius_max_km':int(hi.radius_km),
            'days_min':int(lo.comparison_days),'days_max':int(hi.comparison_days),'change_in_mean_difference':float(hi.mean_difference-lo.mean_difference)})
    pd.DataFrame(changes).to_csv(out/'radius_sensitivity_summary.csv',index=False)
    metrics={'published_summary_rows':len(d),'source_tables':['B1','B2','B3'],
        'raw_satellite_validation_performed':False,'selected_radius_results':selected.to_dict(orient='records')}
    (out/'metrics.json').write_text(json.dumps(metrics,indent=2))
    return metrics
if __name__=='__main__':print(json.dumps(run(),indent=2))
