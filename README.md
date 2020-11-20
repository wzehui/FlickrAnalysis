# Flickr Lake Constance Tourism Analysis
Flicker Analysis project aims to analyzing data from Photo-sharing platform
 Flickr about tourism in Lake Constance. The relevent instructive information
  is extracted for surrounding restaurant and hotel industy.
## Data Proprocessing
Since the photos uploaded on the platform contain not only those from
 tourists during their travels, but also those from people living in the area
  and local businesses, it is necessary to filter them before proceeding to
   the next step. This project optimizes the filtering conditions proposed in
    the previous paper. This project modifies and optimizes the filtering
     conditions proposed in the original thesis and obtains the following
      filtering conditions:

1. delete photos with invalid photo taken time

2. delete photos that photo taken time and photo upload time are identical

3. delete photos that have been taken with too small a geographic range of
 movement and mostly during  working day, or were taken more than 30 days
  apart in a year.   

## Clustering
In this project, DBSCAN is implemented to cluster the location information of
 photos. The use of DBSCAN has an advantage over k-Means since the number of
  tourist hotspots is unknown beforehand. To guarantee the final clustering
   result, a higher percentage of favorite tourist spots (containing more
    than 2% of the overall number of users) to be found, the grid search can
     be used to find the optimal combination of epsilon and minPst.
## Association Analysis
To ensure that the filtered frequent itemset is more reliable, users who have
 only uploaded photos in one location are removed before looking for the
  Association Rule, as they are not contributing to the Association Analysis.
## Visualization
