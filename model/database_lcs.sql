-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Dec 27, 2023 at 01:55 PM
-- Server version: 10.4.32-MariaDB
-- PHP Version: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `grp15`
--

-- --------------------------------------------------------

--
-- Table structure for table `academic_coordinator`
--

CREATE TABLE `academic_coordinator` (
  `Coordinator_id` int(11) NOT NULL,
  `First_name` varchar(30) NOT NULL,
  `Last_name` varchar(30) NOT NULL,
  `Schedule_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `academic_coordinator`
--

INSERT INTO `academic_coordinator` (`Coordinator_id`, `First_name`, `Last_name`, `Schedule_id`) VALUES
(2100000017, 'Mark', 'Nisnea', 12);

-- --------------------------------------------------------

--
-- Table structure for table `admin`
--

CREATE TABLE `admin` (
  `Admin_id` int(11) NOT NULL,
  `First_name` varchar(30) NOT NULL,
  `Last_name` varchar(30) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `admin`
--

INSERT INTO `admin` (`Admin_id`, `First_name`, `Last_name`) VALUES
(1, 'zon trisha', 'Japay'),
(2, 'kenzo', 'arellano'),
(3, 'kobe', 'corpuz'),
(4, 'ashley ', 'morales');

-- --------------------------------------------------------

--
-- Table structure for table `booking_activity`
--

CREATE TABLE `booking_activity` (
  `Booking_id` int(11) NOT NULL,
  `guest_id` int(11) NOT NULL,
  `Date` varchar(30) NOT NULL,
  `Time` varchar(30) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `booking_activity`
--

INSERT INTO `booking_activity` (`Booking_id`, `guest_id`, `Date`, `Time`) VALUES
(25, 217889, '02/20/1996', '12:30'),
(26, 2100001, '02/25/1995', '12:59'),
(27, 217889, '02/20/1996', '12:30'),
(28, 2100001, '02/25/1995', '12:59');

-- --------------------------------------------------------

--
-- Table structure for table `guest`
--

CREATE TABLE `guest` (
  `Guest_id` int(11) NOT NULL,
  `First_name` varchar(30) NOT NULL,
  `Last_name` varchar(30) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `guest`
--

INSERT INTO `guest` (`Guest_id`, `First_name`, `Last_name`) VALUES
(216890, 'peter', 'parker'),
(217889, 'Pineapple', 'Salad'),
(2100001, 'Mark', 'Keras'),
(2145566, 'kobe', 'paras'),
(2168909, 'peter', 'parker');

-- --------------------------------------------------------

--
-- Table structure for table `laboratory`
--

CREATE TABLE `laboratory` (
  `lab_id` int(11) NOT NULL,
  `Capacity` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `laboratory`
--

INSERT INTO `laboratory` (`lab_id`, `Capacity`) VALUES
(1, 40),
(2, 40),
(3, 40),
(4, 40),
(5, 40),
(6, 40),
(7, 40),
(8, 40),
(9, 40),
(10, 40);

-- --------------------------------------------------------

--
-- Table structure for table `log_event`
--

CREATE TABLE `log_event` (
  `Log_id` int(11) NOT NULL,
  `teacher_id` int(11) NOT NULL,
  `lab_id` int(11) NOT NULL,
  `timestamp` varchar(30) NOT NULL,
  `activity` varchar(30) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `log_event`
--

INSERT INTO `log_event` (`Log_id`, `teacher_id`, `lab_id`, `timestamp`, `activity`) VALUES
(1, 1, 10, '12:30PM', 'exam'),
(2, 4, 10, '1:00PM', 'lecture'),
(3, 5, 5, '9:00AM', 'lecture'),
(4, 1, 7, '8:00PM', 'presentation'),
(5, 2, 6, '7:00AM', 'Code');

-- --------------------------------------------------------

--
-- Table structure for table `schedule`
--

CREATE TABLE `schedule` (
  `Schedule_id` int(11) NOT NULL,
  `lab_id` int(11) NOT NULL,
  `teacher_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `schedule`
--

INSERT INTO `schedule` (`Schedule_id`, `lab_id`, `teacher_id`) VALUES
(1, 7, 4),
(2, 6, 1),
(3, 4, 5),
(4, 2, 2),
(5, 9, 3);

-- --------------------------------------------------------

--
-- Table structure for table `teacher`
--

CREATE TABLE `teacher` (
  `Teacher_id` int(11) NOT NULL,
  `First_name` varchar(30) NOT NULL,
  `Last_name` varchar(30) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `teacher`
--

INSERT INTO `teacher` (`Teacher_id`, `First_name`, `Last_name`) VALUES
(1, 'Michelle', 'Bolo'),
(2, 'Rogelio', 'Badiang'),
(3, 'Cris john', 'Manero'),
(4, 'Cylde ', 'Balaman'),
(5, 'Ian', 'Benablo');

-- --------------------------------------------------------

--
-- Table structure for table `user_credential`
--

CREATE TABLE `user_credential` (
  `user_id` int(11) NOT NULL,
  `username` varchar(30) NOT NULL,
  `password` varchar(30) NOT NULL,
  `role` varchar(15) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `user_credential`
--

INSERT INTO `user_credential` (`user_id`, `username`, `password`, `role`) VALUES
(1, 'sirdan@uic.edu.ph', '12345', 'admin');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `academic_coordinator`
--
ALTER TABLE `academic_coordinator`
  ADD PRIMARY KEY (`Coordinator_id`);

--
-- Indexes for table `admin`
--
ALTER TABLE `admin`
  ADD PRIMARY KEY (`Admin_id`);

--
-- Indexes for table `booking_activity`
--
ALTER TABLE `booking_activity`
  ADD PRIMARY KEY (`Booking_id`),
  ADD KEY `fk_guest_id` (`guest_id`);

--
-- Indexes for table `guest`
--
ALTER TABLE `guest`
  ADD PRIMARY KEY (`Guest_id`);

--
-- Indexes for table `laboratory`
--
ALTER TABLE `laboratory`
  ADD PRIMARY KEY (`lab_id`);

--
-- Indexes for table `log_event`
--
ALTER TABLE `log_event`
  ADD PRIMARY KEY (`Log_id`),
  ADD KEY `fk_teach_id` (`teacher_id`),
  ADD KEY `fk_laboratory_id` (`lab_id`);

--
-- Indexes for table `schedule`
--
ALTER TABLE `schedule`
  ADD PRIMARY KEY (`Schedule_id`),
  ADD KEY `fk_teacher_id` (`teacher_id`),
  ADD KEY `fk_lab_id` (`lab_id`);

--
-- Indexes for table `teacher`
--
ALTER TABLE `teacher`
  ADD PRIMARY KEY (`Teacher_id`);

--
-- Indexes for table `user_credential`
--
ALTER TABLE `user_credential`
  ADD PRIMARY KEY (`user_id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `academic_coordinator`
--
ALTER TABLE `academic_coordinator`
  MODIFY `Coordinator_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2100000019;

--
-- AUTO_INCREMENT for table `admin`
--
ALTER TABLE `admin`
  MODIFY `Admin_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=11;

--
-- AUTO_INCREMENT for table `booking_activity`
--
ALTER TABLE `booking_activity`
  MODIFY `Booking_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=29;

--
-- AUTO_INCREMENT for table `laboratory`
--
ALTER TABLE `laboratory`
  MODIFY `lab_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=11;

--
-- AUTO_INCREMENT for table `log_event`
--
ALTER TABLE `log_event`
  MODIFY `Log_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=11;

--
-- AUTO_INCREMENT for table `schedule`
--
ALTER TABLE `schedule`
  MODIFY `Schedule_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=11;

--
-- AUTO_INCREMENT for table `teacher`
--
ALTER TABLE `teacher`
  MODIFY `Teacher_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=11;

--
-- AUTO_INCREMENT for table `user_credential`
--
ALTER TABLE `user_credential`
  MODIFY `user_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `booking_activity`
--
ALTER TABLE `booking_activity`
  ADD CONSTRAINT `fk_guest_id` FOREIGN KEY (`guest_id`) REFERENCES `guest` (`Guest_id`);

--
-- Constraints for table `log_event`
--
ALTER TABLE `log_event`
  ADD CONSTRAINT `fk_laboratory_id` FOREIGN KEY (`lab_id`) REFERENCES `laboratory` (`lab_id`),
  ADD CONSTRAINT `fk_teach_id` FOREIGN KEY (`teacher_id`) REFERENCES `teacher` (`Teacher_id`);

--
-- Constraints for table `schedule`
--
ALTER TABLE `schedule`
  ADD CONSTRAINT `fk_lab_id` FOREIGN KEY (`lab_id`) REFERENCES `laboratory` (`lab_id`),
  ADD CONSTRAINT `fk_teacher_id` FOREIGN KEY (`teacher_id`) REFERENCES `teacher` (`Teacher_id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
