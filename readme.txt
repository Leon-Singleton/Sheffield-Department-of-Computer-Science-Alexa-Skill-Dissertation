CONTENTS OF THIS FILE
--------------------------

* Introduction
* Requirements
* Installation
* Testing and Troubleshooting

INTRODUCTION
------------

This directory provides all of the necessary content required to setup a working copy 
of the Alexa Skill for the Department of Computer Science Alexa Skill as described in
the dissertation report.


REQUIREMENTS
-------------

* A text editor such as Atom
* An Amazon Web Services Account
* Installation of MYSQL Workbench
* An Amazon Alexa Developer Console account

INSTALLATION
------------

Preparing the Database
----------------------

1. Using Amazon RDS found within via Amazon Web Services, create a "free tier" MYSQL database, make a note of the 
database connection URL, database name, username and password.

2. Open MYQSL workbench and connect to the database you created using the
credentials you associated with it.

3. Open each of the SQL script files stored within the "SQL scripts" folder 
and execute each one.

4. Finally, open the sqlConnection.py file in the skill_env folder and change the 
SQL connection details to the details associated with your database.

Building the Lambda Function
------------------------------

1. Create an AWS lambda function from within the Amazon Web Services development portal.
Ensure that the function runtime langauge is Python 3.6 or higher.

2. Create a zipped folder of the entire contents of the skill_env folder and upload this 
as the function package for your lambda function.

3. Set the lambda function handler as "DCS_App.handler" and the lambda function execution role
as "lambda_basic_execution"

4. Add the "Alexa Skill Kit" as a trigger to the lambda function.

5. Make a note of the ARN code at the top of the page.

6. Finally, Save the lambda function.

Building the Interaction Model
------------------------------

1. Go to the Alexa Developer Console and create a custom skill.

2. After creating your skill copy the contents of the InteractionModel.json file
into the JSON editor located on the left-hand side of the development console.

3. Using the lambda function ARN that you obtained earlier set the endpoint 
to point to this url as the default region. Save the endpoint.

4. Make sure to build the Model at the top of the development console.


TESTING AND TROUBLESHOOTING
---------------------------

Testing of the skill can be performed using any Alexa enabled device associated with
the amazon account that the skill has been created for. Alternatively, testing can be done 
via the Alexa Developer Console.

Troubleshooting of the skill can be performed by taking the Skill JSON input and testing it via a test event 
in the lambda function, to see any exceptions causing the skill to not respond as it should.

For more information regarding testing and troubleshooting of the skill refer to the dissertation report.
