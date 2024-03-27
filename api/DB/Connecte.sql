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
-- Dumping data for table `GAMES`
--

INSERT INTO `GAMES` (`id`, `game_board`, `time_date`) VALUES
(13, '[[0. 0. 0. 0. 0. 0. 0.]\n [0. 0. 0. 0. 0. 0. 0.]\n [1. 0. 0. 0. 0. 0. 0.]\n [1. 0. 0. 0. 0. 0. 2.]\n [1. 0. 0. 0. 0. 0. 2.]\n [1. 0. 0. 0. 0. 0. 2.]]', '2024-03-27 14:35:30'),
(14, '[[1. 2. 1. 0. 0. 0. 0.]\n [2. 1. 2. 0. 0. 0. 0.]\n [1. 2. 1. 0. 0. 0. 0.]\n [2. 1. 2. 0. 0. 0. 0.]\n [1. 2. 1. 0. 0. 0. 0.]\n [2. 1. 2. 1. 0. 0. 2.]]', '2024-03-27 14:35:30'),
(15, '[[0. 0. 0. 0. 0. 0. 0.]\n [0. 0. 0. 0. 0. 0. 0.]\n [0. 0. 0. 0. 0. 0. 0.]\n [0. 0. 0. 0. 0. 0. 0.]\n [0. 0. 0. 0. 0. 0. 0.]\n [0. 0. 0. 0. 0. 0. 1.]]', '2024-03-27 14:49:43'),
(16, '[[0. 0. 0. 0. 0. 0. 0.]\n [0. 0. 0. 0. 0. 0. 0.]\n [0. 0. 0. 0. 0. 0. 0.]\n [0. 0. 0. 0. 0. 0. 0.]\n [0. 0. 0. 0. 0. 0. 0.]\n [2. 0. 0. 0. 0. 0. 0.]]', '2024-03-27 14:52:36'),
(17, '[[0. 0. 0. 0. 0. 0. 0.]\n [0. 0. 0. 0. 0. 0. 0.]\n [0. 0. 0. 0. 0. 0. 0.]\n [0. 0. 0. 0. 0. 0. 0.]\n [0. 0. 0. 0. 0. 0. 0.]\n [2. 0. 0. 0. 0. 0. 0.]]', '2024-03-27 14:53:48'),
(18, '[[0. 0. 0. 0. 0. 0. 0.]\n [0. 0. 0. 0. 0. 0. 0.]\n [0. 0. 0. 0. 0. 0. 0.]\n [0. 0. 0. 0. 0. 0. 0.]\n [0. 0. 0. 0. 0. 0. 0.]\n [2. 0. 0. 0. 0. 0. 0.]]', '2024-03-27 14:54:20'),
(19, '[[0. 0. 0. 0. 0. 0. 0.]\n [0. 0. 0. 0. 0. 0. 0.]\n [0. 0. 0. 0. 0. 0. 0.]\n [0. 0. 0. 0. 0. 0. 0.]\n [0. 0. 0. 0. 0. 0. 0.]\n [2. 0. 0. 0. 0. 0. 0.]]', '2024-03-27 14:55:57'),
(20, '[[0. 0. 0. 0. 0. 0. 0.]\n [0. 0. 0. 0. 0. 0. 0.]\n [0. 0. 0. 0. 0. 0. 0.]\n [0. 0. 0. 0. 0. 0. 0.]\n [0. 0. 0. 0. 0. 0. 0.]\n [2. 0. 0. 0. 0. 0. 0.]]', '2024-03-27 15:17:03'),
(21, '[[0. 0. 0. 0. 0. 0. 0.]\n [0. 0. 0. 0. 0. 0. 0.]\n [0. 0. 0. 0. 0. 0. 0.]\n [0. 0. 0. 0. 0. 0. 0.]\n [0. 0. 0. 0. 0. 0. 0.]\n [0. 0. 0. 0. 0. 0. 0.]]', '2024-03-27 15:22:34');

-- --------------------------------------------------------

--
-- Table structure for table `PLAYERS`
--

CREATE TABLE `PLAYERS` (
  `username` varchar(50) NOT NULL,
  `hashed_pass` varchar(255) NOT NULL,
  `email` varchar(255) NOT NULL,
  `token` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `PLAYERS`
--

INSERT INTO `PLAYERS` (`username`, `hashed_pass`, `email`, `token`) VALUES
('afsdaf', '$2b$12$BUoT8zwa3R8hrAnH8xHp9OrUZLCWWmZSJA1LrPRyBNdt4HnDYS0TO', 'aaa', 'a_cookie_goes_here'),
('Guest', '', '', ''),
('matas', '$2b$12$sQLYROOBGURzUCXKJ7SeVu8K9/Z0G3rTZ7PErksbXb.sSjJXn0yBy', 'matas.gudliauskas@gmail.com', 'se10v1roxp5indzw5f2szbamwvssi55jfny2k03dru1djzr0jkfcq6n6guvkqf0f9zfllytuf3333vm3rsgr5fdqtoewben1r84s7xme73qs0cte180wkjeceh9zqfvbcdlfomidn46hthmmsm6rmcqp5g6mnkzjdkrs6b5a9qcby4dy1mjvrctsri4eux2ksngi4ec9lm352zsd6o91rebwo5idmzl9t5mxf5tv7or5a28fr0uch9vvwja51rf'),
('petras', '$2b$12$GXzyf2ohlJFLuKlIJNcqAucJesfjIlyDZOeqtfTvbRRW6i0OkmhjW', '', 'a_cookie_goes_here');

-- --------------------------------------------------------

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
-- Dumping data for table `PLAYERS_GAMES`
--

INSERT INTO `PLAYERS_GAMES` (`id`, `FKplayer`, `FKgame`, `WDL`, `which_turn`) VALUES
(2, 'matas', 13, 'W', 1),
(3, 'Guest', 13, 'L', 2),
(4, 'Guest', 14, 'W', 1),
(5, 'matas', 14, 'L', 2),
(8, 'matas', 19, 'D', 1),
(9, 'Guest', 19, 'D', 2),
(10, 'matas', 20, 'L', 1),
(11, 'Guest', 20, 'W', 2),
(12, 'Guest', 21, 'W', 1);

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
