# Software Requirements Specification for caries_detection gui

## Table of Contents
- Descriptions
- Requirements
- Functionality not required
- Limitations
- Data dictionary


## Descriptions
 This program act as the gui front for the caries detection algorithum. It will inform patient of their caries condition based on uploaded pictures of their teeth. The program will also ask patient question and inform them of their caries risk status and what can be done. Lastly, there will be a feature to open up zocdoc on browser for patient to look for available dentist if caries is detected, or book appointment for check up if none are detected. 

## Requirements


## Input form
- Contain algorithm widget to upload pictures
- Contain caries risk assessment widget
- Submit button to produce result window
- Reset button to reset input form
### Basic information
- Ask for Name
- Ask for DOB and determine age

### Front end for caries risk detection algorithm
- Make a form for patient to enter all relevant data
- Allow upload of the picture of teeth in jpg, connect to caries detection algorithum to determine number and presence of caries. Output of the algorithum should be jpg picture with caries circled, # of caries presence.

### Caries risk detection
Caries risk detection by asking patient simple question
- The caries risk assessment is based on ADA caries risk assessment form for those age>6. 
- The form used in the gui omit questions that cannot be answered by patient themslves, ex. unusual tooth morphology or presence of caries, interproximal restorations)
- (possible feature) if user age < 6, omit caries risk detection
- Question will be presented in widget with options for user to pick from.
- In the result page, if user is determined to be higher risk, patient education about the section will be printed and displayed. 
- (possible features) When hovered over the question, patient education bubble will pop up to offer more information over why the question is asked. 

#### Fluoride exposure
Ask the patient their fluoride exposure. Toothpaste, drinking water and additional supplements will be asked separately to keep question simple to understand. 
The 3 question will be assesed together, where any exposure puts patient at low risk, only if the patient answer no to all question question will they be assessed as moderate risk.

1. Do you consume any water, praticularly tap water that contains fluoride?
yes = low risk; No = moderate risk

2. Does the toothpaste you use contain fluoride? Please note that unless otherwise specified as fluoride-free, popular brands such as Colgate or Crest typically contain fluoride.
Yes = low risk; No = moderate risk

3. Do you consume any fluoride supplements?
yes = low risk; NO = moderate risk

Patient education:
Fluoride, a natural mineral, is essential for strengthening tooth enamel and preventing dental caries (cavities). It helps protect teeth against the acids that cause tooth decay. Regular use of fluoride-containing products like toothpaste and mouthwash, along with fluoride treatments from dental professionals, can significantly lower the risk of cavities. Ensuring adequate fluoride exposure is a key step in maintaining oral health.

### Sugary Food and Drinks
4. Do you consume sugary foods or beverages, including juices, carbonated or non-carbonated soft drinks, energy drinks, or medicinal syrups? If yes, are these consumed primarily during meal times, or do you have frequent exposure throughout the day?
Primarily during mealtimes = low risk; Frequent or prolonged between meal exposures per day = high risk

Patient education:
Sugary foods and drinks are a leading contributor to dental caries (cavities), as the bacteria in your mouth thrive on sugar. When these bacteria digest sugar, they produce acids that erode tooth enamel, leading to cavities. Frequent consumption of sugary items throughout the day amplifies this risk because it continuously feeds these bacteria, allowing them more opportunities to produce harmful acids. Limiting sugary foods and beverages, especially between meals, can significantly reduce your risk of developing caries and promote better oral health.

### Caries experience of mother, caregiver and/or other siblings (age 6-14)
- This question will be asked after assessing patient age, based on DOB information given at the beginning of the form. Only those between age 6-14 will be asked this question
- (possible future feature) grayed out the question if patient is not within the age range
5. How is the carise experience of Mother, Caregiver and/or other siblints
No caries in the last 24 months = low risk
Caries in the last 7 - 23 months = moderate risk
caries in the last 6 months = high risk 

Patient education:
Cavities can be influenced by the dental health of family members such as parents, siblings, or caregivers. If they have experienced cavities, your risk might increase due to the sharing of cavity-causing bacteria within the family. This transmission can occur through common activities like sharing utensils.

### Dental home
- This question will serve 2 purposes, firstly it will be used to assessed patient's caries risk.
- secondly, if patient answer no to question, question will be asked on the result page that allow browser to open to zocdoc for available dentist near the patient's location.
6. Do you have a regular dental office that you visit for your ongoing dental care needs?
yes = low risk; no = moderate risk

Patient education:
Having a dedicated dental practice, or a "dental home," where you go for regular check-ups and cleanings plays a key role in preventing cavities. These visits allow for the early detection and treatment of dental issues, significantly lowering your risk of caries. Your dentist can also offer tailored advice and preventive care, such as fluoride treatments, to further protect your teeth. Establishing a dental home is a proactive step towards maintaining optimal oral health.

### Special health needs
- This question will access age of the user to determine if risk is moderate or high. User who has special health needs along with age (6-14) will be determined as high rather than moderate risk
7.Do you or your caregivers experience any challenges in performing adequate oral health care due to special healthcare needs, developmental, physical, medical, or mental disabilities?
No = low caries risk
Yes and age > 14yrs = moderate risk
Yes and age 6 - 14yrs = high risk

Patient Education:
Special healthcare needs, whether developmental, physical, medical, or mental, can impact one's ability to perform routine oral health care or receive it effectively from caregivers. This situation may increase the risk of dental caries due to difficulties in maintaining consistent and thorough oral hygiene practices, such as brushing and flossing. Moreover, certain conditions may necessitate specialized dental care approaches to prevent caries effectively. Regular dental visits are crucial for individuals with special healthcare needs to receive personalized oral health care strategies, ensuring both prevention and management of dental caries are optimized.

### Chemo or radiation therapy
8. Have you undergone chemothreapy or radiation therapy?
No = low risk; yes = high risk

Patient education:
Undergoing chemotherapy or radiation therapy can significantly affect your oral health, increasing the risk of dental caries. These treatments can reduce saliva flow, leading to a dry mouth condition (xerostomia), which diminishes the natural cleansing effect of saliva on the teeth. Saliva plays a crucial role in neutralizing acids produced by plaque bacteria and in remineralizing tooth enamel. A reduction in saliva flow can therefore make the teeth more susceptible to decay. It's important for patients who have received these treatments to have a tailored oral care plan, including regular dental check-ups, to manage these risks and maintain oral health.

### Eating disorders
9. Do you have a history of any eating disorders?
No = low risk; yes = moderate risk

Patient education:
Eating disorders, such as anorexia or bulimia, can have profound effects on oral health and significantly increase the risk of dental caries. These conditions often lead to nutritional deficiencies that weaken tooth enamel, the protective outer layer of the teeth. Moreover, frequent vomiting, associated with some eating disorders, exposes teeth to stomach acids, further eroding enamel and leading to cavities. Regular dental care and addressing the eating disorder with professional help are vital steps in preventing dental caries and maintaining overall oral health.

### MEdications that reduce salivary flow
10. Are you currently taking any medications that are known to reduce salivary flow, such as antihistamines (e.g., diphenhydramine), antidepressants (e.g., fluoxetine), antihypertensives (e.g., atenolol), or diuretics (e.g., hydrochlorothiazide)?
No = low risk
Yes = moderate risk

Patient education:
Medications like antihistamines (for example, diphenhydramine), antidepressants (such as fluoxetine), antihypertensives (like atenolol), and diuretics (for instance, hydrochlorothiazide) can lead to decreased saliva production, resulting in dry mouth (xerostomia). Saliva plays a crucial role in oral health by neutralizing harmful acids and washing away food particles, thereby protecting against dental caries. When saliva flow is reduced, the risk of cavities increases due to the lack of this natural defense mechanism. If you're taking any of these medications, it's important to manage dry mouth effectively to prevent dental caries. Strategies may include increasing fluid intake, using saliva substitutes, and practicing good oral hygiene. Your dentist can provide personalized advice and preventive measures to safeguard your oral health.

### Drug or alcohol abuse
11. Have you experienced any issues with drug or alcohol abuse?
No = low risk
yes = moderate risk

Patient Education:
Substance abuse, including drugs and alcohol, can significantly impact your oral health, elevating the risk of dental caries. These substances can lead to neglect in oral hygiene practices, dietary changes, and reduced saliva production, creating an environment conducive to tooth decay. Alcohol, in particular, is acidic and can erode tooth enamel, while some drugs can cause dry mouth, further increasing the risk of cavities. Addressing substance abuse is crucial for overall health and maintaining good oral hygiene. Regular dental check-ups and a comprehensive oral care routine are vital for individuals recovering from substance abuse to mitigate the effects on oral health and reduce the risk of dental caries.

### Teeth missing due to caries in the past 36 months
12. Have you had any teeth extracted due to caries in the past 36 months?
No = low risk
yes = high risk

Patient Education:
Having teeth extracted due to caries in the last 36 months highlights a significant risk factor for ongoing dental health issues. Extractions resulting from cavities point to severe decay that could not be remediated by other treatments, underscoring the importance of addressing the root causes of caries, such as dietary habits, oral hygiene practices, and fluoride exposure. Such a history necessitates a proactive approach to oral care, including regular dental check-ups, to prevent new occurrences of caries and to preserve remaining teeth.

### Dental appliances
13. Do you currently use any dental appliances, such as complete dentures, partial dentures, bridges, crowns, implants, or braces?

Patient Education:
Using dental appliances like dentures, bridges, crowns, implants, or braces plays a crucial role in oral health but also requires specialized care to prevent dental caries. These appliances can create niches for plaque accumulation if not cleaned properly, increasing the risk of decay around the appliance edges or on remaining natural teeth. It's essential to follow tailored cleaning routines for your specific appliance to maintain oral hygiene and prevent caries. Regular dental check-ups are also vital for ensuring the appliances are in good condition and for receiving professional cleaning and guidance on oral care practice.

## Results form window
- Currently, an additional window will be displayed over the existing window to show results.
- Back button to close window and reset previous input form
### Result from caries algorithm
- Return output from caries detection algorithm
- return presence of caries
- return jpg with caries bounded

### Results from caries risk assessment
- Return any asnwers that is moderate to high risk
- Offer patient education paragraph in the output

### connection to zocdoc
- if caries is detected and patient don't have dental home, or if they choose to allow for zoc doc feature
- 
- Use URL search term feature of the zocdoc website
- Use & between terms
- Base url = https://www.zocdoc.come/search?
- zipcode += address={zip_code}
- after5pm += after_5pm={true or false}
- before 10 += before_10am={true or false}
- dentist += dr_specialty=98
- reason for caries visit += reason_visit=3305
- reason for check visist += reason_visit=6179
- if children += sess-children=true