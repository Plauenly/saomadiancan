-- MySQL dump 10.13  Distrib 8.0.46, for Linux (x86_64)
--
-- Host: localhost    Database: qrOrder
-- ------------------------------------------------------
-- Server version	8.0.46-0ubuntu0.24.04.3

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Current Database: `qrOrder`
--

/*!40000 DROP DATABASE IF EXISTS `qrOrder`*/;

CREATE DATABASE /*!32312 IF NOT EXISTS*/ `qrOrder` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci */ /*!80016 DEFAULT ENCRYPTION='N' */;

USE `qrOrder`;

--
-- Table structure for table `category`
--

DROP TABLE IF EXISTS `category`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `category` (
  `id` int unsigned NOT NULL AUTO_INCREMENT COMMENT '主键',
  `name` varchar(50) NOT NULL COMMENT '分类名称',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='分类表';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `category`
--

LOCK TABLES `category` WRITE;
/*!40000 ALTER TABLE `category` DISABLE KEYS */;
INSERT INTO `category` VALUES (1,'主食系列'),(2,'精选饮品'),(3,'风味小吃');
/*!40000 ALTER TABLE `category` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `category_product`
--

DROP TABLE IF EXISTS `category_product`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `category_product` (
  `cid` int unsigned NOT NULL COMMENT '分类id',
  `pid` int unsigned NOT NULL COMMENT '商品id',
  PRIMARY KEY (`cid`,`pid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='分类商品关联表';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `category_product`
--

LOCK TABLES `category_product` WRITE;
/*!40000 ALTER TABLE `category_product` DISABLE KEYS */;
INSERT INTO `category_product` VALUES (1,1),(2,2),(3,3),(3,4);
/*!40000 ALTER TABLE `category_product` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `image_product`
--

DROP TABLE IF EXISTS `image_product`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `image_product` (
  `id` int unsigned NOT NULL AUTO_INCREMENT COMMENT '主键',
  `pid` int unsigned NOT NULL COMMENT '商品id',
  `url` varchar(255) NOT NULL COMMENT '图片链接',
  `sort` tinyint NOT NULL DEFAULT '0' COMMENT '展示顺序, 0为封面图',
  PRIMARY KEY (`id`),
  KEY `idx_pid` (`pid`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='商品展示图表';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `image_product`
--

LOCK TABLES `image_product` WRITE;
/*!40000 ALTER TABLE `image_product` DISABLE KEYS */;
INSERT INTO `image_product` VALUES (1,1,'https://dummyimage.com/600x400/ff9999/fff&text=Beef+Noodle+Cover',0),(2,1,'https://dummyimage.com/600x400/ff9999/fff&text=Beef+Noodle+Detail',1),(3,2,'https://dummyimage.com/600x400/99ccff/fff&text=Latte',0),(4,3,'https://dummyimage.com/600x400/ffcc99/fff&text=Tofu',0),(5,4,'https://dummyimage.com/600x400/ffff99/333&text=Fries',0);
/*!40000 ALTER TABLE `image_product` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `label`
--

DROP TABLE IF EXISTS `label`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `label` (
  `id` int unsigned NOT NULL AUTO_INCREMENT COMMENT '主键',
  `name` varchar(50) NOT NULL COMMENT '标签名称(如不支持打包)',
  `color` varchar(30) DEFAULT NULL COMMENT '标签颜色代码',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='标签表';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `label`
--

LOCK TABLES `label` WRITE;
/*!40000 ALTER TABLE `label` DISABLE KEYS */;
INSERT INTO `label` VALUES (1,'店长推荐','#FF3333'),(2,'不支持打包','#999999'),(3,'新品上市','#00CC66');
/*!40000 ALTER TABLE `label` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `label_product`
--

DROP TABLE IF EXISTS `label_product`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `label_product` (
  `lid` int unsigned NOT NULL COMMENT '标签id',
  `pid` int unsigned NOT NULL COMMENT '商品id',
  PRIMARY KEY (`lid`,`pid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='标签商品关联表';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `label_product`
--

LOCK TABLES `label_product` WRITE;
/*!40000 ALTER TABLE `label_product` DISABLE KEYS */;
INSERT INTO `label_product` VALUES (1,1),(2,3),(3,2);
/*!40000 ALTER TABLE `label_product` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `order_product`
--

DROP TABLE IF EXISTS `order_product`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `order_product` (
  `oid` int unsigned NOT NULL COMMENT '订单id',
  `pid` int unsigned NOT NULL COMMENT '商品id',
  `p_name` varchar(100) NOT NULL COMMENT '商品名(快照)',
  `price` decimal(8,2) NOT NULL COMMENT '单价(快照)',
  `quantity` int NOT NULL DEFAULT '1' COMMENT '数量',
  PRIMARY KEY (`oid`,`pid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='订单商品详情表';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `order_product`
--

LOCK TABLES `order_product` WRITE;
/*!40000 ALTER TABLE `order_product` DISABLE KEYS */;
INSERT INTO `order_product` VALUES (1,1,'招牌牛肉面',28.50,1),(1,2,'冰拿铁',18.00,1),(2,3,'铁板脆皮豆腐',15.00,1),(2,4,'黄金炸薯条',12.00,1);
/*!40000 ALTER TABLE `order_product` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `orders`
--

DROP TABLE IF EXISTS `orders`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `orders` (
  `id` int unsigned NOT NULL AUTO_INCREMENT COMMENT '主键',
  `torder` varchar(32) DEFAULT NULL COMMENT '取餐号',
  `status` tinyint NOT NULL DEFAULT '0' COMMENT '状态: 0待支付, 1已支付, 2制作中, 3已完成, 4已退款',
  `is_takeout` tinyint(1) NOT NULL DEFAULT '0' COMMENT '方式: 0堂食, 1打包',
  `remark` varchar(255) DEFAULT NULL COMMENT '用户备注',
  `open_id` varchar(64) NOT NULL COMMENT '支付用户的微信id(快照)',
  `phone` varchar(20) DEFAULT NULL COMMENT '支付用户的绑定电话(快照)',
  `transaction_id` varchar(64) DEFAULT NULL COMMENT '微信支付交易单号',
  `trade_id` varchar(64) NOT NULL COMMENT '商户订单号(含时间戳)',
  `table_no` int unsigned DEFAULT NULL COMMENT '订单对应的桌号',
  `total_price` decimal(8,2) NOT NULL DEFAULT '0.00' COMMENT '总价格',
  `create_at` datetime DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `pay_at` datetime DEFAULT NULL COMMENT '支付时间',
  `shop_num` int unsigned DEFAULT '0' COMMENT '订单商品的总数',
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_trade_id` (`trade_id`),
  KEY `idx_open_id` (`open_id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='订单表';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `orders`
--

LOCK TABLES `orders` WRITE;
/*!40000 ALTER TABLE `orders` DISABLE KEYS */;
INSERT INTO `orders` VALUES (1,'A001',4,1,'拿铁少冰','oUpF8uMuAJO_M2pxb1Q9zNjWeS01','13800138001','4200000000202607310001','TRD202607310001',NULL,46.50,'2026-07-31 11:00:00','2026-07-31 11:01:00',2),(2,'B002',2,0,'豆腐多放葱花','oUpF8uMuAJO_M2pxb1Q9zNjWeS02','13900139002','4200000000202607310002','TRD202607310002',5,27.00,'2026-07-31 11:30:00','2026-07-31 11:30:30',2);
/*!40000 ALTER TABLE `orders` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `product`
--

DROP TABLE IF EXISTS `product`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `product` (
  `id` int unsigned NOT NULL AUTO_INCREMENT COMMENT '主键',
  `name` varchar(100) NOT NULL COMMENT '商品名',
  `description` varchar(150) DEFAULT NULL COMMENT '商品描述',
  `price` decimal(8,2) NOT NULL DEFAULT '0.00' COMMENT '价格',
  `status` tinyint NOT NULL DEFAULT '1' COMMENT '状态: 0下架, 1上架, 2卖完',
  `sold` int unsigned NOT NULL DEFAULT '0' COMMENT '销量',
  `is_takeout` tinyint(1) NOT NULL DEFAULT '1' COMMENT '支持打包: 0不能, 1可以',
  `create_at` datetime DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='商品表';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `product`
--

LOCK TABLES `product` WRITE;
/*!40000 ALTER TABLE `product` DISABLE KEYS */;
INSERT INTO `product` VALUES (1,'招牌牛肉面','大块牛肉，原汤熬制12小时',28.50,1,150,1,'2026-07-31 11:01:09'),(2,'冰拿铁','精选阿拉比卡咖啡豆，冷鲜牛乳',18.00,1,200,1,'2026-07-31 11:01:09'),(3,'铁板脆皮豆腐','外酥里嫩，烫嘴注意（仅限堂食）',15.00,1,80,0,'2026-07-31 11:01:09'),(4,'黄金炸薯条','香脆可口，附赠番茄酱',12.00,1,300,1,'2026-07-31 11:01:09');
/*!40000 ALTER TABLE `product` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `user`
--

DROP TABLE IF EXISTS `user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `user` (
  `id` int unsigned NOT NULL AUTO_INCREMENT COMMENT '主键',
  `open_id` varchar(64) NOT NULL COMMENT '微信open_id',
  `phone` varchar(20) DEFAULT NULL COMMENT '手机号',
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `last_login` datetime DEFAULT NULL COMMENT '最后登录时间',
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_open_id` (`open_id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='用户表';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user`
--

LOCK TABLES `user` WRITE;
/*!40000 ALTER TABLE `user` DISABLE KEYS */;
INSERT INTO `user` VALUES (1,'oUpF8uMuAJO_M2pxb1Q9zNjWeS01','13800138001','2026-07-01 10:00:00','2026-07-31 10:00:00'),(2,'oUpF8uMuAJO_M2pxb1Q9zNjWeS02','13900139002','2026-07-15 14:30:00','2026-07-31 11:00:00');
/*!40000 ALTER TABLE `user` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping routines for database 'qrOrder'
--
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2026-08-03  7:33:10
