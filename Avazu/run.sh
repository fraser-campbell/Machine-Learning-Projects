# //VARINFO
# ../utl/vw-varinfo -c -k --passes 5 --l1 0.0000001 train.vw > varinfoREG.txt
# ../utl/vw-varinfo -c -k --loss_function logistic train.vw > varinfo.txt

# //HYPER-PARAMETER SEARCH
# ../utl/vw-hypersearch -L 1e-20 1 vw --loss_function logistic --l1 % reducedTrain.vw

# //BOOSTRAP
# vw small_test.vw --bs 10 -f outbs_model.vw --loss_function logistic
# vw -d small_test.vw --loss_function logistic -i outbs_model.vw -t -p out_predictions.txt
# vw -d small_test.vw --loss_function logistic -i out_model.vw -t -p out_predictionswithoutBS.txt
# vw test.vw -t -i avazu.model.vw -p avazu.preds.txt

# //PASSES and HOLDHOUT
# vw -d small_test.vw -f outPass_model.vw --loss_function logistic -c -k --passes 10 --holdout_period 5

# //SUBMIT
# vw test.vw -t -i avazu.model.vw -p avazu.preds.txt
# python vw_to_kaggle.py

# //FILE CREATION
# python csv_to_vw.py

# //ALL TOGETHER NOW
# vw -d reducedTrain.vw --bs 10 -f avazu.model.vw --loss_function logistic -c -k --passes 10 --holdout_period 5 -l 4.5