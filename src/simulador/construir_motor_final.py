"""Exporta el modelo Stuff+ final (thread "Modelo Stuff+ y estrategias") a simulador/motor.json para el navegador.

Lee models/ (stuff_clase.txt multiclase + stuff_bip_xrv.txt, escala.json, k_altitud.json)
y outputs/resultados (scores_pitch.parquet, delta_altitud_por_tipo.csv).
"""
import json, sys
import numpy as np, pandas as pd, lightgbm as lgb
from pathlib import Path
RAIZ = Path(__file__).resolve().parents[2]
MOD = str(RAIZ / 'models')
RES = str(RAIZ / 'outputs' / 'resultados')
OUT = str(RAIZ / 'app' / 'simulador')
sys.path.insert(0, str(RAIZ / 'src' / 'modelo'))
from comun import FEATS_STUFF, CLASES

def compacto(node):
    if 'leaf_value' in node:
        return round(node['leaf_value'], 7)
    assert node['decision_type'] == '<=', node['decision_type']
    return [node['split_feature'], node['threshold'], int(node['default_left']),
            compacto(node['left_child']), compacto(node['right_child'])]
def arboles(path):
    d = lgb.Booster(model_file=path).dump_model()
    assert d['feature_names'] == FEATS_STUFF
    return [compacto(t['tree_structure']) for t in d['tree_info']], d.get('num_class', 1)

clase, nc = arboles(f'{MOD}/stuff_clase.txt')
bip, _ = arboles(f'{MOD}/stuff_bip_xrv.txt')
esc = json.load(open(f'{MOD}/escala.json'))
k = json.load(open(f'{MOD}/k_altitud.json'))

# mapa de movimiento y valores típicos, con los Stuff+ nativos del modelo final
sp = pd.read_parquet(f'{RES}/scores_pitch.parquet',
                     columns=['pitcher_anon_id', 'altitude_m', 'harp_helu', 'PitcherThrows', 'AutoPitchType', 'RelSpeed',
                              'SpinRate', 'SpinAxis', 'InducedVertBreak', 'HorzBreak', 'stuff_plus', 'rv_obs'])
s = np.where(sp.PitcherThrows.eq('Left'), -1, 1)
sp['HB'] = sp.HorzBreak * s
sp['env'] = np.where(sp.harp_helu.eq(1), 'hh', np.where(sp.altitude_m <= 20, 'mar', 'otro'))
TIPOS = ['Four-Seam', 'Sinker', 'Cutter', 'Changeup', 'Splitter', 'Slider', 'Curveball']
def puntos(sub):
    a = (sub[sub.AutoPitchType.isin(TIPOS)].groupby(['pitcher_anon_id', 'AutoPitchType'])
         .agg(n=('stuff_plus', 'size'), IVB=('InducedVertBreak', 'mean'), HB=('HB', 'mean'), velo=('RelSpeed', 'mean'),
              spin=('SpinRate', 'mean'), stuff=('stuff_plus', 'mean'), rv=('rv_obs', 'mean')).reset_index())
    a = a[a.n >= 40]
    return [[r.AutoPitchType, round(r.HB, 1), round(r.IVB, 1), round(r.velo, 1), int(r.spin), round(r.stuff, 1),
             round(r.rv * 100, 2), int(r.n)] for r in a.itertuples()]
mapa = {'hh': puntos(sp[sp.env.eq('hh')]), 'mar': puntos(sp[sp.env.eq('mar')])}
viejo = json.load(open(Path(__file__).with_name('motor_provisional.json')))  # generado por construir_motor.py
tipicos = viejo['tipicos']  # medianas en el Harp Helú (espejadas a derecho), de construir_motor.py
dt = pd.read_csv(f'{RES}/delta_altitud_por_tipo.csv').set_index('AutoPitchType')
por_tipo = {t: {'hh': float(dt.loc[t, 'stuff_hh']), 'mar': float(dt.loc[t, 'stuff_mar']), 'mismo': float(dt.loc[t, 'delta_stuff'])}
            for t in TIPOS if t in dt.index}
motor = {'version': 'modelo-final', 'oficial': True, 'features': FEATS_STUFF, 'clases': CLASES, 'num_class': nc,
         'arboles_clase': clase, 'arboles_bip': bip, 'rv_medio_clase': esc['rv_medio_clase'],
         'v_count_medio_bip': esc['v_count_medio_bip'], 'mu': esc['stuff']['media'], 'sd': esc['stuff']['sd'],
         'fb_liga': esc['fb_liga'], 'k_altitud': k, 'altitud_hh': 2240, 'altitud_mar': 0,
         'mapa': mapa, 'tipicos': tipicos, 'stuff_por_tipo': por_tipo,
         'validacion': {'r_pitcher_holdout': 0.44, 'r_parque_hh': 0.66, 'estabilidad_anual': '0.61-0.68'}}
json.dump(motor, open(f'{OUT}/motor.json', 'w'), ensure_ascii=False, separators=(',', ':'))
print('ok', len(clase), 'árboles clase,', len(bip), 'bip;', {k: len(v) for k, v in mapa.items()}, 'puntos')
