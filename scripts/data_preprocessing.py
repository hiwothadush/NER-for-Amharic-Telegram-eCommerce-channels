import pandas as pd
import re
import emoji
from langdetect import detect, DetectorFactory
from langdetect.lang_detect_exception import LangDetectException

class Processor:
    def drop_missing_messsage(self,df):
        df.dropna(subset='Message',inplace=True)
        return df
    
    def clean_message(self,df):
        def clean_txt(text):
            # Replace '\n', '\xa0', and '\ufeff' with a single '\n'
            cleaned_text = re.sub(r'[\n\xa0\ufeff]+', '\n', text)
            
            # Replace multiple occurrences of '\n' with a single '\n'
            cleaned_text = re.sub(r'\n+', '\n', cleaned_text)
            
            return cleaned_text
        
        df.loc[:,'Message'] = df['Message'].apply(lambda x: emoji.replace_emoji(x, replace='') if isinstance(x, str) else x)

        df.loc[:,'Message']=df['Message'].apply(clean_txt)
    
        return df['Message']
    
    def filter_amharic(self,df):
        # Define Amharic character range
        amharic_pattern = re.compile(r'[\u1200-\u137F]')

        def is_majority_amharic(text):
            # Checks if 50% or more of the characters in the message are Amharic.
            total_chars = len(text)
            if total_chars == 0:
                return False
            amharic_chars = len(amharic_pattern.findall(text))
            return (amharic_chars / total_chars) >= 0.5

        # Filter rows where the majority of the message is Amharic
        df_filtered = df[df['Message'].apply(is_majority_amharic)]

        return df_filtered