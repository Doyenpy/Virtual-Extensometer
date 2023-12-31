# Virtual-Extensometer: Implementation of Lucas-Kanade's optical flow algorithm to calculate the strain of a specimen during a tensile test

The aim of the program is to input the video (set of several successive images) taken during the tensile test, read the video in several frames and display the first image (frame 1) to enable the user to select two points on this image, save the coordinates of these points (depending on the resolution of the images), calculate the distance "L0" (in pixels) between the selected points (see Figure 1).
Suppose the points are not aligned on the same axis. 
In that case, the program allows the user to modify the coordinates of these points at his convenience (the program determines and saves the new coordinates). 
Iteratively, the program uses the Lucas-Kanade optical flow tracking method to track the position of the points selected on the first frame in the other successive frames, while calculating the distance "Li" (in pixels) between the position of the new points found on the frame i+1, the displacement "ΔLi" (in pixels) on each frame i +1 and the strain "ɛi" at each iteration (see Figure 2). 
The program plots the trajectory followed by the selected points (see Figure 3). 
At the end of the tracking, the program saves the calculated strain values for each frame in an Excel file. 
For a better estimate of the strain, selecting points at the limit of the specimen's narrow section or in the gage zone is advisable.
