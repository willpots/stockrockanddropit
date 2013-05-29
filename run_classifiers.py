from ham import HAM, RandomClassifier
from sklearn.svm import LinearSVC, SVC
from sklearn.naive_bayes import MultinomialNB, BernoulliNB, GaussianNB
from sklearn.tree import DecisionTreeClassifier
from sklearn.linear_model import SGDClassifier
from sklearn.ensemble import GradientBoostingClassifier, RandomForestClassifier
# import sklearn.ensemble.AdaBoostClassifier as abc
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer

model = GaussianNB()
vectorizer = TfidfVectorizer(stop_words='english', max_features=10000, analyzer='word', ngram_range=(1, 3), token_pattern=ur'\b\w+\b', min_df=1)

ham = HAM(model, vectorizer)
# ham.prep_reviews_data()
ham.prep_news_data()
# ham.print_doc_feats()

charts = False
print '\nTesting all with Idf Bag of Words\n'
# ham.vectorizer = CountVectorizer(stop_words='english', max_features=10000, analyzer='word', ngram_range=(1,3), token_pattern=ur'\b\w+\b', min_df=1)

ham.model = RandomClassifier()
ham.train_test('Random', charts)

ham.model = GaussianNB()
ham.train_test('Gaussian NB', charts)

ham.model = SVC(kernel='linear')
ham.train_test('Linear SVM', charts)

ham.model = SVC(kernel='rbf')
ham.train_test('Radial SVM', charts)

ham.model = MultinomialNB()
ham.train_test('Multinomial Naive Bayes', charts)

ham.model = BernoulliNB(alpha=1.0, binarize=0.0, class_prior=None, fit_prior=True)
ham.train_test('Bernoulli Naive Bayes', charts)

ham.model = SGDClassifier(loss="hinge", penalty="l2")
ham.train_test('Stochastic Gradient Descent', charts)

ham.model = GradientBoostingClassifier()#n_estimators=100, learning_rate=1.0, max_depth=1, random_state=0)
ham.train_test('Gradient Boosting Classifier', charts)

ham.model = RandomForestClassifier(n_estimators=100)
ham.train_test('Random Forest Classifier', charts)

ham.model = DecisionTreeClassifier()
ham.train_test('Decision Tree Classifier', charts)

if charts:
    ham.summary_chart()
    ham.plot_charts()
