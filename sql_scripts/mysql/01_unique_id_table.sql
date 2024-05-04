DROP TABLE IF EXISTS `unique_id`;

CREATE TABLE `unique_id` (
  `tablename` varchar(64) NOT NULL,
  `columnname` varchar(64) NOT NULL,
  `id` int NOT NULL,
  PRIMARY KEY (`tablename`,`columnname`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
