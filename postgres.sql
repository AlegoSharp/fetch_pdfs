-- Adminer 4.8.1 PostgreSQL 16.4 (Debian 16.4-1.pgdg120+1) dump

DROP TABLE IF EXISTS "departement";
DROP SEQUENCE IF EXISTS departement_departement_id_seq;
CREATE SEQUENCE departement_departement_id_seq INCREMENT 1 MINVALUE 1 MAXVALUE 2147483647 CACHE 1;

CREATE TABLE "public"."departement" (
    "departement_id" integer DEFAULT nextval('departement_departement_id_seq') NOT NULL,
    "departement_code" character varying(3),
    "departement_nom" character varying(255),
    "departement_nom_uppercase" character varying(255),
    "departement_slug" character varying(255),
    "departement_nom_soundex" character varying(20),
    CONSTRAINT "departement_pkey" PRIMARY KEY ("departement_id")
) WITH (oids = false);

CREATE INDEX "idx_departement_code" ON "public"."departement" USING btree ("departement_code");

CREATE INDEX "idx_departement_nom_soundex" ON "public"."departement" USING btree ("departement_nom_soundex");

CREATE INDEX "idx_departement_slug" ON "public"."departement" USING btree ("departement_slug");

INSERT INTO "departement" ("departement_id", "departement_code", "departement_nom", "departement_nom_uppercase", "departement_slug", "departement_nom_soundex") VALUES
(1,	'01',	'Ain',	'AIN',	'ain',	'A500'),
(2,	'02',	'Aisne',	'AISNE',	'aisne',	'A250'),
(3,	'03',	'Allier',	'ALLIER',	'allier',	'A460'),
(5,	'05',	'Hautes-Alpes',	'HAUTES-ALPES',	'hautes-alpes',	'H32412'),
(4,	'04',	'Alpes-de-Haute-Provence',	'ALPES-DE-HAUTE-PROVENCE',	'alpes-de-haute-provence',	'A412316152'),
(6,	'06',	'Alpes-Maritimes',	'ALPES-MARITIMES',	'alpes-maritimes',	'A41256352'),
(7,	'07',	'Ardèche',	'ARDÈCHE',	'ardeche',	'A632'),
(8,	'08',	'Ardennes',	'ARDENNES',	'ardennes',	'A6352'),
(9,	'09',	'Ariège',	'ARIÈGE',	'ariege',	'A620'),
(10,	'10',	'Aube',	'AUBE',	'aube',	'A100'),
(11,	'11',	'Aude',	'AUDE',	'aude',	'A300'),
(12,	'12',	'Aveyron',	'AVEYRON',	'aveyron',	'A165'),
(13,	'13',	'Bouches-du-Rhône',	'BOUCHES-DU-RHÔNE',	'bouches-du-rhone',	'B2365'),
(14,	'14',	'Calvados',	'CALVADOS',	'calvados',	'C4132'),
(15,	'15',	'Cantal',	'CANTAL',	'cantal',	'C534'),
(16,	'16',	'Charente',	'CHARENTE',	'charente',	'C653'),
(17,	'17',	'Charente-Maritime',	'CHARENTE-MARITIME',	'charente-maritime',	'C6535635'),
(18,	'18',	'Cher',	'CHER',	'cher',	'C600'),
(19,	'19',	'Corrèze',	'CORRÈZE',	'correze',	'C620'),
(20,	'2a',	'Corse-du-sud',	'CORSE-DU-SUD',	'corse-du-sud',	'C62323'),
(21,	'2b',	'Haute-corse',	'HAUTE-CORSE',	'haute-corse',	'H3262'),
(22,	'21',	'Côte-d''or',	'CÔTE-D''OR',	'cote-dor',	'C360'),
(23,	'22',	'Côtes-d''armor',	'CÔTES-D''ARMOR',	'cotes-darmor',	'C323656'),
(24,	'23',	'Creuse',	'CREUSE',	'creuse',	'C620'),
(25,	'24',	'Dordogne',	'DORDOGNE',	'dordogne',	'D6325'),
(26,	'25',	'Doubs',	'DOUBS',	'doubs',	'D120'),
(27,	'26',	'Drôme',	'DRÔME',	'drome',	'D650'),
(28,	'27',	'Eure',	'EURE',	'eure',	'E600'),
(29,	'28',	'Eure-et-Loir',	'EURE-ET-LOIR',	'eure-et-loir',	'E6346'),
(30,	'29',	'Finistère',	'FINISTÈRE',	'finistere',	'F5236'),
(31,	'30',	'Gard',	'GARD',	'gard',	'G630'),
(32,	'31',	'Haute-Garonne',	'HAUTE-GARONNE',	'haute-garonne',	'H3265'),
(33,	'32',	'Gers',	'GERS',	'gers',	'G620'),
(34,	'33',	'Gironde',	'GIRONDE',	'gironde',	'G653'),
(35,	'34',	'Hérault',	'HÉRAULT',	'herault',	'H643'),
(37,	'36',	'Indre',	'INDRE',	'indre',	'I536'),
(38,	'37',	'Indre-et-Loire',	'INDRE-ET-LOIRE',	'indre-et-loire',	'I536346'),
(39,	'38',	'Isère',	'ISÈRE',	'isere',	'I260'),
(40,	'39',	'Jura',	'JURA',	'jura',	'J600'),
(41,	'40',	'Landes',	'LANDES',	'landes',	'L532'),
(42,	'41',	'Loir-et-Cher',	'LOIR-ET-CHER',	'loir-et-cher',	'L6326'),
(43,	'42',	'Loire',	'LOIRE',	'loire',	'L600'),
(44,	'43',	'Haute-Loire',	'HAUTE-LOIRE',	'haute-loire',	'H346'),
(45,	'44',	'Loire-Atlantique',	'LOIRE-ATLANTIQUE',	'loire-atlantique',	'L634532'),
(46,	'45',	'Loiret',	'LOIRET',	'loiret',	'L630'),
(47,	'46',	'Lot',	'LOT',	'lot',	'L300'),
(48,	'47',	'Lot-et-Garonne',	'LOT-ET-GARONNE',	'lot-et-garonne',	'L3265'),
(49,	'48',	'Lozère',	'LOZÈRE',	'lozere',	'L260'),
(50,	'49',	'Maine-et-Loire',	'MAINE-ET-LOIRE',	'maine-et-loire',	'M346'),
(51,	'50',	'Manche',	'MANCHE',	'manche',	'M200'),
(52,	'51',	'Marne',	'MARNE',	'marne',	'M650'),
(53,	'52',	'Haute-Marne',	'HAUTE-MARNE',	'haute-marne',	'H3565'),
(54,	'53',	'Mayenne',	'MAYENNE',	'mayenne',	'M000'),
(55,	'54',	'Meurthe-et-Moselle',	'MEURTHE-ET-MOSELLE',	'meurthe-et-moselle',	'M63524'),
(56,	'55',	'Meuse',	'MEUSE',	'meuse',	'M200'),
(57,	'56',	'Morbihan',	'MORBIHAN',	'morbihan',	'M615'),
(58,	'57',	'Moselle',	'MOSELLE',	'moselle',	'M240'),
(59,	'58',	'Nièvre',	'NIÈVRE',	'nievre',	'N160'),
(60,	'59',	'Nord',	'NORD',	'nord',	'N630'),
(61,	'60',	'Oise',	'OISE',	'oise',	'O200'),
(62,	'61',	'Orne',	'ORNE',	'orne',	'O650'),
(63,	'62',	'Pas-de-Calais',	'PAS-DE-CALAIS',	'pas-de-calais',	'P23242'),
(64,	'63',	'Puy-de-Dôme',	'PUY-DE-DÔME',	'puy-de-dome',	'P350'),
(65,	'64',	'Pyrénées-Atlantiques',	'PYRÉNÉES-ATLANTIQUES',	'pyrenees-atlantiques',	'P65234532'),
(66,	'65',	'Hautes-Pyrénées',	'HAUTES-PYRÉNÉES',	'hautes-pyrenees',	'H321652'),
(67,	'66',	'Pyrénées-Orientales',	'PYRÉNÉES-ORIENTALES',	'pyrenees-orientales',	'P65265342'),
(68,	'67',	'Bas-Rhin',	'BAS-RHIN',	'bas-rhin',	'B265'),
(69,	'68',	'Haut-Rhin',	'HAUT-RHIN',	'haut-rhin',	'H365'),
(70,	'69',	'Rhône',	'RHÔNE',	'rhone',	'R500'),
(71,	'70',	'Haute-Saône',	'HAUTE-SAÔNE',	'haute-saone',	'H325'),
(72,	'71',	'Saône-et-Loire',	'SAÔNE-ET-LOIRE',	'saone-et-loire',	'S5346'),
(73,	'72',	'Sarthe',	'SARTHE',	'sarthe',	'S630'),
(74,	'73',	'Savoie',	'SAVOIE',	'savoie',	'S100'),
(75,	'74',	'Haute-Savoie',	'HAUTE-SAVOIE',	'haute-savoie',	'H321'),
(76,	'75',	'Paris',	'PARIS',	'paris',	'P620'),
(77,	'76',	'Seine-Maritime',	'SEINE-MARITIME',	'seine-maritime',	'S5635'),
(78,	'77',	'Seine-et-Marne',	'SEINE-ET-MARNE',	'seine-et-marne',	'S53565'),
(79,	'78',	'Yvelines',	'YVELINES',	'yvelines',	'Y1452'),
(80,	'79',	'Deux-Sèvres',	'DEUX-SÈVRES',	'deux-sevres',	'D2162'),
(81,	'80',	'Somme',	'SOMME',	'somme',	'S500'),
(82,	'81',	'Tarn',	'TARN',	'tarn',	'T650'),
(83,	'82',	'Tarn-et-Garonne',	'TARN-ET-GARONNE',	'tarn-et-garonne',	'T653265'),
(84,	'83',	'Var',	'VAR',	'var',	'V600'),
(85,	'84',	'Vaucluse',	'VAUCLUSE',	'vaucluse',	'V242'),
(86,	'85',	'Vendée',	'VENDÉE',	'vendee',	'V530'),
(87,	'86',	'Vienne',	'VIENNE',	'vienne',	'V500'),
(88,	'87',	'Haute-Vienne',	'HAUTE-VIENNE',	'haute-vienne',	'H315'),
(89,	'88',	'Vosges',	'VOSGES',	'vosges',	'V200'),
(90,	'89',	'Yonne',	'YONNE',	'yonne',	'Y500'),
(91,	'90',	'Territoire de Belfort',	'TERRITOIRE DE BELFORT',	'territoire-de-belfort',	'T636314163'),
(92,	'91',	'Essonne',	'ESSONNE',	'essonne',	'E250'),
(93,	'92',	'Hauts-de-Seine',	'HAUTS-DE-SEINE',	'hauts-de-seine',	'H32325'),
(94,	'93',	'Seine-Saint-Denis',	'SEINE-SAINT-DENIS',	'seine-saint-denis',	'S525352'),
(95,	'94',	'Val-de-Marne',	'VAL-DE-MARNE',	'val-de-marne',	'V43565'),
(96,	'95',	'Val-d''oise',	'VAL-D''OISE',	'val-doise',	'V432'),
(97,	'976',	'Mayotte',	'MAYOTTE',	'mayotte',	'M300'),
(98,	'971',	'Guadeloupe',	'GUADELOUPE',	'guadeloupe',	'G341'),
(99,	'973',	'Guyane',	'GUYANE',	'guyane',	'G500'),
(100,	'972',	'Martinique',	'MARTINIQUE',	'martinique',	'M6352'),
(101,	'974',	'Réunion',	'RÉUNION',	'reunion',	'R500'),
(36,	'35',	'Ile-et-Vilaine',	'ILE-ET-VILAINE',	'ille-et-vilaine',	'I43145');

DROP TABLE IF EXISTS "pdf_link";
DROP SEQUENCE IF EXISTS pdf_link_id_seq;
CREATE SEQUENCE pdf_link_id_seq INCREMENT 1 MINVALUE 1 MAXVALUE 2147483647 CACHE 1;

CREATE TABLE "public"."pdf_link" (
    "id" integer DEFAULT nextval('pdf_link_id_seq') NOT NULL,
    "departement_id" integer,
    "pdf_url" text NOT NULL,
    "start_date" date NOT NULL,
    "end_date" date NOT NULL,
    CONSTRAINT "pdf_link_pkey" PRIMARY KEY ("id")
) WITH (oids = false);

INSERT INTO "pdf_link" ("id", "departement_id", "pdf_url") VALUES
(199,	30,	'/contenu/telechargement/64051/486125/file/RAA 29-2024-110-du 12 août 2024.pdf'),
(233,	23,	'/contenu/telechargement/69004/571943/file/recueil-22-2024-166-recueil-des-actes-administratifs-special.pdf'),
(234,	57,	'/contenu/telechargement/72548/563446/file/56-2024-068 - RAA du 14 août 2024 - 1ère quinzaine.pdf'),
(235,	57,	'/contenu/telechargement/72486/562975/file/56-2024-065 - RAA Spécial du 8 août 2024.pdf');

DROP TABLE IF EXISTS "raa";
DROP SEQUENCE IF EXISTS raa_id_seq;
CREATE SEQUENCE raa_id_seq INCREMENT 1 MINVALUE 1 MAXVALUE 2147483647 CACHE 1;

CREATE TABLE "public"."raa" (
    "id" integer DEFAULT nextval('raa_id_seq') NOT NULL,
    "departement_id" integer,
    "year" character varying(4) NOT NULL,
    "publications_url" text,
    "raa_url" text,
    CONSTRAINT "raa_pkey" PRIMARY KEY ("id")
) WITH (oids = false);

INSERT INTO "raa" ("id", "departement_id", "year", "publications_url", "raa_url") VALUES
(1,	30,	'2024',	'/contenu/telechargement/64042/486037/file/RAA 29-2024-110-du 12 août 2024.pdf',	'https://www.finistere.gouv.fr/Publications/Recueil-des-actes-administratifs/Recueils-publies-en-2024'),
(34,	57,	'2024',	NULL,	'https://www.morbihan.gouv.fr/RAA/Annee-2024'),
(35,	36,	'2024',	NULL,	'https://www.ille-et-vilaine.gouv.fr/Publications/Recueil-des-actes-administratifs/Recueil-des-actes-administratifs-2024'),
(36,	23,	'2024',	NULL,	'https://www.cotes-darmor.gouv.fr/Publications/Recueil-des-actes-administratifs/AOUT-2024'),
(37,	23,	'2024',	NULL,	'https://www.cotes-darmor.gouv.fr/Publications/Recueil-des-actes-administratifs/SEPTEMBRE-2024'),
(38,	23,	'2024',	NULL,	'https://www.cotes-darmor.gouv.fr/Publications/Recueil-des-actes-administratifs/OCTOBRE-2024');

ALTER TABLE ONLY "public"."pdf_link" ADD CONSTRAINT "pdf_link_departement_id_fkey" FOREIGN KEY (departement_id) REFERENCES departement(departement_id) NOT DEFERRABLE;

ALTER TABLE ONLY "public"."raa" ADD CONSTRAINT "raa_departement_id_fkey" FOREIGN KEY (departement_id) REFERENCES departement(departement_id) NOT DEFERRABLE;

-- 2024-08-21 15:54:22.542445+00
