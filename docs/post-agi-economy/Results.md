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

==========
Exporting results...
Results exported to d:\Development\tools\research\prevention\simulator\results/
==========

==========
Summary
==========
Scenario                               kappa    SI_Econ     A_Econ    SI_Ecol   Disp_GTD     
----------
1. Weak coupling                         0.5      91.37     0.0227      99.98     0.4167     
2. Canonical coupling                    1.0      99.29     0.0208     100.00     0.4421     
3. Strong coupling                       2.0      99.39     0.0208     100.00     0.4794     
4. Low aperture start                    1.0      93.86     0.0194      99.94     0.2042     
5. Asymmetric                            1.0      90.42     0.0187      99.97     0.1984     
6. At A* (equilibrium)                   1.0      93.43     0.0193      99.96     0.2042     
7. Uniform weights (null)                1.0      99.63     0.0206     100.00     0.3906     
----------
Target: A* = 0.0207                       --     100.00     0.0207     100.00     0.0000     
==========

Note: SI_Ecol measures structural coherence (dominated by canonical memory).
      Disp_GTD = |x_deriv - x_balanced|[0] shows actual displacement.
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
  threshold_90: A=0.0500, SI=41.4 (SI >= 90)
  threshold_95: A=0.0300, SI=69.0 (SI >= 95)
  canonical: A=0.0207, SI=100.0 (A = A*)

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