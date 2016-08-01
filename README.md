# CBSE 2016 12th Grade Result Crawler

A script to find results of 12th Boards using selenium implementation on headless browser.
Works by brute forcing the roll numbers of a specific range. Requires school code.

Attached .exe to run out of the box. Please note you need the all the .exe(s) in one folder. The other two are for the simulated browsers.

Saves all the extracted data into 2 tables in SQLITE, namely 'Records' and 'Marks'.
'Records' stores all the basic data like roll number, identity, etc.
'Marks' stores marks of each roll number for each subject in different rows along with breakup of the marks.

Data isn't normalized perfectly, SQLITE probably wasn't a good idea to go with. MongoDB would have been a better choice for such a nested data structure.
Went with SQLITE due to lack of time and care. This was mostly a bet.

It isn't like its unusable, just requires a bit of SQL knowledge. Join and select statements should do the job pretty nicely.

Contact me for more.

** Please note I am not in  favour of anyone taking this code and calling it their own without any sort of acknowledgement. A lot of hardwork went into this. See the License for more **