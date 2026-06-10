"""
🚴 SURVEILLANCE VELO'V - Théophile Jomier
📍 22 rue du Mail, 69004 Lyon
🎯 Stations: AVEYRON-1036, PLACE BERTONE-4005, PLACE COMMANDANT ARNAUD-4003, 4022-PLACE DE LA CROIX-ROUSSE
"""

import requests
import time
from datetime import datetime

# ============================================
# ⚠️  REMPLACE PAR TON URL WEBHOOK PUSHCU
# ============================================
PUSHCUT_WEBHOOK_URL = "https://pushcut.io/webhook/YOUR_TOKEN_HERE"

# Tes 4 stations Vélo'v
STATIONS_CIBLEES = ["1036", "4005", "4003", "4022"]

# Noms des stations
NOMS_STATIONS = {
    "1036": "AVEYRON",
    "4005": "PLACE BERTONE",
    "4003": "PLACE COMMANDANT ARNAUD",
    "4022": "PLACE DE LA CROIX-ROUSSE"
}

# Check toutes les 2 minutes
INTERVALE_CHECK = 120

# API Vélo'v
API_VEOLOV_URL = "https://transport.data.gouv.fr/api/v1/stations/gbfs/velov/realtime"


def check_velos_disponibles():
    try:
        print(f"\n🔍 [{datetime.now().strftime('%H:%M:%S')}] Check API...")
        
        response = requests.get(API_VEOLOV_URL, timeout=10)
        
        if response.status_code != 200:
            return []
        
        data = response.json()
        velos_dispo = []
        
        for station in data.get("stations", []):
            station_id = station.get("id")
            
            if station_id in STATIONS_CIBLEES:
                vélos = station.get("available_bikes", 0)
                
                if vélos > 0:
                    velos_dispo.append({
                        "id": station_id,
                        "nom": NOMS_STATIONS.get(station_id, station_id),
                        "vélos": vélos,
                        "adresse": station.get("address", "Lyon")
                    })
        
        return velos_dispo
    
    except Exception as e:
        print(f"❌ Erreur: {e}")
        return []


def send_pushcut_notification(velos_dispo):
    try:
        station = velos_dispo[0]
        message = f"🚴 {station['vélos']} vélo(s) mécanique(s) disponible(s)!"
        detail = f"Station: {station['nom']} ({station['adresse']})"
        
        print(f"📱 NOTIFICATION: {message}")
        
        webhook_data = {
            "title": "Velo'v Disponible !",
            "message": message,
            "detail": detail,
            "priority": 5
        }
        
        response = requests.post(PUSHCUT_WEBHOOK_URL, json=webhook_data, timeout=10)
        print(f"✅ Status: {response.status_code}")
    
    except Exception as e:
        print(f"❌ Erreur: {e}")


def main():
    print("=" * 60)
    print("🚴 SURVEILLANCE VELO'V")
    print("📍 22 rue du Mail, 69004 Lyon")
    print(f"🎯 Stations: {', '.join(NOMS_STATIONS.values())}")
    print("=" * 60)
    print(f"\n⏰ Check toutes {INTERVALE_CHECK}s")
    print("\n🚀 START!\n")
    
    while True:
        try:
            velos_dispo = check_velos_disponibles()
            
            if len(velos_dispo) > 0:
                print(f"\n🎉 {len(velos_dispo)} station(s) avec vélos :")
                for v in velos_dispo:
                    print(f"   • {v['nom']}: {v['vélos']} vélo(s)")
                send_pushcut_notification(velos_dispo)
            else:
                print("   → Aucun vélo")
            
            time.sleep(INTERVALE_CHECK)
        
        except KeyboardInterrupt:
            print("\n🛑 Stop")
            break
        except Exception as e:
            print(f"\n❌ Erreur: {e}")
            time.sleep(INTERVALE_CHECK)


if __name__ == "__main__":
    if PUSHCUT_WEBHOOK_URL == "https://api.pushcut.io/NIS09nfMIkU2vDwjeHveK/notifications/V%C3%A9lo%E2%80%99v%20":
        print("⚠️  REMPLACE PUSHCUT_WEBHOOK_URL par ton URL !")
        print("   → pushcut.io → notification → webhook URL")
        print()
    
    main()
