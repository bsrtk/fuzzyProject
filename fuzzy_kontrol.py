import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl
import matplotlib.pyplot as plt

# Girdiler
zaman = ctrl.Antecedent(np.arange(0, 10, 1), 'zaman')
kullanma_orani = ctrl.Antecedent(np.arange(0, 10, 1), 'kullanma_orani')
enerji_kullanimi = ctrl.Antecedent(np.arange(0, 100, 1), 'enerji_kullanimi')
mevsimsel = ctrl.Antecedent(np.arange(0, 3, 1), 'mevsimsel')
toplam_enerji = ctrl.Antecedent(np.arange(0, 100, 1), 'toplam_enerji')

# Çıktılar
tasarruf_seviyesi = ctrl.Consequent(np.arange(0, 100, 1), 'tasarruf_seviyesi')
kullanim_suresi = ctrl.Consequent(np.arange(0, 3, 0.1), 'kullanim_suresi')

# Manuel üyelik fonksiyonları
zaman['kisa'] = fuzz.trimf(zaman.universe, [0, 0, 3])
zaman['orta'] = fuzz.trimf(zaman.universe, [2, 5, 8])
zaman['uzun'] = fuzz.trimf(zaman.universe, [6, 9, 9])

kullanma_orani['az'] = fuzz.trimf(kullanma_orani.universe, [0, 0, 3])
kullanma_orani['orta'] = fuzz.trimf(kullanma_orani.universe, [2, 5, 8])
kullanma_orani['cok'] = fuzz.trimf(kullanma_orani.universe, [6, 9, 9])

enerji_kullanimi['dusuk'] = fuzz.trimf(enerji_kullanimi.universe, [0, 0, 30])
enerji_kullanimi['orta'] = fuzz.trimf(enerji_kullanimi.universe, [20, 50, 80])
enerji_kullanimi['yuksek'] = fuzz.trimf(enerji_kullanimi.universe, [70, 100, 100])

mevsimsel['yaz'] = fuzz.trimf(mevsimsel.universe, [0, 0, 1])
mevsimsel['kis'] = fuzz.trimf(mevsimsel.universe, [1, 1, 2])
mevsimsel['bahar'] = fuzz.trimf(mevsimsel.universe, [2, 2, 2])

toplam_enerji['dusuk'] = fuzz.trimf(toplam_enerji.universe, [0, 0, 30])
toplam_enerji['orta'] = fuzz.trimf(toplam_enerji.universe, [20, 50, 80])
toplam_enerji['yuksek'] = fuzz.trimf(toplam_enerji.universe, [70, 100, 100])

tasarruf_seviyesi['dusuk'] = fuzz.trimf(tasarruf_seviyesi.universe, [0, 0, 30])
tasarruf_seviyesi['orta'] = fuzz.trimf(tasarruf_seviyesi.universe, [20, 50, 80])
tasarruf_seviyesi['yuksek'] = fuzz.trimf(tasarruf_seviyesi.universe, [70, 100, 100])

kullanim_suresi['az'] = fuzz.trimf(kullanim_suresi.universe, [0, 0, 1])
kullanim_suresi['orta'] = fuzz.trimf(kullanim_suresi.universe, [0.5, 1.5, 2])
kullanim_suresi['cok'] = fuzz.trimf(kullanim_suresi.universe, [1.5, 2.5, 3])

# Kurallar
kural1 = ctrl.Rule(zaman['uzun'] & enerji_kullanimi['yuksek'] & mevsimsel['kis'],
                   (tasarruf_seviyesi['yuksek'], kullanim_suresi['az']))
kural2 = ctrl.Rule(kullanma_orani['cok'] & toplam_enerji['yuksek'] & mevsimsel['yaz'],
                   (tasarruf_seviyesi['orta'], kullanim_suresi['orta']))
kural3 = ctrl.Rule(zaman['kisa'] & toplam_enerji['dusuk'],
                   (tasarruf_seviyesi['dusuk'], kullanim_suresi['cok']))

# Kontrol Sistemi
energy_ctrl = ctrl.ControlSystem([kural1, kural2, kural3])
sim = ctrl.ControlSystemSimulation(energy_ctrl)

def hesapla_tasarruf(zaman_val, kullanma_val, enerji_val, mevsim_val, toplam_val, show_graph=False):
    sim.input['zaman'] = zaman_val
    sim.input['kullanma_orani'] = kullanma_val
    sim.input['enerji_kullanimi'] = enerji_val
    sim.input['mevsimsel'] = mevsim_val
    sim.input['toplam_enerji'] = toplam_val

    sim.compute()

    tasarruf = sim.output['tasarruf_seviyesi']
    kullanim = sim.output['kullanim_suresi']

    if show_graph:
        plt.figure(figsize=(6, 3))
        tasarruf_seviyesi.view(sim=sim)
        plt.title("Tasarruf Seviyesi")

        plt.figure(figsize=(6, 3))
        kullanim_suresi.view(sim=sim)
        plt.title("Kullanım Süresi")
        plt.tight_layout()
        plt.show()

    return tasarruf, kullanim
