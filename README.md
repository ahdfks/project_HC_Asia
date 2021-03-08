# Healthcare Market in the Greater China Region: project overview(https://github.com/ahdfks/project_HC_Asia)
## ➢ Created a dashboard to understand the healthcare market in mainland China, Hongkong, Taiwan and South Korea
## ➢ Data collection: scraped over 1000 companies from LinkedIn using linked helper scraper
## ➢ Data cleaning: cleand raw data and derived a file to prioritize companies covering target therapeutic areas
## ➢ EDA: parsed string data of each company's specialities to quantify the value they put on each therapeutic area
## ➢ Data visualisation: built a dashboard to understand companies/therapeutic areas ditribution by each specific level

# Code and Resources used
## Python version: 3.8.5
## Packages: pandas, numpy, seaborn, matplotlib.pyplot
## Tableau: 2020.4

# LinkedIn company profile scraping
## Scraped 1000 companies in pharmaceuticals, biotechnology, and medical device industry in the Greater China Region
## With each company profile, we got the following: 
## •	 Company ID
## •	 Company name
## •	 Industry
## •	 Type of ownership
## •	 Founded year
## •	 Company description: with FDA, CE, EMA and other international certifications
## •	 HQ country: China, Taiwan, South Korea
## •	 HQ city level
## •	 HQ province level
## •	 Specialities: immuno-oncology, CNS, probiotics, cardiovascular, diabetes, orthopedics etc
## •	 Profile url
## •	 Website
## •	 Phone
## •	 Staff counts
## •	 Follower counts

# Data Cleaning
After scraping the data, it is necessary to clean it up. 
I made the following changes and created the following variables:
•	 Simplified name by removing city and business structure abbr out of company name text
•	 Transformed founded year into age of company
•  Created 18 therapeutic categories and matches list
o  Oncology
o  Rare diseases
o  Dermatology
o  Cardiology
o  Gastroenterology
o  Immunology
o  Neurology
o  Orthopedics
o  Pulmonology
o  Infectious diseases
o  Hematology
o  Rheumatology
o  Endocrinology
o  Ophthalmology
o  Diabetes
o  ENT
o  Pain management
o  Urology
•  Made a function to separate multi strings in specialities column and then classify therapeutic areas list(above) from each separated speciality
•  Added a therapeutic areas file by keeping companies who covered therapeutic areas above
•  Removed duplicated therapeutic areas by company level
•  Added specialities length col to get detailed information
•  Made a column for if intl certifications were listed in the company description column
o  CE
o  FDA
o  EMA
•	 Added description length column for in-depth information
•	 Replaced NaN with null

# Exploratory Data Analysis
Created the distributions of cleaned data and the value counts for the various categorical variables
Below are a few highlights from the pivot tables:
