-- MySQL Script generated by MySQL Workbench
-- Пт 08 дек 2017 23:01:32
-- Model: New Model    Version: 1.0
-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='TRADITIONAL,ALLOW_INVALID_DATES';

-- -----------------------------------------------------
-- Schema football
-- -----------------------------------------------------

-- -----------------------------------------------------
-- Schema football
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `football` DEFAULT CHARACTER SET utf8 ;
USE `football` ;

-- -----------------------------------------------------
-- Table `football`.`countrys`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `football`.`countrys` (
  `id` INT UNSIGNED NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE INDEX `color_UNIQUE` (`name` ASC),
  UNIQUE INDEX `id_UNIQUE` (`id` ASC))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `football`.`sitys`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `football`.`sitys` (
  `id` INT UNSIGNED NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(45) NOT NULL,
  `country` INT UNSIGNED NOT NULL,
  PRIMARY KEY (`id`),
  INDEX `fk_sitys_1_idx` (`country` ASC),
  UNIQUE INDEX `id_UNIQUE` (`id` ASC),
  CONSTRAINT `fk_sitys_1`
    FOREIGN KEY (`country`)
    REFERENCES `football`.`countrys` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `football`.`emblems`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `football`.`emblems` (
  `id` INT UNSIGNED NOT NULL AUTO_INCREMENT,
  `image` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE INDEX `id_UNIQUE` (`id` ASC),
  UNIQUE INDEX `image_path_UNIQUE` (`image` ASC))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `football`.`teams`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `football`.`teams` (
  `id` INT UNSIGNED NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(45) NOT NULL,
  `city` INT UNSIGNED NOT NULL,
  `emblem` INT UNSIGNED NULL,
  PRIMARY KEY (`id`),
  INDEX `fk_teams_1_idx` (`city` ASC),
  INDEX `fk_teams_2_idx` (`emblem` ASC),
  UNIQUE INDEX `id_UNIQUE` (`id` ASC),
  CONSTRAINT `fk_teams_1`
    FOREIGN KEY (`city`)
    REFERENCES `football`.`sitys` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_teams_2`
    FOREIGN KEY (`emblem`)
    REFERENCES `football`.`emblems` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `football`.`personal_info`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `football`.`personal_info` (
  `id` INT UNSIGNED NOT NULL AUTO_INCREMENT,
  `first_name` VARCHAR(45) NOT NULL,
  `last_name` VARCHAR(45) NOT NULL,
  `birthday` DATE NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE INDEX `id_UNIQUE` (`id` ASC))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `football`.`team_roles`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `football`.`team_roles` (
  `id` INT UNSIGNED NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(45) NOT NULL,
  `description` BLOB NULL,
  PRIMARY KEY (`id`),
  UNIQUE INDEX `id_UNIQUE` (`id` ASC),
  UNIQUE INDEX `name_UNIQUE` (`name` ASC))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `football`.`players`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `football`.`players` (
  `id` INT UNSIGNED NOT NULL AUTO_INCREMENT,
  `personal_info` INT UNSIGNED NOT NULL,
  `team` INT UNSIGNED NOT NULL,
  `number` INT UNSIGNED NOT NULL,
  `role` INT UNSIGNED NOT NULL,
  PRIMARY KEY (`id`),
  INDEX `fk_players_1_idx` (`personal_info` ASC),
  INDEX `fk_players_2_idx` (`team` ASC),
  INDEX `fk_players_3_idx` (`role` ASC),
  UNIQUE INDEX `id_UNIQUE` (`id` ASC),
  UNIQUE INDEX `personal_info_UNIQUE` (`personal_info` ASC),
  CONSTRAINT `fk_players_1`
    FOREIGN KEY (`personal_info`)
    REFERENCES `football`.`personal_info` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_players_2`
    FOREIGN KEY (`team`)
    REFERENCES `football`.`teams` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_players_3`
    FOREIGN KEY (`role`)
    REFERENCES `football`.`team_roles` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `football`.`arena`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `football`.`arena` (
  `id` INT UNSIGNED NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(45) NOT NULL,
  `sity` INT UNSIGNED NOT NULL,
  PRIMARY KEY (`id`),
  INDEX `fk_arena_1_idx` (`sity` ASC),
  UNIQUE INDEX `id_UNIQUE` (`id` ASC),
  CONSTRAINT `fk_arena_1`
    FOREIGN KEY (`sity`)
    REFERENCES `football`.`sitys` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `football`.`match_results`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `football`.`match_results` (
  `id` INT UNSIGNED NOT NULL AUTO_INCREMENT,
  `length` TIME NOT NULL,
  `home_team_score` INT UNSIGNED NOT NULL,
  `guest_team_score` INT UNSIGNED NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE INDEX `id_UNIQUE` (`id` ASC))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `football`.`matchs`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `football`.`matchs` (
  `id` INT UNSIGNED NOT NULL AUTO_INCREMENT,
  `home_team` INT UNSIGNED NOT NULL,
  `guest_team` INT UNSIGNED NOT NULL,
  `start` DATETIME NOT NULL,
  `arena` INT UNSIGNED NOT NULL,
  `result` INT UNSIGNED NULL,
  PRIMARY KEY (`id`),
  INDEX `fk_matchs_1_idx` (`home_team` ASC),
  INDEX `fk_matchs_2_idx` (`guest_team` ASC),
  INDEX `fk_matchs_3_idx` (`arena` ASC),
  INDEX `fk_matchs_4_idx` (`result` ASC),
  UNIQUE INDEX `id_UNIQUE` (`id` ASC),
  UNIQUE INDEX `result_UNIQUE` (`result` ASC),
  CONSTRAINT `fk_matchs_1`
    FOREIGN KEY (`home_team`)
    REFERENCES `football`.`teams` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_matchs_2`
    FOREIGN KEY (`guest_team`)
    REFERENCES `football`.`teams` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_matchs_3`
    FOREIGN KEY (`arena`)
    REFERENCES `football`.`arena` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_matchs_4`
    FOREIGN KEY (`result`)
    REFERENCES `football`.`match_results` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `football`.`goals`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `football`.`goals` (
  `id` INT UNSIGNED NOT NULL AUTO_INCREMENT,
  `match` INT UNSIGNED NOT NULL,
  `time` TIME NOT NULL,
  `player` INT UNSIGNED NOT NULL,
  PRIMARY KEY (`id`),
  INDEX `fk_goals_1_idx` (`match` ASC),
  INDEX `fk_goals_2_idx` (`player` ASC),
  UNIQUE INDEX `id_UNIQUE` (`id` ASC),
  CONSTRAINT `fk_goals_1`
    FOREIGN KEY (`match`)
    REFERENCES `football`.`matchs` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_goals_2`
    FOREIGN KEY (`player`)
    REFERENCES `football`.`players` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `football`.`card_types`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `football`.`card_types` (
  `id` INT UNSIGNED NOT NULL AUTO_INCREMENT,
  `color` VARCHAR(45) NOT NULL,
  `description` BLOB NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE INDEX `id_UNIQUE` (`id` ASC),
  UNIQUE INDEX `color_UNIQUE` (`color` ASC))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `football`.`cards`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `football`.`cards` (
  `id` INT UNSIGNED NOT NULL AUTO_INCREMENT,
  `type` INT UNSIGNED NOT NULL,
  `match` INT UNSIGNED NOT NULL,
  `time` TIME NOT NULL,
  `player` INT UNSIGNED NOT NULL,
  PRIMARY KEY (`id`),
  INDEX `fk_cards_1_idx` (`type` ASC),
  INDEX `fk_cards_2_idx` (`match` ASC),
  INDEX `fk_cards_3_idx` (`player` ASC),
  UNIQUE INDEX `id_UNIQUE` (`id` ASC),
  CONSTRAINT `fk_cards_1`
    FOREIGN KEY (`type`)
    REFERENCES `football`.`card_types` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_cards_2`
    FOREIGN KEY (`match`)
    REFERENCES `football`.`matchs` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_cards_3`
    FOREIGN KEY (`player`)
    REFERENCES `football`.`players` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `football`.`replaces`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `football`.`replaces` (
  `id` INT UNSIGNED NOT NULL AUTO_INCREMENT,
  `match` INT UNSIGNED NOT NULL,
  `replaced_player` INT UNSIGNED NOT NULL,
  `player` INT UNSIGNED NOT NULL,
  `time` TIME NOT NULL,
  PRIMARY KEY (`id`),
  INDEX `fk_replaces_1_idx` (`match` ASC),
  INDEX `fk_replaces_2_idx` (`replaced_player` ASC),
  INDEX `fk_replaces_3_idx` (`player` ASC),
  UNIQUE INDEX `id_UNIQUE` (`id` ASC),
  CONSTRAINT `fk_replaces_1`
    FOREIGN KEY (`match`)
    REFERENCES `football`.`matchs` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_replaces_2`
    FOREIGN KEY (`replaced_player`)
    REFERENCES `football`.`players` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_replaces_3`
    FOREIGN KEY (`player`)
    REFERENCES `football`.`players` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `football`.`users`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `football`.`users` (
  `id` INT UNSIGNED NOT NULL AUTO_INCREMENT,
  `login` VARCHAR(45) NOT NULL,
  `password` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE INDEX `login_UNIQUE` (`login` ASC))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `football`.`admins`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `football`.`admins` (
  `id` INT UNSIGNED NOT NULL AUTO_INCREMENT,
  `user` INT UNSIGNED NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE INDEX `id_UNIQUE` (`id` ASC),
  UNIQUE INDEX `user_UNIQUE` (`user` ASC),
  CONSTRAINT `fk_admins_user`
    FOREIGN KEY (`user`)
    REFERENCES `football`.`users` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `football`.`changes`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `football`.`changes` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `table` INT UNSIGNED NOT NULL,
  `object` INT UNSIGNED NOT NULL,
  `action` INT UNSIGNED NOT NULL,
  `admin` INT UNSIGNED NOT NULL,
  `time` DATETIME NOT NULL,
  PRIMARY KEY (`id`),
  INDEX `fk_changes_1_idx` (`admin` ASC),
  CONSTRAINT `fk_changes_1`
    FOREIGN KEY (`admin`)
    REFERENCES `football`.`admins` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `football`.`team_state`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `football`.`team_state` (
  `id` INT UNSIGNED NOT NULL AUTO_INCREMENT,
  `matchId` INT UNSIGNED NOT NULL,
  `playerId` INT UNSIGNED NOT NULL,
  `number` INT UNSIGNED NOT NULL,
  `playHomeTeam` TINYINT(1) NOT NULL,
  INDEX `fk_team_state_2_idx` (`playerId` ASC),
  PRIMARY KEY (`id`),
  CONSTRAINT `fk_team_state_1`
    FOREIGN KEY (`matchId`)
    REFERENCES `football`.`matchs` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_team_state_2`
    FOREIGN KEY (`playerId`)
    REFERENCES `football`.`players` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
