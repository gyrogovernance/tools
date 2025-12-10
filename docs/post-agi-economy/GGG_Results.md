CGM Scenario Runner
==========

==========
CGM Constants
==========

Q_G = 4π = 12.566371
m_a = 1/(2√(2π)) = 0.199471140201
δ_BU = 0.195342176580 rad
A* = 1 - δ_BU/m_a = 0.020700
δ_BU/m_a = 0.979300

S_CS = 7.874805
S_UNA = 3.544908
S_ONA = 3.937402
S_BU = 0.199471

w_CS = 0.512779
w_UNA = 0.230832
w_ONA = 0.256389
w_BU = 0.012822

κ₀ = 1/(2Q_G) = 0.039789
κ(dt=1) = 0.199471

Verification: Q_G × m_a² = 0.500000 (expect 0.5)
==========

==========
Time Scales (dt interpretations)
==========

atomic cycle    : Caesium-133 hyperfine transition period
                  (period ≈ 1.09e-10 s)
day             : 1 Earth rotation
4 days          : 1 domain cycle (4 Earth rotations)
year            : 1 Solar gyration
                  (≈ 365.25 days)

Simulation steps are dimensionless.
Choose time scale based on governance context.
==========

==========
Scenario 1: Weak coupling (kappa=0.5)
==========

Step   Time (steps) SI_Econ    SI_Emp     SI_Edu     SI_Ecol
------ ------------ ---------- ---------- ---------- ----------
0      0.00         13.80      17.25      11.50      100.00
20     20.00        43.11      60.95      32.12      99.58     
40     40.00        69.47      95.19      55.61      99.76     
60     60.00        81.42      86.90      75.69      99.89     
80     80.00        87.31      90.12      88.88      99.96     
100    100.00       91.37      94.47      95.71      99.98     

Final: SI_Econ=91.37
Final Lyapunov: V_CGM=0.164, V_stage=0.158, V_apert=0.006657

==========
Scenario 2: Canonical coupling (kappa=1.0)
==========

Step   Time (steps) SI_Econ    SI_Emp     SI_Edu     SI_Ecol
------ ------------ ---------- ---------- ---------- ----------
0      0.00         13.80      17.25      11.50      100.00
20     20.00        62.01      98.71      47.68      99.63     
40     40.00        83.16      88.28      83.21      99.89     
60     60.00        92.93      96.61      97.45      99.97     
80     80.00        97.67      99.50      99.74      99.99     
100    100.00       99.29      98.66      99.47      100.00    

Final: SI_Econ=99.29
Final Lyapunov: V_CGM=0.168, V_stage=0.168, V_apert=0.000130

==========
Time to SI >= 95 (canonical scenario, κ=1.0):
==========
- Econ:
  67 steps interpreted as:
    atomic cycle   : ≈ 7.29e-09 s
    day            : ≈ 67.0 days
    4 days         : ≈ 268.0 days
    year           : ≈ 67.00 years
- Emp:
  19 steps interpreted as:
    atomic cycle   : ≈ 2.07e-09 s
    day            : ≈ 19.0 days
    4 days         : ≈ 76.0 days
    year           : ≈ 19.00 years
- Edu:
  54 steps interpreted as:
    atomic cycle   : ≈ 5.87e-09 s
    day            : ≈ 54.0 days
    4 days         : ≈ 216.0 days
    year           : ≈ 54.00 years
Note: These interpretations are optional. The simulator runs in
dimensionless steps. Time scales are provided only as possible
mappings for governance contexts.
==========

==========
Scenario 3: Strong coupling (kappa=2.0)
==========

Step   Time (steps) SI_Econ    SI_Emp     SI_Edu     SI_Ecol
------ ------------ ---------- ---------- ---------- ----------
0      0.00         13.80      17.25      11.50      100.00
20     20.00        76.35      85.36      74.25      99.75     
40     40.00        97.02      99.47      99.35      99.96     
60     60.00        99.83      98.96      99.16      100.00    
80     80.00        99.50      99.38      99.09      100.00    
100    100.00       99.39      99.55      99.26      100.00    

Final: SI_Econ=99.39
Final Lyapunov: V_CGM=0.186, V_stage=0.185, V_apert=0.000057

==========
Scenario 4: Low aperture (below A*)
==========

Step   Time (steps) SI_Econ    SI_Emp     SI_Edu     SI_Ecol
------ ------------ ---------- ---------- ---------- ----------
0      0.00         24.16      38.65      19.32      100.00
20     20.00        28.70      58.59      40.54      99.52     
40     40.00        56.82      93.12      76.16      99.65     
60     60.00        76.02      94.90      94.47      99.81     
80     80.00        87.48      89.56      97.75      99.90     
100    100.00       93.86      85.84      95.09      99.94     

Final: SI_Econ=93.86
Final Lyapunov: V_CGM=0.158, V_stage=0.143, V_apert=0.014931

==========
Scenario 5: Asymmetric initial conditions
==========

Step   Time (steps) SI_Econ    SI_Emp     SI_Edu     SI_Ecol
------ ------------ ---------- ---------- ---------- ----------
0      0.00         48.31      20.70      100.00     100.00    
20     20.00        77.59      51.82      47.56      99.83     
40     40.00        63.40      81.69      79.50      99.90     
60     60.00        72.99      96.68      97.02      99.94     
80     80.00        83.39      95.72      95.45      99.96     
100    100.00       90.42      91.74      92.84      99.97     

Final: SI_Econ=90.42
Final Lyapunov: V_CGM=0.098, V_stage=0.086, V_apert=0.011545

==========
Scenario 6: Initialized at A* (equilibrium)
==========

Step   Time (steps) SI_Econ    SI_Emp     SI_Edu     SI_Ecol
------ ------------ ---------- ---------- ---------- ----------
0      0.00         100.00     100.00     100.00     100.00
20     20.00        38.62      47.37      47.98      99.87     
40     40.00        62.23      83.87      79.74      99.88     
60     60.00        77.19      99.66      96.79      99.92     
80     80.00        87.33      93.30      95.87      99.95     
100    100.00       93.43      89.61      93.36      99.96     

Final: SI_Econ=93.43
Final Lyapunov: V_CGM=0.107, V_stage=0.096, V_apert=0.010683

==========
Scenario 7: Uniform stage weights (null model)
==========

Step   Time (steps) SI_Econ    SI_Emp     SI_Edu     SI_Ecol
------ ------------ ---------- ---------- ---------- ----------
0      0.00         13.80      17.25      11.50      100.00
20     20.00        47.05      79.05      35.60      99.95     
40     40.00        73.94      96.38      74.91      99.98     
60     60.00        89.83      95.92      96.45      100.00    
80     80.00        97.75      98.34      98.72      100.00    
100    100.00       99.63      99.66      98.85      100.00    

Final: SI_Econ=99.63
Final Lyapunov: V_CGM=0.111, V_stage=0.111, V_apert=0.000079

==========
Long-Horizon Stability Test (1000 steps, κ=1.0)
==========
Post-transient statistics (t >= 200):
  Max deviation from A*: 2.46e-04
    (Econ: 1.92e-04, Emp: 1.07e-04, Edu: 2.46e-04)
  SI minimum values: Econ=99.08, Emp=99.49, Edu=98.83
  Overall SI min: 98.83

Final state (t=1000):
  Apertures:
    A_Econ = 0.020724
    A_Emp  = 0.020702
    A_Edu  = 0.020703
  Superintelligence indices:
    SI_Econ = 99.88
    SI_Emp  = 99.99
    SI_Edu  = 99.98
  SI range: [98.83, 99.99]
  SI mean: 99.68
  V_CGM: 0.195449

==========

==========
Exporting results...
Results exported to d:\Development\tools\research\prevention\simulator\results/
==========

==========
Summary - SI Values
==========
Scenario                               kappa    SI_Econ     SI_Emp     SI_Edu    SI_Ecol     
----------
1. Weak coupling                         0.5      91.37      94.47      95.71      99.98     
2. Canonical coupling                    1.0      99.29      98.66      99.47     100.00     
3. Strong coupling                       2.0      99.39      99.55      99.26     100.00     
4. Low aperture start                    1.0      93.86      85.84      95.09      99.94     
5. Asymmetric                            1.0      90.42      91.74      92.84      99.97     
6. At A* (equilibrium)                   1.0      93.43      89.61      93.36      99.96     
7. Uniform weights (null)                1.0      99.63      99.66      98.85     100.00     
----------
Target                                    --     100.00     100.00     100.00     100.00     
==========

==========
Summary - Apertures
==========
Scenario                               kappa     A_Econ      A_Emp      A_Edu     A_Ecol     
----------
1. Weak coupling                         0.5     0.0227     0.0196     0.0216     0.0207     
2. Canonical coupling                    1.0     0.0208     0.0210     0.0208     0.0207     
3. Strong coupling                       2.0     0.0208     0.0208     0.0209     0.0207     
4. Low aperture start                    1.0     0.0194     0.0241     0.0218     0.0207     
5. Asymmetric                            1.0     0.0187     0.0226     0.0223     0.0207     
6. At A* (equilibrium)                   1.0     0.0193     0.0231     0.0222     0.0207
7. Uniform weights (null)                1.0     0.0206     0.0206     0.0205     0.0207     
----------
Target A*                                 --     0.0207     0.0207     0.0207     0.0207     
==========

==========
Summary - Displacement Measures
==========
Scenario                               kappa        GTD        IVD        IAD        IID     
----------
1. Weak coupling                         0.5     0.4167     0.2239     0.0462     0.2987     
2. Canonical coupling                    1.0     0.4421     0.2181     0.0370     0.3013     
3. Strong coupling                       2.0     0.4794     0.2151     0.0270     0.3068     
4. Low aperture start                    1.0     0.2042     0.0889     0.0620     0.4830
5. Asymmetric                            1.0     0.1984     0.0734     0.0530     0.3528     
6. At A* (equilibrium)                   1.0     0.2042     0.0850     0.0523     0.3745     
7. Uniform weights (null)                1.0     0.3906     0.1842     0.0107     0.1896     
----------
Target                                    --     0.0000     0.0000     0.0000     0.0000     
==========

==========
Summary - Lyapunov Values
==========
Scenario                               kappa      V_CGM    V_stage      V_apert
----------
1. Weak coupling                         0.5      0.164      0.158     0.006657
2. Canonical coupling                    1.0      0.168      0.168     0.000130
3. Strong coupling                       2.0      0.186      0.185     0.000057
4. Low aperture start                    1.0      0.158      0.143     0.014931
5. Asymmetric                            1.0      0.098      0.086     0.011545
6. At A* (equilibrium)                   1.0      0.107      0.096     0.010683
7. Uniform weights (null)                1.0      0.111      0.111     0.000079
----------
Target                                    --      0.000      0.000     0.000000
==========

==========
Summary - Final Stage Profiles
==========
Scenario                            Domain     Stg1     Stg2     Stg3     Stg4
----------
1. Weak coupling                    Econ      0.088    0.472    0.308    0.395
                                    Emp       0.090    0.444    0.296    0.170
                                    Edu       0.090    0.440    0.293    0.370
----------
2. Canonical coupling               Econ      0.064    0.447    0.291    0.390
                                    Emp       0.064    0.444    0.289    0.203
                                    Edu       0.064    0.446    0.290    0.350
----------
3. Strong coupling                  Econ      0.027    0.445    0.281    0.378
                                    Emp       0.027    0.441    0.279    0.253
                                    Edu       0.027    0.443    0.280    0.328
----------
4. Low aperture start               Econ      0.311    0.337    0.333    0.763
                                    Emp       0.295    0.303    0.302    0.099
                                    Edu       0.300    0.310    0.310    0.625
----------
5. Asymmetric                       Econ      0.314    0.314    0.318    0.509
                                    Emp       0.304    0.293    0.299    0.104
                                    Edu       0.305    0.296    0.302    0.484
----------
6. At A* (equilibrium)              Econ      0.308    0.327    0.318    0.579
                                    Emp       0.298    0.304    0.297    0.102
                                    Edu       0.300    0.308    0.301    0.481
----------
7. Uniform weights (null)           Econ      0.114    0.409    0.262    0.201
                                    Emp       0.116    0.415    0.265    0.204
                                    Edu       0.116    0.413    0.265    0.203
----------

==========
Summary - V_stage by Domain
==========
Scenario                               kappa     Econ      Emp      Edu     Ecol
----------
1. Weak coupling                         0.5    0.000    0.000    0.000    0.000
2. Canonical coupling                    1.0    0.000    0.000    0.000    0.000
3. Strong coupling                       2.0    0.000    0.000    0.000    0.000
4. Low aperture start                    1.0    0.000    0.000    0.000    0.000
5. Asymmetric                            1.0    0.000    0.000    0.000    0.000
6. At A* (equilibrium)                   1.0    0.000    0.000    0.000    0.000
7. Uniform weights (null)                1.0    0.000    0.000    0.000    0.000
----------

==========
Summary - V_apert by Domain
==========
Scenario                               kappa     Econ      Emp      Edu     Ecol
----------
1. Weak coupling                         0.5 0.004077 0.001618 0.000962 0.000000
2. Canonical coupling                    1.0 0.000025 0.000091 0.000014 0.000000
3. Strong coupling                       2.0 0.000019 0.000010 0.000028 0.000000
4. Low aperture start                    1.0 0.002009 0.011655 0.001267 0.000000
5. Asymmetric                            1.0 0.005066 0.003718 0.002761 0.000000
6. At A* (equilibrium)                   1.0 0.002306 0.006017 0.002360 0.000000
7. Uniform weights (null)                1.0 0.000007 0.000006 0.000067 0.000000
----------

==========
Summary - Ecology Components (BU Vertex)
==========
Scenario                               kappa      E_gov     E_info      E_inf    E_intel     
----------
1. Weak coupling                         0.5     0.4976     0.2325     0.2541     0.0190     
2. Canonical coupling                    1.0     0.4971     0.2324     0.2539     0.0191     
3. Strong coupling                       2.0     0.4963     0.2323     0.2537     0.0192
4. Low aperture start                    1.0     0.5020     0.2297     0.2544     0.0228     
5. Asymmetric                            1.0     0.5021     0.2294     0.2542     0.0201     
6. At A* (equilibrium)                   1.0     0.5020     0.2296     0.2542     0.0206     
7. Uniform weights (null)                1.0     0.4981     0.2317     0.2533     0.0167     
----------

Note: SI_Ecol measures structural coherence (dominated by canonical memory).
      Displacement measures: GTD=Governance Traceability, IVD=Information Variety,
      IAD=Inference Accountability, IID=Intelligence Integrity.
      V_CGM = total Lyapunov potential, V_stage = stage-profile displacement,
      V_apert = aperture deviation sum.
      Stage profiles show internal domain configuration (CS, UNA, ONA, BU stages).
      Ecology components show BU-vertex stage balance from BU dual combination.
==========

(.venv) PS D:\Development\tools> & d:/Development/tools/.venv/Scripts/python.exe d:/Development/tools/research/prevention/simulator/historical_timeline.py
==========
Milestones
==========
1956: A=0.950, SI=2.2 (Dartmouth conference)
1997: A=0.700, SI=3.0 (Deep Blue)
2016: A=0.400, SI=5.2 (AlphaGo)
2020: A=0.250, SI=8.3 (GPT-3 release)
2023: A=0.150, SI=13.8 (LLM adoption)
2025: A=0.120, SI=17.2 (Present)

==========
SI Thresholds
==========
A* = 0.0207
  threshold_90: A=0.0500, SI=41.4
  threshold_95: A=0.0300, SI=69.0
  canonical: A=0.0207, SI=100.0

==========
Calibration
==========
Interval: 1956 -> 2025
Aperture: 0.95 -> 0.12
κ: 0.1
Steps: 23
years_per_step: 3.000

==========
Projections (SI >= 95)
==========
Initial: A=0.12, year=2025

κ=0.5:
  years_per_step: 0.600
  Steps: 16
  Year: 2034

κ=1.0:
  years_per_step: 0.300
  Steps: 10
  Year: 2028

κ=2.0:
  years_per_step: 0.150
  Steps: 5
  Year: 2025

κ=5.0:
  years_per_step: 0.060
  Steps: 53
  Year: 2028

==========
Parameters
==========
A* = 0.0207
κ_calibration = 0.1
years_per_step_base = 3.000