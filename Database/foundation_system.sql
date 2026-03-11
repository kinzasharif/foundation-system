-- phpMyAdmin SQL Dump
-- version 3.4.5
-- http://www.phpmyadmin.net
--
-- Host: localhost
-- Generation Time: Mar 11, 2026 at 02:55 PM
-- Server version: 5.5.16
-- PHP Version: 5.3.8

SET SQL_MODE="NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;

--
-- Database: `foundation_system`
--

-- --------------------------------------------------------

--
-- Table structure for table `donations`
--

CREATE TABLE IF NOT EXISTS `donations` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `donor_id` int(11) DEFAULT NULL,
  `amount` decimal(10,2) DEFAULT NULL,
  `donation_date` date DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1 AUTO_INCREMENT=9 ;

--
-- Dumping data for table `donations`
--

INSERT INTO `donations` (`id`, `donor_id`, `amount`, `donation_date`) VALUES
(1, 2, '21312.00', '2026-03-01'),
(2, 1, '123.00', '2026-03-01'),
(3, 2, '333333.00', '2026-03-01'),
(4, 1, '44444.00', '2026-03-01'),
(5, 3, '321.00', '2026-03-06'),
(6, 4, '222.00', '2026-03-06'),
(7, 2, '340000.00', '2026-03-07'),
(8, 2, '777.00', '2026-03-10');

-- --------------------------------------------------------

--
-- Table structure for table `donors`
--

CREATE TABLE IF NOT EXISTS `donors` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `phone` varchar(50) DEFAULT NULL,
  `cnic` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1 AUTO_INCREMENT=7 ;

--
-- Dumping data for table `donors`
--

INSERT INTO `donors` (`id`, `name`, `phone`, `cnic`) VALUES
(1, 'safeer', '123', '213'),
(2, 'kinza', '12312', '12312'),
(3, 'new donor', '1111', '1231'),
(4, '222', '111', '111'),
(5, 'kinza sharif', '123123', '6578439'),
(6, 'shakeel', '123', '123');

-- --------------------------------------------------------

--
-- Table structure for table `expenses`
--

CREATE TABLE IF NOT EXISTS `expenses` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `description` varchar(255) DEFAULT NULL,
  `amount` decimal(10,2) DEFAULT NULL,
  `expense_date` date DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1 AUTO_INCREMENT=8 ;

--
-- Dumping data for table `expenses`
--

INSERT INTO `expenses` (`id`, `description`, `amount`, `expense_date`) VALUES
(1, 'Food', '11213.00', '2026-03-01'),
(2, 'Food', '1231.00', '2026-03-02'),
(3, 'Medicine', '123.00', '2026-03-31'),
(4, 'Food', '2222.00', '2026-03-02'),
(5, 'Blood', '2222.00', '2026-03-06'),
(6, 'Medicine', '65000.00', '2026-03-07'),
(7, 'Blood', '777.00', '2026-03-10');

-- --------------------------------------------------------

--
-- Table structure for table `users`
--

CREATE TABLE IF NOT EXISTS `users` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `username` varchar(100) NOT NULL,
  `email` varchar(150) NOT NULL,
  `password` varchar(255) NOT NULL,
  `phone` varchar(20) DEFAULT NULL,
  `cnic` varchar(30) DEFAULT NULL,
  `picture` varchar(255) DEFAULT '',
  `role` enum('user','admin') NOT NULL DEFAULT 'user',
  `created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`),
  UNIQUE KEY `email` (`email`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1 AUTO_INCREMENT=6 ;

--
-- Dumping data for table `users`
--

INSERT INTO `users` (`id`, `username`, `email`, `password`, `phone`, `cnic`, `picture`, `role`, `created_at`) VALUES
(1, 'kinza', 'kinzasharif790@gmail.com', 'scrypt:32768:8:1$hTHNq07CejxyFsfJ$55a20899c7ed611f6bcc86a918bfd40803e2f408b2aa0bec67f85249caa6b7c59fa4c9a08718aff21f0ae2ff3df8f152059fbcafe7508504213c4f7dbc61a941', '123', '123', 'uploads/users/kinza_20260302_225901_Screenshot_2026-03-02_225502.png', 'user', '2026-03-02 17:59:02'),
(2, 'admin', 'admin@gmail.com', 'scrypt:32768:8:1$hTHNq07CejxyFsfJ$55a20899c7ed611f6bcc86a918bfd40803e2f408b2aa0bec67f85249caa6b7c59fa4c9a08718aff21f0ae2ff3df8f152059fbcafe7508504213c4f7dbc61a941', '123', '123', NULL, 'admin', '2026-03-03 01:54:06'),
(3, 'newuser', 'new@gmail.com', 'scrypt:32768:8:1$hEUVXNPNBPTxIKvN$c9e9dee7f499b1d355cd44f2344b1846531d02c1ca64b9949fb9a5c2fc9430182fa6ece9d6d06c3b879aca038ad76dd7fd78e058ec15bad86b350fa215f8a57c', '123', '123', NULL, 'user', '2026-03-06 09:53:50'),
(4, 'Arslan Ahmad', 'arslan889@gmail.com', 'scrypt:32768:8:1$t8p31TWDteWyu61U$427becebcb8286357a19c6abdd7b7bfe50e06fa28e13a7cb4c16fc6d95d082fb150fd40bfdd4ce5abefe9e4a0f6cbb55256393f840511a25d2b88d35c4008950', '009', '1234567', NULL, 'user', '2026-03-07 11:16:15'),
(5, 'shakeel', 'shakeel@ahmed.com', 'scrypt:32768:8:1$AYle28B9s2ps33gW$32d01e373736f1519761927845970507873a4c96b31b4f76aa72b7a0f955e4087abcad83cdbf48c8d5d17fb11b53e6b205e1a183d2a214653fbfc8ba1c4124fb', '123', '123', NULL, 'user', '2026-03-10 15:24:44');

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
