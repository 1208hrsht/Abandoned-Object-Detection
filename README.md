# Abandoned-Object-Detection
Abandoned Object Detection using Canny Edge Detection to find contours and Background Subtraction method.


Steps invloved:
1)	The input video is divided into frames.
2)	Frames are converted to Grey from RGB.
3)	First frame is taken as a reference.
4)	Frame difference between the first frame and the current frame is taken.
5)	Canny Edge Detection Technique is applied.
6)	Contours are formed.
7)	Contours formed are abandoned objects and are tracked for a predefined time.
8)	If the object is not moved within a specified time, an alarm is generated

Research Papers used for the same:
•	An Approach for Unattended Object Detection through Contour Formation using Background Subtraction 
  Author: Dwivedi, Neelam & Singh, Dushyant & Kushwaha, Dharmender 
• Analysis of Image Edge Detection Techniques
  Author: Ansari, Mohd & Kurchaniya, Diksha & Dixit, Manish
•	Research on Improved Canny Edge Detection Algorithm
  Author: Liu, Ruiyuan; Mao, Jian

