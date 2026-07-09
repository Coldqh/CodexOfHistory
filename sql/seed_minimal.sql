-- Minimal seed is intentionally small. Import full MVP data from /data/*.json through your app/importer.
insert into eras (id, title, date_start, date_end, description) values
('ERA_EARLY_ROME','Early Rome','-753','-509','Legendary and early historical Rome'),
('ERA_ROMAN_REPUBLIC','Roman Republic','-509','-27','Republican Rome before imperial rule'),
('ERA_ROMAN_EMPIRE','Roman Empire','-27','476','Roman imperial system, especially the West for the MVP')
on conflict do nothing;

insert into regions (id, title) values
('REG_LATIUM','Latium'),
('REG_ROME','Rome'),
('REG_MEDITERRANEAN','Mediterranean'),
('REG_CARTHAGE','Carthage'),
('REG_ITALY','Italy'),
('REG_NORTH_AFRICA','North Africa')
on conflict do nothing;
