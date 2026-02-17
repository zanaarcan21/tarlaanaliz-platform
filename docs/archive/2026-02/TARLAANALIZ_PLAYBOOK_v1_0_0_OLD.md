# TarlaAnaliz – Playbook (Ürün + Operasyon)
**Sürüm:** 1.0.0 | **Tarih:** 2026-02-08

## Okuma ve Çelişki Kuralı
- **Normatif (değişmez) kaynak:** `TARLAANALIZ_SSOT_v1_0_0.txt`
- Bu Playbook, SSOT’u tekrar yazmak yerine **uygulama/operasyon anlatısı** sağlar.
- Bir çelişki varsa **SSOT kazanır** (Playbook “bilgilendirici”dir).

## Bu dosya neyi birleştirir?
- Kanonik Ürün ve İşleyiş Rehberi (ürün/iş kuralları anlatısı)
- Saha ve Operasyon SOP (DJI Pilot 2 + WPML + yerel istasyon)
- İş Planı Akış Dokümanı (yalnızca özet akış görünümü)

---

# 1) Ürün ve İşleyiş (Kanonik Anlatı – Bilgilendirici)

[KR-000] Bu doküman seti nasıl okunur?
Saha adımları ve DJI entegrasyon ayrıntıları ayrı bir SOP dokümanında; geliştirici promptları, API ve test/acceptance şablonları ayrı bir geliştirici paketinde tutulur.
Kimlik modeli: Yalnızca telefon numarası + 6 haneli PIN. E-posta/TCKN toplanmaz; SMS doğrulama / tek kullanımlık kod adımı yoktur.
Notasyon: FieldID, MissionID, BatchID, ParcelRef gibi kimlikler için temel tanımlar bu dokümanda verilir; ayrıntılı teknik uçlar (endpoint, şema, prompt) Geliştirici Paketine taşınır.
Not: Doküman dilinde 'kapsama-izi' terimi kullanılır. Sistem/API tarafında aynı kavram teknik olarak 'footprint' (observed footprint) olarak geçebilir; ikisi eş anlamlıdır.
Saha SOP ve Geliştirici Paketi, aynı kuralları tekrar yazmak yerine ilgili KR etiketine referans verir (ör: 'Bkz. [KR-050]').
Bu dokümanda kanonik (normatif) kurallar, bölüm başlıklarının başında [KR-xxx] etiketi ile tanımlanır.
KR Referans Sistemi (Tek Doğru Kaynak); Kanonik içerik (İş Planı Akış Dokümanı temelli)
[KR-001] 0. Proje Özeti
Amac: Ciftcilerin urun kaybini erken uyari ile azaltmak ve donum bazli analiz hizmeti satmak. Baslangic bolgesi GAP, ardindan Turkiye geneline olcekleme.
Sabit cerceve (degismez): Drone: DJI Mavic 3M. Veri: RGB + multispektral (NDVI/NDRE). Yapay zeka sadece analiz yapar; ilaclama/gubreleme karari vermez.
Sonuclar web (PWA) uygulamasında harita uzerinde renk + desen/ikon ile gosterilir.
[KR-002] Harita katmanı anlamları (renk + desen)
Saglik (Health): Yesil
Hastalik (Disease): Turuncu
Zararli Bocek (Pest): Kirmizi
Mantar (Fungus): Mor
Yabanci Ot (Weed): Sari/Hardal + noktali desen
Su Stresi: Mavi + damla noktali desen
Azot Stresi: Soluk gri + capraz cizgili desen
 [KR-010] 1. Web (PWA)
[KR-011] 1.1 Kullanıcı rolleri ve temel yaklaşım
Rol	Sorumluluk
Ciftci	Kendi tarlalarini kaydeder, bitki turlerini tanimlar, analiz talebi olusturur, sonuclari gorur.
Kooperatif/Ureticiler birligi	Kurumsal hesapla uye olur; uye ciftcileri davet eder/aktarir; yetkisine gore tarlalari yonetir ve analiz talebi acabilir.
Drone pilotu	Sadece DJI Mavic 3M ile ucus yapar; goruntuleri her gun hafiza kartiyla yerel istasyona aktarir; sonuc raporunu gormeZ.
Il Operatoru (temsilci)	PII gormeden ticari KPI + kapasite planlama metriklerini izler; sozlesmeye gore gelir payi alir.
Merkez yonetim	KVKK/PII erisimi olan tek yetkili katman; kullanici/kooperatif dogrulama ve sistem politikalarini yonetir.
[KR-012] 1.2 İş planlaması
[KR-013] 1.2.1 Çiftçi üyeliği ve tarla yönetimi
Uyelik: PWA veya web uzerinden uye olunur. Il, ilce, ad, soyad ve telefon numarasi alinır; uye olunca kendi sayfasina yonlendirilir.
Tarla kaydi: Her tarla icin il, ilce, mahalle/koy, ada, parsel ve alan (m2) girilir. Sistem benzersiz FieldID uretir.
Tekil kayit kurali: Ayni il + ilce + mahalle/koy + ada + parsel kombinasyonu ile ayni tarla ikinci kez kaydedilemez.
Bitki turu tanimi: Her tarla icin ekili bitki turu secilir. Birden fazla bitki varsa her biri ayri secilir ve alan (m2) girilir.
Analiz talebi: Bitki turu bazinda olusturulur. Seçenekler: yillik abonelik veya tek seferlik analiz.
Bitki turu degistirme kurali: Bir tarladaki bitki turleri yilda yalnizca 1 defa degistirilebilir. Sadece 1 Ekim - 31 Aralik araliginda; tarih disinda degisiklik engellenir.
[KR-014] 1.2.2 Kooperatif/Üretici Birliği üyeliği ve işleyiş
Dogrulama: Hesap 'Onay Bekliyor' acilir. Evrak kontrolu sonrasi Merkez yonetim 'Aktif' yapar; eksik evrak varsa aktif edilemez.
Üye çiftçi dahil etme: (a) davet (QR / 6 haneli davet kodu), (b) toplu içe aktarım (Excel/CSV). Çiftçi kooperatif bağlantısını kendi hesabından onaylar.
Tarla ve analiz: Tarla benzersizligi aynidir. Kooperatif yetkisine gore uyeleri adina analiz talebi acabilir. "Tarla kaydi tekil, sahiplik/erisim ayri" yaklasimi uygulanir.
Yetki matrisi: COOP_OWNER, COOP_ADMIN, COOP_AGRONOMIST (aksiyon karari vermez), COOP_VIEWER.
[KR-015] 1.2.3 Drone pilotları (DJI Mavic 3M ile uçuş)
Uyelik/kayit: Il, ilce, ad soyad, telefon; drone modeli ve seri numarasi; hizmet verdigi mahalle/koy listesi( başlangıçta opsiyonel). Drone seri numarasi dogrulama referansidir.
Günlük veri teslimi: Uçuş çıktısı her gün hafıza kartı ile yerel istasyona aktarılır. Her uçuşta farklı hafıza kartı kullanılır. Not: DJI tarafındaki kart kilidi/şifre/PIN gibi özellikler cihaz ve sürüme göre değişebilir; güvenlik garantisi olarak değil, sadece ek katman olarak değerlendirilir.
Her aktarim log uretir: pilot kimligi, drone seri no, tarih/saat, batch id, tarla eslestirme durumu.
Eslestirme zorunlu: Yuke gelen veri seti mutlaka kayitli bir tarla ile otomatik eslesir; minimum: il, ilce, mahalle/koy, ada, parsel, bitki turu (varsa FieldID). Eslestirme yoksa islenmez.

---

## Bileşen Haritası ve Referans Kuralları (Component Map)

Bu doküman **ürün ve işleyiş anlatısını** taşır. Teknik doğruların (kural metinlerinin) tek kanonik kaynağı **SSOT**’tur.

### SSOT – Tek kanonik kayıt
- `ssot/kr_registry.md` : KR’lerin tekil normatif metni + `applies_to`
- `ssot/contracts_ssot.md` : Contracts görünümü (filtrelenmiş)
- `ssot/platform_ssot.md` : Platform görünümü
- `ssot/edgekiosk_ssot.md` : Edge-Kiosk görünümü
- `ssot/worker_ssot.md` : Worker görünümü
- `ssot/kr_aliases.md` : Tarihsel/uyumluluk eşlemeleri (örn. KR-082 ⇢ KR-018)

### Uygulama Paketi (Devpack) – “Nasıl uygularız?”
- `devpack/core.md`
- `devpack/contracts.md`
- `devpack/platform.md`
- `devpack/edgekiosk.md`
- `devpack/worker.md`

### Cross‑ref (çapraz referans) kuralı
- **KR kodu tekildir**: Aynı KR farklı dokümanda farklı anlama gelemez.
- Bu kanonik rehber, KR metnini **tekrar yazmaz**; ilgili KR’ye ve bileşen SSOT’una referans verir.
- Bir bölüm birden fazla bileşene dokunuyorsa: “Platform/Worker/Edge davranışı” alt başlığı açılır ve her biri ilgili SSOT görünümüne bağlanır.

### Alias kuralı (uyumluluk/tarihçe)
- Alias yalnızca **tarihsel etiket** içindir; normatif kural **kanonik KR** altında yaşar.
- Örnek: `[KR-082] RADIOMETRY` etiketi, kanonik metin olarak `[KR-018] Tam Radyometrik Kalibrasyon Zorunluluğu` ile eşlenir.

---

[KR-015-1] Pilot Çalışma Günleri ve Günlük Kapasite Tanımı
Amaç: Pilotların çalışacağı günleri seçebilmesi ve sistemin planlama motoruna net kapasite kısıtları sağlaması.
[ZORUNLU] Pilot, haftalık çalışma günlerini work_days olarak seçer (Pzt–Paz kümesi).
[ZORUNLU] |work_days| ≤ 6 (pilot en fazla 6 gün çalışabilir).
[ZORUNLU] Pilot için daily_capacity_donum aralığı: 2500–3000 dönüm/gün.
[ZORUNLU] Varsayılan kapasite (atanmamışsa): 2750 dönüm/gün.
[ZORUNLU] Bitki türü bazlı kapasite profili (CropOpsProfile): admin, her CropType için daily_capacity_donum (varsayılan 2750; önerilen aralık 2500–3000) ve SYSTEM_SEED_QUOTA (varsayılan 1500) değerlerini tanımlar; planlama motoru Mission.crop_type profiline göre kota/kapasite uygular.
[ZORUNLU] Kapasite aşım toleransı yalnızca “acil durum” için %10 olabilir; üst sınır: daily_capacity_donum × 1.10.
[OPSİYONEL] Pilot, sezon yoğunluğuna göre kapasiteyi “gelecek hafta geçerli olacak şekilde” güncelleyebilir (anlık değişiklik yok; operasyon stabilitesi).

[KR-015-2] Seed + Pull İş Dağıtım Politikası (Sistem Verir + Pilot/Çiftçi Seçimi)
Amaç: İlk işlerin sistem tarafından garanti edilmesi; kalan kapasitenin ise çiftçinin pilot seçimi / pilotun müşteri bulmasıyla dolması.
[ZORUNLU] Her pilot için günlük kapasite iki kotaya bölünür: SYSTEM_SEED_QUOTA ve PULL_QUOTA.
[ZORUNLU] SYSTEM_SEED_QUOTA varsayılan: 1500 dönüm/gün.
[ZORUNLU] SYSTEM_SEED_QUOTA ve PULL_QUOTA değerleri, Mission.crop_type profiline göre belirlenir (admin ayarı). Profil tanımı yoksa global varsayılanlar uygulanır.
[ZORUNLU] PULL_QUOTA varsayılan: daily_capacity_donum - 1500.
[ZORUNLU] SYSTEM_SEED görevleri: sistem otomatik atar; pilot bu kotayı reddedemez.
[ZORUNLU] PULL görevleri: çiftçi pilot seçebilir ve/veya pilot kendi işi bağlayabilir; kapasite uygunsa kabul/ret hakkı tanınabilir.
[ZORUNLU] Pilot, çiftçi PII görmeden çalışır; görevler MissionID + Field/ParcelRef + konum düzeyinde sunulur.

[KR-015-3] Pilot İptal / Uygun Değilim Bildirimi ve Otomatik Yeniden Atama
Amaç: Pilot görev yapamayacaksa zamanında bildirsin; sistem görevi başka pilota aktarsın.
[ZORUNLU] Pilot, atanmış işi yapamayacaksa en az 12 saat önce bildirir (öneri: 24 saat).
[ZORUNLU] Bildirim geldiğinde görev yeniden atama kuyruğuna alınır ve alternatif pilot atanır.
[ZORUNLU] Bildirimsiz no-show pilot güvenilirlik skorunu düşürür ve admin incelemesini tetikleyebilir.
[ZORUNLU] İptal ve yeniden atamalar audit log’a yazılır (actor, timestamp, reason, eski/yeni pilot, mission).

[KR-015-4] Admin Atama Değişikliği ve Otomatik Yeniden Dengeleme
Amaç: Sistem otomatik atar; admin gerekirse değiştirir; sistem çakışmaları otomatik toparlar.
[ZORUNLU] Admin override alanları: new_pilot_id, override_reason, admin_id (audit).
[ZORUNLU] Override sonrası sistem sadece ilgili pencereyi yeniden dengeler; admin seçimini otomatik bozmaz.

[KR-015-5] Sezonluk Abonelikte Tarama Takvimi, Görünürlük ve Sınırlı Gün Değiştirme
Amaç: Çiftçi sezon başında sıklık seçer; tüm sezon günlerini görür; sezonda 2–3 kez gün kaydırabilir; pilot onayı gerekir.
[ZORUNLU] UI terminolojisi: “Yıllık abonelik” yerine “Sezonluk Paket”.
[ZORUNLU] Çiftçi start_date, end_date, interval_days ve toplam N analiz + fiyatı görür.
[ZORUNLU] Takvim görünümü: computed schedule.
[ZORUNLU] reschedule_tokens_per_season varsayılan 2 (opsiyonel 3); her token bir gün kaydırma talebidir.
- Hava engeli (Weather Block) / force majeure nedeniyle yapılan ertelemeler **reschedule token tüketmez**; sistem otomatik yeniden planlar ve audit log’a yazar.
[ZORUNLU] Gün değiştirme akışı: çiftçi önerir; sistem slot/pilot önerir; pilota bildirim; pilot onaylarsa kesinleşir; audit log’a yazılır.

[KR-015-6] Büyük Alanlarda Çoklu Pilot Planlama (Pencere Bazlı Bölme)
Amaç: Büyük alanlarda (örn. 10.000 dönüm) 7 günlük pencere içinde birden fazla pilotla tarama yapılabilsin.
[ZORUNLU] Her interval_days penceresi için hedef tamamlanma kuralı.
[OPSİYONEL] Eşik aşılınca pencere iş paketlerine bölünebilir; aynı pencerede 2–N pilot atanabilir.
[ZORUNLU] Denetlenebilirlik: her pilot katkısı ayrı kanıt üretir; sonuç raporu tek zaman serisine birleşir.

[KR-016] Drone - Tarla - Bitki Eşleştirme Politikası (routing)
Amac: Veri setini dogru FieldID ve o tarihte gecerli bitki turu ile eslestirip dogru bitki-ozel YZ modelini otomatik secmek.
Tarla siniri: Ada/parsel girilir; TKGM/MEGSIS ile parsel geometrisi alinarak field boundary saklanir.
Ucus gorevi: Field boundary uzerinden gorev dosyasi uretilir (KML/KMZ/WPML). Pilot DJI Pilot 2 ile ice aktarip standard mapping gorevini baslatir. Pilot egitim dokumani: DJI_ENTEGRASYON_SAHA_KILAVUZU_v1.
Görev dosyası adlandırma standardı: {MissionID}_{ParcelRef}_{YYYYMMDD}.kmz (dosya adında PII bulunmaz; MissionID dosya adında ve metadata içinde yer alır).
Islenmis ciktilar: DJI Terra (Agriculture Module) veya Pix4Dfields ile uretilen GeoTIFF standart kabul edilir.
Yükleme anı: İstasyon batch metadata’dan Drone Seri No + MissionID (varsa) + kapsama-izi/footprint alanını alır. Öncelik MissionID; yoksa kapsama-izi-boundary kesişimi.
Bitki turu: FieldID icin sezon bitkisi kaydi esas (1 Ekim - 31 Aralik araliginda guncellenebilir).
[KR-017] 1.2.4 YZ modeli ile analiz
“FieldID + bitki turu + MissionID; PII yok” bu bilgiler sadece ucus yapacak drone pilotuna ve hafiza kartlarina islenir. Hafıza kartındaki görüntüler “FieldID + bitki turu + MissionID; PII yok” altında sıralanır. Yani yz modeli hafıza kartında hangi görüntünün hangi tarladaki hangi bitkiye ait olduğunu bilir.
Eslestirme zorunlu: Yuklenen cekimler mutlaka kayitli bir tarla ile otomatik eslesmelidir. Minimum: il, ilce, mahalle/koy, ada, parsel, bitki turu (ture ozel FieldID).
Hafiza kartlari yerel istasyonda guvenlik onlemlerinden gectikten sonra analiz icin ana merkeze gonderilir.
Analizler tamamlaninca sonuclar kesinlikle tek yonlu iletisim ile FieldID + bitki turu + harita katmanlari (renk+desen) olarak web (PWA) uygulamaya gonderilir.
Web (PWA) tarafindan YZ modellerine dogrudan iletisim olmamalidir (inbound kapali; sadece results okuma).
[KR-018] 1.2.5 Tam Radyometrik Kalibrasyon Zorunluluğu (Radiometric Calibration: ışık/sensör etkilerini düzeltme)
Uyumluluk Notu: Bazı geliştirici dokümanlarında aynı zorunluluk [KR-082] RADIOMETRY olarak referanslanabilir. Kanonik kod [KR-018]'dir; SSOT içinde KR-082, KR-018 için alias olarak tanımlıdır.
Amaç:
- Model eğitimi (training: modelin öğrenmesi) ve saha sonuçları arasında tutarlılık (training-serving parity: eğitim/çalıştırma aynı dağılım).
- Müşteri memnuniyeti için zaman serisi (time-series: haftalık takip) ve tarlalar arası kıyasın (cross-field comparison: farklı tarlaları karşılaştırma) güvenilir olması.
Kural (Hard Gate: sert kapı):
- Calibrated Dataset (kalibre veri seti) üretilmeden AnalysisJob (analiz işi) başlatılamaz.
- Worker (AI/Processing: yapay zekâ işleyici) ham DN (Digital Number: sensör ham sayısal değeri) veya kalibrasyonu belirsiz veriyi kabul etmez.
İstasyon akışı (Real-world: saha şartlarına uygun):
1) Offline Security PC (internetsiz): AV + manifest/hash + quarantine (karantina).
2) Online Producer Workstation (izole internetli): Producer ile tam kalibrasyon + panel + raporlar.
3) Dispatch/Upload: Calibrated Dataset + raporlar + manifest/hash -> Worker.
Platform sorumluluğu (Backend: sunucu):
- Calibration Gate: calibrated yoksa job açma.
- QC Gate: PASS/WARN/FAIL kararını sakla, UI’a taşı, audit trail üret.
Çıktı sözleşmeleri (Contracts: ortak veri şemaları):
- CalibrationJob/CalibrationResult; QCReport (pass_warn_fail + flags + recommended_action).
- AnalysisJob yalnızca requires_calibrated=true ile açılır.
[KR-083] 1.2.5 İl Operatörü
Not: Rol kodu ProvinceOperator'dur; SSOT ve uygulama paketlerinde bu rol her zaman [KR-083] ile referanslanmalıdır.
İl Operatörü (sistem rol kodu: ProvinceOperator); sözleşmeye göre %5-%15 kar payı alır (admin panelden tanımlanır).
Ihtiyac: KPI + kapasite planlama (abonelik sayisi, hizmet verilen alan, odeme toplamı, ilce yogunlugu, SLA).
PII gormez. Sunum iki katmanli: (A) Merkez - PII ayri, (B) Operator - SubscriberRef + ilce veya 1-2 km grid.
[KR-019] 1.2.6 Expert Portal (Uzman İnceleme)
- Uzman portalı, modelin düşük güven verdiği veya çelişkili durumlarda manuel inceleme için kullanılır (PII görünmez).
- Üyelik self-signup değildir: uzman hesabı ADMIN kontrollü açılır (curated onboarding).
- Bildirim kanalları: SMS + web portal içi gerçek zamanlı bildirim (WebSocket); e-posta kullanılmaz.
- Erişim kuralı: uzman yalnızca kendisine atanmış incelemeleri görür (ownership check zorunlu).
- Uzman karar formatı (özet): confirmed | corrected | rejected | needs_more_expert.
- Uzman geri bildirimi 'training_grade' ile etiketlenir: enum A|B|C|D|REJECT; ayrıca grade_reason alanı tutulur (max 200 karakter).
[KR-020] 2. Ücretlendirme
[KR-021] 2.1 Genel prensip
Ucretler bitki turu ve analiz secenegine gore: tek seferlik analiz veya yillik abonelik.
Birim: donum. Kullanici m2 girse bile sistem donume cevirip hesaplar.
Yillik abonelikte periyot secilebilir; sistem bitkiye gore onerir. Oneri disinda secimde uyarı gosterilir.
[KR-022] 2.1.1 Fiyat Yönetimi Politikası
Fiyatlar uygulamada serbest yazilmaz; tek kaynak PriceBook (Fiyat Katalogu).
Degisiklik sadece ADMIN rolunden yonetim paneliyle.
Versiyonlu + tarih aralikli; gecmis siparislerin fiyati sonradan degismez.
Siparis/abonelik olusurken fiyat snapshot siparise yazilir.
Degisiklikler audit log’a yazilir.
[KR-023] 2.2 Örnek fiyat kurgusu (Pamuk)
Secenek	Liste fiyat	Ilk yil / abonelik kurgusu
Tek seferlik analiz	50 TL / donum / analiz	Ilk yil tanitim: %50 indirim -> 25 TL / donum / analiz
Yillik abonelik	-	Tanitim fiyati uzerinden ekstra %25 indirim -> 20 TL / donum (yillik birim)

[KR-024] 2.3 Önerilen tarama periyodu (gün)
Bitki	Onerilen periyot (gun)
Pamuk	7-10
Antep fistigi	10-15
Misir	15-20
Bugday	10-15
Aycicegi	7-10
Uzum	7-10
Zeytin	15-20
Kirmizi mercimek	10-15

[KR-025] 2.4 Analiz içeriği (hizmet kapsamı)
Temel ilke: Sistem ilaclama karari vermez; yalnizca tespit, risk skoru ve erken uyari saglar.
Rapor ciktisi (tarla + bitki bazinda): Health Score; su/azot stresi; hastalik/mantar bulgulari; zararli bocek riski; yabanci ot yogunlugu.
[KR-026] 2.5 Sunum biçimi
Harita katmanlari (isi haritasi / grid / zonlama).
Zaman serisi (yillik abonelikte karsilastirma).
Ozet rapor (PDF ve/veya uygulama ici rapor).

[KR-032] EK: Training Export Standardı
Amaç: Uzman feedback’lerini (expert review outputs) standart formatta export ederek model eğitim pipeline’ına aktarılabilir hale getirmek.
Format önerisi: JSONL (cls) + GeoJSON (seg) + manifest/hash ile birlikte; şema sözleşmeleri SSOT’taki tanımlara göre kilitlenir.
[KR-033] 2.2 Ödeme (Payment: ödeme) + Manuel Onay (Manual Approval: insan onayı)
Amaç: Sahada EFT/IBAN (banka havalesi) gibi manuel kanıtlarla ödeme alınabilmesi; yanlış/çift ödeme riskini azaltmak.
Kural:
- PaymentIntent (ödeme niyeti) oluşturulmadan abonelik/sipariş “paid” olmaz.
- Banka/EFT ödemelerinde kanıt (dekont) yüklenir; admin manuel doğrular.
- Doğrulama sonrası sistem PaymentStatus’u günceller ve audit log’a yazar.
Notlar:
- PII minimizasyonu: kanıt dokümanında gereksiz kişisel veri maskelenebilir.
- İade/iptal politikaları kanonik kurallara göre yönetilir.

[KR-030] 3. Notlar, sınırlar ve uyum
Drone standardi: Baslangicta DJI Mavic 3M disinda veri kabul edilmez (sonraki fazda degerlendirilir).
Goruntuler yerel istasyon uzerinden sisteme alinir; log kayitlari denetim izi olusturur.
KVKK: PII ile operasyon/raporlama verisi ayridir; il operatoru PII gormeZ.
Model ciktisi karar degildir; nihai aksiyon ciftci ve/veya ziraat muhendisinin sorumlulugundadir.
[KR-031] EK: Pilot Hakediş ve Ödeme Politikası
Pilotlar, bir ay icinde ONAYLANMIS gorevlerde taradiklari alan uzerinden hakedis kazanir.
Odeme donemi: takip eden ayin ilk haftasi (1-7 arasi) toplu odeme.
Birim fiyat: varsayilan 3 TL/donum; il bazinda CENTRAL_ADMIN tanimlayabilir (PilotRateByProvince).
Oneri: ay sonu 23:59 cut-off + 3 is gunu itiraz penceresi + ilk 7 gun icinde odeme.
Observed kapsama-izi olmadan odeme yok; MissionID eslesmeden odeme yok.
[KR-040] EK-SEC-01: Güvenlik Kabul Kriterleri/Test Checklist (SDLC Entegrasyonu)
Amaç: TXT repo mantalitesindeki savunma-derinliği (defense-in-depth) güvenlik yaklaşımını, ölçülebilir kabul kriterlerine ve SDLC kapılarına (PR/CI/Release/Ops) bağlamak.
Yer: İş Planı seviyesinde politika ve denetim beklentileri. Bu ek, ürün ve saha dokümanları için bağlayıcı kabul kriteridir.
[KR-041] A) SDLC Kapıları (Gate) - Zorunlu Kontroller
PR Gate (merge öncesi):
Contracts pinleme: CONTRACTS_VERSION (SemVer) + CONTRACTS_SHA256 zorunlu; değişiklikte breaking-change kontrolü.
Unit test: kritik güvenlik fonksiyonları (hash, imza doğrulama, allowlist, RBAC) %80+ satır kapsama hedefi.
Secret scan: repo içinde anahtar/sertifika/PIN bulunmayacak (pre-commit + CI).
Lint/Type-check: statik analiz hatasız; şema validasyonu (OpenAPI/JSON Schema) çalışır.
CI Gate (pipeline):
Integration test: EdgeKiosk -> Backend mTLS el sıkışması + cihaz kimliği doğrulama.
Contract test: DTO/Schema üretimi + geriye dönük uyumluluk (backward-compatible) kontrolü.
SAST/Dependency scan: bilinen kritik zafiyet yok (CVSS yüksek olanlar blok).
Container scan + SBOM: imaj taraması temiz; SBOM üretilir ve arşivlenir.
Release Gate (prod’a çıkış):
Sürümleme: release notları + migration planı; breaking change varsa sürüm artışı ve geriye uyumluluk stratejisi.
Smoke test: uçtan uca örnek akış (Mission create -> ingest -> worker -> sonuç -> harita katmanı) başarılı.
Sertifika yönetimi: kiosk sertifikaları basılı/dağıtılmış; rotasyon takvimi kayıtlı.
Rollback planı: veri bütünlüğünü bozmadan geri dönüş adımları tanımlı.
Ops Checklist (günlük/haftalık):
Karantina kuyruğu: bekleyen dosya/mission sayısı ve sebepleri raporlanır.
Audit/WORM log doğrulaması: logların değişmediği kontrol edilir, saklama süresi politikası izlenir.
Anahtar/sertifika rotasyonu: süre dolumu yaklaşanlar listelenir, planlı yenileme yapılır.
Anomali izleme: olağandışı ingest hızı, tekrar eden başarısız doğrulama, şüpheli IP/cihaz hareketleri alarm üretir.
[KR-042] B) Kabul Kriterleri Matrisi
Güvenlik Katmanı	Kabul Kriteri (DoD)	Test Kanıtı	SDLC Gate
Kimlik & Yetki (RBAC) + PII ayrımı	İl Operatörü ve saha rolleri PII görmez; sadece FieldID/özet KPI görür. Admin işlemleri audit log üretir.	RBAC unit + API yetki e2e; negatif test: yetkisiz erişim 403. Audit log kaydı doğrulanır.	PR + CI
Cihaz kimliği + mTLS	Sadece kayıtlı kiosk cihazı, sertifikalı mTLS ile ingest endpoint’ine erişebilir; sertifika iptali anında bloklar.	Integration test: mTLS başarılı/başarısız senaryolar; sertifika revocation testi.	CI + Release
Veri bütünlüğü: SHA-256 manifest + imza	Her ingest paketi için manifest (dosya listesi + hash) ve imza zorunlu; hash uyuşmazsa karantina.	Unit test (hash/manifest), e2e: bozuk dosya -> karantina + alarm.	PR + CI
Allowlist / içerik doğrulama	Sadece izinli uzantı/MIME; maksimum boyut/çözünürlük limitleri; zip-slip ve path traversal engelli.	Unit test: uzantı/MIME; fuzz test örnekleri; e2e negatif senaryo.	PR + CI
Zararlı taraması (AV/EDR) + karantina	AV taraması geçmeden hiçbir dosya iş akışına giremez; şüpheli içerik karantinaya alınır, etiketlenir.	E2e senaryo: EICAR test dosyası -> karantina + olay kaydı.	CI + Ops
Air-gapped karantina PC + tek yönlü aktarım	Karantina PC internetsiz; dış medya steril prosedürü; çıktı sadece imzalı paket olarak ilerler.	SOP denetim checklisti + örnek denetim kaydı.	Release + Ops
Zincir-of-custody + immutable (WORM) audit	MissionID/BatchID/CardID ve işlem adımları değiştirilemez logda; log saklama süresi uygulanır.	Log bütünlüğü kontrolü + denetim raporu; e2e: ingest adımı log zinciri.	CI + Ops
Secrets yönetimi (rotasyon)	Hiçbir secret repo’da yok; vault/secret store; rotasyon periyodu tanımlı; sızma halinde iptal prosedürü.	Secret scan raporu + rotasyon kaydı + revocation drill çıktısı.	PR + Release + Ops
Rate limiting + anomali tespiti	Ingest ve auth endpoint’lerinde rate limit; tekrar eden başarısız doğrulama alarmları.	Load test + saldırı simülasyonu (çoklu deneme) -> 429 ve alarm.	CI + Ops
AI izolasyonu + least privilege	Worker sadece job kuyruğu/sonuç yazma yetkisine sahip; ham PII yok; ağ erişimi minimum.	IAM policy testi + container/network policy doğrulama; e2e job akışı.	CI + Release

[KR-043] C) Test Checklist (Senaryo Bazlı)
Senaryo	Adımlar (özet)	Beklenen Sonuç	Kanıt/Artefakt
SC-01: Normal ingest (offline -> senkron)	Pilot görev dosyası -> uçuş -> SD ingest -> manifest doğrula -> AV tarama -> upload/queue -> worker sonuç -> harita katmanı	Tüm adımlar başarılı; sonuç katmanı oluşur; audit zinciri tam	E2E test raporu + log zinciri + sonuç ekran görüntüsü
SC-02: Hash uyuşmazlığı	Manifestteki bir dosyayı değiştir -> ingest	Karantina; olay kaydı; işleme alınmaz	Karantina kaydı + alarm kaydı
SC-03: Yetkisiz cihaz	mTLS sertifikası olmayan cihazla ingest dene	Erişim reddi; audit log + alarm	Integration test çıktısı + log
SC-04: EICAR/zararlı içerik	Test imzası bulunan dosyayı ingest et	AV blok + karantina	AV raporu + karantina kaydı
SC-05: PII sızma testi	İl Operatörü rolüyle PII endpoint’ine erişmeyi dene	403; veri dönmez; deneme audit log’a düşer	RBAC e2e raporu
SC-06: Contract breaking change	Schema’da alan sil/isim değiştir	CI breaking-change detector fail; merge/release blok	CI artefaktı + diff raporu

[KR-050] EK - Kimlik Doğrulama ve Üyelik Akışı (Sade Model)
Kimlik bilgisi olarak yalnızca Telefon Numarası kullanılır (E-posta ve TCKN toplanmaz.).
Kayıt: Telefon Numarası girilir ve 6 haneli sayısal PIN belirlenir.
Giriş: Telefon Numarası + 6 haneli PIN ile yapılır.
Doğrulama adımı yoktur; süreç bilinçli olarak sadeleştirilmiştir.
PIN unutulursa: Merkez/Kooperatif/İl Operatörü panelinden PIN sıfırlanır; kullanıcı ilk girişte yeni PIN belirler.
Kullanıcıyı yormayan minimum korumalar: giriş deneme sınırı (rate limit) ve kısa süreli kilitleme (lockout).

[KR-060] Ek A – Ürün/Teknik Spesifikasyondan Normatif
[KR-061] 1. Amaç ve Sabit Çerçeve
Drone: DJI Mavic 3M  Veri: RGB + multispektral (NDVI/NDRE başta)
Yapay zekâ sadece analiz üretir; ilaçlama/gübreleme kararı vermez
Sonuçlar web (PWA) uygulamasında harita ve rapor olarak sunulur
KVKK: PII ile operasyon/raporlama verileri ayrıştırılır; il operatörü PII görmez
[KR-062] 2. Tasarım İlkeleri
Tek kaynak gerçek: API ve veri modeli. Web (PWA) iş kuralı kopyalamaz.
Offline-first: Yerel istasyon internetsiz çalışabilir; senkronizasyon opsiyonel ve güvenli.
Denetlenebilirlik (Audit Log): fiyat, kurum onayı, eşleştirme ve hakediş adımlarında zorunlu log.
Eşleştirme hiyerarşisi: MissionID -> BatchID -> FieldID -> CropSeason. MissionID yoksa coğrafi kesişim + manuel kuyruk.
[KR-063] 3. Roller ve Yetkiler (RBAC)
Rol Kodu	Kısa Tanım	Özet Yetki
FARMER_SINGLE	Tekil çiftçi	Tarla ekle, analiz talebi aç, rapor görüntüle
FARMER_MEMBER	Kurum üyesi çiftçi	Kendi tarlaları için rapor gör, kurum bağlantısını onayla
COOP_OWNER	Kooperatif sahibi/yetkili	Paket satın alma, kullanıcı yönetimi, analiz talebi, dashboard
COOP_ADMIN	Kooperatif admin	Üye yönetimi, tarla ekleme, analiz talebi
COOP_AGRONOMIST	Kooperatif agronomist	Rapor gör, not gir (aksiyon kararı yok)
COOP_VIEWER	Kooperatif izleyici	Sadece özet/rapor
PILOT	Drone pilotu	Görev gör, uçuş yap, veri teslim et, hakediş önizle
STATION_OPERATOR	Yerel istasyon operatörü	Kiosk ingest, eşleştirme, karantina/antivirüs sonuçları
IL_OPERATOR	İl Operatörü	PII görmeden KPI/özet gelir ve operasyon metrikleri
CENTRAL_ADMIN	Merkez yönetici	Fiyat/PriceBook, kurum onayı, rol atama, audit
AI_SERVICE	YZ analiz servisi	Job tüket, rapor üret, sonuç yaz

[KR-064] 5. Harita Katman Standardı (Layer Registry)
Katmanlar web (PWA) arayüzünde aynı Layer Registry üzerinden tanımlanır. Renk + desen/ikon + opaklık + öncelik tutarlı olmalıdır.
LayerCode	Legend	Renk	Desen/İkon	Opaklık	Öncelik	Çıktı Tipi
HEALTH	Sağlık	Yeşil	Leaf ikon + gradient heatmap	0.55	10	Raster/Heatmap
WEED	Yabancı ot	Sarı/Hardal	Noktalı desen + weed ikon	0.60	60	Polygon/Zone
DISEASE	Hastalık	Turuncu	Çapraz çizgi + stethoscope ikon	0.65	70	Polygon/Zone
PEST	Zararlı böcek	Kırmızı	X/desen + bug ikon	0.70	80	Polygon/Zone
FUNGUS	Mantar	Mor	Çapraz tarama + mushroom ikon	0.65	75	Polygon/Zone
WATER_STRESS	Su stresi	Mavi	Damla noktalı desen + droplet ikon	0.45	50	Raster/Zone
N_STRESS	Azot stresi	Soluk gri	Çapraz çizgili desen + N ikon	0.45	40	Raster/Zone

Çakışma kuralı: priority yüksek katman üstte görünür. Erişilebilirlik için ikon + desen zorunludur.
[KR-065] 6. Pilot Hakediş Doğrulama (Expected vs Observed)
Expected Area: FieldBoundary veya Mission flightplan sınırı (m²).
Observed Area: GeoTIFF/ortomozaik kapsama-izi (kapsama) poligonu (m²).
coverage_ratio = Area(intersection(observed, expected)) / Area(expected)
Hakediş kuralı: coverage_ratio >= 0.95 tam; 0.80-0.95 kısmi + opsiyonel inceleme; <0.80 tekrar uçuş veya itiraz/inceleme.
[KR-066] 8. Güvenlik ve KVKK
PII ayrı veri alanında tutulur; raporlama ve KPI katmanı pseudonymous kimliklerle çalışır.
İl operatörü: ilçe veya 1-2 km grid yoğunluk; isim/telefon/IBAN alanlarına erişemez.
Yerel istasyon: offline karantina, hash doğrulama, antivirüs raporu ve zincir log (chain-of-custody).
Drone seri no ve kart kimliği doğrulama sahte veri enjeksiyon riskini azaltır.
Fiyat ve kurum onayı değişiklikleri audit log zorunlu; snapshot ile geçmiş siparişler etkilenmez.
[KR-070] EK: YZ Analiz İzolasyonu
[KR-071] YZ Modeli ile Analiz - Tek Yönlü Veri Akışı (One-way data flow)
Bitkiye ozel YZ modeli (AI model) routing (yonlendirme) ile otomatik secilir. Bu secim karari; MissionID, FieldID ve bitki turu ile kayit altina alinir, PII (kisisel veri) tasinmaz.
Pilot tarafinda gorunen gorev bilgisi: MissionID, il/ilce/mahalle-koy, ada/parsel (ParcelRef), bitki turu, hedef tarama penceresi, teslim son tarihi. Ciftci adi/telefonu gosterilmez.
Hafiza kartlari yerel istasyonda guvenlik kontrollerinden (hash manifest, virus tarama, whitelist uzantilar, karantina) gectikten sonra analiz icin ana merkeze transfer edilir.
Analiz tamamlaninca sonuclar sadece FieldID + bitki turu + harita katmani (renk+desen) + skor/uyari olarak "sonuc servisine" yazilir ve web (PWA) uygulamaya tek yonlu (outbound) gonderilir.
Web (PWA), YZ analiz altyapisina dogrudan erismez; analiz servisi icin inbound istek kabul edilmez. En fazla "sonuc okuma" API’leri vardir (Results API).
Tum akis audit log ile izlenir: MissionID, BatchID, CardID, drone seri no, pilot kimligi, zaman damgalari ve QC bayraklari (coverage, blur, mismatch vb.).
[KR-080] Ek A0 – Ana İş Akışları için teknik kurallar (Teknik Spesifikasyon ekleri)
Bu bölüm; ana iş akışlarının iş planı anlatısında zaten bulunan kısımlarını tekrar etmez. Sadece teknik spesifikasyonda eklenen/sertleştirilen kuralları listeler.
Tarla ekleme: il/ilçe/mahalle/köy + ada/parsel + alan (m²); sistem FieldID üretir
Tekil kayıt kuralı: il+ilçe+mahalle/köy+ada+parsel kombinasyonu tekrar edemez
Bitki türü tanımı (tarla bazında); birden fazla bitki varsa alan (m²) ile ayrı ayrı
Analiz talebi: bitki türü bazında; yıllık abonelik veya tek seferlik
Bitki türü değişimi: yılda 1 defa, sadece 1 Ekim - 31 Aralık (backend kuralı)
Başvuru: evrak + 'Onay Bekliyor' durumunda açılır; admin onayı ile 'Aktif' olur.
Üye daveti: QR / 6 haneli davet kodu; çiftçi hesabından bağlantıyı onaylar (onay olmadan kooperatif adına işlem kısıtlanabilir).
Tarla tekil; sahiplik/erişim ayrı yaklaşımı önerilir (çakışma/yanlış ekleme riskine karşı).
Pilot sadece DJI Mavic 3M kullanır; drone seri numarası doğrulama referansıdır.
Günlük teslim: uçuş çıktısı her gün hafıza kartı ile yerel istasyona aktarılır.
Her uçuşta farklı hafıza kartı kullanılır. DJI tarafındaki kart kilidi/PIN gibi özellikler varsa opsiyonel ek katmandır; güvenlik garantisi değildir (bkz. [KR-015]).
Eşleştirme zorunlu: Yüklenen çekimler kayıtlı tarla ile eşleşmezse işlenmez.
Pilot sonuç raporunu görmez; sadece operasyon durumu görür.
İl operatörü PII görmez; sadece ticari KPI ve kapasite planlama metrikleri görür.
Coğrafya: ilçe düzeyi veya 1-2 km grid yoğunluk katmanı (pseudonymous).

---

[KR-081] Kontrat Şemaları (Contract‑First) — Kanonik JSON Schema

Amaç: “olmalı” seviyesinden çıkıp, kodlamadan önce ortak dilin **makine‑doğrulanabilir** (machine‑verifiable) hale gelmesi.
Bu bölümde iki kanonik payload tanımı **dokümana gömülüdür** ve `shared/contracts` üretiminin tek kaynağı olarak kabul edilir.

### KR‑081.1 AnalysisJob — JSON Schema (draft 2020‑12)

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://tarlaanaliz.example/contracts/analysis_job.v1.schema.json",
  "title": "AnalysisJob",
  "type": "object",
  "additionalProperties": false,
  "required": [
    "schema_version",
    "job_id",
    "created_at",
    "field",
    "crop",
    "mission",
    "capture_set",
    "inputs",
    "processing",
    "pricing_snapshot",
    "status"
  ],
  "properties": {
    "schema_version": {
      "const": "analysis_job.v1"
    },
    "job_id": {
      "type": "string",
      "description": "UUID v4",
      "pattern": "^[0-9a-fA-F-]{36}$"
    },
    "idempotency_key": {
      "type": "string",
      "maxLength": 128
    },
    "created_at": {
      "type": "string",
      "format": "date-time"
    },
    "requested_by": {
      "type": "object",
      "additionalProperties": false,
      "required": [
        "actor_type",
        "actor_id_hash"
      ],
      "properties": {
        "actor_type": {
          "type": "string",
          "enum": [
            "farmer",
            "pilot",
            "il_operator",
            "admin",
            "system"
          ]
        },
        "actor_id_hash": {
          "type": "string",
          "description": "PII olmayan, tek-yönlü hash/ID",
          "minLength": 8,
          "maxLength": 128
        }
      }
    },
    "field": {
      "type": "object",
      "additionalProperties": false,
      "required": [
        "field_id",
        "area_donum",
        "parcel_ref"
      ],
      "properties": {
        "field_id": {
          "type": "string",
          "maxLength": 64
        },
        "parcel_ref": {
          "type": "string",
          "maxLength": 128
        },
        "province": {
          "type": "string",
          "maxLength": 64
        },
        "district": {
          "type": "string",
          "maxLength": 64
        },
        "area_donum": {
          "type": "number",
          "minimum": 0
        },
        "bbox_wgs84": {
          "type": "array",
          "items": {
            "type": "number"
          },
          "minItems": 4,
          "maxItems": 4,
          "description": "[minLon,minLat,maxLon,maxLat]"
        }
      }
    },
    "crop": {
      "type": "object",
      "additionalProperties": false,
      "required": [
        "crop_code",
        "crop_name"
      ],
      "properties": {
        "crop_code": {
          "type": "string",
          "maxLength": 32
        },
        "crop_name": {
          "type": "string",
          "maxLength": 64
        },
        "growth_stage": {
          "type": "string",
          "maxLength": 64
        }
      }
    },
    "mission": {
      "type": "object",
      "additionalProperties": false,
      "required": [
        "mission_id",
        "flight_date",
        "drone"
      ],
      "properties": {
        "mission_id": {
          "type": "string",
          "maxLength": 64
        },
        "flight_date": {
          "type": "string",
          "format": "date"
        },
        "pilot_id_hash": {
          "type": "string",
          "maxLength": 128
        },
        "drone": {
          "type": "object",
          "additionalProperties": false,
          "required": [
            "model"
          ],
          "properties": {
            "model": {
              "const": "DJI Mavic 3M"
            },
            "serial_number": {
              "type": "string",
              "maxLength": 64
            }
          }
        }
      }
    },
    "capture_set": {
      "type": "object",
      "additionalProperties": false,
      "required": [
        "batch_id",
        "card_id",
        "station_ingest_run_id",
        "modalities"
      ],
      "properties": {
        "batch_id": {
          "type": "string",
          "maxLength": 64
        },
        "card_id": {
          "type": "string",
          "maxLength": 64
        },
        "station_ingest_run_id": {
          "type": "string",
          "maxLength": 64
        },
        "modalities": {
          "type": "array",
          "items": {
            "type": "string",
            "enum": [
              "RGB",
              "MS"
            ]
          },
          "minItems": 1
        },
        "bands": {
          "type": "array",
          "items": {
            "type": "string",
            "enum": [
              "B",
              "G",
              "R",
              "RE",
              "NIR"
            ]
          }
        },
        "altitude_m": {
          "type": "number",
          "minimum": 0
        },
        "front_overlap_pct": {
          "type": "number",
          "minimum": 0,
          "maximum": 100
        },
        "side_overlap_pct": {
          "type": "number",
          "minimum": 0,
          "maximum": 100
        }
      }
    },
    "inputs": {
      "type": "array",
      "minItems": 1,
      "items": {
        "type": "object",
        "additionalProperties": false,
        "required": [
          "type",
          "uri",
          "sha256",
          "size_bytes",
          "mime"
        ],
        "properties": {
          "type": {
            "type": "string",
            "enum": [
              "raw_images",
              "metadata",
              "orthomosaic_rgb",
              "orthomosaic_ms",
              "indices",
              "qc_report"
            ]
          },
          "uri": {
            "type": "string",
            "maxLength": 2048
          },
          "sha256": {
            "type": "string",
            "pattern": "^[0-9a-f]{64}$"
          },
          "size_bytes": {
            "type": "integer",
            "minimum": 0
          },
          "mime": {
            "type": "string",
            "maxLength": 128
          }
        }
      }
    },
    "processing": {
      "type": "object",
      "additionalProperties": false,
      "required": [
        "pipeline_version",
        "priority",
        "requested_outputs"
      ],
      "properties": {
        "pipeline_version": {
          "type": "string",
          "maxLength": 32
        },
        "priority": {
          "type": "string",
          "enum": [
            "low",
            "normal",
            "high",
            "urgent"
          ]
        },
        "requested_outputs": {
          "type": "array",
          "minItems": 1,
          "items": {
            "type": "string",
            "maxLength": 64
          }
        },
        "model_profile": {
          "type": "string",
          "maxLength": 64
        },
        "notes": {
          "type": "string",
          "maxLength": 2048
        }
      }
    },
    "pricing_snapshot": {
      "type": "object",
      "additionalProperties": false,
      "required": [
        "pricebook_version",
        "pricebook_sha256",
        "currency",
        "unit",
        "unit_price",
        "area_donum",
        "total_price"
      ],
      "properties": {
        "pricebook_version": {
          "type": "string",
          "maxLength": 32
        },
        "pricebook_sha256": {
          "type": "string",
          "pattern": "^[0-9a-f]{64}$"
        },
        "currency": {
          "const": "TRY"
        },
        "unit": {
          "const": "donum"
        },
        "unit_price": {
          "type": "number",
          "minimum": 0
        },
        "area_donum": {
          "type": "number",
          "minimum": 0
        },
        "total_price": {
          "type": "number",
          "minimum": 0
        },
        "discount_code": {
          "type": "string",
          "maxLength": 64
        }
      }
    },
    "security": {
      "type": "object",
      "additionalProperties": false,
      "properties": {
        "device_id": {
          "type": "string",
          "maxLength": 128
        },
        "mtls_cert_fingerprint": {
          "type": "string",
          "maxLength": 128
        }
      }
    },
    "status": {
      "type": "string",
      "enum": [
        "queued",
        "running",
        "succeeded",
        "failed",
        "cancelled"
      ]
    },
    "updated_at": {
      "type": "string",
      "format": "date-time"
    },
    "tags": {
      "type": "array",
      "items": {
        "type": "string",
        "maxLength": 64
      }
    }
  }
}
```

### KR‑081.2 AnalysisResult — JSON Schema (draft 2020‑12)

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://tarlaanaliz.example/contracts/analysis_result.v1.schema.json",
  "title": "AnalysisResult",
  "type": "object",
  "additionalProperties": false,
  "required": [
    "schema_version",
    "result_id",
    "job_id",
    "produced_at",
    "status",
    "quality",
    "layers",
    "summary",
    "audit"
  ],
  "properties": {
    "schema_version": {
      "const": "analysis_result.v1"
    },
    "result_id": {
      "type": "string",
      "pattern": "^[0-9a-fA-F-]{36}$"
    },
    "job_id": {
      "type": "string",
      "pattern": "^[0-9a-fA-F-]{36}$"
    },
    "produced_at": {
      "type": "string",
      "format": "date-time"
    },
    "status": {
      "type": "string",
      "enum": [
        "succeeded",
        "failed",
        "partial"
      ]
    },
    "quality": {
      "type": "object",
      "additionalProperties": false,
      "required": [
        "coverage_pct",
        "qc_flags"
      ],
      "properties": {
        "coverage_pct": {
          "type": "number",
          "minimum": 0,
          "maximum": 100
        },
        "blur_score": {
          "type": "number",
          "minimum": 0
        },
        "geo_alignment_error_m": {
          "type": "number",
          "minimum": 0
        },
        "qc_flags": {
          "type": "array",
          "items": {
            "type": "string",
            "maxLength": 64
          }
        }
      }
    },
    "findings": {
      "type": "array",
      "items": {
        "type": "object",
        "additionalProperties": false,
        "required": [
          "category",
          "label",
          "severity",
          "confidence"
        ],
        "properties": {
          "category": {
            "type": "string",
            "enum": [
              "disease",
              "pest",
              "weed",
              "nutrient_stress",
              "water_stress",
              "other_stress"
            ]
          },
          "label": {
            "type": "string",
            "maxLength": 128
          },
          "severity": {
            "type": "number",
            "minimum": 0,
            "maximum": 1
          },
          "confidence": {
            "type": "number",
            "minimum": 0,
            "maximum": 1
          },
          "area_donum": {
            "type": "number",
            "minimum": 0
          },
          "geometry_uri": {
            "type": "string",
            "maxLength": 2048
          }
        }
      }
    },
    "layers": {
      "type": "array",
      "minItems": 1,
      "items": {
        "type": "object",
        "additionalProperties": false,
        "required": [
          "layer_code",
          "uri",
          "sha256",
          "mime"
        ],
        "properties": {
          "layer_code": {
            "type": "string",
            "maxLength": 32
          },
          "uri": {
            "type": "string",
            "maxLength": 2048
          },
          "sha256": {
            "type": "string",
            "pattern": "^[0-9a-f]{64}$"
          },
          "mime": {
            "type": "string",
            "maxLength": 128
          },
          "legend": {
            "type": "string",
            "maxLength": 256
          }
        }
      }
    },
    "summary": {
      "type": "object",
      "additionalProperties": false,
      "required": [
        "overall_health_index",
        "notes"
      ],
      "properties": {
        "overall_health_index": {
          "type": "number",
          "minimum": 0,
          "maximum": 1
        },
        "notes": {
          "type": "string",
          "maxLength": 4000,
          "description": "YZ analizidir; ilaçlama kararı vermez."
        },
        "next_scan_recommendation_days": {
          "type": "integer",
          "minimum": 1,
          "maximum": 60
        }
      }
    },
    "errors": {
      "type": "array",
      "items": {
        "type": "object",
        "additionalProperties": false,
        "required": [
          "code",
          "message"
        ],
        "properties": {
          "code": {
            "type": "string",
            "maxLength": 64
          },
          "message": {
            "type": "string",
            "maxLength": 1024
          }
        }
      }
    },
    "audit": {
      "type": "object",
      "additionalProperties": false,
      "required": [
        "correlation_id"
      ],
      "properties": {
        "correlation_id": {
          "type": "string",
          "maxLength": 64
        },
        "trace_id": {
          "type": "string",
          "maxLength": 64
        },
        "station_ingest_run_id": {
          "type": "string",
          "maxLength": 64
        },
        "worker_run_id": {
          "type": "string",
          "maxLength": 64
        }
      }
    }
  }
}
```

### KR‑081.3 OpenAPI bağlama (minimal örnek)

```yaml
components:
  schemas:
    AnalysisJob:
      $ref: "https://tarlaanaliz.example/contracts/analysis_job.v1.schema.json"
    AnalysisResult:
      $ref: "https://tarlaanaliz.example/contracts/analysis_result.v1.schema.json"
```

**Sürümleme kuralı (SemVer):**
- `v1.x`: geriye uyumlu (backward compatible) eklemeler serbest (optional field eklenebilir).
- `v2.0`: breaking change; `CONTRACTS_VERSION` ve `CONTRACTS_SHA256` zorunlu güncellenir.

---

# 2) Saha ve Operasyon SOP (Bilgilendirici)

TarlaAnaliz – Saha ve Operasyon SOP
DJI Pilot 2 + WPML + Yerel İstasyon / EdgeKiosk (Offline-first)
Not (2026-02-03): Haftalık görev dağıtımı + “Hava Engeli (Weather Block)” raporu ve haftalık yeniden planlama akışı eklendi (Bkz. [KR-015-3], [KR-015-5]).


Kapsam
Bu SOP; görev dosyası (KMZ/WPML) standardını, pilotun sahadaki adımlarını, yerel istasyonda QC + bütünlük kontrollerini ve YZ analizine tek yönlü akışı tanımlar.
Kimlik modeli ve iş kurallarının kanonik açıklaması için: Kanonik Ürün ve İşleyiş Rehberi’ndeki [KR-010], [KR-013]–[KR-019], [KR-020]–[KR-026], özellikle [KR-050] bölümlerine bakınız.
Bu SOP, kanonik kuralları tekrar etmez; adımların gerekçesi için ilgili KR referansını kullanır (ör. ‘Bkz. [KR-015]’).

1. Temel kavramlar ve kimlikler
FieldID: Sistemde üretilen benzersiz tarla kimliği (Tarla ID).
MissionID: Bir tarlanın belirli bir tarih penceresinde planlanan tek görev kimliği (sistem tarafından üretilir; görev dosyası adında ayrıca ParcelRef ve YYYYMMDD yer alır).
BatchID: Yerel istasyona tek seferde yüklenen veri paketi kimliği.
CardID: Hafıza kartına verilen envanter kimliği (QR/etiket).
ParcelRef: Ada/parsel referansı (resmi referans), PII değildir.
2. Görev dosyası standardı: KMZ içinde WPML
Pratik standart: KMZ paketinin içinde WPML ile tanımlı waypoint/waylines görev verisi bulunur (wpmz/template.kml + wpmz/waylines.wpml).
Görev dosyası adlandırma: {MissionID}_{ParcelRef}_{YYYYMMDD}.kmz (dosya adında PII bulunmaz; MissionID dosya adında ve metadata içinde yer alır).
Seed-KMZ önerisi: Pilot 2 ile bir kez “doğru ayarlı” örnek görev oluşturulup export edilen KMZ şablon kabul edilir; sistem sadece sınır/parametre alanlarını günceller. Bu, sürüm farklarında kırılmayı azaltır.
3. Pilot 2 operatör SOP (saha adımları)
Not: Görevler haftalık pencere (rolling 7 gün) üzerinden dağıtılır. Pilot, haftanın başında uygulamadaki haftalık görev listesini kontrol eder ve çakışma/uygunsuzluk varsa zamanında bildirir (Bkz. [KR-015-3]).
3.1 Görev import
Kumandaya (RC) SD kart veya dahili depolamaya görev KMZ dosyasını kopyala.
DJI Pilot 2 > Flight Route > Import Route (KMZ/KML) > dosyayı seç.
Görev türünü onayla ve görevi Run/Start ile başlat.
3.2 Görev bitişi ve teslim
Görev tamamlandığında, karttaki dosya sayısı/boyutu mantıklı mı kontrol et (aşırı düşükse eksik çekim şüphesidir).
Kart, yerel istasyona teslim edilir. Pilot PII görmez; sadece MissionID/ParcelRef seviyesinde görev bilgisi görür.

3.3 Hava engeli (Weather Block) raporu ve haftalık yeniden planlama
Uçuş güvenliği (rüzgâr, yağış, görüş, sis vb.) nedeniyle uçuş yapılamıyorsa aşağıdaki adımlar zorunludur.
- Pilot, görev için sahaya gittiğinde uçuş yapılamayacağını anlarsa uygulamada MissionID ile “HAVA_ENGELI” raporu açar.
- Süre kuralı: due_at’tan 12 saat önce bildirim mümkün değilse, pilot uçuş penceresi başlangıcından itibaren en geç 1 saat içinde raporlar.
- Kanıt: en az 1 adet foto/video + (varsa) RC ekran görüntüsü / rüzgâr ölçümü; kısa serbest metin notu (örn: “rüzgâr > 10 m/s, güvenli değil”).
- Rapor durumu başlangıçta PENDING_VERIFY olur. İl operatörü/admin VERIFIED verirse Mission REPLAN_QUEUE’ya alınır ve pilot no-show sayılmaz.
- İnternet yoksa: pilot yerel istasyon sorumlusunu arar; istasyon sorumlusu raporu sisteme girer (pilotun kanıtı saklanır). Bu kayıt en geç 2 saat içinde yapılmalıdır.
- Sistem davranışı: haftalık planlayıcı REPLAN_QUEUE’daki görevleri aynı hafta içinde uygun slotlara taşır; sığmazsa bir sonraki haftaya erteler (SLA/abonelik penceresi uyarılarıyla).
- Uyarı: Hava engeli raporu yoksa ve veri teslim edilmezse, durum no-show olarak değerlendirilir ve pilot güvenilirlik skorunu etkiler (Bkz. [KR-015-3]).

4. Yerel istasyon: QC + bütünlük + eşleştirme
Öncelik eşleştirme: MissionID -> FieldID. MissionID yoksa, kapsama-izi/footprint - field boundary kesişimi ile aday eşleştirme yapılır; düşük güven veya çakışma varsa manuel inceleme kuyruğuna (gerekirse Expert Portal) alınır.
Bütünlük: MANIFEST.json + SHA-256 hash (dosya listesi, boyutlar, zaman damgaları).
Hızlı QC (MVP): coverage_ratio, blur/overexposure bayrakları, CRS/extent kontrolü (GeoTIFF), eksik bant/indeks bayrakları.
Karantina: hash uyuşmazlığı, malware şüphesi veya eşleştirme hatası olan paketler quarantine klasörüne alınır, audit log’a yazılır.
5. DJI Terra / Pix4Dfields çıktı standardı (GeoTIFF)
5.1 Tam Radyometrik Kalibrasyon Zorunluluğu (Bkz. [KR-018])
- Calibrated Dataset (kalibre veri seti) üretilmeden AnalysisJob (analiz işi) başlatılamaz.
- Offline Security PC (internetsiz): AV + manifest/hash + quarantine (karantina).
- Online Producer Workstation (izole internetli): Producer ile tam kalibrasyon + Reflectance Panel + Processing/Calibration/QC raporları.
- Dispatch/Upload: Calibrated Dataset + raporlar + manifest/hash -> Worker’a gönder; eksikse upload başlamaz (hard gate).

5.2 QC Gate (Quality Control Gate: kalite kapısı) — PASS/WARN/FAIL
- Worker QC raporu üretir: PASS/WARN/FAIL + flags (bayraklar) + recommended_action (önerilen aksiyon).
- Platform bu kararı saklar, UI’a taşır ve audit trail (denetim izi) üretir.

Hedef çıktılar: ortomozaik + indeks haritaları (NDVI/NDRE vb.) + bant kompozitleri.
Format: Coğrafi referanslı GeoTIFF (CRS bilgisi ve extent doğru olmalı).
Not: DJI Terra Operation Guide v4.2; NDVI ve NDRE gibi vegetation index çıktılarının desteklendiğini belirtir.
6. YZ modeli ile analiz: izolasyon ve tek yönlü akış
Bitkiye özel YZ modeli (AI model) routing (yönlendirme) ile otomatik seçilir. Bu seçim kararı; MissionID, FieldID ve bitki türü ile kayıt altına alınır, PII (kişisel veri) taşınmaz.
Pilot tarafında görünen görev bilgisi: MissionID, il/ilçe/mahalle-köy, ada/parsel (ParcelRef), bitki türü, hedef tarama penceresi, teslim son tarihi. Çiftçi adı/telefonu gösterilmez.
Hafıza kartları yerel istasyonda güvenlik kontrollerinden (hash manifest, virüs tarama, whitelist uzantılar, karantina) geçtikten sonra analiz için ana merkeze transfer edilir.
Analiz tamamlanınca sonuçlar sadece FieldID + bitki türü + harita katmanı (renk+desen) + skor/uyarı olarak “sonuç servisine” yazılır ve web (PWA) uygulamaya tek yönlü (outbound) gönderilir.
Web (PWA), YZ analiz altyapısına doğrudan erişmez; analiz servisi için inbound istek kabul edilmez. En fazla “sonuç okuma” API’leri vardır (Results API).
Tüm akış audit log ile izlenir: MissionID, BatchID, CardID, drone seri no, pilot kimliği, zaman damgaları ve QC bayrakları (coverage, blur, mismatch vb.).
7. Uçuş manifesti: pratik ve sürdürülebilir yöntem
Manifesti karta “elle yazmak” yerine, manifesti dijital olarak MissionID merkezli tut: pilot uygulamasında görev check-in/out, yerel istasyonda kart intake taraması.
CardID için QR etiket kullan: pilot göreve başlarken CardID + MissionID eşleştirmesini tek tıkla kaydeder; istasyon teslimde aynı eşleşmeyi doğrular.
DJI Pilot 2 uçuş kayıtları ihtiyaç halinde kumandadan export edilebilir (Flight Record / log export). Bu kayıtlar, manifestin kanıt katmanıdır.
8. Kaynaklar
•	DJI Cloud API - WPML dokümantasyonu: template.kml ve waylines.wpml referansları (developer.dji.com, 2025).
•	DJI Terra Operation Guide v4.2 (djicdn.com, 2024-10-08).
•	DJI Pilot 2 Flight Record / log export kılavuzu (support.dji.com).
EK-SOP-SEC: Saha Güvenlik Checklist (Pilot + İstasyon)
Bu ek, saha operasyonunda veri bütünlüğü ve zincir izlenebilirliğini (chain-of-custody) korumak için minimum kontrol listesidir.
Pilot Checklist
Görev dosyası (KMZ) yalnızca kanonik formatta olmalı ve MissionID/ParcelRef/Date alanları doğrulanmalı.
Uçuş sonrası SD kartta beklenmeyen dosya/klasör var mı hızlı kontrol (allowlist dışı ise istasyona bildirim).
SD kart, mühür/etiket ile istasyona teslim; teslim anında CardID/MissionID eşleştirmesi yapılır.
İstasyon (Kiosk/Karantina) Checklist
CardID + MissionID + BatchID kaydı açılır; giriş zamanı ve teslim alan kişi loglanır.
Dosya allowlist/MIME/size kontrolü yapılır; uygunsuz içerik karantinaya alınır.
SHA-256 manifest üretilir veya doğrulanır; hash uyuşmazlığı varsa karantina + alarm.
AV taraması (EICAR dahil test prosedürü) geçmeden hiçbir dosya işlenmez.
Karantina PC internetsiz; dış medya steril prosedürü uygulanır; çıktılar imzalı paket olarak aktarılır.
Upload/queue sonrası worker sonucu geldiğinde MissionID üzerinden sonuç-tarla eşleşmesi doğrulanır.
Tüm adımlar audit log’a yazılır; günlük karantina raporu üretilir.
Minimum Kanıt (Denetim İçin)
Manifest dosyası + hash raporu
AV tarama raporu
Karantina kayıtları (varsa)
MissionID tabanlı ingest/işleme log zinciri
EK - Kimlik Doğrulama ve Üyelik Akışı (Sade Model)
Bu bölümün kanonik tanımı için: Kanonik Rehber [KR-050].

---

# 3) İş Planı Akış Dokümanı (Özet Görünüm)

> Not: Bu bölüm, tam metni tekrar etmek yerine “akış haritası” olarak tutulur. Detay kural metinleri için SSOT ve Kanonik bölümlere bakılır.

tarlaanaliz.com – İş Planı Akış Dokümanı
Tarım + Drone + Yapay Zekâ ile Hastalık / Zararlı / Yabancı Ot Tespiti (Web + Mobil + YZ Analiz Altyapısı)
Uyum: SSOT v1.0.0 + Kanonik Ürün/İşleyiş v2.5.2 + Geliştirici Paket 1.0.0
0. Proje özeti (KR-001)
Amaç: Çiftçilerin ürün kaybını erken uyarı ile azaltmak ve dönüm bazlı analiz hizmeti satmak. Başlangıç bölgesi GAP, ardından Türkiye geneline ölçekleme.
Sabit çerçeve (değişmez): Drone: DJI Mavic 3M. Veri: RGB + multispektral (NDVI/NDRE). Yapay zekâ sadece analiz yapar; ilaçlama/gübreleme kararı vermez. Sonuçlar web + PWA ile harita üzerinde renk + desen/ikon ile gösterilir.
Harita katmanı anlamları (renk + desen):
Sağlık (Health): Yeşil
Hastalık (Disease): Turuncu
Zararlı Böcek (Pest): Kırmızı
Mantar (Fungus): Mor
Yabancı Ot (Weed): Sarı/Hardal + noktalı desen
Su Stresi: Mavi + damla noktalı desen
Azot Stresi: Soluk gri + çapraz çizgili desen
Öncelikli ürünler (ilk 2 yıl): Pamuk, Antep fıstığı, mısır, buğday, ayçiçeği, üzüm, zeytin, kırmızı mercimek.
1. Web sitesi / Mobil uygulama (KR-013)
1.1 Kullanıcı rolleri ve temel yaklaşım (KR-011)
1.1.1 Kimlik modeli (Telefon + 6 haneli PIN) (KR-050)
Kimlik doğrulama: sadece telefon numarası + 6 haneli PIN (SMS PIN / tek kullanımlık kod yoktur).
PII minimizasyonu: e-posta ve TCKN sistemde toplanmaz ve DB'ye yazılmaz.
Roller arası erişim: Drone Pilotu ve İl Operatörü PII görmez; Merkez yönetim PII erişimi olan tek katmandır.
Bildirim kanalları: SMS + uygulama içi bildirim; e-posta kanal olarak kullanılmaz.
1.2 İş planlaması (KR-012)
1.2.1 Çiftçi üyeliği ve tarla yönetimi (KR-013)
1) Üyelik: Çiftçiler mobil uygulama veya web sitesi üzerinden üye olur. Üyelik formunda il, ilçe, ad, soyad ve telefon numarası alınır. Üye olduktan sonra kendi sayfasına yönlendirilir. (KR-050, KR-013)
2) Tarla kaydı (birden fazla tarla): Her tarla için il, ilçe, mahalle/köy, ada, parsel ve alan (m²) bilgisi girilir. Sistem her tarla için benzersiz Tarla ID (FieldID) üretir. Çiftçi üyelik sonrası tarlalarını sisteme ekler. (KR-013)
3) Tekil kayıt kuralı: Aynı il + ilçe + mahalle/köy + ada + parsel kombinasyonu ile aynı tarla ikinci kez kayıt edilemez. (KR-013)
4) Bitki türü tanımı (tarla bazında): Her tarla için ekili bitki türü seçilir. Birden fazla bitki varsa her bitki ayrı ayrı seçilir ve her biri için ekili alan (m²) girilir. (KR-013)
5) Analiz talebi (bitki türü bazında): Çiftçi analiz talebini bitki türü bazında oluşturur. Aynı tarlada birden fazla bitki varsa her bitki için ayrı talep açılır. Seçenekler: Sezonluk Paket (abonelik) veya tek seferlik analiz. (KR-012, KR-017, KR-020)
6) Bitki türü değiştirme kuralı: Bir tarlaya tanımlanan bitki türleri yılda yalnızca 1 defa değiştirilebilir. Değişiklik sadece 1 Ekim - 31 Aralık tarihleri arasında yapılabilir; tarih dışında değişiklik engellenir. (KR-013)
7) Sezonluk Paket tarama takvimi (KR-015-5): Çiftçi sezon başında tarih aralığı + sıklık seçer; sistem tüm sezon tarama günlerini görünür kılar. Sezonda 2-3 kez gün kaydırma hakkı vardır; pilot onayı ve reschedule token gerekir.
1.2.2 Kooperatif/Üreticiler birliği üyeliği ve işleyiş (KR-014)
Kooperatif/Üreticiler birliği üyelik formu: ünvan (zorunlu), kooperatif türü (enum), vergi no/VKN, MERSİS no (varsa); il/ilçe, açık adres, telefon; yetkili kişi bilgileri (ad soyad, telefon, görev, yetki seviyesi); evrak yükleme (tescil belgesi, yetki belgesi); KVKK/aydınlatma ve açık rıza beyanları. (Kimlik modeli: telefon + PIN; e-posta/TCKN toplanmaz.)
Doğrulama ve hesap durumu: Hesap 'Onay Bekliyor' durumunda açılır. Evrak kontrolü sonrası merkez yönetim tarafından 'Aktif' yapılır; eksik evrak varsa aktif edilemez. Üye olduktan sonra kendi sayfasına yönlendirilir
Üye çiftçilerin sisteme dahil edilmesi: (a) davet (QR / 6 haneli davet kodu), (b) toplu içe aktarım (Excel/CSV). Çiftçi, kooperatif bağlantısını kendi hesabından onaylar.
Tarla ve analiz yönetimi: Kooperatif veya çiftçi tarlaları ekleyebilir; tarla benzersizliği kuralı aynıdır. Kooperatif, yetkisine göre üyeleri adına analiz talebi açabilir. 'Tarla kaydı tekil, sahiplik/erişim ayrı' yaklaşımı önerilir.
Kooperatif rol/yetki matrisi
COOP_OWNER: fatura/paket satın alma + kullanıcı yönetimi dahil tüm yetkiler
COOP_ADMIN: üye/taşra operasyonu + tarla ekleme + analiz talebi açma
COOP_AGRONOMIST: analiz sonuçlarını görür, not girer (aksiyon kararı vermez)
COOP_VIEWER: sadece rapor/özet
1.2.3 Drone pilotları (DJI Mavic 3M ile uçuş) (KR-015)
Üyelik/kayıt: Pilotlar mobil veya web üzerinden üye olur. Alanlar: il, ilçe, ad soyad, telefon; drone modeli ve seri numarası; (opsiyonel) hizmet verdiği mahalle/köy listesi. Drone seri numarası güvenlik/doğrulama için referanstır.
Günlük veri teslimi: Pilotlar uçuş çıktısını her gün hafıza kartı ile yerel istasyona aktarır. Her uçuş için kart rotasyonu ve kart-ID takibi uygulanır. Kart kilitleme/şifreleme (DJI ekosistemi) mümkünse ek katmandır; güvenlik varsayımı değildir (asıl güvenlik: offline tarama + hash/manifest + karantina akışı).
Her aktarım operasyonel iş kanıtıdır ve log üretir: pilot kimliği, drone seri no, tarih/saat, batch id, tarla eşleştirme durumu (eşleşti/beklemede/hata).
Planlama kısıtları (KR-015): Pilot haftalık çalışma günlerini seçer; |work_days| <= 6.
Günlük kapasite (KR-015): Pilot daily_capacity_donum 2500-3000 dönüm/gün aralığında tanımlıdır; planlama motoru bunu aşamaz.
Kota mantığı (KR-015): Sistem 'seed' (yeni müşteri/alan) ve 'pull' (mevcut abonelik taraması) için ayrı kota uygular.
İptal/yeniden atama (KR-015): Müşteri iptali veya hava koşulu gibi durumlarda görev başka pilota yeniden atanabilir; audit log zorunludur.
Bitki türü bazlı operasyon profili (admin): Her crop_type için effort_factor (eşdeğer dönüm), sistem seed kota (varsayılan 1500), tarama periyodu (interval_days) ve opsiyonel uyarı/öncelik parametreleri tanımlanır. Pilot daily_capacity_donum 2500-3000 kanonik kalır; planlama motoru eşdeğer dönüm üzerinden kapasiteyi uygular. (KR-015-1, KR-015-2)
Haftalık görev dağıtımı (Weekly Plan): Sistem her hafta başında (pazartesi 00:00) önümüzdeki 7 gün için Pilot Inbox planını üretir ve görünür kılar (soft-freeze). Hafta içi değişiklik gerekiyorsa (hava/iptal/arıza) replan yapılır ve tüm değişiklikler audit log'a yazılır. (KR-015-1..4, KR-015-5)
Hava nedeniyle uçuş engeli raporu (Weather Block): Pilot, uygulamadan "Uçuş yapılamıyor (hava)" raporu açar (MissionID, zaman, kısa neden; opsiyonel kanıt). Rapor PENDING olur ve sistem + yerel istasyon operatörü doğrulamasıyla VERIFIED/REJECTED'e döner. (KR-015-3)
Doğrulanan Weather Block sonrası yeniden planlama: Mission REPLAN_QUEUE'ya alınır; aynı hafta içinde uygun slot aranır (aynı pilot/bir başka gün veya başka pilot). Sezonluk paketlerde replan, seçilen tarih aralığı içinde kalmaya çalışır. Slot bulunamazsa ESCALATION ile admin uyarılır. (KR-015-3, KR-015-5)
Reschedule token politikası: Weather Block (force majeure) yeniden planlaması çiftçinin reschedule_token hakkını tüketmez; sistem içi "system_reschedule" olarak işlenir. Tüm bildirimler (SMS + uygulama içi) ve audit trail zorunludur. (KR-015-5)
Not: Bu planlama akışı AI inference değildir; kural tabanlı (rule-based) çalışır. Yerel istasyonda model çalıştırmama ilkesi korunur.
Uçuş görevi üretimi: Field boundary üzerinden otomatik uçuş görevi dosyası üretilir (KML/KMZ/WPML). Pilot bu görevi DJI Pilot 2 üzerinden içe aktararak standard mapping görevini başlatır. Pilot eğitim/entegrasyon adımları: DJI_ENTEGRASYON_SAHA_KILAVUZU_v1 (SOP dokümanı). Görev dosyası isimlendirmesi PII içermez; MissionID/GörevID esas alınır.
Büyük alanlar (KR-015): Tek görev kapasiteyi aşıyorsa çoklu pilot/çoklu sortie ile bölünür; tek Mission altında alt-görevler izlenir.
Taranan alanın tarla ile ilişkilendirilmesi (zorunlu): Yüklenen çekimler mutlaka sistemde kayıtlı bir tarla ile otomatik eşleşmelidir. Minimum eşleştirme alanları: il, ilçe, mahalle/köy, ada, parsel, bitki türü (varsa FieldID). Eşleştirme yoksa işlenmez.
Drone - Tarla - Bitki Eşleştirme Politikası (routing - yönlendirme):
Amaç: Yüklenen veri setini doğru TarlaID (FieldID) ve o tarihte geçerli bitki türü ile eşleştirip analizde doğru bitki-özel YZ modelini otomatik seçmek.
Tarla sınırı doğrulama: Ada/parsel girilir; kurum anlaşmasıyla TKGM/MEGSIS harita servislerinden parsel geometrisi alınarak field boundary saklanır. (Ada/parsel resmi referans olarak korunur.)
Uçuş görevi üretimi: Field boundary üzerinden otomatik uçuş görevi dosyası üretilir (KML/KMZ/WPML). Pilot bu görevi DJI Pilot 2 üzerinden içe aktararak standard mapping görevini başlatır. Pilot eğitim/entegrasyon adımları: DJI_ENTEGRASYON_SAHA_KILAVUZU_v1 (SOP dokümanı).
İşlenmiş çıktılar: DJI Terra (Agriculture Module) veya Pix4Dfields gibi yazılımlarla üretilen GeoTIFF çıktılar standart kabul edilir.
Alternatif/ileri seviye: DJI Cloud API / WPML şablonları ile görev dosyası üretimi ve görev-ID takibi otomatikleştirilebilir.
Yükleme anı eşleştirme: Yerel istasyon, batch metadata’dan Drone Seri No + görev-ID (varsa) + kapsama alanını alır. Öncelik görev-ID eşleştirmesidir; yoksa kapsama alanı ile field boundary kesişimi kullanılır.
Bitki türü seçimi: TarlaID için tanımlı sezon bitkisi kaydı esas alınır (1 Ekim-31 Aralık aralığında güncellenebilir).
1.2.4 yz modeli ile analiz (KR-017)
Hard gate (KR-018): Calibrated Dataset (kalibre veri seti) üretilmeden AnalysisJob (analiz işi) başlatılamaz; Worker ham DN veriyi kabul etmez.
İstasyon akışı (KR-018): Offline Security PC (internetsiz tarama) -> Producer Workstation (DJI Terra/Pix4Dfields ile kalibrasyon + QC) -> CalibratedDatasetManifest + QC raporu -> Dispatch (merkez analiz kuyruğu).
Eşleştirme zorunluluğu: Her dataset TarlaID (FieldID) + o tarihte geçerli bitki türü (CropType) ile eşleşmeden işlenmez.
Model seçimi: Bitki türü + görev tipi (tek seferlik / sezonluk paket) + tarih bağlamına göre otomatik yapılır; pilot sonuç görmez, model detayları paylaşılmaz.
Çıktı akışı: Analiz sonuçları tek yönlü olarak web/mobil uygulamaya gönderilir (harita katmanları: renk + desen/ikon). Web/mobil tarafı Worker'a erişemez.
1.2.5 İl Operatörü (ildeki operasyon ortağı) (KR-083)
İl Operatörü ildeki operasyonu koordine eden ticari/operasyon ortağıdır; sözleşmeye göre %5 - %15 arası kar payı alır (admin panelden tanımlanır).
İhtiyacı: ticari KPI + kapasite planlama (abonelik sayısı, hizmet verilen alan, ödeme toplamı, ilçe yoğunluğu, SLA durumu).
KVKK gereği isim/telefon gibi PII görmeden yalnızca özet metrikleri görür.
PII'siz sunum için iki katman: Katman A (Merkez) - PII ayrı; Katman B (Operatör) - SubscriberRef gibi anonim kimlik; hassas coğrafya ilçe veya 1-2 km grid yoğunluk ile sunulur.
1.2.6 Uzman Portalı (Expert Portal) - Manuel İnceleme (KR-019)
Uzman portalı, modelin düşük güven verdiği veya çelişkili durumlarda manuel inceleme için kullanılır; PII görünmez (KR-019).
Üyelik self-signup değildir: uzman hesabı ADMIN kontrollü açılır (curated onboarding).

