CREATE TABLE `Courses` (
  `CourseName` varchar(255) NOT NULL PRIMARY KEY,
  `Description` text NOT NULL,
  `EntryReq` varchar(255) NOT NULL,
  `UcasCode` varchar(255) NOT NULL,
  `Type` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

INSERT INTO `Courses` (`CourseName`,`Description`,`EntryReq`,`UcasCode`,`Type` ) VALUES ('Computer Science','You\'ll learn to understand the theoretical principles underlying a problem, and how to engineer a solution. You\'ll also become familiar with the practical issues involved in developing reliable, effective software systems in business or industry. \nAs well as learning to program and think analytically, you\'ll be encouraged to work in teams and develop your communication skills. In the third year, half of your time is spent on a substantial individual project, giving you scope for creative and intellectual input.','Three A grades at A level including maths.','G402', 'Under Graduate');
INSERT INTO `Courses` (`CourseName`,`Description`,`EntryReq`,`UcasCode`,`Type`) VALUES ('Software Engineering','You\'ll learn about the latest developments in programming languages, software design and project management techniques. The course will help you develop interpersonal and team-working skills expected by employers. You\'ll also get a solid grounding in the fundamentals of computer science and a chance to explore aspects of artificial intelligence. \nIn the second year, you\'ll develop software for real, external clients. In the third year, you\'ll carry out an individual research project, giving you scope for creative and intellectual input. You can specialise in many areas including intelligent web, speech and language technology; 3D computer graphics, and computer security and forensics.','Three A grades at A level including maths.','G600', 'Under Graduate');
INSERT INTO `Courses` (`CourseName`,`Description`,`EntryReq`,`UcasCode`,`Type`) VALUES ('Artificial Intelligence and Computer Science','This course is about biologically inspired algorithms, their relationship to living biological intelligence and the nature of consciousness itself. Some modules overlap with the main Computer Science degree, so you get the same solid grounding in the fundamentals. \nYou\'ll get the chance to specialise in speech recognition, language processing or robotics. We encourage you to take optional modules in psychology and philosophy to enhance your understanding.','Three A grades at A level including maths.','GG74' , 'Under Graduate');

INSERT INTO `Courses` (`CourseName`,`Description`,`EntryReq`,`UcasCode`,`Type` ) VALUES ('Data Analytics','Data Analytics focuses on managing vast amounts of information and transforming it into actionable knowledge. The programme teaches the key skills that are required to carry out practical analysis of the types of data sets that need to be interpreted in the modern world. The types of data sets encountered include large data sets as well as structured and unstructured data. The programme makes use of techniques developed within a range of disciplines, including computer science, artificial intelligence, mathematics and statistics.','Applicants are expected to have at least a 2:1 honours degree in computer science or a closely related subject.','COMT130', 'Post Graduate');
INSERT INTO `Courses` (`CourseName`,`Description`,`EntryReq`,`UcasCode`,`Type`) VALUES ('Cybersecurity and Artificial Intelligence','There is little doubt that we are hugely dependent on interconnected devices and systems and there are many opportunities to inflict malicious damage on them. Unsurprisingly, cybersecurity problems are reported in the media everyday. Cybersecurity is one of the most pressing problems of our day and securing computational systems and infrastructures is critical for healthy operation of modern societies. Artificial Intelligence (AI) has achieved an exceptional profile in recent years. If cybersecurity is one of the most pressing problems of our day then AI is perhaps the highest profile solution technology. Much ’smart’ infrastructure is underpinned by AI and the provision of insight via data analytics is becoming pervasive. Harnessing AI to provide more secure component and system designs and to provide insights into system operation, e.g. to detect intruders, is a natural goal.','Applicants are expected to have at least a 2:1 honours degree in computer science or a closely related subject.','COMT141', 'Post Graduate');
INSERT INTO `Courses` (`CourseName`,`Description`,`EntryReq`,`UcasCode`,`Type`) VALUES ('Advanced Software Engineering','The MSc (Eng) in Advanced Software Engineering is suited to graduates in Computer Science and related disciplines, who wish to complete their academic profile in specialist areas, and obtain practical experience of commercial software engineering. The programme provides a full awareness of leading-edge techniques for the specification, analysis, design, implementation and maintenance of complex software systems.','Applicants are expected to have at least a 2:1 honours degree in computer science or a closely related subject.','COMT06' , 'Post Graduate');
INSERT INTO `Courses` (`CourseName`,`Description`,`EntryReq`,`UcasCode`,`Type` ) VALUES ('Advanced Computer Science','The MSc in Advanced Computer Science is suited to graduates in Computer Science and related disciplines, such as Software Engineering or Computing and Mathematics, who wish to complete their academic profile in specialist areas, and study in a research-led teaching environment. The programme provides students with an education in leading-edge aspects of computer science, and offers a wide range of elective modules that are informed by the departments research interests.','Applicants are expected to have at least a 2:1 honours degree in computer science or a closely related subject.','COMT123', 'Post Graduate');
INSERT INTO `Courses` (`CourseName`,`Description`,`EntryReq`,`UcasCode`,`Type`) VALUES ('Computer Science with Speech and Language Processing','The capabilities of computational speech and language processing (SLP) have grown substantially in recent years, both in the research laboratory and in the commercial marketplace. There are now a wide range of applications for SLP systems such as automatic translation between languages (e.g. Arabic and English), automatic speech recognition, automatic answering of questions, text mining (e.g. from the web) and access to information through spoken human-computer dialogue. Systems which use speech and language processing are now in everyday use, through technologies such as internet search engines and mobile phones, and most major international computer and telecoms companies now engage in SLP research and development.','Applicants are expected to have at least a 2:1 honours degree in computer science or a closely related subject.','COMT127', 'Post Graduate');
INSERT INTO `Courses` (`CourseName`,`Description`,`EntryReq`,`UcasCode`,`Type`) VALUES ('Software Systems and Internet Technology','The MSc in Software Systems and Internet Technology is designed for graduates of disciplines other than Computer Science, who have some experience of computer programming, and wish to build on their existing knowledge. The programme covers key topics in computer science and software engineering, but with an emphasis on current topics in internet computing.','Applicants are expected to have at least a 2:1 honours degree in computer science or a closely related subject.','COMT138' , 'Post Graduate');