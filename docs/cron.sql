/*
 Navicat MySQL Data Transfer

 Source Server         : PAAS
 Source Server Type    : MySQL
 Source Server Version : 50556

 Target Server Type    : MySQL
 Target Server Version : 50556
 File Encoding         : 65001

 Date: 15/01/2019 15:25:31
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for task_log
-- ----------------------------
DROP TABLE IF EXISTS `task_log`;
CREATE TABLE `task_log` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `task_id` varchar(16) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `status` tinyint(1) DEFAULT NULL,
  `exe_time` datetime DEFAULT NULL,
  `cmd` varchar(128) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `stdout` text COLLATE utf8mb4_unicode_ci,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=11386 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

SET FOREIGN_KEY_CHECKS = 1;
