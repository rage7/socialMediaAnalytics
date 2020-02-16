-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='TRADITIONAL,ALLOW_INVALID_DATES';

-- -----------------------------------------------------
-- Schema mydb
-- -----------------------------------------------------

-- -----------------------------------------------------
-- Schema mydb
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `mydb` DEFAULT CHARACTER SET utf8 ;
USE `mydb` ;

-- -----------------------------------------------------
-- Table `mydb`.`campaign`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `mydb`.`campaign` ;

CREATE TABLE IF NOT EXISTS `mydb`.`campaign` (
  `campaign_id` INT NOT NULL AUTO_INCREMENT,
  `timestamp` DATE NOT NULL,
  `campaign_name` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`campaign_id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`sm_user`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `mydb`.`sm_user` ;

CREATE TABLE IF NOT EXISTS `mydb`.`sm_user` (
  `user_id` INT NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(100) NOT NULL,
  `followers` INT NOT NULL DEFAULT 0,
  `social_medium` ENUM('tw', 'fb', 'insta') NOT NULL,
  PRIMARY KEY (`user_id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`post`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `mydb`.`post` ;

CREATE TABLE IF NOT EXISTS `mydb`.`post` (
  `post_id` INT NOT NULL AUTO_INCREMENT,
  `text` VARCHAR(5000) NOT NULL DEFAULT '',
  `timestamp` TIMESTAMP(6) NOT NULL,
  `likes` INT NULL DEFAULT 0,
  `replies` INT NULL DEFAULT 0,
  `shares` INT NULL DEFAULT 0,
  `sm_user_user_id` INT NOT NULL,
  `favorites` INT NULL DEFAULT 0,
  `campaign_campaign_id` INT NOT NULL,
  PRIMARY KEY (`post_id`, `sm_user_user_id`, `campaign_campaign_id`),
  INDEX `fk_post_sm_user1_idx` (`sm_user_user_id` ASC),
  INDEX `fk_post_campaign1_idx` (`campaign_campaign_id` ASC),
  CONSTRAINT `fk_post_sm_user1`
    FOREIGN KEY (`sm_user_user_id`)
    REFERENCES `mydb`.`sm_user` (`user_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_post_campaign1`
    FOREIGN KEY (`campaign_campaign_id`)
    REFERENCES `mydb`.`campaign` (`campaign_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
CHARACTER SET utf8mb4 COLLATE utf8mb4_bin
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`url`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `mydb`.`url` ;

CREATE TABLE IF NOT EXISTS `mydb`.`url` (
  `url_id` INT NOT NULL AUTO_INCREMENT,
  `url` VARCHAR(3000) NOT NULL,
  `post_post_id` INT NOT NULL,
  PRIMARY KEY (`url_id`, `post_post_id`),
  INDEX `fk_url_post1_idx` (`post_post_id` ASC),
  CONSTRAINT `fk_url_post1`
    FOREIGN KEY (`post_post_id`)
    REFERENCES `mydb`.`post` (`post_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
CHARACTER SET utf8mb4 COLLATE utf8mb4_bin
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`mention`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `mydb`.`mention` ;

CREATE TABLE IF NOT EXISTS `mydb`.`mention` (
  `mention_id` INT NOT NULL AUTO_INCREMENT,
  `username` VARCHAR(45) NOT NULL,
  `post_post_id` INT NOT NULL,
  PRIMARY KEY (`mention_id`, `post_post_id`),
  INDEX `fk_mention_post1_idx` (`post_post_id` ASC),
  CONSTRAINT `fk_mention_post1`
    FOREIGN KEY (`post_post_id`)
    REFERENCES `mydb`.`post` (`post_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
CHARACTER SET utf8mb4 COLLATE utf8mb4_bin
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`hashtag`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `mydb`.`hashtag` ;

CREATE TABLE IF NOT EXISTS `mydb`.`hashtag` (
  `hashtag_id` INT NOT NULL AUTO_INCREMENT,
  `hashtag` VARCHAR(45) NOT NULL,
  `post_post_id` INT NOT NULL,
  PRIMARY KEY (`hashtag_id`, `post_post_id`),
  INDEX `fk_hashtag_post1_idx` (`post_post_id` ASC),
  CONSTRAINT `fk_hashtag_post1`
    FOREIGN KEY (`post_post_id`)
    REFERENCES `mydb`.`post` (`post_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
CHARACTER SET utf8mb4 COLLATE utf8mb4_bin
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`campaign_has_sm_user`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `mydb`.`campaign_has_sm_user` ;

CREATE TABLE IF NOT EXISTS `mydb`.`campaign_has_sm_user` (
  `campaign_campaign_id` INT NOT NULL,
  `sm_user_user_id` INT NOT NULL,
  PRIMARY KEY (`campaign_campaign_id`, `sm_user_user_id`),
  INDEX `fk_campaign_has_sm_user_sm_user1_idx` (`sm_user_user_id` ASC),
  INDEX `fk_campaign_has_sm_user_campaign1_idx` (`campaign_campaign_id` ASC),
  CONSTRAINT `fk_campaign_has_sm_user_campaign1`
    FOREIGN KEY (`campaign_campaign_id`)
    REFERENCES `mydb`.`campaign` (`campaign_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_campaign_has_sm_user_sm_user1`
    FOREIGN KEY (`sm_user_user_id`)
    REFERENCES `mydb`.`sm_user` (`user_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`media`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `mydb`.`media` ;

CREATE TABLE IF NOT EXISTS `mydb`.`media` (
  `media_id` INT NOT NULL AUTO_INCREMENT,
  `url` VARCHAR(100) NOT NULL,
  `type` VARCHAR(15) NOT NULL,
  `post_post_id` INT NOT NULL,
  PRIMARY KEY (`media_id`, `post_post_id`),
  INDEX `fk_media_post1_idx` (`post_post_id` ASC),
  CONSTRAINT `fk_media_post1`
    FOREIGN KEY (`post_post_id`)
    REFERENCES `mydb`.`post` (`post_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
