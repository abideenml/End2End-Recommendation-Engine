import pandas as pd
from sklearn import preprocessing
label_encoder = preprocessing.LabelEncoder()
data=pd.read_csv('Updated.csv')
data['Q1'] = label_encoder.fit_transform(data['Q1'])
data['Q2'] = label_encoder.fit_transform(data['Q2'])
data['Q3'] = label_encoder.fit_transform(data['Q3'])
data['Q4'] = label_encoder.fit_transform(data['Q4'])
data['Q5'] = label_encoder.fit_transform(data['Q5'])
data['Q6'] = label_encoder.fit_transform(data['Q6'])
data['Q7'] = label_encoder.fit_transform(data['Q7'])
data['Q8'] = label_encoder.fit_transform(data['Q8'])
data['Q9'] = label_encoder.fit_transform(data['Q9'])
data['Q10'] = label_encoder.fit_transform(data['Q10'])
data['Q11'] = label_encoder.fit_transform(data['Q11'])
data['Q12'] = label_encoder.fit_transform(data['Q12'])
q1=data.Q1.values
q2=data.Q2.values
q3=data.Q3.values
q4=data.Q4.values
q5=data.Q5.values
q6=data.Q6.values
q7=data.Q7.values
q8=data.Q8.values
q9=data.Q9.values
q10=data.Q10.values
q11=data.Q11.values
q12=data.Q12.values
similarity=[]
def findsimilarity(a):
    avg_a_q2 = sum(a[:40]) / len(a[:40])
    print(sum(a[:40]))
    print(len(a[:40]))
    print(avg_a_q2)
    avg_b_q2 = sum(a[40:82]) / len(a[40:82])
    print(avg_b_q2)
    print(round((1 - abs(avg_a_q2 - avg_b_q2)) * 100,2))
    similarity.append(round((1 - abs(avg_a_q2 - avg_b_q2)) * 100,2))
# for i in [q1,q2,q3,q4,q5,q6,q7,q8,q9,q10,q11,q12]:
#     findsimilarity(i)
# print(similarity)
findsimilarity(q3)
# questions = ['Q1-Did you feel that counselling and guidance by faculty members improved your academic performance?','Q2-Do you think counselling and guidance by faculty members is required to cope difficult schedule of medical education?','Q3-Did vigilance of faculty members help you in improving attendance % during session?','Q4-Did vigilance of faculty members help you in improving grades during routine module exams?','Q5-Guidance and training  by faculty members  regarding professional written  exam (seq & mcq) and viva helped you a lot?','Q6- Do you think that personal experiences of faculty members( shared with students  regarding studies and exams ) guide you a lot?','Q7-Did counselling  and guidance of faculty member help you regarding  time management?','Q8-Did counselling of faculty member help you in solving your day to day Social problems?','Q9- Did counselling of faculty member help you in solving your day to day domestic problems?','Q10- Did you find your medical teacher guiding you whenever you get detracked in studies?','Q11- Did  guidance of your teachers  help you in scoring (position, distinction )in professional or module exams?','Q12-Career Counselling of medical students should be practiced in medical colleges?']
#
# group_A_yes = []
# group_B_yes = []
# group_A_no = []
# group_B_no = []
# def count(a):
#     a_count_yes=0
#     b_count_yes=0
#     for i in a[:40]:
#         if i == 1:
#             a_count_yes = a_count_yes+1
#     for i in a[40:82]:
#         if i == 1:
#             b_count_yes = b_count_yes+1
#     a_count_no=40-a_count_yes
#     b_count_no=42-b_count_yes
#     group_A_yes.append(a_count_yes)
#     group_B_yes.append(b_count_yes)
#     group_A_no.append(a_count_no)
#     group_B_no.append(b_count_no)
#
# for i in [q1,q2,q3,q4,q5,q6,q7,q8,q9,q10,q11,q12]:
#     count(i)
# print(group_A_yes,group_A_no,group_B_yes,group_B_no)
#
# results = pd.DataFrame(questions,columns = ['Questions'])
# results['Group A Yes'] = group_A_yes
# results['Group A No'] = group_A_no
# results['Group B Yes'] = group_B_yes
# results['Group B No'] = group_B_no
# results['Correlation between A and B'] = similarity
# results.to_csv('Results.csv',index=False)
# print(results.head())
#
