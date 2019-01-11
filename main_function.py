from abnormal_enterprise import SVM_model
from abnormal_enterprise import test_model
from abnormal_enterprise import naive_bayes

if __name__ == '__main__':
    a = input("enter\n")

    if a == "accuracy":
        w = input("enter_model:\n")
        if w == "bayes":
            test_model.test_function().test_model_function_naive()
        if w == "svm":
            test_model.test_function().test_model_function_svm()

    if a=="model":
        w = input("enter_model:\n")
        if w == "svm":
            SVM_model.svm_model().svm_model()
        if w == "bayes":
            naive_bayes.naive_bayes().naive_bayes_model()

    if a=="single":
        """单个输入企业的ID 得到企业的异常与否"""
        company_ID=input("enter_company_ID:")
        test_model.test_function(company_ID=company_ID).single_enterprise_test(company_ID)
