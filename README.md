# GetClicked.GOP
Team Members:
Daniel Ostrowski	ostrowsd@purdue.edu
Harsh Patel		patel682@purdue.edu
Andy Gao		gao353@purdue.edu

Name of Project: GetCLicked.GOP

Technologies:
Amazon Web Services - hosting
Languages: Java, javaScript, AngularJS, python, MySQL, Css, BootStrap, 

Functionality & Brief Description:

Main Objective: 
2 types of accounts, associated thru the app, , students answer question that the prof posts within a certain time frame
Posting answering questions
Text responses
**export responses as a CSV file**


Side:	
Check IP address to see if the student is on the wifi, where the session is taking place
Integrate a kahoot-like program


ORIGINAL DOC:
/////////////////////////////////////////////////
Login/index page
Intent: Allow user to login/ sign up as a professor or student
Post: username=string&password=string&var=bool&login=bool
Links: to About page
Home Page
Intent: Need to be able to get classes the user is an instructor or a student for
Get: Classes associated with user
Links: Create class page, Join class page
Create class page
Post: Submits name of new class, then redirects to home page
TODO: name checking
Join class page
Post: Submit name of class
TODO: name checking
Class page
Intent: allow users to answer questions
Post: question answers

Server’s API:
Notes: Input is represented in JSON / Python dictionary syntax for simplicity - I don’t actually know enough to know if it has to JSON. The output returned by the server is in JSON except where noted.

curl is a fantastic tool for playing with these.
curl -b cookies -c cookies --data "argument1=value1&argument2=value2&argument3=value3" http://18.216.65.48/app/nameofapicall/; echo

To test a post:
Post to “http://18.216.65.48/app/testpost/”
Input:
Anything
Output:
A human-readable string that explains what the server received from the client.

To create a new user:
Post to “http://18.216.65.48/app/createuser/”
Input:
{
	username : foo_username,
	password : foo_password
}
Output:
{
	success : a_boolean,
	comment : human_readable_string
}
Notes: “comment” is a human-readable string saying that the user was created successfully, or if a user was not created, explaining why the user could not be created. An example user is Username: a
Password: a

To log a user in:
Post to “http://18.216.65.48/app/loginuser/”
Input:
{
	username : foo_username,
	password : foo_password
}
Output:
{
	success : a_boolean,
	comment : human_readable_string
}
Notes: “comment” is a human-readable string saying that the user logged in successfully, or if they did not, explaining why the user could not be logged in

To log a user out:
Post to “http://18.216.65.48/app/logoutuser/”
Input:
{ }
Output:
{
	success : true
}
Notes: “Logging out” always succeeds whether or not a user was actually logged in.

To create a class:
Post to “http://18.216.65.48/app/createsection/”
Input:
{
name: name_of_the_class_section_to_create
}
Output:
{
success : a_boolean,
	comment : human_readable_string
}
Notes: The name of the section must be unique or else the result is a failure.

To list the names of all class sections that the user is an instructor of
Post to “http://18.216.65.48/app/sectionsasinstructor/”
Input:
{}
Output:
{
	success: a_boolean,
	comment: human_readable_string
	sections: [“section name 1”, “section name 2”, … “section name n”]
}
Notes:

To join a class:
Post to “http://18.216.65.48/app/enrollinsection/” 
Input:
{
section: name_of_class_section_to_enroll_in
}
Output:
{
success : a_boolean,
	comment : human_readable_string
}
Notes: Fails if the user is already enrolled in the class. Nothing prevents the instructor of a class section from also enrolling in the class

To list the names of all class sections that the user is student of
Post to “http://18.216.65.48/app/sectionsasstudent/”
Input:
{}
Output:
{
	success: a_boolean,
	comment: human_readable_string
	sections: [“section name 1”, “section name 2”, … “section name n”]
}
Notes:

To create a question:
Post to “http://18.216.65.48/app/createquestion/”
Input:
{
	section: name_of_class_section_to_make_question_for,
	label: text_of_the_question,
	responses: python_literal_list_of_lists_see_notes
}
Output:
{
	success: a_boolean,
	comment: human_readable_string
}
Notes: The operation fails if the user is not the section’s instructor. The format for the “responses” is a 2-dimensional Python-style list, where each subarray has length 2, with the first entry being the answer’s label and the second entry being a boolean specifying if the answer is correct or not. The following line is an exact string that could be used as the value of “responses”
[['This is one answer choice’, True], ['This is another’, False], ['No order guarantee is made', False]]
Note that True and False must be capitalized as such or the call will fail. Single quotes must be used. Certain characters in the answer labels must be escaped with backslash, such as double quotes and backslashes. In short, the value of “response” must be a valid Python list literal. This format is cumbersome. If this submission proves overly burdensome please let Daniel know.

To submit an answer to a question
Post to “http://18.216.65.48/app/answerquestion/”
Input:
{
	questionid: id_of_question_to_answer,
	label: text_label_of_answer_to_select,
}
Output:
{
	success: a_boolean,
	comment: human_readable_string
}
Notes: A question’s numerical id can be found in the results of other calls. Fails if there is no question with that id. Fails if the question does not have an answer with that label text. Fails if the user is not enrolled in the class section for which the question was created. If the user has already answered that question, their response is updated.

To get information about the questions that exist in a particular section
Post to “http://18.216.65.48/app/getquestionsbysection/”
Input:
{
	section: name_of_section_to_look_in,
}
Output:
{
	success: a_boolean,
	comment: human_readable_string
	questions: [[question_id, question_text, boolean_has_user_answered_it, users_chosen_answer], [question2_id, question2_text, boolean_has_user_answered_it2, users_chosen_answer2], …]
}
Notes: Fails if the class section name is not supplied, if there is no class section with that name, and if the user is not enrolled in the specified section.

To get information about a specific question
Post to “http://18.216.65.48/app/getquestiondetail/”
Input:
{
	questionid: id_of_question_to_retrieve_details_for
}
Output:
{
	success: a_boolean,
	comment: human_readable_string,
	questionid: questionid_that_the_output_describes,
	hasanswered: boolean_has_the_user_answered_the_question,
	chosenanswer: label_of_answer_user_selected,
	label: question_text,
	answers: [label_of_answer_choice_1, label_of_answer_choice_2, … ]x`
}
Notes: Fails if the questionid is not supplied, if there is no question with the specified id, and if the user is not enrolled in the appropriate section.

TODO:
getusername
getscorescsv
