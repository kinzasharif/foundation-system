-- phpMyAdmin SQL Dump
-- version 3.4.5
-- http://www.phpmyadmin.net
--
-- Host: localhost
-- Generation Time: Mar 03, 2026 at 01:09 AM
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
) ENGINE=InnoDB  DEFAULT CHARSET=latin1 AUTO_INCREMENT=12 ;

--
-- Dumping data for table `donations`
--

INSERT INTO `donations` (`id`, `donor_id`, `amount`, `donation_date`) VALUES
(1, 2, '3000.00', '2026-03-01'),
(2, 1, '123.00', '2026-03-01'),
(3, 2, '6000.00', '2026-03-01'),
(4, 1, '3555.00', '2026-03-01'),
(5, 1, '55.00', '2026-03-09'),
(6, 3, '5.00', '2026-03-02'),
(7, 6, '555.00', '2026-03-02'),
(8, 9, '6.00', '2026-03-02'),
(9, 14, '313.00', '2026-03-02'),
(10, 2, '222.00', '2026-03-02'),
(11, 2, '4343.00', '2026-03-02');

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
) ENGINE=InnoDB  DEFAULT CHARSET=latin1 AUTO_INCREMENT=15 ;

--
-- Dumping data for table `donors`
--

INSERT INTO `donors` (`id`, `name`, `phone`, `cnic`) VALUES
(1, 'safeer', '123', '213'),
(2, 'kinza', '12312', '12312'),
(7, 'Safeer Ahmad Awan', '23234', '2342342'),
(14, 'nnnnnn', '222', '22222');

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
) ENGINE=InnoDB  DEFAULT CHARSET=latin1 AUTO_INCREMENT=13 ;

--
-- Dumping data for table `expenses`
--

INSERT INTO `expenses` (`id`, `description`, `amount`, `expense_date`) VALUES
(1, 'Food', '11213.00', '2026-03-01'),
(2, 'Food', '1231.00', '2026-03-02'),
(3, 'Medicine', '123.00', '2026-03-31'),
(4, 'Blood', '123.00', '2026-03-01'),
(5, 'Medicine', '66.00', '2026-03-01'),
(6, 'Blood', '222.00', '2026-03-08'),
(7, 'Food', '33.00', '2026-03-02'),
(8, 'Blood', '231.00', '2026-03-12'),
(9, 'Food', '2.00', '2026-03-02'),
(10, 'Blood', '22.00', '2026-03-02'),
(11, 'Blood', '22.00', '2026-03-02'),
(12, 'Medicine', '6.00', '2026-03-02');

-- --------------------------------------------------------

--
-- Table structure for table `users`
--

CREATE TABLE IF NOT EXISTS `users` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `username` varchar(255) NOT NULL,
  `email` varchar(255) NOT NULL,
  `password` varchar(255) NOT NULL,
  `picture` varchar(500) DEFAULT NULL,
  `phone` varchar(50) NOT NULL,
  `cnic` varchar(50) NOT NULL,
  `role` varchar(50) DEFAULT 'user',
  `created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` timestamp NOT NULL DEFAULT '0000-00-00 00:00:00',
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`),
  UNIQUE KEY `email` (`email`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1 AUTO_INCREMENT=4 ;

--
-- Dumping data for table `users`
--

INSERT INTO `users` (`id`, `username`, `email`, `password`, `picture`, `phone`, `cnic`, `role`, `created_at`, `updated_at`) VALUES
(1, 'safeer', 'safeerahmadawan68208@gmail.com', 'scrypt:32768:8:1$JuGdpEFu1nFz3qei$e9adc76f72a133ba144927ba05da03fbe5b24940f9479b7e5b2790d3e4094fd449bcec17dfa32ac084ac2c2a16450b30d73282e98de8b0edeb844bcdc7a72917', 'uploads/users/safeer_20260303_001820_Screenshot_2026-03-02_231250.png', '213', '123', 'user', '2026-03-02 18:13:00', '0000-00-00 00:00:00'),
(2, 'admin', 'admin@g.com', 'scrypt:32768:8:1$hFpteQA0seJ8dt0R$e0d33493f61be88e99497c535f25d6aca41fb558e76b0b459c51487ad8f71edb5549ac34c4ee0a348202514e98c701ce5e52d458f81e659cd332ff1f47ba5c04', 'uploads/users/admin_admin_20260303_012509_Screenshot_2026-03-02_231250.png', '123', '12', 'admin', '2026-03-02 20:23:30', '0000-00-00 00:00:00'),
(3, 'kinza', 'kinza@ggggg.com', 'scrypt:32768:8:1$MhB2Hzei6h8esj7a$5a1313305b02eec3e636bd62ef5b4b520ddc828d6990f4d99889fb8087b20f7d38d8b4abe2a3378368873c866904acd427aaf4bb1ece5a4a91550d136d3e7a17', NULL, '123', '123', 'user', '2026-03-02 21:33:24', '0000-00-00 00:00:00');

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
