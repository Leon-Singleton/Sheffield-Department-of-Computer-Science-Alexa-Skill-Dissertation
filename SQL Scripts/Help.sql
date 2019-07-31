CREATE TABLE `Help` (
  `HelpID` INT NOT NULL AUTO_INCREMENT,
  `Message` varchar(255) NOT NULL,
  PRIMARY KEY (`HelpID`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

INSERT INTO `Help` (`Message`) VALUES ('Try asking me how a specific module is assessed.');
INSERT INTO `Help` (`Message`) VALUES ('Try asking me how many credits a specific module is worth.');
INSERT INTO `Help` (`Message`) VALUES ('Try asking me when a specific module is taught.');
INSERT INTO `Help` (`Message`) VALUES ('Try asking me who teaches a specific module.');
INSERT INTO `Help` (`Message`) VALUES ('Try asking me about the aims or objectives of a specific module.');
INSERT INTO `Help` (`Message`) VALUES ('Try asking me how a specific module is taught.');
INSERT INTO `Help` (`Message`) VALUES ('Try asking me how about the feedback of a specific module.');
INSERT INTO `Help` (`Message`) VALUES ('Try asking me how about the content of a specific module.');
INSERT INTO `Help` (`Message`) VALUES ('You can ask me about the departments, including how to contact us and where we are located');
INSERT INTO `Help` (`Message`) VALUES ('You can ask me about the courses that we offer');
INSERT INTO `Help` (`Message`) VALUES ('You can ask me about course entry requirements');
INSERT INTO `Help` (`Message`) VALUES ('You can ask me for the ucas code of a specific course');
INSERT INTO `Help` (`Message`) VALUES ('You can ask me about industrial placements');
INSERT INTO `Help` (`Message`) VALUES ('You can add modules of interest to a favourites list');
INSERT INTO `Help` (`Message`) VALUES ('Try asking what modules are in your current favourites list');
INSERT INTO `Help` (`Message`) VALUES ('You can remove or clear the contents of your favourites list');
INSERT INTO `Help` (`Message`) VALUES ('You can ask me about lecturer contact details');
INSERT INTO `Help` (`Message`) VALUES ('You can ask me for the research group of a lecturer');
INSERT INTO `Help` (`Message`) VALUES ('You can ask me about a lecturer');
INSERT INTO `Help` (`Message`) VALUES ('You can ask me about the modules a lecturer teaches');
INSERT INTO `Help` (`Message`) VALUES ('Try asking me about timetable information for a given module');
INSERT INTO `Help` (`Message`) VALUES ('You can ask me FAQ questions reagrding the department');
INSERT INTO `Help` (`Message`) VALUES ('You can ask me FAQ questions reagrding the university more generally, make sure to say search followed up by your question');