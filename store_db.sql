-- phpMyAdmin SQL Dump
-- version 5.1.0
-- https://www.phpmyadmin.net/
--
-- Host: localhost
-- Generation Time: May 10, 2021 at 03:52 AM
-- Server version: 10.4.18-MariaDB-log
-- PHP Version: 7.4.16

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

-- --------------------------------------------------------

--
-- Table structure for table `Categories`
--

DROP TABLE IF EXISTS `Categories`;
CREATE TABLE `Categories` (
  `categoryID` int(11) NOT NULL AUTO_INCREMENT,
  `categoryName` varchar(255) NOT NULL,
  `categoryDescription` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`categoryID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `Categories`
--

INSERT INTO `Categories` (`categoryName`, `categoryDescription`) VALUES
('Flower Seeds', NULL),
('Flower Seedlings', NULL),
('Potting Soil', 'Planting medium');

-- --------------------------------------------------------

--
-- Table structure for table `Customers`
--

DROP TABLE IF EXISTS `Customers`;
CREATE TABLE `Customers` (
  `customerID` int(11) NOT NULL AUTO_INCREMENT,
  `firstName` varchar(255) NOT NULL,
  `lastName` varchar(255) NOT NULL,
  `email` varchar(255) NOT NULL,
  `phoneNumber` varchar(255) NOT NULL,
  `streetAddress` varchar(255) NOT NULL,
  `city` varchar(255) NOT NULL,
  `state` varchar(255) NOT NULL,
  `zipCode` varchar(255) NOT NULL,
  PRIMARY KEY (`customerID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `Customers`
--

INSERT INTO `Customers` (`firstName`, `lastName`, `email`, `phoneNumber`, `streetAddress`, `city`, `state`, `zipCode`) VALUES
('Sterling', 'Archer', 'duchess@isis.gov', '212-220-5240', '2 N. Trenton Street', 'New York', 'New York', '10016'),
('Cyril', 'Figgis', 'chetmanley@isis.gov', '718-380-1669', '8248 S. Cobblestone St.', 'Staten Island', 'New York', '10312'),
('Lana', 'Kane', 'shehulk@isis.gov', '646-391-2933', '70 North Pumpkin Hill Street', 'Bronx', 'New York', '10457'),
('John', 'Hancock', 'JHancock@usa.org', '980-777-4336', '1776 USA Ln', 'Boston', 'Massachusetts', '02205'),
('Marie', 'Curie', 'MCurie@nobel.org', '989-075-3311', '909 Paris Ave', 'Portland', 'Oregon', '97035');

-- --------------------------------------------------------

--
-- Table structure for table `OrderItems`
--

DROP TABLE IF EXISTS `OrderItems`;
CREATE TABLE `OrderItems` (
  `orderItemID` int(11) NOT NULL AUTO_INCREMENT,
  `orderID` int(11) NOT NULL,
  `productID` int(11) NOT NULL,
  `orderItemQuantity` int(11) NOT NULL,
  `orderItemPrice` decimal(10,2) NOT NULL,
  PRIMARY KEY (`orderItemID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `OrderItems`
--

INSERT INTO `OrderItems` (`orderID`, `productID`, `orderItemQuantity`, `orderItemPrice`) VALUES
(1, 1, 1, '7.59'),
(3, 1, 2, '21.79'),
(2, 1, 1, '27.34');

-- --------------------------------------------------------

--
-- Table structure for table `Orders`
--

DROP TABLE IF EXISTS `Orders`;
CREATE TABLE `Orders` (
  `orderID` int(11) NOT NULL AUTO_INCREMENT,
  `customerID` int(11),
  `totalPrice` decimal(10,2) NOT NULL,
  `orderDate` date NOT NULL,
  `orderComments` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`orderID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `Orders`
--

INSERT INTO `Orders` (`customerID`, `totalPrice`, `orderDate`, `orderComments`) VALUES
(1, '101.20', '2019-10-10', NULL),
(1, '27.34', '2021-02-24', NULL),
(3, '30.92', '2021-04-26', NULL),
(5, '16.50', '2019-05-09', 'Please include samples of fertilizer.'),
(4, '0.05', '2020-12-27', 'Thanks!');

-- --------------------------------------------------------

--
-- Table structure for table `Products`
--

DROP TABLE IF EXISTS `Products`;
CREATE TABLE `Products` (
  `productID` int(11) NOT NULL AUTO_INCREMENT,
  `productName` varchar(255) NOT NULL,
  `productInventory` int(11) NOT NULL,
  `productPrice` decimal(10,2) NOT NULL,
  `productDescription` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`productID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `Products`
--

INSERT INTO `Products` (`productName`, `productInventory`, `productPrice`, `productDescription`) VALUES
('Arabian Jasmine Seeds', 50, '7.59', NULL),
('3 Gallon Clay Pots (Set of 5)', 99, '27.34', NULL),
('Organic Fertilizer', 0, '21.79', 'Feed your plants with our special fertilizer blend rich in nutrients.', NULL);

-- --------------------------------------------------------

--
-- Table structure for table `ProductsCategories`
--

DROP TABLE IF EXISTS `ProductsCategories`;
CREATE TABLE `ProductsCategories` (
  `productID` int(11),
  `categoryID` int(11),
  PRIMARY KEY (`productID`, `categoryID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `ProductsCategories`
--

INSERT INTO `ProductsCategories` (`productID`, `categoryID`) VALUES
(1, 1),
(1, 2),
(3, 3);

-- --------------------------------------------------------

--
-- Table structure for table `Shipments`
--

DROP TABLE IF EXISTS `Shipments`;
CREATE TABLE `Shipments` (
  `shipmentID` int(11) NOT NULL AUTO_INCREMENT,
  `orderID` int(11) NOT NULL,
  `trackingNumber` varchar(255) DEFAULT NULL,
  `dateShipped` date NOT NULL,
  `dateDelivered` date DEFAULT NULL,
  PRIMARY KEY (`shipmentID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `Shipments`
--

INSERT INTO `Shipments` (`orderID`, `trackingNumber`, `dateShipped`, `dateDelivered`) VALUES
(1, '1Z12345E0205271688', '2019-10-14', NULL),
(2, '1Z12345E6605272234', '2021-02-26', NULL),
(3, '1Z12345E0305271640', '2021-04-29', NULL);

--
-- Constraints for table `OrderItems`
--

ALTER TABLE `OrderItems`
    ADD CONSTRAINT `OrderItems_ibfk_1` FOREIGN KEY (`orderID`) REFERENCES `Orders` (`orderID`),
    ADD CONSTRAINT `OrderItems_ibfk_2` FOREIGN KEY (`productID`) REFERENCES `Products` (`productID`);

--
-- Constraints for table `Orders`
--

ALTER TABLE `Orders`
  ADD CONSTRAINT `Orders_ibfk_1` FOREIGN KEY (`customerID`) REFERENCES `Customers` (`customerID`) ON DELETE SET NULL;

--
-- Constraints for table `ProductsCategories`
--

ALTER TABLE `ProductsCategories`
  ADD CONSTRAINT `ProductsCategories_ibfk_1` FOREIGN KEY (`productID`) REFERENCES `Products` (`productID`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `ProductsCategories_ibfk_2` FOREIGN KEY (`categoryID`) REFERENCES `Categories` (`categoryID`) ON DELETE CASCADE;

--
-- Constraints for table `Shipments`
--

ALTER TABLE `Shipments`
  ADD CONSTRAINT `Shipments_ibfk_1` FOREIGN KEY (`orderID`) REFERENCES `Orders` (`orderID`);

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;

