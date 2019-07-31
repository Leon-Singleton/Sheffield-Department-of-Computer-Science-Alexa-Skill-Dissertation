CREATE TABLE `FavouriteModules` (
  `FavouriteID` INT NOT NULL AUTO_INCREMENT,
  `ModuleCode` varchar(255) NOT NULL,
  `UserID` varchar(255) NOT NULL,
  PRIMARY KEY (`FavouriteID`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;