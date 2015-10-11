from bs4 import BeautifulSoup
from text_formatting import *

def is_tag_type(object):
    return str(type(object)) == "<class 'bs4.element.Tag'>"

def concat(string_list):
    while(len(string_list) > 1):
        first = string_list[0]
        second = string_list[1]
        first.replace_with(first + second)
        string_list.pop(1)

# Removes the tag from a non-nested tag
def format_unicode_html(unicode_string):
    try:
        bullet = u"\u2022"
        soup = BeautifulSoup(unicode_string, "html.parser")
        hyperlinks = []
        while(len(soup.find_all()) > 0):
            tag = soup.find_all()[-1]
            concat(tag.contents)
            if(str(tag.name) == "b"):
                old_string = tag.string
                new_string = bold(old_string)
                tag.replace_with(new_string)
            elif(str(tag.name) == "strong"):
                old_string = tag.string
                new_string = bold(old_string)
                tag.replace_with(new_string)
            elif(str(tag.name) == "a"):
                url = str(tag['href'])
                display_name = cyan(str(tag.string))
                entry = display_name + ": " + url
                hyperlinks.append(entry)
    
                del tag['href']
                old_string = tag.string
                new_string = cyan(old_string)
                tag.replace_with(new_string)
            elif(str(tag.name) == "li"):
                old_string = tag.string
                new_string = "    " + bullet + " " + old_string + "\n"
                tag.replace_with(new_string)
            elif(str(tag.name) == "code" or str(tag.name) == "pre"):
                old_string = tag.string
                new_string = blue(old_string)
                tag.replace_with(new_string)
            else:
                tag.unwrap()
    
        post = str(soup)
        if (hyperlinks): 
            post += "\n\n"
            post += "Hyperlinks\n"
            post += "==========\n"
            for link in hyperlinks:
                post += link + "\n"
    
        return post
    except:
        return unicode_string.encode('ascii', 'ignore')

#unicode_string = u'<a href="http://cs61a.org/quiz/quiz02/">Quiz 2</a> is posted, due Monday 10/12 &#64; 11:59pm (but you should really just do it today or tomorrow).\n\n<b>You must work alone</b>, but you may talk to the course staff. You may use any course materials, including an interpreter, course videos, slides, and readings. Please <b>do not</b> discuss these specific questions with your classmates, and <b>do not</b> scour the web for answers or post your answers online.\n\nYour submission will be graded automatically for correctness. Your implementations <b>do not</b> need to be efficient, as long as they are correct. We will apply additional correctness tests as well as the ones provided. Passing these tests does not guarantee a perfect score.\n\n<b>Asking Questions:</b> If you believe you need clarification on a question, <b>make a private post</b> on Piazza. Please do not post publicly about the quiz contents. If the staff discovers a problem with the quiz or needs to clarify a question, we will email the class via Piazza. You can also come to office hours to ask questions about the quiz or any other course material, but no answers or hints will be provided in office hours.\n\n<b>Changes:</b>\n<ul><li>10/09, 6:30 PM - the unnecessary <code>minted</code> attribute was removed.</li></ul>\n\n#pin'
contents = [u'<a href="http://cs61a.org/quiz/quiz02/">Quiz 2</a> is posted, due Monday 10/12 &#64; 11:59pm (but you should really just do it today or tomorrow).\n\n<b>You must work alone</b>, but you may talk to the course staff. You may use any course materials, including an interpreter, course videos, slides, and readings. Please <b>do not</b> discuss these specific questions with your classmates, and <b>do not</b> scour the web for answers or post your answers online.\n\nYour submission will be graded automatically for correctness. Your implementations <b>do not</b> need to be efficient, as long as they are correct. We will apply additional correctness tests as well as the ones provided. Passing these tests does not guarantee a perfect score.\n\n<b>Asking Questions:</b> If you believe you need clarification on a question, <b>make a private post</b> on Piazza. Please do not post publicly about the quiz contents. If the staff discovers a problem with the quiz or needs to clarify a question, we will email the class via Piazza. You can also come to office hours to ask questions about the quiz or any other course material, but no answers or hints will be provided in office hours.\n\n<b>Changes:</b>\n<ul><li>10/09, 6:30 PM - the unnecessary <code>minted</code> attribute was removed.</li></ul>\n\n#pin', u'<p><strong>Introduction</strong>\nThis Monday\xa0(10/12), the course tutors will be overseeing the third\xa0of several optional CS61A guerrilla sections specifically aimed at going over past concepts that you may still be struggling with. (The last\xa0was &#64;1675.)\n\n<strong>Format and Logistics</strong>\nYou&#39;ll meet up and form groups of 4-5 and start working on a worksheet. These sections are all about working together to learn the material and getting better at Computer Science together.\n\n<b>The Guerrilla section will be held Monday\xa010/12 in the 2nd Floor Soda Labs from 7 - 9 pm.</b>\n\nWe&#39;ll be covering\xa0<strong>OOP. \xa0</strong>Due to our schedule, we won&#39;t be holding an official guerrilla section on Trees, Lists, and Nonlocals. \xa0However, posted below are the links to the worksheet and solutions for the section from the previous semester if you wanted some more practice problems. \xa0If you have any questions about this worksheet, you can post in the followups of this post, go to office hours, or go to the\xa0OOP guerrilla section.</p>\n<p></p>\n<p><strong>Trees, Lists, and Nonlocals:</strong></p>\n<p>Worksheet:\xa0<a href="http://tinyurl.com/omdmeuc">http://tinyurl.com/omdmeuc</a></p>\n<p>Solutions: <a href="http://tinyurl.com/onubtnt">http://tinyurl.com/onubtnt</a>\n\n<strong>Guidelines</strong></p>\n<ul><li>You should attend if you still feel shaky on topics we&#39;ve covered up until now (especially the early stuff!) We will dwell on details and examples until you feel comfortable.</li><li>There will not be a lecture - the section will be discussion based. You will discuss with each other, with tutors and lab assistants around to oversee things. Think of it as a study group with tutors nearby.</li><li>We will not give help on Ants.\xa0Please go to office hours for that.</li><li>There will be a list of problems for you to discuss and solve together. Bring your notes and laptops for reference.</li><li>Since the meetings are based around working together and talking about Computer Science with each other, do not be rude or condescending. If you understand something, try to explain it patiently and clearly to others.</li><li>It is more important to understand one thing well than many things only partially. Consequently, we will not cover everything from the course, but rather focus on OOP.</li></ul>\n<p></p>\n<p>If you are planning on coming, please respond by voting in the poll below.</p>\n\n [o] I can make the guerrilla section from 7-9 on Monday\n[o] I can&#39;t make it :(\n#pin', u'<p>Hey everyone!</p>\n<p>\xa0</p>\n<p>To help those who are looking for\xa0a partner for the Ants\xa0project, I&#39;ve created a partner finding form where you&#39;ll have access to everyone else&#39;s responses after filling it out. The facilitation here is the same as the partner finding for the Maps project.</p>\n<p></p>\n<p>Rules of Engagement:</p>\n<p>1.\xa0<a href="https://docs.google.com/forms/d/1DoHvyxo1eFpjUF_9VlpZLikeSpkqyB94hOuM-HNeGOU/viewform" target="_blank">Fill out the form</a>.</p>\n<p>2.\xa0Go to the spreadsheet link provided after filling out the form and look for potential partners.</p>\n<p>3. Email potential partners.</p>\n<p>4. Keep checking the spreadsheet for more potential partners and email them.</p>\n<p>5. Find a partner.</p>\n<p>6. Update the spreadsheet if you find a partner (last column), so no one emails you asking to be your partner.</p>\n<p>\xa0</p>\n<p><a href="https://docs.google.com/a/berkeley.edu/spreadsheets/d/1pRoTnQk06mX6OYieayKHko9296ELxohN3mMKwxsQMO8/edit?usp=sharing" target="_blank">Direct link to the spreadsheet</a></p>\n<p></p>\n<p>Hope you find a partner\xa0and have fun working together on Ants! :)</p>\n<p></p>\n<p>#pin</p>', u'Check this post first if you have an issue related to the Ants project. If your issue isn&#39;t here, make a new Piazza question.\n\n<b>General</b>\n<ul><li>You get <b>two</b> additional points by submitting <b>two</b> days early (by 10/14). You get <b>one</b> additional point by submitting <b>one</b> day early (by 10/15).</li><li>You will be able to resubmit for lost composition points.</li><li>You are allowed to write code outside of the <tt># BEGIN ...</tt> and <tt># END ...</tt> blocks.</li><li>Play using the web-based graphics with &lt;tt&gt;python3 gui.py.</li></ul>\n<b>0. Reading</b>\n\n<b>1. HarvesterAnt</b>\n\n<b>2. Entrance</b>\n\n<b>3A. Water</b>\n\n<b>4A. FireAnt</b>\n<ul><li>Why is my place <tt>None</tt> in <tt>FireAnt.reduce_armor</tt>? <tt>Insect.reduce_armor</tt> removes the insect from its place when the insect dies.</li><li>Why are only half the bees are getting killed? Don&#39;t iterate over a list that you&#39;re mutating (<tt>bees</tt>).</li></ul>\n<b>3B. ThrowerAnt</b>\n\n<b>4B. LongThrower and ShortThrower</b>\n\n<b>5A. WallAnt</b>\n\n<b>6A. NinjaAnt</b>\n\n<b>5B. ScubaThrower</b>\n\n<b>6B. HungryAnt</b>\n\n<b>7. BodyguardAnt</b>\n\n<b>8. TankAnt</b>\n\n<b>9. QueenAnt</b>\n\n<b>EC. SlowThrower and StunThrower</b>\n<ul><li>In the tests, <tt>bee.action(colony)</tt> returns a function instead of <tt>None</tt>? &#64;2271</li></ul>\n#pin', u'<p>Hi everyone,</p>\n<p></p>\n<p>Hope you guys are making good progress on HW and have started/are starting on the project</p>\n<p>Here is a question guide for the Mobile Question on the HW. Please refer to this for help on the Mobile question.</p>\n<p></p>\n<p><a href="https://docs.google.com/a/berkeley.edu/document/d/1d8H8kDxSUCqP4bAe0ptQTDsQlgIQ9H9uwxIMp1sqSUA/edit?usp=sharing">https://docs.google.com/a/berkeley.edu/document/d/1d8H8kDxSUCqP4bAe0ptQTDsQlgIQ9H9uwxIMp1sqSUA/edit?usp=sharing</a></p>\n<p></p>\n<p>Good luck!</p>\n<p></p>\n<p>#pin</p>\n<p></p>\n<p></p>', u'Project 3 is now posted, one day later than planned. I have extended the deadline by one day to Friday 10/16. Complete the project by Wednesday 10/14 for 2 early submission extra credit points. Complete the project by Thursday 10/15 for 1 early submission point. Get started this week!\n\nIn order to give you a chance to attend Discussion 5 and review solutions to Homework 5, I have delayed Quiz 2 by two days. It will be released on Friday 10/9 and is due Monday 10/12. The quiz is only 2 points and should not take much time, but does require you to understand the Python object system.\n\nHistorically, some students have fallen behind at this point in the semester. Catching up after you fall behind in lecture material is not fun; you&#39;re highly encouraged to watch lecture the day it is released. \n\nOne great way to make sure that you watch lecture the day it&#39;s released is to attend live lecture in Wheeler Hall. There&#39;s plenty of room. Perhaps I&#39;ll see you tomorrow at 2pm.\n\n#pin', u'I have updated the syllabus to include a more detailed description of how we are going to calculate midterm recovery points. \n\nIf you scored below 20/40 on the midterm you are eligible for midterm recovery points depending on discussion attendance and lab participation. I&#39;ve included the exact logic used to calculate the amount of points you can expect to receive back.\n\n<pre>def recovery_points(your_score, labs, discussions):\n    attendance = labs &#43; discussions\n    max_recovery = max(0, 20 - your_score) / 2\n    return max(0, max_recovery - (5 - attendance)) \n</pre>\n\n\n#pin', u'<script type="text/javascript">PA.load("/dashboard/project_partners", null, function(data){ $(\'#\' + \'questionText\').html(data);});</script> #pin', u'<p>Can someone please explain how to approach 3b? I can&#39;t figure out how to search for places with bees and how to determine which is closest and how to implement that. are we supposed to return the line with\xa0return random_or_none(self.place.bees)?</p>', u'<p>When I try to use reduce_armor for the Insect class, and I pass in insect.armor, I&#39;m getting an error that says reduce_armor() is missing a required positional argument &#39;amount&#39;. Why would this happen? Why doesn&#39;t putting insect.armor in there for &#39;amount&#39; satisfy that?</p>']
soup = BeautifulSoup(contents[1], "html.parser")
