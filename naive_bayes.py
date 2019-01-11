from abnormal_enterprise import value_preprocess
from sklearn.naive_bayes import GaussianNB
import numpy,json
from matplotlib import pyplot as plt
from sklearn.externals import joblib
from sklearn.model_selection import ShuffleSplit
from sklearn.model_selection import learning_curve

class naive_bayes:
    """deploy two model including SVM and naive bayes, compare their accuracy in test_model.py"""
    def __init__(self,times="yes",sql_model="select * from pingantest.RA_MER_BASE_QYNB_X40W27",dict_file='27_dict_bayes.json'):
        self.times=times
        self.sql=sql_model
        self.dict_file=dict_file
        self.model='Gaussian__nb_Bayes_one_1226.model'

    def data_for_model(self):
        data=value_preprocess.value_preprocess(sql=self.sql).parameter_transfer()
        data=numpy.array(data)
        label_train=data[:,-1]
        feature_train=numpy.delete(data[:,:-1],2,1)
        dict_a=self.calculate_probability(feature_train)
        file_w = open(self.dict_file, 'w', encoding='utf-8')
        list_a=[dict_a]
        json.dump(list_a,file_w)
        feature_train=self.convert_probability(feature_train,dict_a)
        label_train,feature_train=numpy.array(label_train),numpy.array(feature_train)
        return label_train,feature_train

    def naive_bayes_model(self):
        label_train,feature_train=self.data_for_model()[0],self.data_for_model()[1]
        # cv = ShuffleSplit(n_splits=20, test_size=0.05, random_state=0)
        bayes_classifer = GaussianNB()
        # self.convergence_line(bayes_classifer, x=feature_train, y=label_train.astype('int'), cv=cv)
        bayes_model = bayes_classifer.fit(feature_train, label_train.astype('int'))
        joblib.dump(bayes_model, self.model)
        # plt.show()

    def calculate_probability(self,numpy_a):
        each_para,each_value={},{}
        """to get its probability"""
        for item in numpy_a:
            for i in range(len(item)):
                if str(item[i])+'_'+str(i) not in each_para.keys():
                    each_para[str(item[i])+'_'+str(i)]=len([x for x in numpy_a[:,i] if x==item[i]])/len([x for x in numpy_a[:,i]])
                    # each_value[item[i]]=len([x for x in numpy_a[:,i] if x==item[i]])/len([x for x in numpy_a[:,i]])
                    """add operation"""
        return each_para

    def convert_probability(self,numpy_a,dict):
        for item in numpy_a:
            for j in range(len(item)):
                try:
                    item[j]=dict.get(str(item[j])+"_"+str(j))
                except Exception as e:
                    continue
        return numpy_a

    def convergence_line(self,model_a,x,y,cv=None,title="learning_curve",ylim=(0.70,0.90),njobs=4):
        plt.figure()
        plt.title(title)
        if ylim is not None:
            plt.ylim(*ylim)
        plt.xlabel("Training examples")
        plt.ylabel("Score")
        train_sizes=numpy.linspace(.1, 1.0, 20)
        train_sizes, train_scores, test_scores = learning_curve(model_a, x, y,cv=cv,train_sizes=train_sizes,n_jobs=njobs)
        train_scores_mean = numpy.mean(train_scores, axis=1)
        train_scores_std = numpy.std(train_scores, axis=1)
        test_scores_mean = numpy.mean(test_scores, axis=1)
        test_scores_std = numpy.std(test_scores, axis=1)
        plt.grid()
        plt.fill_between(train_sizes, train_scores_mean - train_scores_std,train_scores_mean + train_scores_std, alpha=0.1,color="r")
        plt.fill_between(train_sizes, test_scores_mean - test_scores_std,test_scores_mean + test_scores_std, alpha=0.1, color="g")
        plt.plot(train_sizes, train_scores_mean, 'o-', color="r",label="Training score")
        plt.plot(train_sizes, test_scores_mean, 'o-', color="g",label="Cross-validation score")
        plt.legend(loc="best")
        return plt



