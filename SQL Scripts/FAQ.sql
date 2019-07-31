CREATE TABLE Faqs (
    `Question` VARCHAR(255) NOT NULL,
    `Answer` text NOT NULL,
    fulltext (Question)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

INSERT INTO Faqs (Question, Answer)VALUES
    ('I''m taking 3 A levels and an EPQ. Will you accept me?','We require an A at A level Maths. We will accept EPQs if they are suitably related to Computer Science, Maths, or Engineering. We suggest you email ug-compsci@sheffield.ac.uk with your expected results to determine whether you would be considered.'),
    ('What if I''m not doing A level maths?','If you have other A levels or BTEC, you can apply for the Foundation Year, provided you have GCSE maths and science with grades B+'),
    ('What if I don''t meet my offer grades?','We always consider candidates who just miss our offer, if we have space'),
    ('If I fail to get in, can I apply in Clearing?','Clearing is very competitive, and we tend to fill our spaces with applicants who were close to our offer'),
    ('What are the entry requirements for 2019?','For Bachelors degrees, the entry requirements are AAA, including Mathematics. If you are taking A levels and EPQ, the requirements are AAB and an A in your extended project. For international baccalaureate, the requirement is 36 points including 6 points in higher level mathematics'),
    ('What kind of careers or jobs do graduates go into?','Our students go into a range of careers, inlcuding software developers, technical consultants, web designers, data scientists, and academic researchers. They work for businesses such as : ARM, BT, Google, IBM, Sky, and Jaguar Land Rover, as well as various SMEs and start ups'),
    ('What is a typical timetable in first year?','20 taught hours a week, and 20 private study hours'),
    ('How are the courses assessed?','Generally exams make up 40% of assessment and coursework is 60% of the assessment, although each module varies'),
    ('How many students gain a first class degree?','Roughly 35% of students leave year 3 with a first.'),
    ('What are the fee rates for home students?','9250 pounds'),
    ('What are the fee rates for overseas students?','21450 pounds'),
    ('What is the difference between computer science and software engineering?','Computer science concentrates on the theory behind the discipline; what is possible in computing. Whereas software engineering focuses on the application of the discipline; meeting customer requirements, quality assurance etc.'),
    ('Can I study abroad as part of the course?','Yes, in your 2nd year'),
    ('What is the ratio of women on the course?','Roughly 15% of each cohort are female. Our 2018 cohort is 20% female. 40% of our academic staff are women.'),
    ('How many students are currently on a Year in Industry?','24 students from the 2017 cohort went on a year in industry, compared to 30 students in the 2018 cohort.');
