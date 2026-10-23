"""EDA: Diablos y la altura del Harp Helú. Uso: python3 eda.py <parquet>"""
import sys, json
from pathlib import Path
import numpy as np, pandas as pd

RAIZ = Path(__file__).resolve().parents[2]
PQ = sys.argv[1] if len(sys.argv) > 1 else str(RAIZ / 'data' / 'stuff_model_df.parquet')
OUT = str(RAIZ / 'results' / 'diablos')
cols = ['year','game_anon_id','pitcher_anon_id','batter_anon_id','PitcherThrows','BatterSide','AutoPitchType','RelSpeed',
        'InducedVertBreak','HorzBreak','PitchCall','KorBB','play_result','hit_type','ExitSpeed','Angle','Balls','Strikes',
        'Inning','Top/Bottom','Outs','RunsScored','OutsOnPlay','is_swing','is_whiff','in_strike_zone','PlateLocHeight']
df = pd.read_parquet(PQ, columns=cols)
df['row'] = np.arange(len(df))
J = pd.read_csv(RAIZ / 'results' / 'estadios' / 'juegos_equipo_local.csv')
df = df.merge(J[['game_anon_id','home_equipo','away_equipo','estadio','altitud_m','harp_helu']], on='game_anon_id', how='left').sort_values('row')
df['top'] = df['Top/Bottom'].eq('Top')
df['pit_team'] = np.where(df.top, df.home_equipo, df.away_equipo)
df['bat_team'] = np.where(df.top, df.away_equipo, df.home_equipo)
df['pit_local'] = df.top
# ---- run value por pitcheo (igual que el simulador) ----
LW = {'Out':-0.27,'FieldersChoice':-0.27,'Sacrifice':-0.20,'Error':0.48,'Single':0.47,'Double':0.78,'Triple':1.06,'HomeRun':1.40}
t = pd.Series(np.nan, index=df.index)
t[df.PitchCall.eq('InPlay')] = df.play_result.map(LW)
t[df.KorBB.eq('Strikeout')] = -0.28; t[df.KorBB.eq('Walk')] = 0.32; t[df.PitchCall.eq('HitByPitch')] = 0.34
df['term'] = t
df['pa_val'] = df.groupby('game_anon_id')['term'].bfill()
cnt = lambda b, s: b.astype('Int64').astype(str) + '-' + s.astype('Int64').astype(str)
df['cnt'] = cnt(df.Balls, df.Strikes)
V = df.dropna(subset=['pa_val']).groupby('cnt').pa_val.mean()
nb, ns = df.Balls.copy(), df.Strikes.copy()
ib = df.PitchCall.isin(['BallCalled','BallinDirt']); ist = df.PitchCall.isin(['StrikeCalled','StrikeSwinging']); fo = df.PitchCall.str.startswith('Foul')
nb[ib] += 1; ns[ist] += 1; ns[fo] = np.minimum(ns[fo] + 1, 2)
rv = cnt(nb, ns).map(V) - df.cnt.map(V); rv[df.term.notna()] = df.term - df.cnt.map(V)
df['rv'] = rv
R = {}
# ---- 1. récords y localía ----
g = df.groupby(['game_anon_id','top']).RunsScored.sum().unstack()   # top=True: carreras del visitante
g.columns = ['home_r','away_r']  # False(Bottom)=local batea
g = g.join(J.set_index('game_anon_id')[['year','home_equipo','away_equipo','estadio','altitud_m']])
g = g[(g.home_r != g.away_r) & g.home_equipo.notna() & g.away_equipo.notna()]
g['home_win'] = (g.home_r > g.away_r).astype(int)
rows = []
for tm in sorted(set(g.home_equipo)):
    h = g[g.home_equipo.eq(tm)]; a = g[g.away_equipo.eq(tm)]
    rows.append(dict(equipo=tm, altitud=h.altitud_m.mode().iat[0], jl=len(h), wl=int(h.home_win.sum()), jv=len(a), wv=int((1-a.home_win).sum()),
                     dif_local=(h.home_r-h.away_r).mean(), dif_visita=(a.away_r-a.home_r).mean(),
                     carreras_juego_local=(h.home_r+h.away_r).mean(), carreras_juego_visita=(a.home_r+a.away_r).mean()))
T = pd.DataFrame(rows)
T['pct_local'] = T.wl/T.jl; T['pct_visita'] = T.wv/T.jv; T['ventaja'] = T.pct_local - T.pct_visita
T['dif_ventaja'] = T.dif_local - T.dif_visita
T['factor_parque'] = T.carreras_juego_local / T.carreras_juego_visita
T = T.sort_values('ventaja', ascending=False)
T.round(3).to_csv(f'{OUT}/localia_por_equipo.csv', index=False)
R['liga_pct_local'] = float(g.home_win.mean())
by_year = []
for y in sorted(g.year.unique()):
    gy = g[g.year.eq(y)]
    for tm in ['Diablos']:
        h = gy[gy.home_equipo.eq(tm)]; a = gy[gy.away_equipo.eq(tm)]
        by_year.append(dict(year=int(y), wl=int(h.home_win.sum()), ll=int(len(h)-h.home_win.sum()), wv=int((1-a.home_win).sum()), lv=int(a.home_win.sum()),
                            dif_local=round((h.home_r-h.away_r).mean(),2), dif_visita=round((a.away_r-a.home_r).mean(),2)))
R['diablos_por_anio'] = by_year
# Diablos por tipo de parque de visita
a = g[g.away_equipo.eq('Diablos')].copy()
a['cat'] = pd.cut(a.altitud_m, [-1, 700, 1700, 3000], labels=['bajo 700 m','700-1700 m','1700 m o más'])
R['diablos_visita_por_altitud'] = a.groupby('cat', observed=True).apply(lambda x: {'j': len(x), 'pct': round(1-x.home_win.mean(),3), 'dif': round((x.away_r-x.home_r).mean(),2), 'carreras_juego': round((x.home_r+x.away_r).mean(),2)}).to_dict()
# ---- 2. pitcheo: métricas por pitcheo ----
pa_end = df.term.notna()
def met(x):
    pa = x[x.term.notna()]; bip = x[x.PitchCall.eq('InPlay')]
    return pd.Series({'pitcheos': len(x), 'PA': len(pa), 'K%': (pa.KorBB.eq('Strikeout')).mean()*100, 'BB%': (pa.KorBB.eq('Walk')).mean()*100,
        'whiff/swing%': x.is_whiff.sum()/max(x.is_swing.sum(),1)*100, 'HR/BIP%': bip.play_result.eq('HomeRun').mean()*100,
        'H/BIP%': bip.play_result.isin(['Single','Double','Triple','HomeRun']).mean()*100,
        'GB%': bip.hit_type.eq('GroundBall').mean()*100, 'EV': bip.ExitSpeed.mean(), 'RV/100': x.rv.mean()*100})
dia_p = df[df.pit_team.eq('Diablos')]; vis_hh = df[df.harp_helu.eq(1) & ~df.pit_team.eq('Diablos')]
P = pd.DataFrame({'Diablos en casa': met(dia_p[dia_p.pit_local]), 'Diablos de visita': met(dia_p[~dia_p.pit_local]),
                  'Visitantes en HH': met(vis_hh)})
# mismos pitchers visitantes fuera del HH
vp = set(vis_hh.pitcher_anon_id)
P['Esos visitantes en otros parques'] = met(df[df.pitcher_anon_id.isin(vp) & df.harp_helu.ne(1)])
dia_b = df[df.bat_team.eq('Diablos')]
P['Bateo Diablos en casa'] = met(dia_b[~dia_b.pit_local]); P['Bateo Diablos de visita'] = met(dia_b[dia_b.pit_local])
P.round(2).to_csv(f'{OUT}/pitcheo_casa_visita.csv')
print(P.round(2).to_string())
print(df.hit_type.value_counts().head())
# ---- 3. tipos de pitcheo en HH ----
df['env'] = np.where(df.harp_helu.eq(1), 'HH', np.where(df.altitud_m <= 20, 'mar', 'otro'))
tp = df[df.env.isin(['HH','mar'])].groupby(['AutoPitchType','env']).agg(n=('rv','size'), rv100=('rv', lambda s: s.mean()*100),
        whiff=('is_whiff','sum'), sw=('is_swing','sum')).reset_index()
tp['whiff%'] = tp.whiff/tp.sw*100
tp = tp[tp.n > 1000]
TP = tp.pivot(index='AutoPitchType', columns='env', values=['rv100','whiff%','n']).round(2)
uso = pd.DataFrame({'uso Diablos casa %': dia_p[dia_p.pit_local].AutoPitchType.value_counts(normalize=True)*100,
                    'uso Diablos visita %': dia_p[~dia_p.pit_local].AutoPitchType.value_counts(normalize=True)*100,
                    'rv100 Diablos casa': dia_p[dia_p.pit_local].groupby('AutoPitchType').rv.mean()*100,
                    'rv100 Diablos visita': dia_p[~dia_p.pit_local].groupby('AutoPitchType').rv.mean()*100}).round(2)
TP.columns = [f'{a}_{b}' for a, b in TP.columns]
TP = TP.join(uso, how='left')
TP.to_csv(f'{OUT}/tipos_pitcheo.csv'); print(TP.to_string())
# ---- 4. desgaste y relevo ----
df['np_juego'] = df.groupby(['game_anon_id','pitcher_anon_id']).cumcount() + 1
first = df.groupby(['game_anon_id','top']).pitcher_anon_id.transform('first')
df['abridor'] = df.pitcher_anon_id.eq(first)
df['np_bin'] = pd.cut(df.np_juego, [0,25,50,75,90,105,200], labels=['1-25','26-50','51-75','76-90','91-105','106+'])
df['lugar'] = np.where(df.harp_helu.eq(1), 'HH', 'otros')
ab = df[df.abridor].groupby(['lugar','np_bin'], observed=True).agg(n=('rv','size'), rv100=('rv', lambda s: s.mean()*100)).round(2)
print(ab.unstack(0).to_string()); ab.to_csv(f'{OUT}/desgaste_abridores.csv')
# Diablos: abridores vs relevo en casa y fuera
dd = df[df.pit_team.eq('Diablos')]
rel = dd.groupby([np.where(dd.pit_local,'casa','visita'), np.where(dd.abridor,'abridor','relevo')]).agg(n=('rv','size'), rv100=('rv', lambda s: s.mean()*100)).round(2)
print(rel.to_string()); rel.to_csv(f'{OUT}/diablos_abridor_relevo.csv')
# vuelta al orden (bateadores enfrentados por el abridor)
pa = df[df.term.notna() & df.abridor].copy()
pa['bf'] = pa.groupby(['game_anon_id','pitcher_anon_id']).cumcount() + 1
pa['vuelta'] = np.minimum((pa.bf - 1)//9 + 1, 4)
pa = pa.join(df.groupby(['game_anon_id','pitcher_anon_id']).size().rename('tot'), on=['game_anon_id','pitcher_anon_id'])
tto = pa.groupby(['lugar','vuelta']).agg(PA=('term','size'), rv_pa=('term','mean'), woba_proxy=('term','mean')).round(3)
print(tto.unstack(0).to_string()); tto.to_csv(f'{OUT}/vuelta_orden.csv')
# innings: Diablos en casa por inning (carreras permitidas)
inn = dd.groupby([np.where(dd.pit_local,'casa','visita'), dd.Inning.clip(upper=10)]).rv.mean().unstack(0).mul(100).round(2)
print(inn.to_string()); inn.to_csv(f'{OUT}/diablos_rv_por_inning.csv')
# ---- 5. pitchers de Diablos: brecha casa-visita y perfil ----
pp = dd.groupby(['pitcher_anon_id', np.where(dd.pit_local,'casa','visita')]).agg(n=('rv','size'), rv100=('rv', lambda s: s.mean()*100)).unstack()
pp = pp[(pp['n']['casa'] >= 250) & (pp['n']['visita'] >= 250)]
bip = dd[dd.PitchCall.eq('InPlay')]
prof = pd.DataFrame({'GB%': bip.groupby('pitcher_anon_id').hit_type.apply(lambda s: s.eq('GroundBall').mean()*100),
    'uso_rectas%': dd.groupby('pitcher_anon_id').AutoPitchType.apply(lambda s: s.isin(['Four-Seam']).mean()*100),
    'uso_sinker%': dd.groupby('pitcher_anon_id').AutoPitchType.apply(lambda s: s.isin(['Sinker']).mean()*100),
    'uso_rompientes%': dd.groupby('pitcher_anon_id').AutoPitchType.apply(lambda s: s.isin(['Slider','Curveball','Cutter']).mean()*100),
    'uso_cambio%': dd.groupby('pitcher_anon_id').AutoPitchType.apply(lambda s: s.isin(['Changeup','Splitter']).mean()*100),
    'abridor%': dd.groupby('pitcher_anon_id').abridor.mean()*100})
pp.columns = ['n_casa','n_visita','rv100_casa','rv100_visita']
pp = pp.join(prof); pp['brecha'] = pp.rv100_casa - pp.rv100_visita
pp.round(2).to_csv(f'{OUT}/pitchers_diablos_casa_visita.csv')
print(len(pp)); print(pp.corr(numeric_only=True)['brecha'].round(2).to_string())
R['pitchers_brecha'] = pp.round(2).sort_values('brecha').reset_index().to_dict('records')
json.dump(R, open(f'{OUT}/resumen.json','w'), ensure_ascii=False, indent=1, default=str)
print(T.round(3).to_string()); print(json.dumps(R['diablos_por_anio']), R['liga_pct_local'], R['diablos_visita_por_altitud'])
