-- --------------------------------------------------------
-- 호스트:                          127.0.0.1
-- 서버 버전:                        12.3.2-MariaDB - MariaDB Server
-- 서버 OS:                        Win64
-- HeidiSQL 버전:                  12.17.0.7270
-- --------------------------------------------------------

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET NAMES utf8 */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;


-- baseball2 데이터베이스 구조 내보내기
CREATE DATABASE IF NOT EXISTS `baseball2` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci */;
USE `baseball2`;

-- 테이블 baseball2.batting_stats 구조 내보내기
CREATE TABLE IF NOT EXISTS `batting_stats` (
  `player_id` int(11) NOT NULL,
  `games` int(11) NOT NULL,
  `plate_appearances` int(11) NOT NULL,
  `at_bats` int(11) NOT NULL,
  `runs` int(11) NOT NULL,
  `hits` int(11) NOT NULL,
  `doubles` int(11) NOT NULL,
  `triples` int(11) NOT NULL,
  `home_runs` int(11) NOT NULL,
  `rbi` int(11) NOT NULL,
  PRIMARY KEY (`player_id`),
  CONSTRAINT `fk_batting_stats_player` FOREIGN KEY (`player_id`) REFERENCES `players` (`player_id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;

-- 내보낼 데이터가 선택되어 있지 않습니다.

-- 테이블 baseball2.inning_scores 구조 내보내기
CREATE TABLE IF NOT EXISTS `inning_scores` (
  `match_id` int(11) NOT NULL COMMENT '경기 고유 번호',
  `inning` int(11) NOT NULL COMMENT '이닝 번호',
  `away_score` int(11) DEFAULT NULL COMMENT '해당 이닝 원정 팀 득점',
  `home_score` int(11) DEFAULT NULL COMMENT '해당 이닝 홈 팀 득점',
  PRIMARY KEY (`match_id`,`inning`),
  CONSTRAINT `fk_inning_scores_match` FOREIGN KEY (`match_id`) REFERENCES `matches` (`match_id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci COMMENT='경기별 이닝 스코어';

-- 내보낼 데이터가 선택되어 있지 않습니다.

-- 테이블 baseball2.match_lineups 구조 내보내기
CREATE TABLE IF NOT EXISTS `match_lineups` (
  `match_id` int(11) NOT NULL COMMENT '경기 고유 번호',
  `player_id` int(11) NOT NULL COMMENT '선수 고유 번호',
  `team_id` int(11) NOT NULL COMMENT '경기 당시 출전 팀 번호',
  `batting_order` int(11) DEFAULT NULL COMMENT '타순',
  `starting_position` varchar(50) NOT NULL COMMENT '출전 포지션',
  `is_starter` tinyint(1) NOT NULL COMMENT '선발 출전 여부',
  PRIMARY KEY (`match_id`,`player_id`),
  KEY `idx_match_lineups_player_id` (`player_id`),
  KEY `idx_match_lineups_team_id` (`team_id`),
  CONSTRAINT `fk_match_lineups_match` FOREIGN KEY (`match_id`) REFERENCES `matches` (`match_id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `fk_match_lineups_player` FOREIGN KEY (`player_id`) REFERENCES `players` (`player_id`) ON UPDATE CASCADE,
  CONSTRAINT `fk_match_lineups_team` FOREIGN KEY (`team_id`) REFERENCES `teams` (`team_id`) ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci COMMENT='경기별 출전 선수 명단';

-- 내보낼 데이터가 선택되어 있지 않습니다.

-- 테이블 baseball2.matches 구조 내보내기
CREATE TABLE IF NOT EXISTS `matches` (
  `match_id` int(11) NOT NULL AUTO_INCREMENT COMMENT '경기 고유 번호',
  `match_date` date NOT NULL COMMENT '경기 일자',
  `stadium_id` int(11) NOT NULL COMMENT '경기 구장 번호',
  `away_team_id` int(11) NOT NULL COMMENT '원정 팀 번호',
  `home_team_id` int(11) NOT NULL COMMENT '홈 팀 번호',
  `away_final_score` int(11) NOT NULL COMMENT '원정 팀 최종 점수',
  `home_final_score` int(11) NOT NULL COMMENT '홈 팀 최종 점수',
  PRIMARY KEY (`match_id`),
  KEY `idx_matches_stadium_id` (`stadium_id`),
  KEY `idx_matches_away_team_id` (`away_team_id`),
  KEY `idx_matches_home_team_id` (`home_team_id`),
  CONSTRAINT `fk_matches_away_team` FOREIGN KEY (`away_team_id`) REFERENCES `teams` (`team_id`) ON UPDATE CASCADE,
  CONSTRAINT `fk_matches_home_team` FOREIGN KEY (`home_team_id`) REFERENCES `teams` (`team_id`) ON UPDATE CASCADE,
  CONSTRAINT `fk_matches_stadium` FOREIGN KEY (`stadium_id`) REFERENCES `stadiums` (`stadium_id`) ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci COMMENT='경기 일정 및 최종 결과';

-- 내보낼 데이터가 선택되어 있지 않습니다.

-- 테이블 baseball2.players 구조 내보내기
CREATE TABLE IF NOT EXISTS `players` (
  `player_id` int(11) NOT NULL AUTO_INCREMENT COMMENT '선수 고유 번호',
  `team_id` int(11) DEFAULT NULL COMMENT '현재 소속 팀 고유 번호',
  `player_name` varchar(100) NOT NULL COMMENT '선수 이름',
  `back_number` int(11) NOT NULL COMMENT '등번호',
  `birth_year` int(11) NOT NULL COMMENT '출생년도',
  `position` varchar(50) NOT NULL COMMENT '포지션',
  PRIMARY KEY (`player_id`),
  KEY `idx_players_team_id` (`team_id`),
  CONSTRAINT `fk_players_team` FOREIGN KEY (`team_id`) REFERENCES `teams` (`team_id`) ON DELETE SET NULL ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=61 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci COMMENT='선수 개인 정보';

-- 내보낼 데이터가 선택되어 있지 않습니다.

-- 테이블 baseball2.stadiums 구조 내보내기
CREATE TABLE IF NOT EXISTS `stadiums` (
  `stadium_id` int(11) NOT NULL AUTO_INCREMENT COMMENT '구장 고유 번호',
  `stadium_name` varchar(100) NOT NULL COMMENT '구장 이름',
  `location` varchar(255) NOT NULL COMMENT '구장 위치',
  PRIMARY KEY (`stadium_id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci COMMENT='구장 정보';

-- 내보낼 데이터가 선택되어 있지 않습니다.

-- 테이블 baseball2.team_stadiums 구조 내보내기
CREATE TABLE IF NOT EXISTS `team_stadiums` (
  `team_id` int(11) NOT NULL COMMENT '팀 고유 번호',
  `stadium_id` int(11) NOT NULL COMMENT '구장 고유 번호',
  `usage_type` varchar(50) NOT NULL COMMENT '구장 구분',
  PRIMARY KEY (`team_id`,`stadium_id`),
  KEY `fk_team_stadiums_stadium` (`stadium_id`),
  CONSTRAINT `fk_team_stadiums_stadium` FOREIGN KEY (`stadium_id`) REFERENCES `stadiums` (`stadium_id`) ON UPDATE CASCADE,
  CONSTRAINT `fk_team_stadiums_team` FOREIGN KEY (`team_id`) REFERENCES `teams` (`team_id`) ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci COMMENT='팀과 구장의 관계';

-- 내보낼 데이터가 선택되어 있지 않습니다.

-- 테이블 baseball2.teams 구조 내보내기
CREATE TABLE IF NOT EXISTS `teams` (
  `team_id` int(11) NOT NULL AUTO_INCREMENT COMMENT '팀 고유 번호',
  `team_name` varchar(100) NOT NULL COMMENT '팀명',
  `founded_year` int(11) NOT NULL COMMENT '창단 연도',
  PRIMARY KEY (`team_id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci COMMENT='팀 정보';

-- 내보낼 데이터가 선택되어 있지 않습니다.

-- 뷰 baseball2.v_match_scoreboard 구조 내보내기
-- VIEW 종속성 오류를 극복하기 위해 임시 테이블을 생성합니다.
CREATE TABLE `v_match_scoreboard` (
	`match_id` INT(11) NOT NULL COMMENT '경기 고유 번호',
	`match_date` DATE NOT NULL COMMENT '경기 일자',
	`away_team` VARCHAR(1) NOT NULL COMMENT '팀명' COLLATE 'utf8mb4_uca1400_ai_ci',
	`home_team` VARCHAR(1) NOT NULL COMMENT '팀명' COLLATE 'utf8mb4_uca1400_ai_ci',
	`away_1` BIGINT(11) NULL,
	`away_2` BIGINT(11) NULL,
	`away_3` BIGINT(11) NULL,
	`away_4` BIGINT(11) NULL,
	`away_5` BIGINT(11) NULL,
	`away_6` BIGINT(11) NULL,
	`away_7` BIGINT(11) NULL,
	`away_8` BIGINT(11) NULL,
	`away_9` BIGINT(11) NULL,
	`away_final_score` INT(11) NOT NULL COMMENT '원정 팀 최종 점수',
	`home_1` BIGINT(11) NULL,
	`home_2` BIGINT(11) NULL,
	`home_3` BIGINT(11) NULL,
	`home_4` BIGINT(11) NULL,
	`home_5` BIGINT(11) NULL,
	`home_6` BIGINT(11) NULL,
	`home_7` BIGINT(11) NULL,
	`home_8` BIGINT(11) NULL,
	`home_9` BIGINT(11) NULL,
	`home_final_score` INT(11) NOT NULL COMMENT '홈 팀 최종 점수'
);

-- 임시 테이블을 제거하고 최종 VIEW 구조를 생성
DROP TABLE IF EXISTS `v_match_scoreboard`;
CREATE ALGORITHM=UNDEFINED SQL SECURITY DEFINER VIEW `v_match_scoreboard` AS SELECT
  m.match_id,
  m.match_date,
  away.team_name AS away_team,
  home.team_name AS home_team,
  MAX(CASE WHEN s.inning = 1 THEN s.away_score END) AS away_1,
  MAX(CASE WHEN s.inning = 2 THEN s.away_score END) AS away_2,
  MAX(CASE WHEN s.inning = 3 THEN s.away_score END) AS away_3,
  MAX(CASE WHEN s.inning = 4 THEN s.away_score END) AS away_4,
  MAX(CASE WHEN s.inning = 5 THEN s.away_score END) AS away_5,
  MAX(CASE WHEN s.inning = 6 THEN s.away_score END) AS away_6,
  MAX(CASE WHEN s.inning = 7 THEN s.away_score END) AS away_7,
  MAX(CASE WHEN s.inning = 8 THEN s.away_score END) AS away_8,
  MAX(CASE WHEN s.inning = 9 THEN s.away_score END) AS away_9,
  m.away_final_score,
  MAX(CASE WHEN s.inning = 1 THEN s.home_score END) AS home_1,
  MAX(CASE WHEN s.inning = 2 THEN s.home_score END) AS home_2,
  MAX(CASE WHEN s.inning = 3 THEN s.home_score END) AS home_3,
  MAX(CASE WHEN s.inning = 4 THEN s.home_score END) AS home_4,
  MAX(CASE WHEN s.inning = 5 THEN s.home_score END) AS home_5,
  MAX(CASE WHEN s.inning = 6 THEN s.home_score END) AS home_6,
  MAX(CASE WHEN s.inning = 7 THEN s.home_score END) AS home_7,
  MAX(CASE WHEN s.inning = 8 THEN s.home_score END) AS home_8,
  MAX(CASE WHEN s.inning = 9 THEN s.home_score END) AS home_9,
  m.home_final_score
FROM `matches` m
JOIN `teams` away ON away.team_id = m.away_team_id
JOIN `teams` home ON home.team_id = m.home_team_id
LEFT JOIN `inning_scores` s ON s.match_id = m.match_id
GROUP BY
  m.match_id,
  m.match_date,
  away.team_name,
  home.team_name,
  m.away_final_score,
  m.home_final_score 
;

/*!40103 SET TIME_ZONE=IFNULL(@OLD_TIME_ZONE, 'system') */;
/*!40101 SET SQL_MODE=IFNULL(@OLD_SQL_MODE, '') */;
/*!40014 SET FOREIGN_KEY_CHECKS=IFNULL(@OLD_FOREIGN_KEY_CHECKS, 1) */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40111 SET SQL_NOTES=IFNULL(@OLD_SQL_NOTES, 1) */;
