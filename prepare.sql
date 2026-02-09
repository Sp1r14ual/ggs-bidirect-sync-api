ALTER TABLE [dbo].[house] ADD object_ks_crm_id INTEGER, gasification_stage_crm_id INTEGER;
ALTER TABLE [dbo].[organization] ADD company_crm_id INTEGER, requisite_crm_id INTEGER, bankdetail_requisite_crm_id INTEGER, has_crm_jur_address INTEGER, has_crm_fact_address INTEGER;
ALTER TABLE [dbo].[person] ADD contact_crm_id INTEGER, requisite_crm_id INTEGER, has_crm_address INTEGER;
ALTER TABLE [dbo].[equip] ADD equip_crm_id INTEGER;
ALTER TABLE [dbo].[house_equip] ADD equip_crm_id INTEGER;
ALTER TABLE [dbo].[contract] ADD contract_crm_id INTEGER;
alter table type_contract add crm_category varchar(32);
ALTER TABLE [dbo].[house_owner]
    ADD id_organization INTEGER,
    FOREIGN KEY(id_organization) REFERENCES organization(id);
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
alter table [dbo].[net] add ground_crm_id integer;

CREATE TABLE [dbo].[type_boil_classification](
        [id] [int] IDENTITY(1,1) NOT NULL,
        [name] [varchar](128) NOT NULL,
PRIMARY KEY CLUSTERED 
(
        [id] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY],
UNIQUE NONCLUSTERED 
(
        [name] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
) ON [PRIMARY]

GO

insert into type_boil_classification(name) values('конденсационный');
insert into type_boil_classification(name) values('вентиляторный');
insert into type_boil_classification(name) values('атмосферный');
insert into type_boil_classification(name) values('проточный');
insert into type_boil_classification(name) values('автоматический');
insert into type_boil_classification(name) values('полуавтоматический');
insert into type_boil_classification(name) values('емкостной');

ALTER TABLE house_equip ADD id_type_boil_classification INTEGER REFERENCES type_boil_classification(id);
