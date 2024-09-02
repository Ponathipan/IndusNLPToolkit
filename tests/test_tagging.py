import pandas as pd

# Assuming df is your DataFrame
#df1 = pd.read_csv('/mnt/c/indus-phase-2/phase-2-fine-tuning/Vedant/translated/convo_wildchat5.csv')
#print(df1)
#print(df1.head())


df2 = pd.read_csv('/mnt/e/indus-phase-2/phase-2-fine-tuning/Ashmi/translated/conv_LDJnr_Puffin_train_hi_translated.csv',escapechar="\\")

#print(df2)
#print(df2.head())

df2.to_csv('conv_LDJnr_Puffin_train_hi_translated_modified.csv', index=False)
#import pandas as pd
# Set the display options to ensure the full content is printed
#pd.set_option('display.max_colwidth', None)



#df3 = pd.read_csv('/mnt/c/indus-phase-2/phase-2-fine-tuning/Vedant/cleaned/convo_wildchat_4_cleaned.csv')

#print(df3)
