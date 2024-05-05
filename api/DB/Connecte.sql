-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: localhost
-- Generation Time: Mar 27, 2024 at 02:50 PM
-- Server version: 10.4.28-MariaDB
-- PHP Version: 8.0.28

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `Connecte`
--

-- --------------------------------------------------------

--
-- Table structure for table `GAMES`
--

CREATE TABLE `GAMES` (
  `id` int(11) NOT NULL,
  `game_board` varchar(1024) NOT NULL,
  `time_date` datetime NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Table structure for table `PLAYERS`
--

CREATE TABLE `PLAYERS` (
  `username` varchar(50) NOT NULL,
  `hashed_pass` varchar(255) NOT NULL,
  `email` varchar(255) NOT NULL,
  `token` varchar(255) NOT NULL,
  `verifyID` varchar(50) NOT NULL,
  `verified` tinyint(1) NOT NULL,
  `lastChange` datetime DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `PLAYERS`
--

INSERT INTO `PLAYERS` (`username`, `hashed_pass`, `email`, `token`, `verifyID`, `verified`, `lastChange`) VALUES
('Guest', '', '', '', '', 0, NULL);

--
-- Table structure for table `PLAYERS_GAMES`
--

CREATE TABLE `PLAYERS_GAMES` (
  `id` int(11) NOT NULL,
  `FKplayer` varchar(50) NOT NULL,
  `FKgame` int(11) NOT NULL,
  `WDL` char(1) NOT NULL,
  `which_turn` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Indexes for dumped tables
--

--
-- Indexes for table `GAMES`
--
ALTER TABLE `GAMES`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `PLAYERS`
--
ALTER TABLE `PLAYERS`
  ADD PRIMARY KEY (`username`);

--
-- Indexes for table `PLAYERS_GAMES`
--
ALTER TABLE `PLAYERS_GAMES`
  ADD PRIMARY KEY (`id`),
  ADD KEY `FKgame` (`FKgame`),
  ADD KEY `FKplayer` (`FKplayer`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `GAMES`
--
ALTER TABLE `GAMES`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=22;

--
-- AUTO_INCREMENT for table `PLAYERS_GAMES`
--
ALTER TABLE `PLAYERS_GAMES`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=13;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `PLAYERS_GAMES`
--
ALTER TABLE `PLAYERS_GAMES`
  ADD CONSTRAINT `players_games_ibfk_1` FOREIGN KEY (`FKgame`) REFERENCES `GAMES` (`id`),
  ADD CONSTRAINT `players_games_ibfk_2` FOREIGN KEY (`FKplayer`) REFERENCES `PLAYERS` (`username`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
