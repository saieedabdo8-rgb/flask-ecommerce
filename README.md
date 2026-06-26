# 🛒 متجر إلكتروني - Flask + SQLite

موقع متجر إلكتروني بسيط باستخدام Flask + SQLite + Tailwind CSS.
جاهز للنشر على **PythonAnywhere** مجاناً.

## المميزات
- عرض المنتجات (صور، اسم، سعر)
- تقديم طلب شراء بدون تسجيل دخول
- لوحة تحكم للأدمن (إضافة/تعديل/حذف منتجات + مشاهدة الطلبات)
- تصميم متجاوب بالعربية (RTL)

## 📁 ملفات المشروع

| الملف | الوظيفة |
|-------|---------|
| `app.py` | ملف Flask الرئيسي (routes, config) |
| `models.py` | نماذج قاعدة البيانات (Product, Order, Admin) |
| `wsgi.py` | ملف WSGI للنشر على PythonAnywhere |
| `requirements.txt` | الحزم المطلوبة |
| `templates/` | قوالب HTML (Tailwind CSS) |

## 🚀 النشر على PythonAnywhere

### 1. افتح Bash Console في PythonAnywhere
```
Dashboard → Consoles → Bash
```

### 2. انسخ المشروع
```bash
git clone https://github.com/saieedabdo8-rgb/flask-ecommerce.git
cd flask-ecommerce
```

### 3. أنشئ Virtual Environment
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 4. إعداد Web App
- Dashboard → **Web** → **Add a new web app**
- **Manual configuration** → **Python 3.10**
- الإعدادات:
  - **Source code:** `/home/Abdoerhman/flask-ecommerce`
  - **Working directory:** `/home/Abdoerhman/flask-ecommerce`
  - **Virtual environment:** `/home/Abdoerhman/flask-ecommerce/venv`

### 5. تعديل WSGI file
- اضغط على رابط **WSGI configuration file**
- امسح الكل وحط:

```python
import sys
import os

path = '/home/Abdoerhman/flask-ecommerce'
if path not in sys.path:
    sys.path.append(path)

os.environ['FLASK_ENV'] = 'production'

from app import app as application
```

### 6. شغّل الموقع
- رجوع لصفحة Web → **Reload**
- الموقع على: `https://Abdoerhman.pythonanywhere.com`

### 7. أدخل بيانات الأدمن
- رابط تسجيل الدخول: `/admin/login`
- اسم المستخدم: `admin`
- كلمة السر: `admin123`

## 🗄️ قاعدة البيانات
البيانات بتتحفظ في `instance/shop.db` (جذر المشروع).
لإضافة منتجات أو تجربة، استخدم لوحة التحكم.

## ⚠️ ملاحظة PythonAnywhere المجاني
الموقع بينام بعد 3 شهور من عدم الاستخدام.
لإفاقته: افتح رابط الموقع، أو سجل دخولك على PythonAnywhere واضغط **Reload**.
