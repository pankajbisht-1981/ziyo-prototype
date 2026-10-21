-- ============================================================================
-- Ziyo — Impact KPI Dashboard · Metabase migration kit
-- Postgres schema + seed data, generated from the dashboard's DATA object.
-- Run once against an empty database:  psql "$DATABASE_URL" -f ziyo_kpi_metabase.sql
-- Then point Metabase at this database.
-- ============================================================================

BEGIN;

DROP VIEW IF EXISTS kpi_with_status;
DROP VIEW IF EXISTS kpi_latest;
DROP TABLE IF EXISTS kpi_values;
DROP TABLE IF EXISTS kpi_metrics;
DROP TABLE IF EXISTS kpi_layers;

CREATE TABLE kpi_layers (
  layer_key           text PRIMARY KEY,
  name                text NOT NULL,
  sublabel            text,
  question            text,
  position            int  NOT NULL,
  reported_to_donors  boolean NOT NULL DEFAULT false
);

CREATE TABLE kpi_metrics (
  id                serial PRIMARY KEY,
  layer_key         text NOT NULL REFERENCES kpi_layers(layer_key),
  name              text NOT NULL,
  unit              text DEFAULT '',
  target            numeric,                 -- NULL = no target (north star)
  higher_is_better  boolean NOT NULL DEFAULT true,
  definition        text,
  position          int NOT NULL
);

CREATE TABLE kpi_values (
  metric_id  int  NOT NULL REFERENCES kpi_metrics(id) ON DELETE CASCADE,
  period     date NOT NULL,            -- first of month
  value      numeric NOT NULL,
  PRIMARY KEY (metric_id, period)
);
CREATE INDEX idx_kpi_values_period ON kpi_values(period);

-- ---- layers ----------------------------------------------------------------
INSERT INTO kpi_layers(layer_key,name,sublabel,question,position,reported_to_donors) VALUES ('northstar','North Star','Headline metric','The single number that defines success',0,true);
INSERT INTO kpi_layers(layer_key,name,sublabel,question,position,reported_to_donors) VALUES ('reach','Reach','Growth KPIs','Are we reaching the right people?',1,false);
INSERT INTO kpi_layers(layer_key,name,sublabel,question,position,reported_to_donors) VALUES ('engage','Engagement','Behaviour KPIs','Are they using the platform purposefully?',2,false);
INSERT INTO kpi_layers(layer_key,name,sublabel,question,position,reported_to_donors) VALUES ('outcome','Outcome','Impact KPIs','Did anything change in their lives?',3,true);
INSERT INTO kpi_layers(layer_key,name,sublabel,question,position,reported_to_donors) VALUES ('ops','Operations','Foundation KPIs','Is the platform healthy, reliable and shipping?',4,false);

-- ---- metrics ---------------------------------------------------------------
INSERT INTO kpi_metrics(id,layer_key,name,unit,target,higher_is_better,definition,position) VALUES (1,'northstar','Active Beneficiaries','',NULL,true,'Users who completed at least one outcome-linked action and shared a success story.',1);
INSERT INTO kpi_metrics(id,layer_key,name,unit,target,higher_is_better,definition,position) VALUES (2,'reach','Total registered users','',20000,true,'Cumulative sign-ups since launch.',1);
INSERT INTO kpi_metrics(id,layer_key,name,unit,target,higher_is_better,definition,position) VALUES (3,'reach','Organic referral rate','%',25,true,'New users via invite/share / total new. Word-of-mouth trust signal.',2);
INSERT INTO kpi_metrics(id,layer_key,name,unit,target,higher_is_better,definition,position) VALUES (4,'reach','Activation rate','%',45,true,'Onboarding complete + >=1 meaningful action. Quality of user entry.',3);
INSERT INTO kpi_metrics(id,layer_key,name,unit,target,higher_is_better,definition,position) VALUES (5,'engage','Stickiness (DAU/MAU)','%',30,true,'Daily-habit strength. Below 15% signals low stickiness.',1);
INSERT INTO kpi_metrics(id,layer_key,name,unit,target,higher_is_better,definition,position) VALUES (6,'engage','Return after onboarding','%',50,true,'% who return within 7 days of signup. Leading indicator of retention.',2);
INSERT INTO kpi_metrics(id,layer_key,name,unit,target,higher_is_better,definition,position) VALUES (7,'engage','30-day retention','%',35,true,'Active in week 4 / signed up in week 1. Standard cohort-health metric.',3);
INSERT INTO kpi_metrics(id,layer_key,name,unit,target,higher_is_better,definition,position) VALUES (8,'engage','Leaderboard participation','%',50,true,'% of users with >=1 point transaction. Gamification working as designed.',4);
INSERT INTO kpi_metrics(id,layer_key,name,unit,target,higher_is_better,definition,position) VALUES (9,'engage','User satisfaction','/5',4.3,true,'Ratings & feedback from in-app survey, App Store and Play Store.',5);
INSERT INTO kpi_metrics(id,layer_key,name,unit,target,higher_is_better,definition,position) VALUES (10,'engage','Event attendance','%',60,true,'Registered attendees who showed up - plus event ratings & feedback.',6);
INSERT INTO kpi_metrics(id,layer_key,name,unit,target,higher_is_better,definition,position) VALUES (11,'outcome','Job placement rate','%',10,true,'Users placed in jobs via the platform.',1);
INSERT INTO kpi_metrics(id,layer_key,name,unit,target,higher_is_better,definition,position) VALUES (12,'outcome','Internships secured','',300,true,'Number of internships secured by beneficiaries.',2);
INSERT INTO kpi_metrics(id,layer_key,name,unit,target,higher_is_better,definition,position) VALUES (13,'outcome','Grants awarded','',150,true,'Number of grants awarded to beneficiaries.',3);
INSERT INTO kpi_metrics(id,layer_key,name,unit,target,higher_is_better,definition,position) VALUES (14,'outcome','Grant conversion rate','%',12,true,'Grants awarded / applications submitted. Shows real uplift, not just clicks.',4);
INSERT INTO kpi_metrics(id,layer_key,name,unit,target,higher_is_better,definition,position) VALUES (15,'outcome','Volunteer opportunities','',60,true,'Number of volunteer opportunities taken up by beneficiaries.',5);
INSERT INTO kpi_metrics(id,layer_key,name,unit,target,higher_is_better,definition,position) VALUES (16,'outcome','Course completion rate','%',50,true,'Courses finished / courses started. Learning actually happened.',6);
INSERT INTO kpi_metrics(id,layer_key,name,unit,target,higher_is_better,definition,position) VALUES (17,'outcome','Skills progression score','%',20,true,'Average quiz-score improvement over time. Measurable knowledge gain.',7);
INSERT INTO kpi_metrics(id,layer_key,name,unit,target,higher_is_better,definition,position) VALUES (18,'outcome','Event-to-action rate','%',30,true,'Attendees who then applied for a job or grant. Event quality, not just attendance.',8);
INSERT INTO kpi_metrics(id,layer_key,name,unit,target,higher_is_better,definition,position) VALUES (19,'outcome','Certificates issued','',2500,true,'Verified certificates earned by beneficiaries.',9);
INSERT INTO kpi_metrics(id,layer_key,name,unit,target,higher_is_better,definition,position) VALUES (20,'ops','Uptime','%',99.5,true,'Share of time the platform was available this month.',1);
INSERT INTO kpi_metrics(id,layer_key,name,unit,target,higher_is_better,definition,position) VALUES (21,'ops','Incidents reported','/mo',5,false,'Downtime / service incidents reported this month. Lower is better.',2);
INSERT INTO kpi_metrics(id,layer_key,name,unit,target,higher_is_better,definition,position) VALUES (22,'ops','Time to recovery (MTTR)','min',60,false,'Mean time to restore service after an incident. Lower is better.',3);
INSERT INTO kpi_metrics(id,layer_key,name,unit,target,higher_is_better,definition,position) VALUES (23,'ops','Time-to-publish','days',3,false,'Avg time from content ready to live. Lower is better.',4);
INSERT INTO kpi_metrics(id,layer_key,name,unit,target,higher_is_better,definition,position) VALUES (24,'ops','Release frequency','/mo',2,true,'Production releases per month. Delivery velocity.',5);
INSERT INTO kpi_metrics(id,layer_key,name,unit,target,higher_is_better,definition,position) VALUES (25,'ops','Support satisfaction (CSAT)','%',90,true,'Satisfaction from support tickets & resolution feedback.',6);

SELECT setval('kpi_metrics_id_seq', (SELECT MAX(id) FROM kpi_metrics));

-- ---- monthly values --------------------------------------------------------
INSERT INTO kpi_values(metric_id,period,value) VALUES
  (1,'2025-11-01',310),
  (1,'2025-12-01',360),
  (1,'2026-01-01',420),
  (1,'2026-02-01',505),
  (1,'2026-03-01',560),
  (1,'2026-04-01',640),
  (1,'2026-05-01',720),
  (1,'2026-06-01',815),
  (1,'2026-07-01',910),
  (1,'2026-08-01',1040),
  (1,'2026-09-01',1150),
  (1,'2026-10-01',1284);
INSERT INTO kpi_values(metric_id,period,value) VALUES
  (2,'2026-03-01',9000),
  (2,'2026-04-01',11000),
  (2,'2026-05-01',13000),
  (2,'2026-06-01',15000),
  (2,'2026-07-01',18000),
  (2,'2026-08-01',20000),
  (2,'2026-09-01',22000),
  (2,'2026-10-01',24500);
INSERT INTO kpi_values(metric_id,period,value) VALUES
  (3,'2026-03-01',12),
  (3,'2026-04-01',14),
  (3,'2026-05-01',15),
  (3,'2026-06-01',17),
  (3,'2026-07-01',18),
  (3,'2026-08-01',19),
  (3,'2026-09-01',21),
  (3,'2026-10-01',22);
INSERT INTO kpi_values(metric_id,period,value) VALUES
  (4,'2026-03-01',30),
  (4,'2026-04-01',33),
  (4,'2026-05-01',34),
  (4,'2026-06-01',36),
  (4,'2026-07-01',38),
  (4,'2026-08-01',39),
  (4,'2026-09-01',40),
  (4,'2026-10-01',41);
INSERT INTO kpi_values(metric_id,period,value) VALUES
  (5,'2026-03-01',19),
  (5,'2026-04-01',21),
  (5,'2026-05-01',22),
  (5,'2026-06-01',24),
  (5,'2026-07-01',25),
  (5,'2026-08-01',26),
  (5,'2026-09-01',27),
  (5,'2026-10-01',28);
INSERT INTO kpi_values(metric_id,period,value) VALUES
  (6,'2026-03-01',40),
  (6,'2026-04-01',43),
  (6,'2026-05-01',45),
  (6,'2026-06-01',47),
  (6,'2026-07-01',48),
  (6,'2026-08-01',50),
  (6,'2026-09-01',51),
  (6,'2026-10-01',52);
INSERT INTO kpi_values(metric_id,period,value) VALUES
  (7,'2026-03-01',26),
  (7,'2026-04-01',28),
  (7,'2026-05-01',29),
  (7,'2026-06-01',30),
  (7,'2026-07-01',31),
  (7,'2026-08-01',32),
  (7,'2026-09-01',33),
  (7,'2026-10-01',34);
INSERT INTO kpi_values(metric_id,period,value) VALUES
  (8,'2026-03-01',42),
  (8,'2026-04-01',46),
  (8,'2026-05-01',50),
  (8,'2026-06-01',53),
  (8,'2026-07-01',56),
  (8,'2026-08-01',58),
  (8,'2026-09-01',60),
  (8,'2026-10-01',61);
INSERT INTO kpi_values(metric_id,period,value) VALUES
  (9,'2026-03-01',4),
  (9,'2026-04-01',4.1),
  (9,'2026-05-01',4.1),
  (9,'2026-06-01',4.2),
  (9,'2026-07-01',4.2),
  (9,'2026-08-01',4.3),
  (9,'2026-09-01',4.3),
  (9,'2026-10-01',4.4);
INSERT INTO kpi_values(metric_id,period,value) VALUES
  (10,'2026-03-01',55),
  (10,'2026-04-01',58),
  (10,'2026-05-01',60),
  (10,'2026-06-01',62),
  (10,'2026-07-01',63),
  (10,'2026-08-01',65),
  (10,'2026-09-01',67),
  (10,'2026-10-01',68);
INSERT INTO kpi_values(metric_id,period,value) VALUES
  (11,'2026-03-01',6),
  (11,'2026-04-01',7),
  (11,'2026-05-01',8),
  (11,'2026-06-01',9),
  (11,'2026-07-01',10),
  (11,'2026-08-01',11),
  (11,'2026-09-01',11),
  (11,'2026-10-01',12);
INSERT INTO kpi_values(metric_id,period,value) VALUES
  (12,'2026-03-01',120),
  (12,'2026-04-01',165),
  (12,'2026-05-01',200),
  (12,'2026-06-01',240),
  (12,'2026-07-01',275),
  (12,'2026-08-01',300),
  (12,'2026-09-01',320),
  (12,'2026-10-01',340);
INSERT INTO kpi_values(metric_id,period,value) VALUES
  (13,'2026-03-01',60),
  (13,'2026-04-01',78),
  (13,'2026-05-01',92),
  (13,'2026-06-01',105),
  (13,'2026-07-01',118),
  (13,'2026-08-01',128),
  (13,'2026-09-01',136),
  (13,'2026-10-01',142);
INSERT INTO kpi_values(metric_id,period,value) VALUES
  (14,'2026-03-01',5),
  (14,'2026-04-01',6),
  (14,'2026-05-01',6),
  (14,'2026-06-01',7),
  (14,'2026-07-01',7),
  (14,'2026-08-01',8),
  (14,'2026-09-01',8),
  (14,'2026-10-01',8);
INSERT INTO kpi_values(metric_id,period,value) VALUES
  (15,'2026-03-01',28),
  (15,'2026-04-01',36),
  (15,'2026-05-01',44),
  (15,'2026-06-01',52),
  (15,'2026-07-01',58),
  (15,'2026-08-01',64),
  (15,'2026-09-01',70),
  (15,'2026-10-01',76);
INSERT INTO kpi_values(metric_id,period,value) VALUES
  (16,'2026-03-01',35),
  (16,'2026-04-01',38),
  (16,'2026-05-01',40),
  (16,'2026-06-01',42),
  (16,'2026-07-01',44),
  (16,'2026-08-01',45),
  (16,'2026-09-01',46),
  (16,'2026-10-01',47);
INSERT INTO kpi_values(metric_id,period,value) VALUES
  (17,'2026-03-01',12),
  (17,'2026-04-01',14),
  (17,'2026-05-01',16),
  (17,'2026-06-01',18),
  (17,'2026-07-01',19),
  (17,'2026-08-01',21),
  (17,'2026-09-01',22),
  (17,'2026-10-01',23);
INSERT INTO kpi_values(metric_id,period,value) VALUES
  (18,'2026-03-01',20),
  (18,'2026-04-01',22),
  (18,'2026-05-01',24),
  (18,'2026-06-01',26),
  (18,'2026-07-01',27),
  (18,'2026-08-01',29),
  (18,'2026-09-01',30),
  (18,'2026-10-01',31);
INSERT INTO kpi_values(metric_id,period,value) VALUES
  (19,'2026-03-01',1200),
  (19,'2026-04-01',1500),
  (19,'2026-05-01',1800),
  (19,'2026-06-01',2100),
  (19,'2026-07-01',2400),
  (19,'2026-08-01',2700),
  (19,'2026-09-01',2900),
  (19,'2026-10-01',3120);
INSERT INTO kpi_values(metric_id,period,value) VALUES
  (20,'2026-03-01',99.2),
  (20,'2026-04-01',99.3),
  (20,'2026-05-01',99.4),
  (20,'2026-06-01',99.5),
  (20,'2026-07-01',99.6),
  (20,'2026-08-01',99.5),
  (20,'2026-09-01',99.6),
  (20,'2026-10-01',99.7);
INSERT INTO kpi_values(metric_id,period,value) VALUES
  (21,'2026-03-01',11),
  (21,'2026-04-01',9),
  (21,'2026-05-01',8),
  (21,'2026-06-01',7),
  (21,'2026-07-01',6),
  (21,'2026-08-01',5),
  (21,'2026-09-01',5),
  (21,'2026-10-01',4);
INSERT INTO kpi_values(metric_id,period,value) VALUES
  (22,'2026-03-01',95),
  (22,'2026-04-01',82),
  (22,'2026-05-01',74),
  (22,'2026-06-01',66),
  (22,'2026-07-01',58),
  (22,'2026-08-01',50),
  (22,'2026-09-01',44),
  (22,'2026-10-01',38);
INSERT INTO kpi_values(metric_id,period,value) VALUES
  (23,'2026-03-01',5.5),
  (23,'2026-04-01',4.8),
  (23,'2026-05-01',4.2),
  (23,'2026-06-01',3.6),
  (23,'2026-07-01',3.2),
  (23,'2026-08-01',2.9),
  (23,'2026-09-01',2.6),
  (23,'2026-10-01',2.4);
INSERT INTO kpi_values(metric_id,period,value) VALUES
  (24,'2026-03-01',1),
  (24,'2026-04-01',1.2),
  (24,'2026-05-01',1.5),
  (24,'2026-06-01',1.8),
  (24,'2026-07-01',2.2),
  (24,'2026-08-01',2.6),
  (24,'2026-09-01',2.9),
  (24,'2026-10-01',3.2);
INSERT INTO kpi_values(metric_id,period,value) VALUES
  (25,'2026-03-01',84),
  (25,'2026-04-01',85),
  (25,'2026-05-01',87),
  (25,'2026-06-01',88),
  (25,'2026-07-01',89),
  (25,'2026-08-01',90),
  (25,'2026-09-01',91),
  (25,'2026-10-01',92);

-- ---- convenience views -----------------------------------------------------
-- Latest value per metric
CREATE VIEW kpi_latest AS
SELECT v.metric_id,
       v.value      AS latest_value,
       v.period     AS latest_period
FROM kpi_values v
JOIN (SELECT metric_id, MAX(period) AS mp FROM kpi_values GROUP BY metric_id) mx
  ON mx.metric_id = v.metric_id AND mx.mp = v.period;

-- One row per metric with target attainment + status label (for number cards)
CREATE VIEW kpi_with_status AS
SELECT m.id              AS metric_id,
       l.name            AS layer,
       l.position        AS layer_position,
       l.reported_to_donors,
       m.name            AS metric,
       m.unit,
       m.definition,
       m.target,
       m.higher_is_better,
       k.latest_value,
       k.latest_period,
       CASE WHEN m.target IS NULL OR m.target = 0 THEN NULL
            WHEN m.higher_is_better THEN round(100.0 * k.latest_value / m.target, 1)
            ELSE round(100.0 * m.target / NULLIF(k.latest_value,0), 1)
       END               AS pct_of_target,
       CASE
         WHEN m.target IS NULL THEN 'North Star'
         WHEN (m.higher_is_better AND k.latest_value >= m.target)
           OR (NOT m.higher_is_better AND k.latest_value <= m.target) THEN 'On track'
         WHEN (m.higher_is_better AND k.latest_value >= 0.9 * m.target)
           OR (NOT m.higher_is_better AND k.latest_value <= 1.1 * m.target) THEN 'At risk'
         ELSE 'Behind'
       END               AS status
FROM kpi_metrics m
JOIN kpi_layers l ON l.layer_key = m.layer_key
JOIN kpi_latest k ON k.metric_id = m.id;

COMMIT;
