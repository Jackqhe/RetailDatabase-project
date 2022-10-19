/*
 Navicat Premium Data Transfer

 Source Server         : test
 Source Server Type    : MySQL
 Source Server Version : 50720
 Source Host           : localhost:3306
 Source Schema         : retail

 Target Server Type    : MySQL
 Target Server Version : 50720
 File Encoding         : 65001

 Date: 21/04/2022 15:17:02
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for customers
-- ----------------------------
DROP TABLE IF EXISTS `customers`;
CREATE TABLE `customers`  (
  `cid` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `ctel` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `caddr` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  PRIMARY KEY (`cid`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of customers
-- ----------------------------
INSERT INTO `customers` VALUES ('C1', '1111', 'Tuen Mun');
INSERT INTO `customers` VALUES ('C2', '2222', 'Diamond Hill');
INSERT INTO `customers` VALUES ('C3', '3333', 'Tai Wai');

-- ----------------------------
-- Table structure for items
-- ----------------------------
DROP TABLE IF EXISTS `items`;
CREATE TABLE `items`  (
  `iid` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `sid` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `iname` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `price` int(11) NOT NULL,
  `quantity` int(11) NOT NULL,
  `key1` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,
  `key2` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,
  `key3` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,
  PRIMARY KEY (`iid`) USING BTREE,
  INDEX `item_shop`(`sid`) USING BTREE,
  CONSTRAINT `item_shop` FOREIGN KEY (`sid`) REFERENCES `shops` (`sid`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of items
-- ----------------------------
INSERT INTO `items` VALUES ('I1', 'S1', 'Apple', 10, 200, 'Red', 'Sweet', NULL);
INSERT INTO `items` VALUES ('I2', 'S1', 'Orange', 8, 100, 'Yellow', 'Fresh', 'Australia');
INSERT INTO `items` VALUES ('I3', 'S2', 'Apple', 8000, 50, 'Red', '256G', NULL);
INSERT INTO `items` VALUES ('I4', 'S2', 'Samsung', 7000, 20, 'Black', '128G', 'Folding');
INSERT INTO `items` VALUES ('I5', 'S3', 'DB', 500, 90, 'Paperback', 'Relational', 'SQL');
INSERT INTO `items` VALUES ('I6', 'S3', 'AI', 400, 95, 'Paperback', 'Deep learning', 'Python');

-- ----------------------------
-- Table structure for orders
-- ----------------------------
DROP TABLE IF EXISTS `orders`;
CREATE TABLE `orders`  (
  `id` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `oid` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `cid` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `iid` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `amount` int(10) NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `item_order`(`iid`) USING BTREE,
  INDEX `customer_order`(`cid`) USING BTREE,
  CONSTRAINT `customer_order` FOREIGN KEY (`cid`) REFERENCES `customers` (`cid`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `item_order` FOREIGN KEY (`iid`) REFERENCES `items` (`iid`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of orders
-- ----------------------------

-- ----------------------------
-- Table structure for shops
-- ----------------------------
DROP TABLE IF EXISTS `shops`;
CREATE TABLE `shops`  (
  `sid` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `sname` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `rating` int(11) NULL DEFAULT NULL,
  `location` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  PRIMARY KEY (`sid`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of shops
-- ----------------------------
INSERT INTO `shops` VALUES ('S1', 'Fruit shop', 5, 'Lok Fu');
INSERT INTO `shops` VALUES ('S2', 'Phone shop', 5, 'Mong Kok');
INSERT INTO `shops` VALUES ('S3', 'Book shop', 4, 'Kowloon Tong');

-- ----------------------------
-- Triggers structure for table orders
-- ----------------------------
DROP TRIGGER IF EXISTS `trig_order_insert_After`;
delimiter ;;
CREATE TRIGGER `trig_order_insert_After` AFTER INSERT ON `orders` FOR EACH ROW begin
	UPDATE items SET quantity = quantity - new.amount WHERE iid = new.iid;
end
;;
delimiter ;

-- ----------------------------
-- Triggers structure for table orders
-- ----------------------------
DROP TRIGGER IF EXISTS `trig_order_delete_After`;
delimiter ;;
CREATE TRIGGER `trig_order_delete_After` AFTER DELETE ON `orders` FOR EACH ROW begin
	UPDATE items SET quantity = quantity + old.amount WHERE iid = old.iid;
end
;;
delimiter ;

SET FOREIGN_KEY_CHECKS = 1;
