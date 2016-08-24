# Demo_recommendation
Flask-based website, featured with item browsing, shopping cart and recommendation cart

## Overview
This Demo mainly shows how the most naive recommendation engine works. Every time the customer makes a purchase, the shopping cart will
change and effectively influence the result of recommendation. 

## Recommendation Engine
As mentioned, this demo uses the most naive one. It is based on your purchase and everybody else's purchase. 
First it would construct an indicator matrix, in which 

```indicator_matrix[i][j] = occurence_together/(occurence_i+occurence_j-hit_together)```

And it would get score of each items

```score_vector = numpy.dot(indicator_matrix,purchase_vector)```

Now it is up to you how many items you want to recommend since you have the "recommendable score" of each item. For more details, please see ``` recommendation_engine.py ```

## Data
data on item images and user purchase histories are provided by [Tianchi](https://tianchi.shuju.aliyun.com/competition/index.htm)

## How to use this Demo
Once you have **flask** installed, just go to terminal and type:

```python start_engine.py```
