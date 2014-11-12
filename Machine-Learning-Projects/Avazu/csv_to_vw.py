# -*- coding: UTF-8 -*-

########################################################
# __Author__: Sabine Crevoisier and Fraser Campbell            #
# Kaggle competition "Display Advertising Challenge":  #
# https://www.kaggle.com/c/avazu-ctr-prediction #
# Credit: Triskelion <info@mlwave.com>          #
#  and Xueer Chen for providing the starter code for this competition, which we hereby modify.
########################################################

from datetime import datetime, date, time
from csv import DictReader

def csv_to_vw(loc_csv, loc_output, train=True):

  featuresToRemove = []
  import csv
  with open('featureRemove.csv', 'rb') as f:
      reader = csv.reader(f)
      for row in reader:
          featuresToRemove.extend(row)
  featuresToRemove = set(featuresToRemove)

  """
  Munges a CSV file (loc_csv) to a VW file (loc_output). Set "train"
  to False when munging a test set.
  TODO: Too slow for a daily cron job. Try optimize, Pandas or Go.
  """
  start = datetime.now()
  print("\nTurning %s into %s. Is_train_set? %s"%(loc_csv,loc_output,train))
  
  with open(loc_output,"wb") as outfile:
    for e, row in enumerate( DictReader(open(loc_csv)) ):
	
	  #Creating the features
      numerical_features = ""
      categorical_features = ""
      for k,v in row.items():
        if k in ["hour"]:
          dt = datetime.strptime(v[4:6] + "/" + v[2:4] + "/" + v[0:2] + " " + v[6:8], "%d/%m/%y %H")
          # create a hour of the day feature, a day of the week feature, a month of the year feature
          categorical_features += "hour_" + str(v[6:8]) + " day_" + str(dt.weekday()) + " "
        if k not in ["id","click", "hour", "device_id", "device_ip"]:
          if len(str(v)) > 0 and str(v) != "d41d8cd9": #this removes the null values
            if (k + "_" + v) not in featuresToRemove:
              categorical_features += " %s_%s " % (k,v)
            # else:
            #   print "I was not included :( and I am: " + (k + "_" + v)
			  
	  #Creating the labels		  
      if train: #we care about labels
        if row['click'] == "1":
          label = 1
        else:
          label = -1 #we set negative label to -1
        outfile.write( "%s '%s |i%s |c%s\n" % (label,row['id'],numerical_features,categorical_features) )
		
      else: #we dont care about labels
        outfile.write( "1 '%s |i%s |c%s\n" % (row['id'],numerical_features,categorical_features) )
      
	  #Reporting progress
      if e % 100000 == 0:
        print("%s\t%s"%(e, str(datetime.now() - start)))

  print("\n %s Task execution time:\n\t%s"%(e, str(datetime.now() - start)))

# csv_to_vw("train_rev2", "reducedTrain.vw",train=True)
# csv_to_vw("test_rev2", "test.vw",train=False)