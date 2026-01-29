# GGS Integration API

API для двухсторонней интеграции с Битрикс24 и базой данных (ОСА)

---

## 📦 Инструкция по запуску

### 1. Клонирование репозитория

```bash
git clone https://github.com/Sp1r14ual/ggs-integration-api.git
cd ggs-integration-api
```

### 2. Настройка окружения и зависимостей

```
python -m venv .venv

# Активация (Windows)
.venv\Scripts\activate

# Активация (Linux/macOS)
source .venv/bin/activate

pip install -r requirements.txt
```

### 3. Настройка переменных окружения

Скопируйте пример файла конфигурации и заполните его:
```
cp .env.example .env
```
Содержимое .env:
```env
BITRIX_WEBHOOK="https://dev.ggs-nsk.ru/rest/132/%SECRET%/"
DB_ENGINE_STRING='mssql+pyodbc://%COMPUTER_NAME%\\SQLEXPRESS/ggs_stud?driver=SQL+Server+Native+Client+11.0'
```

### 4. Запуск сервера
```bash
fastapi dev app/app.py
```

Сервер запустится на порту 8000

### 5. Модификация БД

Перед запуском каких-либо функций необходимо внести следующие изменения в БД:

```sql
ALTER TABLE [dbo].[house] ADD object_ks_crm_id INTEGER, gasification_stage_crm_id INTEGER;
ALTER TABLE [dbo].[organization] ADD company_crm_id INTEGER, requisite_crm_id INTEGER, bankdetail_requisite_crm_id INTEGER, has_crm_jur_address INTEGER, has_crm_fact_address INTEGER;
ALTER TABLE [dbo].[person] ADD contact_crm_id INTEGER, requisite_crm_id INTEGER, has_crm_address INTEGER;
ALTER TABLE [dbo].[equip] ADD equip_crm_id INTEGER;
ALTER TABLE [dbo].[house_equip] ADD equip_crm_id INTEGER;
ALTER TABLE [dbo].[contract] ADD contract_crm_id INTEGER;
ALTER TABLE type_contract ADD crm_category VARCHAR(32);

create schema zm
go
CREATE TABLE [zm].[gro](
  [id] [int] NOT NULL,
  [name] [varchar](max) NULL,
PRIMARY KEY CLUSTERED 
(
  [id] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
) ON [PRIMARY] TEXTIMAGE_ON [PRIMARY]

alter table net add crm_id_gro int references zm.gro(id)

CREATE TABLE [zm].[district](
  [id] [int] NOT NULL,
  [name] [varchar](max) NULL,
PRIMARY KEY CLUSTERED 
(
  [id] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
) ON [PRIMARY] TEXTIMAGE_ON [PRIMARY]

INSERT INTO [zm].[district] (id, name)
VALUES 
    (1, 'Дзержинский'),
    (2, 'Железнодорожный'),
    (3, 'Заельцовский'),
    (4, 'Калининский'),
    (5, 'Кировский'),
    (6, 'Ленинский'),
    (7, 'Октябрьский'),
    (8, 'Первомайский'),
    (9, 'Советский'),
    (10, 'Центральный'),
    (11, 'Новосибирский');

INSERT INTO [zm].[gro] (id, name)
VALUES 
    (1, 'АО "Городские газовые сети"'),
    (2, 'ООО "Газпром газораспределение Томск"'),
    (3, 'ООО "Техногаз"'),
    (4, 'ООО "НПП «Сибирский энергетический центр"'),
    (5, 'ООО "АльфаГазСтройСервис"'),
    (6, 'ООО "Новосибирскоблгаз"'),
    (7, 'ООО "Промгазсервис"'),
    (8, 'ООО "ТеплоГазСервис"'),
    (9, 'ООО "Фортуна+"'),
    (10, 'ООО "Стимул"'),
    (11, 'ОАО "Новосибирский завод искусственного волокна"'),
    (12, 'АО "УК «Промышленно-логистический парк"'),
    (13, 'ПК "Толмачевский"'),
    (14, 'ООО "Энергосети Сибири"'),
    (15, 'ФГУП "Управление энергетики и водоснабжения"'),
    (16, 'ООО "Аварийно диспетчерская служба"'),
    (17, 'неизвестно'),
    (18, 'частично ГГС');

alter table net add crm_id_district int references zm.district(id)
alter table [dbo].[net] add ground_crm_id integer
```

### 6. Документация API

Документация в формате OpenAPI доступна по адресу:

🔗 http://127.0.0.1:8000/docs