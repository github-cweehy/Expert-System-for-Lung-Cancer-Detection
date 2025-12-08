# engine.py
import clips
import logging

# Create global environment
logging.basicConfig(level=logging.INFO,format='%(message)s')
env = clips.Environment()
router = clips.LoggingRouter()
env.add_router(router)

# Build templates
env.build("""
(deftemplate patient
  (slot age-group)
  (slot smoking)
  (slot exposure)
  (slot breathing-issue)
  (slot chest-tightness)
  (slot family-history)
  (slot long-term-illness)
)
""")

env.build("""
(deftemplate risk-assessment
  (slot risk-level)
  (slot explanation)
)
""")

# Build Rules

# High risk 

# H1: smoker + breathing issue + chest tightness 
env.build("""
(defrule high-risk-1
  (declare (salience 40))
  (not (risk-assessment (risk-level ?l)))
  (patient (smoking yes)
           (breathing-issue yes)
           (chest-tightness yes))
=>
  (assert (risk-assessment
    (risk-level high)
    (explanation "High risk based on smoking and severe respiratory symptoms. Please seek immediate medical consultation.")))
)
""")

# H2: smoker + family history + breathing issue
env.build("""
(defrule high-risk-2
  (declare (salience 40))
  (not (risk-assessment (risk-level ?l)))
  (patient (smoking yes)
           (family-history yes)
           (breathing-issue yes))
=>
  (assert (risk-assessment
    (risk-level high)
    (explanation "High risk due to smoking, family history and breathing issues. Further screening is strongly recommended.")))
)
""")

# H3: exposure + long-term illness + breathing issue
env.build("""
(defrule high-risk-3
  (declare (salience 40))
  (not (risk-assessment (risk-level ?l)))
  (patient (exposure yes)
           (long-term-illness yes)
           (breathing-issue yes))
=>
  (assert (risk-assessment
    (risk-level high)
    (explanation "High risk due to long-term illness, environmental exposure and breathing problems. Please consult a specialist as soon as possible.")))
)
""")

# H4: older age + multiple risk factors
env.build("""
(defrule high-risk-4
  (declare (salience 40))
  (not (risk-assessment (risk-level ?l)))
  (patient (age-group old)
           (breathing-issue yes)
           (chest-tightness yes))
=>
  (assert (risk-assessment
    (risk-level high)
    (explanation "High risk in older age with significant respiratory symptoms. Immediate medical assessment is recommended.")))
)
""")

# H5: severe symptoms (breathing + chest) + ANY major risk factor
env.build("""
(defrule high-risk-5
  (declare (salience 35))
  (not (risk-assessment (risk-level ?l)))
  (patient (breathing-issue yes)
           (chest-tightness yes)
           (smoking ?s)
           (exposure ?e)
           (family-history ?f)
           (long-term-illness ?ill))
  (test (or (eq ?s yes)
            (eq ?e yes)
            (eq ?f yes)
            (eq ?ill yes)))
=>
  (assert (risk-assessment
    (risk-level high)
    (explanation "High risk based on severe respiratory symptoms combined with at least one major risk factor. Please seek urgent medical attention.")))
)
""")

# H6: severe symptoms in middle-aged / old even without known risks
env.build("""
(defrule high-risk-6
  (declare (salience 35))
  (not (risk-assessment (risk-level ?l)))
  (patient (age-group middle|old)
           (breathing-issue yes)
           (chest-tightness yes))
=>
  (assert (risk-assessment
    (risk-level high)
    (explanation "High risk due to severe respiratory symptoms. Even without known risk factors, urgent medical evaluation is advised.")))
)
""")

# Medium Risk

# M1: respiratory symptoms but non-smoker
env.build("""
(defrule medium-risk-1
  (declare (salience 25))
  (not (risk-assessment (risk-level ?l)))
  (patient (smoking no)
           (breathing-issue yes)
           (chest-tightness no|yes))
=>
  (assert (risk-assessment
    (risk-level medium)
    (explanation "Moderate risk due to respiratory symptoms even without smoking history. You should consult a healthcare professional.")))
)
""")

# M2: smoker + exposure but no current symptoms
env.build("""
(defrule medium-risk-2
  (declare (salience 25))
  (not (risk-assessment (risk-level ?l)))
  (patient (smoking yes)
           (exposure yes)
           (breathing-issue no)
           (chest-tightness no))
=>
  (assert (risk-assessment
    (risk-level medium)
    (explanation "Moderate long-term risk due to smoking and environmental exposure. Consider lifestyle changes and regular screening.")))
)
""")

# M3: older age + long-term illness, mild/no symptoms
env.build("""
(defrule medium-risk-3
  (declare (salience 25))
  (not (risk-assessment (risk-level ?l)))
  (patient (age-group old)
           (long-term-illness yes)
           (breathing-issue no|yes)
           (chest-tightness no))
=>
  (assert (risk-assessment
    (risk-level medium)
    (explanation "Moderate risk due to age and existing long-term illness. Regular follow-up with a doctor is recommended.")))
)
""")

# M4: family history + some exposure, but no strong current symptoms
env.build("""
(defrule medium-risk-4
  (declare (salience 25))
  (not (risk-assessment (risk-level ?l)))
  (patient (family-history yes)
           (exposure yes)
           (breathing-issue no)
           (chest-tightness no))
=>
  (assert (risk-assessment
    (risk-level medium)
    (explanation "Moderate risk because of family history and environmental exposure. Consider screening and monitoring of symptoms.")))
)
""")

# M5: smoker without symptoms yet
env.build("""
(defrule medium-risk-5
  (declare (salience 22))
  (not (risk-assessment (risk-level ?l)))
  (patient (smoking yes)
           (breathing-issue no)
           (chest-tightness no)
           (family-history no)
           (long-term-illness no))
=>
  (assert (risk-assessment
    (risk-level medium)
    (explanation "Moderate long-term risk due to smoking even without current symptoms. Quitting smoking and routine check-ups are strongly advised.")))
)
""")

# M6: exposure only (no symptoms, no other risks)
env.build("""
(defrule medium-risk-6
  (declare (salience 22))
  (not (risk-assessment (risk-level ?l)))
  (patient (smoking no)
           (family-history no)
           (long-term-illness no)
           (exposure yes)
           (breathing-issue no)
           (chest-tightness no))
=>
  (assert (risk-assessment
    (risk-level medium)
    (explanation "Moderate long-term risk due to sustained environmental exposure. Limiting exposure and periodic screening are recommended.")))
)
""")

# M7: long-term illness but currently no respiratory symptoms
env.build("""
(defrule medium-risk-7
  (declare (salience 22))
  (not (risk-assessment (risk-level ?l)))
  (patient (long-term-illness yes)
           (breathing-issue no)
           (chest-tightness no))
=>
  (assert (risk-assessment
    (risk-level medium)
    (explanation "Moderate risk due to existing long-term illness even without acute symptoms. Continuous medical follow-up is important.")))
)
""")

# M8: chest tightness alone with at least one risk factor
env.build("""
(defrule medium-risk-8
  (declare (salience 22))
  (not (risk-assessment (risk-level ?l)))
  (patient (breathing-issue no)
           (chest-tightness yes)
           (smoking ?s)
           (exposure ?e)
           (family-history ?f)
           (long-term-illness ?ill))
  (test (or (eq ?s yes)
            (eq ?e yes)
            (eq ?f yes)
            (eq ?ill yes)))
=>
  (assert (risk-assessment
    (risk-level medium)
    (explanation "Moderate risk due to chest discomfort combined with at least one risk factor. A check-up is recommended.")))
)
""")

# Low Risk

# L1: no smoking, no major symptoms, no family history
env.build("""
(defrule low-risk-1
  (declare (salience 15))
  (not (risk-assessment (risk-level ?l)))
  (patient (smoking no)
           (breathing-issue no)
           (chest-tightness no)
           (family-history no))
=>
  (assert (risk-assessment
    (risk-level low)
    (explanation "Low risk based on your answers. Maintain a healthy lifestyle and regular check-ups.")))
)
""")

# L2: young non-smoker, no exposure, no long-term illness
env.build("""
(defrule low-risk-2
  (declare (salience 15))
  (not (risk-assessment (risk-level ?l)))
  (patient (age-group young)
           (smoking no)
           (exposure no)
           (breathing-issue no)
           (chest-tightness no)
           (long-term-illness no))
=>
  (assert (risk-assessment
    (risk-level low)
    (explanation "Low current risk. Continue avoiding smoking and high pollution exposure to keep your lungs healthy.")))
)
""")

# L3: middle age non-smoker, no exposure, no family history, no long-term illness, no symptoms
env.build("""
(defrule low-risk-3
  (declare (salience 15))
  (not (risk-assessment (risk-level ?l)))
  (patient (age-group middle)
           (smoking no)
           (exposure no)
           (family-history no)
           (long-term-illness no)
           (breathing-issue no)
           (chest-tightness no))
=>
  (assert (risk-assessment
    (risk-level low)
    (explanation "Low risk profile. Maintaining current habits and periodic health checks is recommended.")))
)
""")

# L4: mild single risk factor without symptoms (e.g. family history only)
env.build("""
(defrule low-risk-4
  (declare (salience 12))
  (not (risk-assessment (risk-level ?l)))
  (patient (smoking no)
           (exposure no)
           (breathing-issue no)
           (chest-tightness no)
           (long-term-illness no)
           (family-history yes))
=>
  (assert (risk-assessment
    (risk-level low)
    (explanation "Currently low symptom burden but with family history. Staying alert for new symptoms and regular screening is advised.")))
)
""")

# Default rule: if no specific rule fired
env.build("""
(defrule default-risk
  (declare (salience 0))
  (not (risk-assessment (risk-level ?level)))
  (patient)
=>
  (assert (risk-assessment
    (risk-level medium)
    (explanation "Risk cannot be clearly determined from the given information. Please consult a healthcare professional for proper assessment.")))
)
""")


def infer_risk(user_inputs):

    env.reset()

    fact_str = f"""(patient
      (age-group {user_inputs['age-group']})
      (smoking {user_inputs['smoking']})
      (exposure {user_inputs['exposure']})
      (breathing-issue {user_inputs['breathing-issue']})
      (chest-tightness {user_inputs['chest-tightness']})
      (family-history {user_inputs['family-history']})
      (long-term-illness {user_inputs['long-term-illness']})
    )"""

    logging.info("Asserting fact: %s", fact_str.strip())
    env.assert_string(fact_str)
    env.run()

    risk_level = "unknown"
    explanation = "No result."

    for fact in env.facts():
        if fact.template.name == "risk-assessment":
            risk_level = fact["risk-level"]
            explanation = fact["explanation"]
            break

    logging.info("Inference result: %s - %s", risk_level, explanation)
    return risk_level, explanation

# Save the current environment to a .clp file 
env.save("rules.clp")
