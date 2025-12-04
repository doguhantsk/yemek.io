from app import app, db
from models import User, Category, Recipe, Comment, Page
from datetime import datetime

def seed_database():
    """Veritabanına örnek veriler ekle"""
    
    with app.app_context():
        # Önce tüm tabloları temizle
        db.drop_all()
        db.create_all()
        
        print("Veritabanı tablolan oluşturuldu...")
        
        # 1. Admin kullanıcı oluştur
        admin = User(username='admin', is_admin=True)
        admin.set_password('admin123')
        db.session.add(admin)
        
        # 2. Normal kullanıcılar oluştur
        user1 = User(username='ayse')
        user1.set_password('12345')
        db.session.add(user1)
        
        user2 = User(username='mehmet')
        user2.set_password('12345')
        db.session.add(user2)
        
        db.session.commit()
        print("Kullanıcılar eklendi...")
        
        # 3. Kategoriler oluştur
        categories_data = [
            {'name': 'Kahvaltı', 'slug': 'kahvalti', 'description': 'Güne enerjik başlamak için lezzetli kahvaltı tarifleri'},
            {'name': 'Öğle Yemeği', 'slug': 'ogle-yemegi', 'description': 'Doyurucu ve pratik öğle yemeği tarifleri'},
            {'name': 'Akşam Yemeği', 'slug': 'aksam-yemegi', 'description': 'Ailenizle paylaşabileceğiniz özel akşam yemeği tarifleri'},
            {'name': 'Tatlılar', 'slug': 'tatlilar', 'description': 'Damak tadınıza uygun tatlı tarifleri'},
            {'name': 'Çorbalar', 'slug': 'corbalar', 'description': 'Sıcacık ve doyurucu çorba tarifleri'},
            {'name': 'Salatalar', 'slug': 'salatalar', 'description': 'Sağlıklı ve ferahlatıcı salata tarifleri'}
        ]
        
        categories = []
        for cat_data in categories_data:
            cat = Category(**cat_data)
            db.session.add(cat)
            categories.append(cat)
        
        db.session.commit()
        print("Kategoriler eklendi...")
        
        # 4. Tarifler oluştur
        recipes_data = [
            {
                'title': 'Menemen',
                'content': 'Geleneksel Türk kahvaltısının vazgeçilmez lezzeti menemen',
                'ingredients': '''4 adet yumurta
2 adet domates
2 adet sivri biber
1 soğan
3 yemek kaşığı sıvı yağ
Tuz, karabiber''',
                'instructions': '''1. Soğanları doğrayıp yağda kavurun
2. Biberleri ekleyip kavurmaya devam edin
3. Domatesleri ekleyin ve suyunu çekene kadar pişirin
4. Yumurtaları çırpıp ekleyin
5. Karıştırarak pişirin''',
                'category_id': 1,  # Kahvaltı
                'user_id': 1,  # admin
                'prep_time': 10,
                'cook_time': 15,
                'servings': 2
            },
            {
                'title': 'Mercimek Çorbası',
                'content': 'Sıcacık ve doyurucu klasik mercimek çorbası tarifi',
                'ingredients': '''1 su bardağı kırmızı mercimek
1 adet soğan
1 adet havuç
1 yemek kaşığı salça
6 su bardağı su
Tuz, karabiber, kimyon''',
                'instructions': '''1. Mercimeği yıkayın
2. Soğan ve havucu doğrayın
3. Tüm malzemeleri tencereye atın
4. Mercimekler yumuşayana kadar pişirin
5. Blenderdan geçirin''',
                'category_id': 5,  # Çorbalar
                'user_id': 2,  # ayse
                'prep_time': 10,
                'cook_time': 30,
                'servings': 4
            },
            {
                'title': 'Karnıyarık',
                'content': 'Enfes Türk mutfağı klasiği karnıyarık tarifi',
                'ingredients': '''4 adet patlıcan
300g kıyma
2 adet domates
2 adet sivri biber
1 soğan
3 diş sarımsak
Salça, baharatlar''',
                'instructions': '''1. Patlıcanları soyun ve kızartın
2. Kıymayı soğanla kavurun
3. Patlıcanları ortasından yırıp içini doldurun
4. Fırında pişirin''',
                'category_id': 3,  # Akşam Yemeği
                'user_id': 1,  # admin
                'prep_time': 30,
                'cook_time': 45,
                'servings': 4
            },
            {
                'title': 'Sütlaç',
                'content': 'Fırında karamelize olmuş sütlaç',
                'ingredients': '''1 litre süt
1/2 su bardağı pirinç
1 su bardağı şeker
1 yemek kaşığı un
Vanilya''',
                'instructions': '''1. Pirinci haşlayın
2. Sütü ekleyip kaynatın
3. Şeker ve unu ekleyin
4. Kıvam alınca kaselere alın
5. Fırında üstünü karamelize edin''',
                'category_id': 4,  # Tatlılar
                'user_id': 3,  # mehmet
                'prep_time': 15,
                'cook_time': 40,
                'servings': 6
            },
            {
                'title': 'Çoban Salata',
                'content': 'Ferahlatıcı ve sağlıklı çoban salata',
                'ingredients': '''3 adet domates
2 adet salatalık
1 adet yeşil biber
1 soğan
Maydanoz
Zeytinyağı, limon, tuz''',
                'instructions': '''1. Tüm sebzeleri küp küp doğrayın
2. Maydanozu ince kıyın
3. Zeytinyağı, limon ve tuzla karıştırın''',
                'category_id': 6,  # Salatalar
                'user_id': 2,  # ayse
                'prep_time': 15,
                'cook_time': 0,
                'servings': 4
            },
            {
                'title': 'Tavuklu Pilav',
                'content': 'Pratik ve lezzetli tavuklu pilav tarifi',
                'ingredients': '''2 su bardağı pirinç
300g tavuk göğsü
1 soğan
3 su bardağı tavuk suyu
Tereyağı, tuz, karabiber''',
                'instructions': '''1. Tavukları haşlayın ve didikleyin
2. Pirinci yıkayın
3. Soğanı kavurun, pirinci ekleyin
4. Tavuk ve suyu ekleyip pişirin''',
                'category_id': 2,  # Öğle Yemeği
                'user_id': 1,  # admin
                'prep_time': 20,
                'cook_time': 25,
                'servings': 4
            }
        ]
        
        recipes = []
        for recipe_data in recipes_data:
            recipe = Recipe(**recipe_data)
            db.session.add(recipe)
            recipes.append(recipe)
        
        db.session.commit()
        print("Tarifler eklendi...")
        
        # 5. Yorumlar oluştur
        comments_data = [
            {
                'recipe_id': 1,
                'user_id': 2,
                'body': 'Çok lezzetli oldu, teşekkürler!',
                'rating': 5
            },
            {
                'recipe_id': 1,
                'user_id': 3,
                'body': 'Ailem çok beğendi, kesinlikle tekrar yapacağım.',
                'rating': 5
            },
            {
                'recipe_id': 2,
                'user_id': 1,
                'body': 'Klasik tarif, harika oldu.',
                'rating': 4
            },
            {
                'recipe_id': 3,
                'user_id': 2,
                'body': 'İlk defa denedim ve çok güzel oldu!',
                'rating': 5
            },
            {
                'recipe_id': 4,
                'user_id': 1,
                'body': 'Annemin tarifi gibi oldu, harika!',
                'rating': 5
            },
            {
                'recipe_id': 5,
                'user_id': 3,
                'body': 'Çok taze ve lezzetli bir salata.',
                'rating': 4
            },
            {
                'recipe_id': 6,
                'user_id': 2,
                'body': 'Pratik ve doyurucu, teşekkürler.',
                'rating': 4
            }
        ]
        
        for comment_data in comments_data:
            comment = Comment(**comment_data)
            db.session.add(comment)
        
        db.session.commit()
        print("Yorumlar eklendi...")
        
        # 6. Sayfalar oluştur
        pages_data = [
            {
                'slug': 'about',
                'title': 'Hakkımızda',
                'content': '''<h2>Nefis Yemekler'e Hoş Geldiniz!</h2>
                <p>Biz, yemek yapmanın sadece bir ihtiyaç değil, aynı zamanda bir sanat ve tutku olduğuna inanıyoruz. 
                Nefis Yemekler platformu, lezzetli tarifleri paylaşmak, yeni tatlar keşfetmek ve mutfak deneyimlerinizi 
                geliştirmek için oluşturuldu.</p>
                
                <h3>Misyonumuz</h3>
                <p>Türk mutfağının zengin lezzetlerini ve dünya mutfaklarından seçkin tarifleri bir araya getirerek, 
                herkesin kolayca erişebileceği bir tarif platformu oluşturmak.</p>
                
                <h3>Vizyonumuz</h3>
                <p>Türkiye'nin en kapsamlı ve kullanıcı dostu yemek tarifi platformu olmak.</p>
                
                <h3>Değerlerimiz</h3>
                <ul>
                    <li>Kaliteli ve test edilmiş tarifler</li>
                    <li>Kullanıcı dostu arayüz</li>
                    <li>Topluluk odaklı yaklaşım</li>
                    <li>Sürekli gelişim ve yenilik</li>
                </ul>'''
            },
            {
                'slug': 'contact',
                'title': 'İletişim',
                'content': '''<h2>Bizimle İletişime Geçin</h2>
                <p>Sorularınız, önerileriniz veya geri bildirimleriniz için bizimle iletişime geçebilirsiniz.</p>
                
                <h3>İletişim Bilgileri</h3>
                <p><strong>E-posta:</strong> info@nefisyemekler.com</p>
                <p><strong>Telefon:</strong> +90 (212) 555 00 00</p>
                <p><strong>Adres:</strong> İstanbul, Türkiye</p>
                
                <h3>Sosyal Medya</h3>
                <p>Bizi sosyal medyada takip edin!</p>'''
            }
        ]
        
        for page_data in pages_data:
            page = Page(**page_data)
            db.session.add(page)
        
        db.session.commit()
        print("Sayfalar eklendi...")
        
        print("\n✅ Veritabanı başarıyla dolduruldu!")
        print(f"👤 Kullanıcılar: {User.query.count()}")
        print(f"📁 Kategoriler: {Category.query.count()}")
        print(f"🍳 Tarifler: {Recipe.query.count()}")
        print(f"💬 Yorumlar: {Comment.query.count()}")
        print(f"📄 Sayfalar: {Page.query.count()}")
        print("\n🔑 Admin kullanıcı: username='admin', password='admin123'")
        print("🔑 Normal kullanıcı: username='ayse', password='12345'")
        print("🔑 Normal kullanıcı: username='mehmet', password='12345'")

if __name__ == '__main__':
    seed_database()
