# The client's task
## Title
Skeletonize polygon in Python with computational geometry using standard libraries

## Description
We need a py file that takes a polygon as input and skeletonizes it.

The algo should do something like this: 
1. skeletonize using `skeletonize` from `scikit-image` or similar
2. use a parameter to control the amount of branch pruning done (we need a lot): 
`https://www.researchgate.net/figure/The-skeleton-in-a-has-many-redundant-branches-To-remove-them-usually-skeleton-pruning_fig1_6576882`
3. extend the ends of the skeletonized polyline so that they touch the edges of the original polygon