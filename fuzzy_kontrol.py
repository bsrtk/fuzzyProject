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
kullanim_suresi = ctrl.Consequent(np.arange(0, 3, 1), 'kullanim_suresi')

# Üyelik fonksiyonları
mevsimsel.automf(3, names=["yaz", "kis", "bahar"])
toplam_enerji.automf(3, names=["dusuk", "orta", "yuksek"])
zaman.automf(3, names=["kisa", "orta", "uzun"])
kullanma_orani.automf(3, names=["az", "orta", "cok"])
enerji_kullanimi.automf(3, names=["dusuk", "orta", "yuksek"])
tasarruf_seviyesi.automf(3, names=["dusuk", "orta", "yuksek"])
kullanim_suresi.automf(3, names=["az", "orta", "cok"])

# Kurallar
kural1 = ctrl.Rule(zaman['uzun'] & enerji_kullanimi['yuksek'] & mevsimsel['kis'],
                   (tasarruf_seviyesi['yuksek'], kullanim_suresi['az']))
kural2 = ctrl.Rule(kullanma_orani['cok'] & toplam_enerji['yuksek'] & mevsimsel['yaz'],
                   (tasarruf_seviyesi['orta'], kullanim_suresi['orta']))
kural3 = ctrl.Rule(zaman['kisa'] & toplam_enerji['dusuk'],
                   (tasarruf_seviyesi['dusuk'], kullanim_suresi['cok']))

energy_ctrl = ctrl.ControlSystem([kural1, kural2, kural3])
energy_simulation = ctrl.ControlSystemSimulation(energy_ctrl)


def hesapla_tasarruf(zaman_val, kullanma_val, enerji_val, mevsim_val, toplam_val, show_graph=False):
    sim = ctrl.ControlSystemSimulation(energy_ctrl)

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
        plt.tight_layout()

        plt.figure(figsize=(6, 3))
        kullanim_suresi.view(sim=sim)
        plt.title("Kullanım Süresi")
        plt.tight_layout()
        plt.show()

    return tasarruf, kullanim

