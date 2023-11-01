import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl


def calculate_FLS(age_input, bp_input, chl_input, diabetes_input, chest_pain_input):
    age = ctrl.Antecedent(np.arange(0, 100, 1), 'age')
    bp = ctrl.Antecedent(np.arange(0, 250, 1), 'bp')
    chl = ctrl.Antecedent(np.arange(0, 240, 1), 'chl')
    diabetes = ctrl.Antecedent(np.arange(0, 16, 0.1), 'diabetes')
    chest_pain = ctrl.Antecedent(np.arange(0, 1, 0.1), 'chest_pain')
    # ecg = ctrl.Antecedent(np.arange(0, 100, 1), 'ecg')
    hd = ctrl.Consequent(np.arange(0, 1, 0.1), 'hd')

    age['child'] = fuzz.trapmf(age.universe, [0, 0, 12, 18])
    age['young'] = fuzz.trapmf(age.universe, [16, 21, 30, 38])
    age['old'] = fuzz.trapmf(age.universe, [36, 60, 100, 100])

    bp['low'] = fuzz.trapmf(bp.universe, [0, 0, 80, 90])
    bp['normal'] = fuzz.trapmf(bp.universe, [80, 90, 138, 140])
    bp['high'] = fuzz.trapmf(bp.universe, [138, 140, 250, 250])

    chl['optimal'] = fuzz.trapmf(chl.universe, [0, 0, 90, 95])
    chl['desirable'] = fuzz.trapmf(chl.universe, [90, 95, 120, 125])
    chl['aboveNormal'] = fuzz.trapmf(chl.universe, [120, 125, 240, 240])

    diabetes['controlled'] = fuzz.trapmf(diabetes.universe, [0, 0, 0.55, 0.6])
    diabetes['wellControlled'] = fuzz.trapmf(
        diabetes.universe, [0.55, 0.6, 7.5, 8])
    diabetes['unControlled'] = fuzz.trapmf(diabetes.universe, [7.5, 8, 16, 16])

    chest_pain['nonCardiac'] = fuzz.trapmf(
        chest_pain.universe, [0, 0, 0.3, 0.35])
    chest_pain['atypical'] = fuzz.trapmf(
        chest_pain.universe, [0.3, 0.35, 0.65, 0.7])
    chest_pain['typical'] = fuzz.trapmf(chest_pain.universe, [0.65, 0.7, 1, 1])

    # ecg['nonSignificant'] = fuzz.trapmf(ecg.universe, [0, 0, 0.3, 0.35])
    # ecg['STSegment_Depression'] = fuzz.trapmf(
    #     ecg.universe, [0.3, 0.35, 0.65, 0.7])
    # ecg['STSegment'] = fuzz.trapmf(ecg.universe, [0.65, 0.7, 1, 1])

    hd['negative'] = fuzz.trapmf(hd.universe, [0, 0, 0.2, 0.3])
    hd['borderline'] = fuzz.trapmf(hd.universe, [0.2, 0.3, 0.55, 0.6])
    hd['positive'] = fuzz.trapmf(hd.universe, [0.55, 0.6, 0.7, 0.8])
    hd['stronglyPositive'] = fuzz.trapmf(hd.universe, [0.7, 0.8, 1, 1])

    # defuzz_centroid = fuzz.defuzz(x, mfx, 'centroid')  # Same as skfuzzy.centroid
    # defuzz_bisector = fuzz.defuzz(x, mfx, 'bisector')
    # defuzz_mom = fuzz.defuzz(x, mfx, 'mom')
    # defuzz_som = fuzz.defuzz(x, mfx, 'som')
    # defuzz_lom = fuzz.defuzz(x, mfx, 'lom')

    #hd.defuzzify_method="mom"
    #hd.defuzzify_method="bisector"

    age.view()
    bp.view()
    chl.view()
    diabetes.view()
    chest_pain.view()
    

    rules = []

    rules.append(ctrl.Rule(age['child'], hd['negative']))

    rules.append(ctrl.Rule(~age['child'] &
                 chest_pain['nonCardiac'], hd['negative']))

    rules.append(ctrl.Rule(~age['child'] &
                 chest_pain['typical'], hd['stronglyPositive']))
    rules.append(ctrl.Rule(~age['child'] & chest_pain['atypical'] & bp['high'] &
                 diabetes['unControlled'] & chl['aboveNormal'], hd['stronglyPositive']))

    rules.append(
        ctrl.Rule(age['old'] & chest_pain['atypical'] & ((bp['high'] & diabetes['unControlled']) | (bp['high'] & chl['aboveNormal']) | (diabetes['unControlled'] & chl['aboveNormal'])), hd['stronglyPositive']))
    rules.append(ctrl.Rule(age['old'] & chest_pain['atypical'] & ((bp['high'] & ~diabetes['unControlled'] & ~chl['aboveNormal']) | (
        ~bp['high'] & diabetes['unControlled'] & ~chl['aboveNormal']) | (~bp['high'] & ~diabetes['unControlled'] & chl['aboveNormal'])), hd['positive']))
    rules.append(ctrl.Rule(age['old'] & chest_pain['atypical'] & ~bp['high'] &
                           ~diabetes['unControlled'] & ~chl['aboveNormal'], hd['borderline']))

    rules.append(
        ctrl.Rule(age['young'] & chest_pain['atypical'] & ((bp['high'] & diabetes['unControlled'] & ~chl['aboveNormal']) | (~bp['high'] & diabetes['unControlled'] & chl['aboveNormal']) | (bp['high'] & ~diabetes['unControlled'] & chl['aboveNormal'])), hd['positive']))
    # rules.append(
    #     ctrl.Rule(age['young'] & chest_pain['atypical'] & (bp['high'] | diabetes['unControlled'] | chl['aboveNormal']), hd['positive']))
    rules.append(ctrl.Rule(age['young'] & chest_pain['atypical'] & ((bp['high'] & ~diabetes['unControlled'] & ~chl['aboveNormal']) | (
        ~bp['high'] & diabetes['unControlled'] & ~chl['aboveNormal']) | (~bp['high'] & ~diabetes['unControlled'] & chl['aboveNormal'])), hd['borderline']))
    rules.append(ctrl.Rule(age['young'] & chest_pain['atypical'] & ~bp['high'] &
                           ~diabetes['unControlled'] & ~chl['aboveNormal'], hd['negative']))

    # rules.append(
    #     ctrl.Rule(age['old'] & chest_pain['atypical'] & bp['high'] & (diabetes['controlled'] | diabetes['wellControlled']) & (chl['optimal'] | chl['desirable']), hd['stronglyPositive']))

    output_ctrl = ctrl.ControlSystem(rules)
    output_ctrl_sys = ctrl.ControlSystemSimulation(output_ctrl)
    output_ctrl_sys.input['age'] = age_input
    output_ctrl_sys.input['bp'] = bp_input
    output_ctrl_sys.input['chl'] = chl_input
    output_ctrl_sys.input['diabetes'] = diabetes_input
    output_ctrl_sys.input['chest_pain'] = chest_pain_input
    # output_ctrl_sys.input['ecg'] = ecg_input
    output_ctrl_sys.compute()

    hd.view(sim=output_ctrl_sys)

    return output_ctrl_sys.output['hd'] * 100
