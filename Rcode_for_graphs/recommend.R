# Load required library
library(recommenderlab) # package being evaluated
library(ggplot2) # For plots
 
# Load the data we are going to work with
data(MovieLense)
MovieLense
# 943 x 1664 rating matrix of class ‘realRatingMatrix’ with 99392 ratings.
 
# Visualizing a sample of this
image(sample(MovieLense, 500), main = "Raw ratings")

# Visualizing ratings
qplot(getRatings(MovieLense), binwidth = 1,
main = "Histogram of ratings", xlab = "Rating")
summary(getRatings(MovieLense)) # Skewed to the right
# Min. 1st Qu. Median Mean 3rd Qu. Max.
# 1.00 3.00 4.00 3.53 4.00 5.00

# How about after normalization?
qplot(getRatings(normalize(MovieLense, method = "Z-score")),
main = "Histogram of normalized ratings", xlab = "Rating")
summary(getRatings(normalize(MovieLense, method = "Z-score"))) # seems better
# Min. 1st Qu. Median Mean 3rd Qu. Max.
# -4.8520 -0.6466 0.1084 0.0000 0.7506 4.1280 

# How many movies did people rate on average
qplot(rowCounts(MovieLense), binwidth = 10,
main = "Movies Rated on average",
xlab = "# of users",
ylab = "# of movies rated")
# Seems people get tired of rating movies at a logarithmic pace. But most rate some.

# What is the mean rating of each movie
qplot(colMeans(MovieLense), binwidth = .1,
main = "Mean rating of Movies",
xlab = "Rating",
ylab = "# of movies")
 
# The big spike on 1 suggests that this could also be intepreted as binary
# In other words, some people don't want to see certain movies at all.
# Same on 5 and on 3.
# We will give it the binary treatment later

recommenderRegistry$get_entries(dataType = "realRatingMatrix")
# We have a few options
 
# Let's check some algorithms against each other
scheme <- evaluationScheme(MovieLense, method = "split", train = .9,
k = 1, given = 10, goodRating = 4)
 
scheme

algorithms <- list(
# `random items` = list(name = "RANDOM", param = NULL),
# `popular items` = list(name = "POPULAR", param = NULL),
 `user-based CF` = list(name = "UBCF", param = list(method = "Cosine", nn = 50)),
 `item-based CF` = list(name = "IBCF", param = list(method = "Cosine", k = 50)),
 'SVD CF' = list(name = "SVD", param=list(method = "Cosine"))
 )

# run algorithms, predict next n movies
results <- evaluate(scheme, algorithms, n=c(1, 3, 5, 10, 15, 20))
 
# Draw ROC curve
plot(results, annotate = 1:4, legend="topleft")
 
# See precision / recall
plot(results, "prec/rec", annotate=3)