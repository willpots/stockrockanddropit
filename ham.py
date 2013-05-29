# Opting for a procedural approach

from util import *
from news import News

from sklearn import svm
from sklearn import naive_bayes
from sklearn.linear_model import SGDClassifier
from sklearn.ensemble import GradientBoostingClassifier

from sklearn.metrics import *
import matplotlib.pyplot as plt
import math
from random import choice
import numpy as np
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from nltk.stem.wordnet import WordNetLemmatizer
# from output import *


class HAM(object):

    def __init__(self, model, vectorizer):
        self.model = model
        self.vectorizer = vectorizer
        self.news_market_data = False
        self.movie_review_data = False
        self.models = []
        self.pos_acc = []
        self.neg_acc = []
        self.avg_acc = []
        self.pos_prec = []
        self.neg_prec = []
        self.avg_prec = []
        self.pos_rec = []
        self.neg_rec = []
        self.avg_rec = []
        self.pos_f1 = []
        self.neg_f1 = []
        self.avg_f1 = []

    def train_test(self, name="A Model", charts=False):
        self.model.fit(self.train_vecs, self.train_labs)
        preds = self.model.predict(self.test_vecs)
        self.test_labs
        if charts is True:
            self.graph_data(self.test_labs, preds, name)
        else:
        	print "Test %s", name
            print classification_report(self.test_labs, preds,
                                        [-1, 1],
                                        ['Negative', 'Positive'])

    def graph_data(self, labs, preds, model="A Model"):

        pos_acc = accuracy_score(labs, preds)
        neg_acc = accuracy_score(labs, preds)
        avg_acc = accuracy_score(labs, preds)
        pos_prec = precision_score(labs, preds, labels=[-1, 1], pos_label=1)
        neg_prec = precision_score(labs, preds, labels=[-1, 1], pos_label=-1)
        avg_prec = precision_score(labs, preds, labels=[-1, 1], pos_label=None, average="weighted")
        pos_rec = recall_score(labs, preds, labels=[-1, 1], pos_label=1)
        neg_rec = recall_score(labs, preds, labels=[-1, 1], pos_label=-1)
        avg_rec = recall_score(labs, preds, labels=[-1, 1], pos_label=None, average="weighted")
        pos_f1 = f1_score(labs, preds, labels=[-1, 1], pos_label=1)
        neg_f1 = f1_score(labs, preds, labels=[-1, 1], pos_label=-1)
        avg_f1 = f1_score(labs, preds, labels=[-1, 1], pos_label=None, average="weighted")

        print "\n\n"
        output = '\\begin{tabular}{c | c c c c}\n'
        output += "\\textbf{%s}\t& Accuracy\t& Precision\t& Recall\t& F1 Score\t\\\\\n" % (model)
        output += "\\hline \n"
        output += "Negative\t\t& %.3f\t\t& %.3f\t\t& %.3f\t\t& %.3f\t\t\\\\\n" % (neg_acc, neg_prec, neg_rec, neg_f1)
        output += "Positive\t\t& %.3f\t\t& %.3f\t\t& %.3f\t\t& %.3f\t\t\\\\\n" % (pos_acc, pos_prec, pos_rec, pos_f1)
        output += "Average \t\t& %.3f\t\t& %.3f\t\t& %.3f\t\t& %.3f\t\t\\\\\n" % (pos_acc, avg_prec, avg_rec, avg_f1)
        output += "\\end{tabular}"
        print output



        self.models.append(model)
        self.pos_acc.append(pos_acc)
        self.neg_acc.append(neg_acc)
        self.avg_acc.append(avg_acc)
        self.pos_prec.append(pos_prec)
        self.neg_prec.append(neg_prec)
        self.avg_prec.append(avg_prec)
        self.pos_rec.append(pos_rec)
        self.neg_rec.append(neg_rec)
        self.avg_rec.append(avg_rec)
        self.pos_f1.append(pos_f1)
        self.neg_f1.append(neg_f1)
        self.avg_f1.append(avg_f1)

    def plot_charts(self):
        plot_chart(self.avg_acc, self.models, name="accuracy", title="Accuracy", yaxis="Accuracy (%)")
        plot_chart_3(self.pos_prec, self.neg_prec, self.avg_prec, self.models, name="precision", title="Precision", yaxis="Precision (%)")
        plot_chart_3(self.pos_rec, self.neg_rec, self.avg_rec, self.models, name="recall", title="Recall", yaxis="Recall (%)")
        plot_chart_3(self.pos_f1, self.neg_f1, self.avg_f1, self.models, name="f1", title="F1 Score", yaxis="F1 Score (%)")

    def summary_chart(self):
        print "\n\n"
        output = '\\begin{tabular}{c | c c c c}\n'
        output += "\\textbf{%s}\t& Accuracy\t& Precision\t& Recall\t& F1 Score\t\\\\\n" % ("Summary")
        output += "\\hline \n"
        for i in range(len(self.models)):
            output += "%s\t\t& %.3f\t\t& %.3f\t\t& %.3f\t\t& %.3f\t\t\\\\\n" % (self.models[i], self.avg_acc[i], self.avg_prec[i], self.avg_rec[i], self.avg_f1[i])
        output += "\\end{tabular}"
        print output

    def print_doc_feats(self):
        for feature in self.vectorizer.get_feature_names():
            print feature

    def prep_news_data(self):
        if not self.news_market_data:
            print 'Preparing news and stock data...\n'
            news = News('Resources/articles.db')
            raw = news.db_articles()
            train_raw, test_raw = divide_list_by_ratio(raw) # prep_news_data returns a tuple of vectors, labels
            self.train_vecs, self.train_labs = self.prep_news_articles(train_raw, fit=True)
            self.test_vecs, self.test_labs = self.prep_news_articles(test_raw)
            self.news_market_data = True
            self.movie_review_data = False

    def prep_news_articles(self, raw_docs, fit=False):
        docs = self.filter_old_news(raw_docs)
        doc_labels = self.news_labels(docs)
        doc_bodies = map(lambda x: x[4], docs) # 3 is title, 4 is body
        if fit:
            self.vectorizer.fit(doc_bodies, doc_labels)
        doc_vectors = self.vectorizer.transform(doc_bodies)
        if isinstance(self.model, naive_bayes.GaussianNB): # check if need dense vectors
            doc_vectors = doc_vectors.toarray()
        return doc_vectors, doc_labels

    def prep_reviews_data(self): # messy code to test classifier with movie reviews
        if not self.movie_review_data:
            print 'Preparing movie reviews...\n'
            from nltk.corpus import movie_reviews
            docs = [movie_reviews.raw(fileid) 
                    for category in movie_reviews.categories() 
                    for fileid in movie_reviews.fileids(category)]

            process = lambda x: 1 if x == 'pos' else -1
            labels = [process(category)
                    for category in movie_reviews.categories() 
                    for fileid in movie_reviews.fileids(category)]

            docs, labels = double_shuffle(docs, labels)
            training, testing = divide_list_by_ratio(docs)
            self.train_labs, self.test_labs = divide_list_by_ratio(labels)

            train_vecs = self.vectorizer.fit_transform(training)
            test_vecs = self.vectorizer.transform(testing)

            if isinstance(self.model, naive_bayes.GaussianNB):
                train_vecs = train_vecs.toarray()
                test_vecs = test_vecs.toarray()

            self.train_vecs = train_vecs
            self.test_vecs = test_vecs

            self.movie_review_data = True
            self.news_market_data = False

    def filter_old_news(self, docs):
        fn = lambda d: bool(db_symbol_change(d[2], datetime.strptime(d[0], '%Y-%m-%d')))
        return filter(fn, docs)

    def news_labels(self, corpus):
        ''' Returns a numpy array of integer labels that correspond to the corpus docs.
            1 for a doc about a stock that happened to go up, -1 for a doc about a stock that went down. Removes data entry if no stock data.
         '''
        labels = []
        for doc in corpus:
            date = datetime.strptime(doc[0], '%Y-%m-%d')
            change = db_symbol_change(doc[2], date)
            if change:
                label = change/math.fabs(change)  # => 1 or -1
                labels.append(label)
        return np.array(labels, dtype=np.int8)

    def advanced_train_test():
        self.model.fit(self.train_vecs, self.train_labs)
        preds = model.predict(self.test_vecs)
        total = len(preds)
        correct = 0.0
        up_count = 0
        down_count = 0
        for pred, act in zip(preds, self.test_labs):
            if pred == 1:
                up_count += 1
            elif pred == -1:
                down_count += 1
            if pred == act:
                correct += 1
        acc = correct/total
        print "%d/%d Correct" % (correct, total)
        print "Accuracy: %.2f" % acc
        print "Predictions: %d UP, %d DOWN" % (up_count, down_count)
        return acc
>>>>>>> 7570875e948014a1e5921d292902569b750e17ee

class RandomClassifier(object):
	def fit(self, A, B):
		pass
	def predict(self, A):
		return [choice([-1, 1]) for i in range(len(A))]

# class DocPreprocessor(object):
#   def __init__(self):
#       self.wnl = WordNetLemmatizer()

#   def preprocess(self, doc):
#       def process_word(word):
#           word = word.lower()
#           word = self.wnl.lemmatize(word)
#           return word
#       return ' '.join(map(process_word, doc.split()))


def plot_chart(results, labels, name="figure", title=None, yaxis=None):

	N = len(results)

	ind = np.arange(N)
	width = 0.35

	fig = plt.figure(facecolor="#ffffff")
	ax = fig.add_subplot(111)
	rects1 = ax.bar(ind + (width / 4), results, width, color='#6AA8EB')

	# add some
	ax.set_ylabel(yaxis, family="serif")
	ax.set_title(title, family="serif")
	ax.set_xticks(ind + (width * 3 / 4))
	ax.set_xticklabels(labels, family="serif", fontname="Computer Modern", size="x-small", rotation=14)

	plt.savefig(name + '.png')

	# plt.show()


def plot_chart_3(results, results2, results3, labels, name="figure", title=None, yaxis=None):

	N = len(results)

	ind = np.arange(N)
	width = 0.30

	fig = plt.figure(facecolor="#ffffff")
	ax = fig.add_subplot(111)
	pos = ax.bar(ind, results, width, color='#C7430A')
	neg = ax.bar(ind + width, results2, width, color='#456772')
	avg = ax.bar(ind + 2 * width, results3, width, color='#378F00')

	# add some
	ax.set_ylabel(yaxis, family="serif")
	ax.set_title(title, family="serif")
	ax.set_xticks(ind + 3 * width / 2)
	ax.set_xticklabels(labels, family="serif", fontname="Computer Modern", size="x-small", rotation=14)

	ax.legend((pos, neg, avg), ('Positive', 'Negative', 'Average'))

	plt.savefig(name + '.png')
