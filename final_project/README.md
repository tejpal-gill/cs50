# INSIGHT
#### Video Demo:  <https://youtu.be/KE71dOIEV8U>
#### Description:

This project helps to keep record of tests conducted in an eduacational institute and provides visual insights on academic performance of the students.

**Function**

![Signup Page Screenshot](screenshots/signup.png)
User can create a new account on signup page.

![Signup Page Screenshot](screenshots/login.png)
Existing users can login through the login page.

![Index Page Screenshot](screenshots/index.png)
On the index page, the user gets a general view of all the students in the institute, with there average marks on x-axis and the difference between there best and worst performance on the y-axis.

![Students Screenshot](screenshots/students.png)
The form is use to register new students into the database by providing there name, class in which they be enrolling and assigning them any rollno between the range 1 to 999 usless it's already assigned.
Below the form are all the registerd students.

![Adding new test Screenshot](screenshots/test1.png)
Form to create a new test.
Below that are all the previous tests with their respective class and subject.
![Adding marks for the test Screenshot](screenshots/test2.png)
When the test name, grade and subject are it submitted. It automatically retrives all the students names along with their roll numbers to avoid any confusion with students having same names. Just input there respecive marks and submit.

![Analyse Screenshot](screenshots/analyse.png)
Select the grade and subject which the user wants to analyse. A scatter plot with each test of different colors which can be turned off or on just by clicking the name of the test.
The marks are on the x-axis and the deviation from that particular student's average in particular subject on y-axis.
This helps to identify each students weaknesses and strengths while also looking a class as a whole. This can also help to realise the topic where the teacher lacked.

**Selection**

I choose this project beacause when i was doing the pset 7, i was wondering how much nicer it would be if we could visualize information. So i decided that i would do something with data visualization.

**The Database**

Within the Insight application, the database comprises of six essential tables to store and manage crucial information. Here's are the key tables:

Users for containg the username, id and the password hash.

Classes table to store classes with the ClassID

Subjects table to store subject names and SubjectID

Students to store data Associated user ID, Unique identifier for each student and personal details like the name, rollno and the grade in with they are enrolled in.

Tests table to maintain reference to the user ID, subject and class for which the test is conducted.

Marks table to store student's performance in various tests.

**Coding and Thinking**

Coding the login, signup form were simple as i had already done it in the pset9 Finance.
A new feature implemented was the option to unhide or hide the password, which had been done using javascript. It was pretty easy.
![Password hidden Screenshot](screenshots/login.png)
![Password visible Screenshot](screenshots/loginpass.png)
The most difficult part on the login/signup page was marking the gif cented in the brading div.

Setting up the forms for registering students and recording test was alringht.
The funny thing is that, near the end of this project, i learnt that something named Flaskforms exisits. :cry:
I had to make many changes to my intial database to work in the desired fashion.
The validating the inputs was straight-forward.

![Desktop Screenshot](screenshots/analyse.png)
![Mobile Screenshot](screenshots/dynamic.png)
I thought making the site mobile friendly would be very difficult, surprising it was very easy, even for the charts i just had to set resposive to true and maintain aspect ratio to false

The actual difficult part was making the data from database work with charts.js. I spent a lot of days just trying to figure out the right sql query to retrive the data that i needed then jsonify it to pass it on.

Showing all the datapoints under one head was easy but i didn't want that so i had to learn a fair amount to js syntax.

Then i faced the problem of labels not showing correctly, tooltips callback was the key to that. Figuring that out took a lot of documentation reading as just googling it was not doing it.

If i had more time i wish could have used median instead of means.

**Aesthetics**

The structure was inpired by pset9 Finance.

colors: <https://coolors.co/palette/0d1b2a-1b263b-415a77-778da9-e0e1dd>

fonts: <https://fonts.google.com/>

brand: <https://www.ddesignerr.com/wp-content/uploads/2012/05/038.gif>
