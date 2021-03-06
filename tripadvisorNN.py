
import tensorflow as tf

import numpy as np

feature_names = ['Usercountry', 'Nrreviews','Nrhotelreviews','Helpfulvotes','Periodofstay',
           'Travelertype','Pool','Gym','Tenniscourt','Spa','Casino','Freeinternet',
                  'Hotelname','Hotelstars','Nrrooms','Usercontinent','Memberyears',
           'Reviewmonth','Reviewweekday']
FIELD_DEFAULTS = [[0], [0], [0], [0], [0],
                  [0], [0], [0], [0], [0],
                  [0], [0], [0], [0], [0],
                  [0], [0], [0], [0], [0]]

def parse_line(line):
    parsed_line = tf.decode_csv(line, FIELD_DEFAULTS)
    tf.Print(input_=parsed_line , data=[parsed_line ], message="parsed_line ")
    tf.Print(input_=parsed_line[4], data=[parsed_line[4]], message="score")
    label = parsed_line[4]
    del parsed_line[4]
    tf.Print(input_=parsed_line[1], data=[parsed_line[1]], message="Usercountry")
    tf.Print(input_=parsed_line[2], data=[parsed_line[2]], message="Nrreviews")
    tf.Print(input_=parsed_line[3], data=[parsed_line[3]], message="Nrhotelreviews")
    tf.Print(input_=parsed_line[5], data=[parsed_line[5]], message="Helpfulvotes")
    tf.Print(input_=parsed_line[6], data=[parsed_line[6]], message="Periodofstay")
    tf.Print(input_=parsed_line[7], data=[parsed_line[7]], message="Travelertype")
    tf.Print(input_=parsed_line[8], data=[parsed_line[8]], message="Pool")
    tf.Print(input_=parsed_line[9], data=[parsed_line[9]], message="Gym")
    tf.Print(input_=parsed_line[10], data=[parsed_line[10]], message="Tenniscourt")
    tf.Print(input_=parsed_line[11], data=[parsed_line[11]], message="Spa")
    tf.Print(input_=parsed_line[12], data=[parsed_line[12]], message="Casino")
    tf.Print(input_=parsed_line[13], data=[parsed_line[13]], message="Freeinternet")
    tf.Print(input_=parsed_line[14], data=[parsed_line[14]], message="Hotelname")
    tf.Print(input_=parsed_line[15], data=[parsed_line[15]], message="Hotelstars")
    tf.Print(input_=parsed_line[16], data=[parsed_line[16]], message="Nrrooms")
    tf.Print(input_=parsed_line[17], data=[parsed_line[17]], message="Usercontinent")
    tf.Print(input_=parsed_line[18], data=[parsed_line[18]], message="Memberyears")
    '''tf.Print(input_=parsed_line[19], data=[parsed_line[19]], message="Reviewmonth")
    tf.Print(input_=parsed_line[20], data=[parsed_line[20]], message="Reviewweekday")'''
    features = parsed_line  
    d = dict(zip(feature_names, features))
    print ("dictionary", d, " label = ", label)    
    return d, label
     
def csv_input_fn(csv_path, batch_size):
    dataset = tf.data.TextLineDataset(csv_path)
    dataset = dataset.map(parse_line)
    dataset = dataset.shuffle(1000).repeat().batch(batch_size)
    return dataset

Usercountry = tf.feature_column.numeric_column("Usercountry")
Nrreviews = tf.feature_column.numeric_column("Nrreviews")
Nrhotelreviews = tf.feature_column.numeric_column("Nrhotelreviews")
Helpfulvotes = tf.feature_column.numeric_column("Helpfulvotes")
Periodofstay = tf.feature_column.numeric_column("Periodofstay")
Travelertype = tf.feature_column.numeric_column("Travelertype")
Pool = tf.feature_column.numeric_column("Pool")
Gym = tf.feature_column.numeric_column("Gym")
Tenniscourt = tf.feature_column.numeric_column("Tenniscourt")
Spa = tf.feature_column.numeric_column("Spa")
Casino = tf.feature_column.numeric_column("Casino")
Freeinternet = tf.feature_column.numeric_column("Freeinternet")
Hotelname = tf.feature_column.numeric_column("Hotelname")
Hotelstars = tf.feature_column.numeric_column("Hotelstars")
Nrrooms = tf.feature_column.numeric_column("Nrrooms")
Usercontinent = tf.feature_column.numeric_column("Usercontinent")
Memberyears = tf.feature_column.numeric_column("Memberyears")
Reviewmonth = tf.feature_column.numeric_column("Reviewmonth")
Reviewweekday = tf.feature_column.numeric_column("Reviewweekday")

feature_columns = [Usercountry, Nrreviews,Nrhotelreviews,Helpfulvotes,Periodofstay,
         Travelertype,Pool,Gym,Tenniscourt,Spa,Casino,Freeinternet,Hotelname,Hotelstars,Nrrooms,Usercontinent,Memberyears,Reviewmonth,Reviewweekday]

classifier=tf.estimator.DNNClassifier(
    feature_columns=feature_columns,  
    hidden_units=[10, 10], 
    n_classes=6,
    model_dir="/tmp")
batch_size = 100
classifier.train(
    steps=100,
    input_fn=lambda : csv_input_fn("/home/walker/tripAdvisorFL.csv", batch_size))

features = {'Usercountry': np.array([233]), 'Nrreviews': np.array([11]),'Nrhotelreviews': np.array([4]),'Helpfulvotes': np.array([13]),'Periodofstay': np.array([582]),'Travelertype': np.array([715]),'Pool' : np.array([0]),'Gym' : np.array([1]),'Tenniscourt' : np.array([0]),'Spa' : np.array([0]),'Casino' : np.array([0]),'Freeinternet' : np.array([1]),'Hotelname' : np.array([3367]),'Hotelstars' : np.array([3]),'Nrrooms' : np.array([3773]),'Usercontinent' : np.array([1245]),'Memberyears' : np.array([9]),'Reviewmonth' : np.array([730]),'Reviewweekday' : np.array([852])}

label = np.array([5])

def test_input_fn():
    return features, label

def predict_input_fn():   
    return features 

'''accuracy_score = classifier.evaluate(input_fn=test_input_fn)["accuracy"]

print("\nTest Accuracy: {0:f}\n".format(accuracy_score))'''

predict = classifier.predict(input_fn=predict_input_fn)

expected = [5]

prediction = classifier.predict(input_fn=predict_input_fn)

for pred_dict, expec in zip(prediction, expected):
    class_id = pred_dict['class_ids'][0]
    probability = pred_dict['probabilities'][class_id]
    print ('class_ids=', class_id, ' probabilities=',  probability)


