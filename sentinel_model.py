import numpy as np

# Monsoon & Landslide Sentinel - NISAR & SRTM Slope Instability Model
# Team Aithra | NASA Space Apps Challenge 2026 (Dancing with the SARs)

def compute_landslide_risk(nisar_displacement_cm, soil_moisture_delta, slope_deg, rainfall_24h_mm):
    """
    Fuses NISAR L-band ground displacement & moisture shifts with
    NASA SRTM slope angle and NASA GPM IMERG 24-hour rainfall.
    """
    # Normalize physical risk indicators (0.0 to 1.0 scale)
    disp_factor = min(abs(nisar_displacement_cm) / 5.0, 1.0)      # >= 5 cm shift = max risk
    moisture_factor = min(max(soil_moisture_delta, 0.0) / 0.35, 1.0)
    slope_factor = min(max(slope_deg - 15.0, 0.0) / 30.0, 1.0)    # Slopes > 15 deg susceptible
    rain_factor = min(rainfall_24h_mm / 150.0, 1.0)               # >= 150 mm/24h extreme trigger

    # Weighted Physical Instability Index
    risk_score = (0.35 * disp_factor) + (0.25 * slope_factor) + (0.25 * rain_factor) + (0.15 * moisture_factor)
    
    if risk_score >= 0.70:
        alert = "HIGH RISK - Immediate Slope Evacuation Warning"
    elif risk_score >= 0.40:
        alert = "MODERATE RISK - Active Radar & Rainfall Monitoring"
    else:
        alert = "LOW RISK - Stable Terrain"
        
    return round(risk_score, 3), alert

if __name__ == "__main__":
    # Sample Case Study: Steep Western Ghats terrain during heavy monsoon pass
    score, status = compute_landslide_risk(
        nisar_displacement_cm=3.8,
        soil_moisture_delta=0.28,
        slope_deg=34.0,
        rainfall_24h_mm=135.0
    )
    print(f"Instability Index: {score} | Status: {status}")
