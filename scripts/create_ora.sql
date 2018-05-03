-- -----------------------------------------------------
-- Schema football
-- -----------------------------------------------------
CREATE USER football IDENTIFIED BY football;
GRANT UNLIMITED TABLESPACE TO football;

GRANT CREATE SESSION TO football;
GRANT CREATE TABLE TO football;
GRANT CREATE PROCEDURE TO football;
GRANT CREATE TRIGGER TO football;
GRANT CREATE VIEW TO football;
GRANT CREATE SEQUENCE TO football;
GRANT ALTER ANY TABLE TO football;
GRANT ALTER ANY PROCEDURE TO football;
GRANT ALTER ANY TRIGGER TO football;
GRANT ALTER PROFILE TO football;
GRANT DELETE ANY TABLE TO football;
GRANT DROP ANY TABLE TO football;
GRANT DROP ANY PROCEDURE TO football;
GRANT DROP ANY TRIGGER TO football;
GRANT DROP ANY VIEW TO football;
GRANT DROP PROFILE TO football;

ALTER SESSION SET CURRENT_SCHEMA = football ;

-- -----------------------------------------------------
-- Table `football`.`countrys`
-- -----------------------------------------------------
CREATE TABLE football.countrys (
  id NUMBER(10) CHECK (id > 0) NOT NULL,
  name VARCHAR2(45) NOT NULL,
  PRIMARY KEY (id),
  CONSTRAINT countrys_name_UNIQUE UNIQUE  (name)
);

-- Generate ID using sequence and trigger
CREATE SEQUENCE football.countrys_seq START WITH 1 INCREMENT BY 1;

CREATE OR REPLACE TRIGGER football.countrys_seq_tr
 BEFORE INSERT ON football.countrys FOR EACH ROW
 WHEN (NEW.id IS NULL)
BEGIN
 SELECT football.countrys_seq.NEXTVAL INTO :NEW.id FROM DUAL;
END;
/


-- -----------------------------------------------------
-- Table `football`.`sitys`
-- -----------------------------------------------------
CREATE TABLE football.sitys (
  id NUMBER(10) CHECK (id > 0) NOT NULL,
  name VARCHAR2(45) NOT NULL,
  country NUMBER(10) CHECK (country > 0) NOT NULL,
  PRIMARY KEY (id),
  CONSTRAINT fk_sitys_1
    FOREIGN KEY (country)
    REFERENCES football.countrys (id)
   )
;

-- Generate ID using sequence and trigger
CREATE SEQUENCE football.sitys_seq START WITH 1 INCREMENT BY 1;

CREATE OR REPLACE TRIGGER football.sitys_seq_tr
 BEFORE INSERT ON football.sitys FOR EACH ROW
 WHEN (NEW.id IS NULL)
BEGIN
 SELECT football.sitys_seq.NEXTVAL INTO :NEW.id FROM DUAL;
END;
/

CREATE INDEX fk_sitys_1_idx ON football.sitys (country ASC);


-- -----------------------------------------------------
-- Table `football`.`emblems`
-- -----------------------------------------------------
CREATE TABLE football.emblems (
  id NUMBER(10) CHECK (id > 0) NOT NULL,
  image VARCHAR2(45) NOT NULL,
  PRIMARY KEY (id),
  CONSTRAINT image_path_UNIQUE UNIQUE  (image))
;

-- Generate ID using sequence and trigger
CREATE SEQUENCE football.emblems_seq START WITH 1 INCREMENT BY 1;

CREATE OR REPLACE TRIGGER football.emblems_seq_tr
 BEFORE INSERT ON football.emblems FOR EACH ROW
 WHEN (NEW.id IS NULL)
BEGIN
 SELECT football.emblems_seq.NEXTVAL INTO :NEW.id FROM DUAL;
END;
/


-- -----------------------------------------------------
-- Table `football`.`teams`
-- -----------------------------------------------------
CREATE TABLE football.teams (
  id NUMBER(10) CHECK (id > 0) NOT NULL,
  name VARCHAR2(45) NOT NULL,
  city NUMBER(10) CHECK (city > 0) NOT NULL,
  emblem NUMBER(10) CHECK (emblem > 0) NULL,
  PRIMARY KEY (id),
  CONSTRAINT fk_teams_1
    FOREIGN KEY (city)
    REFERENCES football.sitys (id)
   ,
  CONSTRAINT fk_teams_2
    FOREIGN KEY (emblem)
    REFERENCES football.emblems (id)
   )
;

-- Generate ID using sequence and trigger
CREATE SEQUENCE football.teams_seq START WITH 1 INCREMENT BY 1;

CREATE OR REPLACE TRIGGER football.teams_seq_tr
 BEFORE INSERT ON football.teams FOR EACH ROW
 WHEN (NEW.id IS NULL)
BEGIN
 SELECT football.teams_seq.NEXTVAL INTO :NEW.id FROM DUAL;
END;
/

CREATE INDEX fk_teams_1_idx ON football.teams (city ASC);
CREATE INDEX fk_teams_2_idx ON football.teams (emblem ASC);


-- -----------------------------------------------------
-- Table `football`.`personal_info`
-- -----------------------------------------------------
CREATE TABLE football.personal_info (
  id NUMBER(10) CHECK (id > 0) NOT NULL,
  first_name VARCHAR2(45) NOT NULL,
  last_name VARCHAR2(45) NOT NULL,
  birthday DATE NOT NULL,
  PRIMARY KEY (id)
  )
;

-- Generate ID using sequence and trigger
CREATE SEQUENCE football.personal_info_seq START WITH 1 INCREMENT BY 1;

CREATE OR REPLACE TRIGGER football.personal_info_seq_tr
 BEFORE INSERT ON football.personal_info FOR EACH ROW
 WHEN (NEW.id IS NULL)
BEGIN
 SELECT football.personal_info_seq.NEXTVAL INTO :NEW.id FROM DUAL;
END;
/


-- -----------------------------------------------------
-- Table `football`.`team_roles`
-- -----------------------------------------------------
CREATE TABLE football.team_roles (
  id NUMBER(10) CHECK (id > 0) NOT NULL,
  name VARCHAR2(45) NOT NULL,
  PRIMARY KEY (id),
  CONSTRAINT name_UNIQUE UNIQUE  (name))
;

-- Generate ID using sequence and trigger
CREATE SEQUENCE football.team_roles_seq START WITH 1 INCREMENT BY 1;

CREATE OR REPLACE TRIGGER football.team_roles_seq_tr
 BEFORE INSERT ON football.team_roles FOR EACH ROW
 WHEN (NEW.id IS NULL)
BEGIN
 SELECT football.team_roles_seq.NEXTVAL INTO :NEW.id FROM DUAL;
END;
/


-- -----------------------------------------------------
-- Table `football`.`players`
-- -----------------------------------------------------
CREATE TABLE football.players (
  id NUMBER(10) CHECK (id > 0) NOT NULL,
  personal_info NUMBER(10) CHECK (personal_info > 0) NOT NULL,
  team NUMBER(10) CHECK (team > 0) NULL,
  playerNumber NUMBER(10) CHECK (playerNumber > 0) NOT NULL,
  role NUMBER(10) CHECK (role > 0) NOT NULL,
  PRIMARY KEY (id)
 ,
  CONSTRAINT personal_info_UNIQUE UNIQUE  (personal_info),
  CONSTRAINT fk_players_1
    FOREIGN KEY (personal_info)
    REFERENCES football.personal_info (id)
    ON DELETE CASCADE
   ,
  CONSTRAINT fk_players_2
    FOREIGN KEY (team)
    REFERENCES football.teams (id)
   ,
  CONSTRAINT fk_players_3
    FOREIGN KEY (role)
    REFERENCES football.team_roles (id)
   )
;

-- Generate ID using sequence and trigger
CREATE SEQUENCE football.players_seq START WITH 1 INCREMENT BY 1;

CREATE OR REPLACE TRIGGER football.players_seq_tr
 BEFORE INSERT ON football.players FOR EACH ROW
 WHEN (NEW.id IS NULL)
BEGIN
 SELECT football.players_seq.NEXTVAL INTO :NEW.id FROM DUAL;
END;
/

CREATE INDEX fk_players_2_idx ON football.players (team ASC);
CREATE INDEX fk_players_3_idx ON football.players (role ASC);


-- -----------------------------------------------------
-- Table `football`.`arena`
-- -----------------------------------------------------
CREATE TABLE football.arena (
  id NUMBER(10) CHECK (id > 0) NOT NULL,
  name VARCHAR2(45) NOT NULL,
  sity NUMBER(10) CHECK (sity > 0) NOT NULL,
  PRIMARY KEY (id)
 ,
  CONSTRAINT fk_arena_1
    FOREIGN KEY (sity)
    REFERENCES football.sitys (id)
   )
;

-- Generate ID using sequence and trigger
CREATE SEQUENCE football.arena_seq START WITH 1 INCREMENT BY 1;

CREATE OR REPLACE TRIGGER football.arena_seq_tr
 BEFORE INSERT ON football.arena FOR EACH ROW
 WHEN (NEW.id IS NULL)
BEGIN
 SELECT football.arena_seq.NEXTVAL INTO :NEW.id FROM DUAL;
END;
/

CREATE INDEX fk_arena_1_idx ON football.arena (sity ASC);


-- -----------------------------------------------------
-- Table `football`.`matchs`
-- -----------------------------------------------------
CREATE TABLE football.matchs (
  id NUMBER(10) CHECK (id > 0) NOT NULL,
  home_team NUMBER(10) CHECK (home_team > 0) NOT NULL,
  guest_team NUMBER(10) CHECK (guest_team > 0) NOT NULL,
  matchStart TIMESTAMP(0) NOT NULL,
  arena NUMBER(10) CHECK (arena > 0) NOT NULL,
  result NUMBER(10) CHECK (result > 0) NULL,
  PRIMARY KEY (id)
 ,
  CONSTRAINT result_UNIQUE UNIQUE  (result),
  CONSTRAINT fk_matchs_1
    FOREIGN KEY (home_team)
    REFERENCES football.teams (id)
   ,
  CONSTRAINT fk_matchs_2
    FOREIGN KEY (guest_team)
    REFERENCES football.teams (id)
   ,
  CONSTRAINT fk_matchs_3
    FOREIGN KEY (arena)
    REFERENCES football.arena (id)
   )
;

-- Generate ID using sequence and trigger
CREATE SEQUENCE football.matchs_seq START WITH 1 INCREMENT BY 1;

CREATE OR REPLACE TRIGGER football.matchs_seq_tr
 BEFORE INSERT ON football.matchs FOR EACH ROW
 WHEN (NEW.id IS NULL)
BEGIN
 SELECT football.matchs_seq.NEXTVAL INTO :NEW.id FROM DUAL;
END;
/

CREATE INDEX fk_matchs_1_idx ON football.matchs (home_team ASC);
CREATE INDEX fk_matchs_2_idx ON football.matchs (guest_team ASC);
CREATE INDEX fk_matchs_3_idx ON football.matchs (arena ASC);


-- -----------------------------------------------------
-- Table `football`.`goals`
-- -----------------------------------------------------
CREATE TABLE football.goals (
  id NUMBER(10) CHECK (id > 0) NOT NULL,
  match NUMBER(10) CHECK (match > 0) NOT NULL,
  time TIMESTAMP(0) NOT NULL,
  player NUMBER(10) CHECK (player > 0) NOT NULL,
  PRIMARY KEY (id)
 ,
  CONSTRAINT fk_goals_1
    FOREIGN KEY (match)
    REFERENCES football.matchs (id)
    ON DELETE CASCADE
   ,
  CONSTRAINT fk_goals_2
    FOREIGN KEY (player)
    REFERENCES football.players (id)
    ON DELETE SET NULL
   )
;

-- Generate ID using sequence and trigger
CREATE SEQUENCE football.goals_seq START WITH 1 INCREMENT BY 1;

CREATE OR REPLACE TRIGGER football.goals_seq_tr
 BEFORE INSERT ON football.goals FOR EACH ROW
 WHEN (NEW.id IS NULL)
BEGIN
 SELECT football.goals_seq.NEXTVAL INTO :NEW.id FROM DUAL;
END;
/

CREATE INDEX fk_goals_1_idx ON football.goals (match ASC);
CREATE INDEX fk_goals_2_idx ON football.goals (player ASC);


-- -----------------------------------------------------
-- Table `football`.`card_types`
-- -----------------------------------------------------
CREATE TABLE football.card_types (
  id NUMBER(10) CHECK (id > 0) NOT NULL,
  color VARCHAR2(45) NOT NULL,
  PRIMARY KEY (id),
  CONSTRAINT color_UNIQUE UNIQUE  (color))
;

-- Generate ID using sequence and trigger
CREATE SEQUENCE football.card_types_seq START WITH 1 INCREMENT BY 1;

CREATE OR REPLACE TRIGGER football.card_types_seq_tr
 BEFORE INSERT ON football.card_types FOR EACH ROW
 WHEN (NEW.id IS NULL)
BEGIN
 SELECT football.card_types_seq.NEXTVAL INTO :NEW.id FROM DUAL;
END;
/


-- -----------------------------------------------------
-- Table `football`.`cards`
-- -----------------------------------------------------
CREATE TABLE football.cards (
  id NUMBER(10) CHECK (id > 0) NOT NULL,
  type NUMBER(10) CHECK (type > 0) NOT NULL,
  match NUMBER(10) CHECK (match > 0) NOT NULL,
  time TIMESTAMP(0) NOT NULL,
  player NUMBER(10) CHECK (player > 0) NOT NULL,
  PRIMARY KEY (id)
 ,
  CONSTRAINT fk_cards_1
    FOREIGN KEY (type)
    REFERENCES football.card_types (id)
   ,
  CONSTRAINT fk_cards_2
    FOREIGN KEY (match)
    REFERENCES football.matchs (id)
    ON DELETE CASCADE
   ,
  CONSTRAINT fk_cards_3
    FOREIGN KEY (player)
    REFERENCES football.players (id)
    ON DELETE SET NULL
   )
;

-- Generate ID using sequence and trigger
CREATE SEQUENCE football.cards_seq START WITH 1 INCREMENT BY 1;

CREATE OR REPLACE TRIGGER football.cards_seq_tr
 BEFORE INSERT ON football.cards FOR EACH ROW
 WHEN (NEW.id IS NULL)
BEGIN
 SELECT football.cards_seq.NEXTVAL INTO :NEW.id FROM DUAL;
END;
/

CREATE INDEX fk_cards_1_idx ON football.cards (type ASC);
CREATE INDEX fk_cards_2_idx ON football.cards (match ASC);
CREATE INDEX fk_cards_3_idx ON football.cards (player ASC);


-- -----------------------------------------------------
-- Table `football`.`users`
-- -----------------------------------------------------
CREATE TABLE football.users (
  id NUMBER(10) CHECK (id > 0) NOT NULL,
  login VARCHAR2(45) NOT NULL,
  password VARCHAR2(45) NOT NULL,
  hiden NUMBER(3) DEFAULT 0 NOT NULL,
  PRIMARY KEY (id),
  CONSTRAINT login_UNIQUE UNIQUE  (login))
;

-- Generate ID using sequence and trigger
CREATE SEQUENCE football.users_seq START WITH 1 INCREMENT BY 1;

CREATE OR REPLACE TRIGGER football.users_seq_tr
 BEFORE INSERT ON football.users FOR EACH ROW
 WHEN (NEW.id IS NULL)
BEGIN
 SELECT football.users_seq.NEXTVAL INTO :NEW.id FROM DUAL;
END;
/


-- -----------------------------------------------------
-- Table `football`.`admins`
-- -----------------------------------------------------
CREATE TABLE football.admins (
  id NUMBER(10) CHECK (id > 0) NOT NULL,
  userId NUMBER(10) CHECK (userId > 0) NOT NULL,
  PRIMARY KEY (id),
  CONSTRAINT user_UNIQUE UNIQUE  (userId),
  CONSTRAINT fk_admins_user
    FOREIGN KEY (userId)
    REFERENCES football.users (id)
   )
;

-- Generate ID using sequence and trigger
CREATE SEQUENCE football.admins_seq START WITH 1 INCREMENT BY 1;

CREATE OR REPLACE TRIGGER football.admins_seq_tr
 BEFORE INSERT ON football.admins FOR EACH ROW
 WHEN (NEW.id IS NULL)
BEGIN
 SELECT football.admins_seq.NEXTVAL INTO :NEW.id FROM DUAL;
END;
/


-- -----------------------------------------------------
-- Table `football`.`changes`
-- -----------------------------------------------------
CREATE TABLE football.changes (
  id NUMBER(10) NOT NULL,
  admin NUMBER(10) CHECK (admin > 0) NOT NULL,
  time TIMESTAMP(0) NOT NULL,
  text BLOB NOT NULL,
  PRIMARY KEY (id)
 ,
  CONSTRAINT fk_changes_1
    FOREIGN KEY (admin)
    REFERENCES football.admins (id)
   )
;

-- Generate ID using sequence and trigger
CREATE SEQUENCE football.changes_seq START WITH 1 INCREMENT BY 1;

CREATE OR REPLACE TRIGGER football.changes_seq_tr
 BEFORE INSERT ON football.changes FOR EACH ROW
 WHEN (NEW.id IS NULL)
BEGIN
 SELECT football.changes_seq.NEXTVAL INTO :NEW.id FROM DUAL;
END;
/

CREATE INDEX fk_changes_1_idx ON football.changes (admin ASC);


-- -----------------------------------------------------
-- Table `football`.`team_state`
-- -----------------------------------------------------
CREATE TABLE football.team_state (
  id NUMBER(10) CHECK (id > 0) NOT NULL,
  matchId NUMBER(10) CHECK (matchId > 0) NOT NULL,
  playerId NUMBER(10) CHECK (playerId > 0) NOT NULL,
  playerNumber NUMBER(10) CHECK (playerNumber > 0) NOT NULL,
  playHomeTeam NUMBER(3) NOT NULL
 ,
  PRIMARY KEY (id),
  CONSTRAINT fk_team_state_1
    FOREIGN KEY (matchId)
    REFERENCES football.matchs (id)
   ,
  CONSTRAINT fk_team_state_2
    FOREIGN KEY (playerId)
    REFERENCES football.players (id)
   )
;

-- Generate ID using sequence and trigger
CREATE SEQUENCE football.team_state_seq START WITH 1 INCREMENT BY 1;

CREATE OR REPLACE TRIGGER football.team_state_seq_tr
 BEFORE INSERT ON football.team_state FOR EACH ROW
 WHEN (NEW.id IS NULL)
BEGIN
 SELECT football.team_state_seq.NEXTVAL INTO :NEW.id FROM DUAL;
END;
/

CREATE INDEX fk_team_state_2_idx ON football.team_state (playerId ASC);

/*
DROP USER football CASCADE;
*/
