from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]

# Data folder
DATA_DIR = PROJECT_ROOT / "data"

# Physical constants 
G_SI      = 6.67430e-11          # m^3 kg^-1 s^-2
M_SUN_SI  = 1.988416e30          # kg
M_STAR_SI = 3.227471 * M_SUN_SI  # kg

# Basic conversions 
M_CM  = 1e2                 # 1 m = 100 cm
KG_G  = 1e3                 # 1 kg = 1000 g
AU_CM = 1.495978707e13      # 1 AU = 1.495978707e13 cm
CM_KM = 1e-5                # 1 cm = 1e-5 km

# Constants in cgs 
G      = G_SI * ((M_CM**3) / (KG_G)) # = 6.67430e-8 cm^3 g^-1 s^-2
M_SUN  = M_SUN_SI * KG_G             # g
M_STAR = M_STAR_SI * KG_G            # g