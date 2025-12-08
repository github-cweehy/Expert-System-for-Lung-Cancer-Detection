(deftemplate MAIN::patient
   (slot age-group)
   (slot smoking)
   (slot exposure)
   (slot breathing-issue)
   (slot chest-tightness)
   (slot family-history)
   (slot long-term-illness))

(deftemplate MAIN::risk-assessment
   (slot risk-level)
   (slot explanation))

(defrule MAIN::high-risk-1
   (declare (salience 40))
   (not (risk-assessment (risk-level ?l)))
   (patient (smoking yes) (breathing-issue yes) (chest-tightness yes))
   =>
   (assert (risk-assessment (risk-level high) (explanation "High risk based on smoking and severe respiratory symptoms. Please seek immediate medical consultation."))))

(defrule MAIN::high-risk-2
   (declare (salience 40))
   (not (risk-assessment (risk-level ?l)))
   (patient (smoking yes) (family-history yes) (breathing-issue yes))
   =>
   (assert (risk-assessment (risk-level high) (explanation "High risk due to smoking, family history and breathing issues. Further screening is strongly recommended."))))

(defrule MAIN::high-risk-3
   (declare (salience 40))
   (not (risk-assessment (risk-level ?l)))
   (patient (exposure yes) (long-term-illness yes) (breathing-issue yes))
   =>
   (assert (risk-assessment (risk-level high) (explanation "High risk due to long-term illness, environmental exposure and breathing problems. Please consult a specialist as soon as possible."))))

(defrule MAIN::high-risk-4
   (declare (salience 40))
   (not (risk-assessment (risk-level ?l)))
   (patient (age-group old) (breathing-issue yes) (chest-tightness yes))
   =>
   (assert (risk-assessment (risk-level high) (explanation "High risk in older age with significant respiratory symptoms. Immediate medical assessment is recommended."))))

(defrule MAIN::high-risk-5
   (declare (salience 35))
   (not (risk-assessment (risk-level ?l)))
   (patient (breathing-issue yes) (chest-tightness yes) (smoking ?s) (exposure ?e) (family-history ?f) (long-term-illness ?ill))
   (test (or (eq ?s yes) (eq ?e yes) (eq ?f yes) (eq ?ill yes)))
   =>
   (assert (risk-assessment (risk-level high) (explanation "High risk based on severe respiratory symptoms combined with at least one major risk factor. Please seek urgent medical attention."))))

(defrule MAIN::high-risk-6
   (declare (salience 35))
   (not (risk-assessment (risk-level ?l)))
   (patient (age-group middle|old) (breathing-issue yes) (chest-tightness yes))
   =>
   (assert (risk-assessment (risk-level high) (explanation "High risk due to severe respiratory symptoms. Even without known risk factors, urgent medical evaluation is advised."))))

(defrule MAIN::medium-risk-1
   (declare (salience 25))
   (not (risk-assessment (risk-level ?l)))
   (patient (smoking no) (breathing-issue yes) (chest-tightness no|yes))
   =>
   (assert (risk-assessment (risk-level medium) (explanation "Moderate risk due to respiratory symptoms even without smoking history. You should consult a healthcare professional."))))

(defrule MAIN::medium-risk-2
   (declare (salience 25))
   (not (risk-assessment (risk-level ?l)))
   (patient (smoking yes) (exposure yes) (breathing-issue no) (chest-tightness no))
   =>
   (assert (risk-assessment (risk-level medium) (explanation "Moderate long-term risk due to smoking and environmental exposure. Consider lifestyle changes and regular screening."))))

(defrule MAIN::medium-risk-3
   (declare (salience 25))
   (not (risk-assessment (risk-level ?l)))
   (patient (age-group old) (long-term-illness yes) (breathing-issue no|yes) (chest-tightness no))
   =>
   (assert (risk-assessment (risk-level medium) (explanation "Moderate risk due to age and existing long-term illness. Regular follow-up with a doctor is recommended."))))

(defrule MAIN::medium-risk-4
   (declare (salience 25))
   (not (risk-assessment (risk-level ?l)))
   (patient (family-history yes) (exposure yes) (breathing-issue no) (chest-tightness no))
   =>
   (assert (risk-assessment (risk-level medium) (explanation "Moderate risk because of family history and environmental exposure. Consider screening and monitoring of symptoms."))))

(defrule MAIN::medium-risk-5
   (declare (salience 22))
   (not (risk-assessment (risk-level ?l)))
   (patient (smoking yes) (breathing-issue no) (chest-tightness no) (family-history no) (long-term-illness no))
   =>
   (assert (risk-assessment (risk-level medium) (explanation "Moderate long-term risk due to smoking even without current symptoms. Quitting smoking and routine check-ups are strongly advised."))))

(defrule MAIN::medium-risk-6
   (declare (salience 22))
   (not (risk-assessment (risk-level ?l)))
   (patient (smoking no) (family-history no) (long-term-illness no) (exposure yes) (breathing-issue no) (chest-tightness no))
   =>
   (assert (risk-assessment (risk-level medium) (explanation "Moderate long-term risk due to sustained environmental exposure. Limiting exposure and periodic screening are recommended."))))

(defrule MAIN::medium-risk-7
   (declare (salience 22))
   (not (risk-assessment (risk-level ?l)))
   (patient (long-term-illness yes) (breathing-issue no) (chest-tightness no))
   =>
   (assert (risk-assessment (risk-level medium) (explanation "Moderate risk due to existing long-term illness even without acute symptoms. Continuous medical follow-up is important."))))

(defrule MAIN::medium-risk-8
   (declare (salience 22))
   (not (risk-assessment (risk-level ?l)))
   (patient (breathing-issue no) (chest-tightness yes) (smoking ?s) (exposure ?e) (family-history ?f) (long-term-illness ?ill))
   (test (or (eq ?s yes) (eq ?e yes) (eq ?f yes) (eq ?ill yes)))
   =>
   (assert (risk-assessment (risk-level medium) (explanation "Moderate risk due to chest discomfort combined with at least one risk factor. A check-up is recommended."))))

(defrule MAIN::low-risk-1
   (declare (salience 15))
   (not (risk-assessment (risk-level ?l)))
   (patient (smoking no) (breathing-issue no) (chest-tightness no) (family-history no))
   =>
   (assert (risk-assessment (risk-level low) (explanation "Low risk based on your answers. Maintain a healthy lifestyle and regular check-ups."))))

(defrule MAIN::low-risk-2
   (declare (salience 15))
   (not (risk-assessment (risk-level ?l)))
   (patient (age-group young) (smoking no) (exposure no) (breathing-issue no) (chest-tightness no) (long-term-illness no))
   =>
   (assert (risk-assessment (risk-level low) (explanation "Low current risk. Continue avoiding smoking and high pollution exposure to keep your lungs healthy."))))

(defrule MAIN::low-risk-3
   (declare (salience 15))
   (not (risk-assessment (risk-level ?l)))
   (patient (age-group middle) (smoking no) (exposure no) (family-history no) (long-term-illness no) (breathing-issue no) (chest-tightness no))
   =>
   (assert (risk-assessment (risk-level low) (explanation "Low risk profile. Maintaining current habits and periodic health checks is recommended."))))

(defrule MAIN::low-risk-4
   (declare (salience 12))
   (not (risk-assessment (risk-level ?l)))
   (patient (smoking no) (exposure no) (breathing-issue no) (chest-tightness no) (long-term-illness no) (family-history yes))
   =>
   (assert (risk-assessment (risk-level low) (explanation "Currently low symptom burden but with family history. Staying alert for new symptoms and regular screening is advised."))))

(defrule MAIN::default-risk
   (declare (salience 0))
   (not (risk-assessment (risk-level ?level)))
   (patient)
   =>
   (assert (risk-assessment (risk-level medium) (explanation "Risk cannot be clearly determined from the given information. Please consult a healthcare professional for proper assessment."))))

