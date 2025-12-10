# The client's task
## Title
Skeletonize polygon in Python with computational geometry using standard libraries

## Description
We need a py file that takes a polygon as input and skeletonizes it like this:
### Example polygon
![skeletonization-overview-1|1200x1112](upload://svR8KZrNtfjBGV5Ulp3q901Xm1B.png)
### Skeletonized polygon
![skeletonization-overview-2|1200x1172](upload://8BBD2Irg2rYDs8oQUCiHkPCAqxM.png)

The algo should do something like this: 
![skeletonization stages|1200x675](upload://nNQVsKgumJI3EQfQjNAZ6RkMD0m.png)

1. skeletonize using `skeletonize` from `scikit-image` or similar
2. use a parameter to control the amount of branch pruning done (we need a lot): 
![figure-1|850x255](upload://2LTCIcHHo7OctG3ANlxUCD7ijys.png)
[researchgate.net/figure/The-skeleton-in-a-has-many-redundant-branches-To-remove-them-usually-skeleton-pruning_fig1_6576882](https://www.researchgate.net/figure/The-skeleton-in-a-has-many-redundant-branches-To-remove-them-usually-skeleton-pruning_fig1_6576882)

3. extend the ends of the skeletonized polyline so that they touch the edges of the original polygon