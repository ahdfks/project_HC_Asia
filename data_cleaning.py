import pandas as pd
import numpy as np

pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 30)
df = pd.read_csv("hc_companies.csv")

df

#keep company name only
minus_abbr = df['name'].apply(lambda x: x.lower().replace('co.,ltd.','').replace('co.,ltd','')
                                                 .replace('inc.','').replace(', inc.','')
                                                 .replace(',',''))

minus_cityorprovince = minus_abbr.apply(lambda x: x.lower().replace('beijing ','').replace('jiangsu ','')
                                                        .replace('shanghai ','').replace('shenzhen ','')
                                                        .replace('guangzhou ','').replace('guangdong ','')
                                                        .replace('chengdu ','').replace('zhuhai ','')
                                                        .replace('wuhan ','').replace('hangzhou ',''))
df['company_name'] = minus_cityorprovince

#remove duplicated companies
df.drop_duplicates(subset = ['company_name'], keep = False, inplace = True) 
df.company_name.value_counts()

#calculate age of company from found year
from datetime import datetime

df['age_of_company'] = df.founded_on.dropna().apply(lambda x: datetime.now().year-x)

#replace NaN with null
df['specialities'] = df['specialities'].fillna('null') 
df['headquarter_province'] = df['headquarter_province'].fillna('null') 
df = df.ffill()

#creat a function: separate multi strings to each row and keep the original index
def explode_str(df, col, sep):
    s = df[col]
    i = np.arange(len(s)).repeat(s.str.count(sep) + 1) #evenly spaced strings
    return df.iloc[i].assign(**{col: sep.join(s).split(sep)}) #return separated str using unpacked dictionary

#use that function to create a new specialities col filled with separated string
df1 = explode_str(df, 'specialities', ',') 
df1['specialities']

#convert spec col into a list to classify therapeutic areas later
specialities_list = df1['specialities'].to_list()

#creat therapeutic categories and [matches]: market research subjects covered by FMR)
therapeutic_areas = [
('oncology', ['oncology', 'anti-tumor', 'cancer', 'breast', 'ovarian', 'prostate tumours', 
            'HCC', 'colorectal', 'renal cell carcinoma', 'NSCLC', 'thyroid', 'head and neck', 
            'pancreatic cancer', 'tumor']),
('rare_diseases', ['rare diseases', 'orphan diseases','familial chylomicronemia syndrome', 
                'familial partial lipodystrophy', 'rare leukemia', 'rare bleeding disorders', 
                'sickle cell anemia', 'squamous cell', 'orphan drug']),
('dermatology', ['dermatology', 'acne', 'atopic dermatitis', 'contact dermatitis', 
               'hives', 'psoriasis', 'rosacea', 'shingles', 'skin cancer', 'skin care']),
('cardiology', ['cardiology', 'cardiovascular', 'myocardial infarction', 
              'cerebrovascular disease', 'CVD', 'hypertension', 'cardio metabolic syndrome', 
              'atherosclerotic vascular disease', 'cardiac', 'coronary heart disease']),
('gastroenterology', ['gastroenterology', 'colorectal cancer', 'colon polyps', 
                    'iron deficiency', 'crohn’s disease', 'IBS', 'IBD', 
                    'ulcerative colitis', 'diarrhoea', 'laxatives', 'bowel', 
                    'probiotics', 'gastrointestinal', 'GI']),
('immunology', ['immunology', 'allergy', 'immunohematology', 'blood disorders', 'immunotherapy',
              'antibody tests', 'immunodeficiency', 'NEMO deficiency syndrome', 'autoimmune', 
              'cellular and complement deficiencies', 'transplantation', 'autoimmune disease',
              'tumor immunology', 'cancer immunology', 'vaccines', 'influenza vaccines',
              'immuno-oncology', 'rheumatism']),
('neurology', ['CNS', 'central nervous system', 'Alzheimer', "Parkinson", 'neurological',
               'senile dementia']),
('orthopedics', ['orthopedics', 'osteoporosis', 'rheumatoid arthritis', 'hyaluronic acid', 
               'spinal disorder', 'arthroplasty', 'arthritis', 'fibromyalgia', 
               'spondylolysis', 'skeletal dysplasia', 'scoliosis']),
('pulmonology', ['respiratory', 'pulmonology', 'asthma', 'tuberculosis']),
('infectious_diseases', ['infectious diseases', 'HIV', 'NASH', 'anti-HIV/AIDS', 
                         'anti-infective']),
('hematology', ['hematology', 'hemodialysis']),
('rheumatology', ['rheumatology']),
('endocrinology', ['endocrinology']),
('ophthalmology', ['ophthalmology', 'optometry', 'optical', 'ophthalmic']),
('diabetes', ['diabetes', 'blood glucose', 'diabetic']),
('ENT', ['ENT', 'otorhinolaryngology']),
('pain_management', ['pain_management', 'anethesia', 'narcotic analgesic', 'sedative', 'antagonist']),
('urology', ['urology', 'urinalysis'])]

#classify therapeutic areas from specialities list above
def classify(specialities_list):
  for category, matches in therapeutic_areas:
    if any(match in specialities_list for match in matches):
      return category
  return None

df1['therapeutic_area'] = df1['specialities'].apply(lambda x: x.lower()).apply(classify)

#keep companies who covered our therapeutic areas
df1 = df1.dropna(subset=['therapeutic_area'])

#remove duplicated thera areas by company level
df1 = df1.drop_duplicates(subset=['therapeutic_area', 'company_name'], keep='last')

#clean df1
df1.rename({'lh_id': 'No.', 'headquarter_country': 'HQ', 'founded_on': 'found_yr',
           'headquarter_city': 'city','headquarter_province': 'province'}, axis=1, inplace=True)

df1_out = df1.drop(columns=['id','public_id','logo','phone','tagline',
                          'staff_count_range_start','staff_count_range_end',
                          'headquarter_line1','headquarter_line2','headquarter_postal_code',
                          'tags'], axis=0)
df1_out.astype({"staff_count": int, "follower_count": int, "found_yr" : int, "age_of_company" : int})

df1_out.to_csv('therapeutic_areas_cleaned.csv', float_format="%.0f",index=False)

#add specialities length col to get detailed spec
df['spec_len'] = df['specialities'].apply(lambda x: len(x))

#add col: products certificated by EMA or FDA
df["certification_by"] = df["description"].map(lambda x: "EMA" if "EMA" in x
                                                         else "CE(for medical devices)" if "CE" in x 
                                                         else "FDA" if "FDA" in x 
                                                         else "n/a")
df.certification_by.value_counts()                                                      

#add description length col to get in-depth desc
df['desc_len'] = df['description'].apply(lambda x: len(x))

#clean df
df.rename({'lh_id': 'No.', 'headquarter_country': 'HQ', 'founded_on': 'found_yr',
           'headquarter_city': 'city','headquarter_province': 'province'}, axis=1, inplace=True)

df_out = df.drop(columns=['id','public_id','logo','phone','tagline',
                          'staff_count_range_start','staff_count_range_end',
                          'headquarter_line1','headquarter_line2','headquarter_postal_code',
                          'tags'], axis=0)

df_out.astype({"staff_count": int, "follower_count": int, "found_yr" : int, "age_of_company" : int})

df_out.to_csv('hc_companies_cleaned.csv', float_format="%.0f",index=False)




