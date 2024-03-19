"""This is a simple version of the app that is gui for the caries detection algorithum"""


from pathlib import Path
from PIL import Image, ImageTk
import tkinter as tk
from tkinter import filedialog
from tkinter import ttk
import webbrowser


class LabelInput(tk.Frame):
    """A widget containing a label on top of input together."""
    def __init__(
        self, parent, label, var, input_class=ttk.Entry,
        input_args=None, label_args=None, **kwargs
        ):
        super().__init__(parent, **kwargs)
        input_args = input_args or {}
        label_args = label_args or {}
        self.variable = var
        self.variable.label_widget = self

        # setup the label
        if input_class in (ttk.Checkbutton, ttk.Button):
            # Buttons don't need labels, they're built-in
            input_args["text"] = label
        else:
            self.label = ttk.Label(self, text=label, **label_args)
            self.label.grid(row=0, column=0, sticky=(tk.W + tk.E))

        # setup the variable
        if input_class in (ttk.Checkbutton, ttk.Button, ttk.Radiobutton):
            input_args["variable"] = self.variable
        else:
            input_args["textvariable"] = self.variable

        # Setup the input
        if input_class == ttk.Radiobutton:
            # for Radiobutton, create one input per value
            self.input = tk.Frame(self)
            for v in input_args.pop('values', []):
                button = ttk.Radiobutton(
                self.input, value=v, text=v, **input_args)
                button.pack(side=tk.LEFT, ipadx=10, ipady=2, expand=True, fill='x')
        else:
            self.input = input_class(self, **input_args)

        self.input.grid(row=1, column=0, sticky=(tk.W + tk.E))
        self.columnconfigure(0, weight=1)

    def grid(self, sticky=(tk.E + tk.W), **kwargs):
        """Override grid to add default sticky values"""
        super().grid(sticky=sticky, **kwargs)

class UserInfo(ttk.LabelFrame):
    """Set up the frame for basic User information"""
    def __init__(self, parent, name_var, age_var, *args, **kwargs):
        super().__init__(parent, text="User Info", **kwargs)
      
        for i in range(2):
          self.columnconfigure(i, weight=1)
        
        # set up labelinput for name
        LabelInput(
          self, label="Name",
          input_class=ttk.Entry,
          var=name_var
        ).grid(row=0, column=0, padx=20, pady=10)

        LabelInput(
          self, label='Age',
          var=age_var,
          input_class=ttk.Spinbox,
          input_args={"from_": 6, "to": 150, "increment": 1}
        ).grid(row=0, column=1, padx=20)

class PicUpload(ttk.LabelFrame):

    """Set up the frame for image upload"""
    # the frame contains one entry widget for typing in file path
    # one button to open up filedialog for selecting path
    # tk.StringVar to tie the entry box path with the filedialog path
    # a widget underneath to display the thumnail of the selected jpg
    def __init__(self, parent, path_var, **kwargs):
        super().__init__(parent, text="Upload pictures", **kwargs)

        # path entry box will be wider
        # button on the same column as entry box, but takes up less space
        # display pictures should take up the entire wideth of the frame
        self.columnconfigure(0, weight=4)
        self.columnconfigure(1, weight=1)

        # configure tkvariable for the file path
        self.file_path_var = path_var

        # configure entry box
        self.path_entry = ttk.Entry(self, textvariable=self.file_path_var)
        self.path_entry.grid(row=0, column=0, sticky=(tk.W + tk.E), padx=20, pady=10)

        # configure button for filedialog
        self.upload_button = ttk.Button(self, text="Browse File", command=self.browse_file)
        self.upload_button.grid(row=0, column=1)

        # label for displaying image
        self.image_label = tk.Label(self)
        self.image_label.grid(row=1, column=0, columnspan=2, 
                              sticky=(tk.W + tk.E), padx=20, pady=10)
        # Placeholder when no image has been selected
        self.image_label.config(text="No image selected")

    def browse_file(self):
       """Open file dialog to select an image, update entry and display image"""
       # use curren path in entry path as file dialog default if available
       initial_dir = self.file_path_var.get() or '/'
       file_path = filedialog.askopenfilename(
          title="Select an image",
          initialdir=initial_dir,
          filetypes=[('JPEG files', '*.jpeg')]
       )
       if file_path:
          self.file_path_var.set(file_path)
          self.display_image(file_path)

    def display_image(self, file_path):
       """Load and display the image in the label"""
       # Open the image file
       with Image.open(file_path) as img:
          img.thumbnail((300,300))
          photo = ImageTk.PhotoImage(img)

          self.image_label.config(image=photo)
          self.image_label.image = photo

class CRA(ttk.LabelFrame):
    """Set up the frame for Caries Risk Assessment"""
    # The question dictionary will be stored here
    # In the form of {q1:{'low': answer, 'moderate': answer, 'high': answer}, q2:{}.....}
    def __init__(self, parent, var_dict, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.columnconfigure(0, weight=1)

        self._var_dict = var_dict

        question_dict={
            "q1":
           {
                'Question': "Do you consume any water, praticularly tap water that contains fluoride?",
                'Low': 'yes',
                'Moderate': 'no',
                'High': '',
                'Type': 'Fluoride Exposure 1',
                'Patient Education': 'Fluoride, a natural mineral, is essential for strengthening tooth enamel and preventing dental caries (cavities). It helps protect teeth against the acids that cause tooth decay. Regular use of fluoride-containing products like toothpaste and mouthwash, along with fluoride treatments from dental professionals, can significantly lower the risk of cavities. Ensuring adequate fluoride exposure is a key step in maintaining oral health.'
           },
           "q2":
           {
                'Question':'Does the toothpaste you use contain fluoride? Please note that unless otherwise specified as fluoride-free, popular brands such as Colgate or Crest typically contain fluoride.',
                'Low': 'yes',
                'Moderate': 'no',
                'High': '',
                'Type': 'Fluoride Exposure 2',
                'Patient Education': 'Fluoride, a natural mineral, is essential for strengthening tooth enamel and preventing dental caries (cavities). It helps protect teeth against the acids that cause tooth decay. Regular use of fluoride-containing products like toothpaste and mouthwash, along with fluoride treatments from dental professionals, can significantly lower the risk of cavities. Ensuring adequate fluoride exposure is a key step in maintaining oral health.'
           },
           "q3":
           {
                'Question':'Do you consume any fluoride supplements?',
                'Low': 'yes',
                'Moderate': 'no',
                'High': '',
                'Type': 'Fluoride Exposure 3',
                'Patient Education':  'Fluoride, a natural mineral, is essential for strengthening tooth enamel and preventing dental caries (cavities). It helps protect teeth against the acids that cause tooth decay. Regular use of fluoride-containing products like toothpaste and mouthwash, along with fluoride treatments from dental professionals, can significantly lower the risk of cavities. Ensuring adequate fluoride exposure is a key step in maintaining oral health.'
           },
           "q4":
           {
                'Question':'Do you consume sugary foods or beverages, including juices, carbonated or non-carbonated soft drinks, energy drinks, or medicinal syrups? If yes, are these consumed primarily during meal times, or do you have frequent exposure throughout the day?',
                'Low':'Primarily during mealtimes',
                'Moderate': '',
                'High': 'frequent exposures between meal',
                'Type': 'Sugary Food and Drinks',
                'Patient Education':'Sugary foods and drinks are a leading contributor to dental caries (cavities), as the bacteria in your mouth thrive on sugar. When these bacteria digest sugar, they produce acids that erode tooth enamel, leading to cavities. Frequent consumption of sugary items throughout the day amplifies this risk because it continuously feeds these bacteria, allowing them more opportunities to produce harmful acids. Limiting sugary foods and beverages, especially between meals, can significantly reduce your risk of developing caries and promote better oral health.'
           },
           "q5":
           {
                'Question':'Do you have a regular dental office that you visit for your ongoing dental care needs?',
                'Low':'yes',
                'Moderate': 'no',
                'High': '',
                'Type': 'Dental Home',
                'Patient Education':'Having a dedicated dental practice, or a "dental home," where you go for regular check-ups and cleanings plays a key role in preventing cavities. These visits allow for the early detection and treatment of dental issues, significantly lowering your risk of caries. Your dentist can also offer tailored advice and preventive care, such as fluoride treatments, to further protect your teeth. Establishing a dental home is a proactive step towards maintaining optimal oral health.'
           },
           "q6":
           {
                'Question':'Do you or your caregivers experience any challenges in performing adequate oral health care due to special healthcare needs, developmental, physical, medical, or mental disabilities?',
                'Low':'no',
                'Moderate': 'yes and age>14',
                'High': 'yes and age 6-14',
                'Type': 'Special Health Needs',
                'Patient Education': "Special healthcare needs, whether developmental, physical, medical, or mental, can impact one's ability to perform routine oral health care or receive it effectively from caregivers. This situation may increase the risk of dental caries due to difficulties in maintaining consistent and thorough oral hygiene practices, such as brushing and flossing. Moreover, certain conditions may necessitate specialized dental care approaches to prevent caries effectively. Regular dental visits are crucial for individuals with special healthcare needs to receive personalized oral health care strategies, ensuring both prevention and management of dental caries are optimized."
           },
           "q7":
           {
                'Question': 'Have you undergone chemothreapy or radiation therapy?',
                'Low':'no',
                'Moderate': '',
                'High': 'yes',
                'Type': 'Chemo or Radiation Therapy',
                'Patient Education': "Undergoing chemotherapy or radiation therapy can significantly affect your oral health, increasing the risk of dental caries. These treatments can reduce saliva flow, leading to a dry mouth condition (xerostomia), which diminishes the natural cleansing effect of saliva on the teeth. Saliva plays a crucial role in neutralizing acids produced by plaque bacteria and in remineralizing tooth enamel. A reduction in saliva flow can therefore make the teeth more susceptible to decay. It's important for patients who have received these treatments to have a tailored oral care plan, including regular dental check-ups, to manage these risks and maintain oral health."


           },
           "q8":
           {
                'Question':'Do you have a history of any eating disorders?',
                'Low':'no',
                'Moderate': 'yes',
                'High': '',
                'Type': 'Eating Disorders',
                'Patient Education': "Eating disorders, such as anorexia or bulimia, can have profound effects on oral health and significantly increase the risk of dental caries. These conditions often lead to nutritional deficiencies that weaken tooth enamel, the protective outer layer of the teeth. Moreover, frequent vomiting, associated with some eating disorders, exposes teeth to stomach acids, further eroding enamel and leading to cavities. Regular dental care and addressing the eating disorder with professional help are vital steps in preventing dental caries and maintaining overall oral health."
           },
           "q9":
           {
                'Question':'Are you currently taking any medications that are known to reduce salivary flow, such as antihistamines (e.g., diphenhydramine), antidepressants (e.g., fluoxetine), antihypertensives (e.g., atenolol), or diuretics (e.g., hydrochlorothiazide)?',
                'Low':'no',
                'Moderate': 'yes',
                'High': '',
                'Type': "Medications that reduce salivary flow",
                'Patient Education':"Medications like antihistamines (for example, diphenhydramine), antidepressants (such as fluoxetine), antihypertensives (like atenolol), and diuretics (for instance, hydrochlorothiazide) can lead to decreased saliva production, resulting in dry mouth (xerostomia). Saliva plays a crucial role in oral health by neutralizing harmful acids and washing away food particles, thereby protecting against dental caries. When saliva flow is reduced, the risk of cavities increases due to the lack of this natural defense mechanism. If you're taking any of these medications, it's important to manage dry mouth effectively to prevent dental caries. Strategies may include increasing fluid intake, using saliva substitutes, and practicing good oral hygiene. Your dentist can provide personalized advice and preventive measures to safeguard your oral health."
           },
           "q10":
           {
                'Question':'Have you experienced any issues with drug or alcohol abuse?',
                'Low':'no',
                'Moderate': 'yes',
                'High': '',
                'Type': "Drug or Alcohol Abuse",
                'Patient Education':"Substance abuse, including drugs and alcohol, can significantly impact your oral health, elevating the risk of dental caries. These substances can lead to neglect in oral hygiene practices, dietary changes, and reduced saliva production, creating an environment conducive to tooth decay. Alcohol, in particular, is acidic and can erode tooth enamel, while some drugs can cause dry mouth, further increasing the risk of cavities. Addressing substance abuse is crucial for overall health and maintaining good oral hygiene. Regular dental check-ups and a comprehensive oral care routine are vital for individuals recovering from substance abuse to mitigate the effects on oral health and reduce the risk of dental caries."
           },
           "q11":
           {
                'Question': 'Have you had any teeth extracted due to caries in the past 36 months?',
                'Low':'no',
                'Moderate': '',
                'High': 'yes',
                'Type':'Teeth Missing due to Caries',
                'Patient Education':"Having teeth extracted due to caries in the last 36 months highlights a significant risk factor for ongoing dental health issues. Extractions resulting from cavities point to severe decay that could not be remediated by other treatments, underscoring the importance of addressing the root causes of caries, such as dietary habits, oral hygiene practices, and fluoride exposure. Such a history necessitates a proactive approach to oral care, including regular dental check-ups, to prevent new occurrences of caries and to preserve remaining teeth."
           },
           "q12":
           {
                'Question': 'Do you currently use any dental appliances, such as complete dentures, partial dentures, bridges, crowns, implants, or braces?',
                'Low':'no',
                'Moderate': 'yes',
                'High': '',
                'Type': 'Dental Appliances',
                'Patient Education': "Using dental appliances like dentures, bridges, crowns, implants, or braces plays a crucial role in oral health but also requires specialized care to prevent dental caries. These appliances can create niches for plaque accumulation if not cleaned properly, increasing the risk of decay around the appliance edges or on remaining natural teeth. It's essential to follow tailored cleaning routines for your specific appliance to maintain oral hygiene and prevent caries. Regular dental check-ups are also vital for ensuring the appliances are in good condition and for receiving professional cleaning and guidance on oral care practice."
           }
        }
        test_dict={
           "question 1":
           {
              "low": 'low risk',
              'moderate': 'moderate risk',
              'high': 'high risk'
           },
           "question 2":
           {
              "low": 'low risk',
              'moderate': 'moderate risk',
              'high': 'high risk'
           },
        }

        for question_num, q_dict in question_dict.items():
            question_input = CariesQuestionInput(self, question_num, q_dict,  self._var_dict[q_dict['Type']]['risk'])
            self._var_dict[q_dict['Type']]['Patient Education'] = q_dict['Patient Education']
            question_input.grid(sticky=(tk.W + tk.E))
    
class CariesQuestionInput(tk.Frame):

    """Widgent containing question and radiobutton for the various caries question"""
    def __init__(
        self, parent, question, question_dict_values, risk_status, 
        *args, **kwargs
        ):
        self.risk_status = risk_status
        super().__init__(parent, **kwargs)

        # Set up the column width
        self.columnconfigure(0, weight=2)
        self.columnconfigure(1, weight=1)
        
        # setting up a question frame
        self.question_frame = tk.Frame(self)
        self.question_frame.grid(column=0, sticky='we')
        self.question_frame.columnconfigure(0, weight=1)

        # Setting up label to display the question
        self.question_label = tk.Label(
           self.question_frame,
           text= question + '. ' + question_dict_values['Question'],
           justify="left",
           anchor='nw',
           wraplength='900'
        )
        self.question_label.grid(column=0, row=0, rowspan=1, padx=0, pady=5, sticky=(tk.W + tk.E))


        # setting up the answer choices with radiobutton
        self.input = tk.Frame(self)
        self.input.columnconfigure(0, weight=1)

        for risk in ('Low', 'Moderate', 'High'):
            if not question_dict_values[risk]:
                continue
            button = ttk.Radiobutton(
            self.input, value=risk, text=question_dict_values[risk], var=self.risk_status
            )
            if risk == 'Low':
               button.grid(column=0, row=1, sticky=(tk.E), padx=10)
               #button.pack(side=tk.LEFT, ipadx=10, ipady=2, fill='x')
            if risk == 'Moderate':
               button.grid(column=1, row=1, sticky=(tk.E), padx=10)
               #button.pack(side=tk.LEFT, ipadx=10, ipady=2, fill='x')
            if risk == 'High':
               button.grid(column=2, row=1, sticky=(tk.E), padx=10)
               #button.pack(side=tk.LEFT, ipadx=10, ipady=2, fill='x')
        self.input.grid(column=1, row=0, padx=0, pady=10, sticky=(tk.W))

# class PicResult(ttk.LabelFrame):   

class InputForm(ttk.LabelFrame):
    def __init__(self, master, var_dict, submit_callback, *args, **kwargs):
        super().__init__(master, *args, **kwargs)

        self._vars = var_dict
        self.submit_callback = submit_callback
        
        self.columnconfigure(0, weight=1)

        # setting up frame for userinfo
        self.userinfo = UserInfo(self, self._vars['Name'], self._vars['Age'])
        # self.userinfo.grid(row=0, padx=10, pady=10, sticky=(tk.W + tk.E))

        # setting up frame for picture upload
        self.picupload = PicUpload(self, self._vars['Image Path'])
        self.picupload.grid(row=1, padx=10, pady=10, sticky=(tk.W + tk.E))

        # setting up frame for CRA
        self.CRA = CRA(self, self._vars)
        self.CRA.grid(row=3, padx=10, sticky=(tk.W + tk.E))

        # Submit button
        buttons = ttk.Frame(self)
        buttons.grid(sticky=tk.W + tk.E, row=2)
        self.resetbutton = ttk.Button(
            buttons, text="Reset", command=self.on_reset
        )

        self.submitbutton = ttk.Button(
            buttons, text="Submit", command=self.on_submit
        )
        # Reset button
        self.submitbutton.pack(side=tk.RIGHT, padx=10)

    def on_submit(self):
        data = dict()
        for key, variable in self._vars.items():
            if key == "Output Image Path" or key =="Number of Caries":
                print("enter if")
                data[key] = variable
            elif isinstance(variable, dict):
                # construct the dictionary again
                data[key] = dict()
                for sub_key, sub_variable in variable.items():
                    if sub_key == 'risk':
                        data[key][sub_key] = sub_variable.get()
                    else:
                        data[key][sub_key] = sub_variable
            else:
                print(key)
                data[key] = variable.get()
        self.submit_callback(data)
        
        # internal test
        for variable, data in data.items():
            if isinstance(data, dict):
                print(f"{variable} risk is {data['risk'] or 'unanswered'}")
                
            else:
                print(f"{variable} is {data or 'unanswered'}")
        print('\n')
        return data

    # will be writen later
    def on_reset(self):
        pass

class ImageOutput(ttk.LabelFrame):
    def __init__(self, parent, path, **kwargs):
        super().__init__(parent, text="AI Result", **kwargs)
        self.columnconfigure(0, weight=1)

        # path for the output image
        self.image_path = path

        # image label
        self.image_label = tk.Label(self)
        self.image_label.grid(row=0, column=0, sticky=(tk.W + tk.E), padx=20, pady=10)
        
        self.display_image(self.image_path)


    def display_image(self, path):
        """load and display the image in the label"""
        with Image.open(path) as img:
            img.thumbnail ((300,300))
            photo = ImageTk.PhotoImage(img)

            self.image_label.config(image=photo)
            self.image_label.image=photo

class CRAresults(ttk.LabelFrame):
    def __init__(self, parent, data_dict, **kwargs):
        super().__init__(parent, text="Caries risk results based on your answers to previous questions", **kwargs)
        self.columnconfigure(0, weight=2)
        self.columnconfigure(1, weight=20)

        high_risk = ('Moderate', 'High')

        if (data_dict['Fluoride Exposure 1']['risk'] in high_risk or 
            data_dict['Fluoride Exposure 2']['risk'] in high_risk or
            data_dict['Fluoride Exposure 3']['risk'] in high_risk):
            ttk.Label(
                self,
                text=f"High risk in fluoride exposure",
            ).grid(row=1, column=0, sticky="ew", padx=10, pady=2, rowspan=5)
            ttk.Label(
                self, 
                text=f"{data_dict['Fluoride Exposure 1']['Patient Education']}",
                justify="left",
                anchor='nw',
                wraplength='1200'
                ).grid(row=1, column=1, sticky="ew", padx=10, pady=2, rowspan=5)

        matched_key = (
            'Sugary Food and Drinks',
            'Dental Home',
            'Special Health Needs',
            'Chemo or Radiation Threapy',
            'Eating Disorders',
            'Medications that reduce salivary flow',
            'Drug or Alcohol Abuse',
            'Teeth Missing due to Caries',
            'Dental Appliances',
            )

        i = 2
        for key, value in data_dict.items():
            if key in matched_key and value['risk'] in high_risk:
                print(key)
                ttk.Label(
                    self,
                    text=f"{key}",
                ).grid(row=i, column=0, sticky="ew", padx=10, pady=2, rowspan=5)
                ttk.Label(
                    self, 
                    text=f"{value['Patient Education']}",
                    justify="left",
                    anchor='nw',
                    wraplength='1200'
                    ).grid(row=i, column=1, sticky="ew", padx=10, pady=2, rowspan=5)
                i = i + 5

class zocdoc(ttk.LabelFrame):
    def __init__(self, parent, data_dict, **kwargs):
        super().__init__(parent, text='Fill out the following and find a dentist near you using ZocDoc:', **kwargs)
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self._vars = {
            'Zip Code': tk.IntVar(),
            'After 5pm': tk.BooleanVar(), 
            'Before 10am': tk.BooleanVar(),
            'Checkup Only': tk.BooleanVar()
        }

        LabelInput(
            self, "Zip Code", input_class=ttk.Entry, var=self._vars['Zip Code']
        ).grid(row=0, column=0)
        LabelInput(
            self, "After 5pm", input_class=ttk.Checkbutton, var=self._vars['After 5pm']
        ).grid(row=1, column=0)
        LabelInput(
            self, "Before 10am", input_class=ttk.Checkbutton, var=self._vars['Before 10am']
        ).grid(row=2, column=0)
        LabelInput(
            self, "Checkup Only", input_class=ttk.Checkbutton, var=self._vars['Checkup Only']
        ).grid(row=3, column=0)
        buttons = ttk.Frame(self)
        buttons.grid(sticky=tk.W + tk.E, row=4)
        self.websitebutton = ttk.Button(
            buttons, text="Go to ZocDoc", command=lambda: self._go_to_zocdoc(self._vars))
        self.websitebutton.pack(side=tk.RIGHT)


    def _go_to_zocdoc(self, var_list):
        baseurl = "https://www.zocdoc.com/search?"
        zip_code = var_list['Zip Code'].get()
        after_5pm = var_list['After 5pm'].get()
        before_10am = var_list['Before 10am'].get()
        checkup_only = var_list['Checkup Only'].get()

        if zip_code:
            baseurl += f"address={zip_code}&"
        if after_5pm:
            baseurl += "after_5pm=true&"
        if before_10am:
            baseurl += "before_10am=true&"
        if checkup_only:
            baseurl += "reason_visit=6179&"
        else:
            baseurl += "reason_visit=3305&"
        
        
        print(baseurl)  # You might want to actually open this URL in a web browser
        # For example, using webbrowser module
        # import webbrowser
        webbrowser.open(baseurl)

class ResultsWindow(tk.Toplevel):
    def __init__(self, parent, data_dict, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.title("Results")

        self.populate_results(data_dict)

    def populate_results(self, data_dict):
        # Populate results using grid
        self.columnconfigure(0, weight=1)  # Make the column expandable
        ImageOutput(self, data_dict['Image Path']).grid(row=0, column=0, sticky="ew", padx=10, pady=10)
        
        ttk.Label(self, text=f"{data_dict['Number of Caries']} caries detected!").grid(row=1, column=0, sticky="ew", padx=10, pady=10)

        zocdoc(self, data_dict).grid(row=2, column=0, sticky="ew", padx=10, pady=10)
        CRAresults(self, data_dict).grid(row=3, column=0, sticky="ew", padx=10, pady=10)

        row = 3  # Starting row for the dynamic content

        # for key, value in data_dict.items():
        #     if isinstance(value, dict):
        #         ttk.Label(self, text=f"{key} risk is {value['risk'] or 'unanswered'}").grid(row=row, column=0, sticky="ew", padx=10, pady=2)
        #     else:
        #         ttk.Label(self, text=f"{key} is {value or 'unanswered'}").grid(row=row, column=0, sticky="ew", padx=10, pady=2)
        #     row += 1

class ScrollResultsWindow(tk.Toplevel):
    def __init__(self, parent, data_dict, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.title("Results")
        self.geometry("600x400")  # Set initial size of the window

        self.canvas = tk.Canvas(self)
        self.scrollbar = tk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.scroll_frame = tk.Frame(self.canvas)  # Frame that will contain widgets

        self.scroll_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(
                scrollregion=self.canvas.bbox("all")
            )
        )

        self.canvas.create_window((0, 0), window=self.scroll_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")

        self.populate_results(data_dict)

    def populate_results(self, data_dict):
        # Add your content to self.scroll_frame instead of self
        ImageOutput(self.scroll_frame, data_dict['Image Path']).pack(padx=10, pady=10, fill=tk.X)
        ttk.Label(self.scroll_frame, text=f"{data_dict['Number of Caries']} caries detected!").pack(padx=10, pady=10, fill=tk.X)
        for key, value in data_dict.items():
            if isinstance(value, dict):
                ttk.Label(self.scroll_frame, text=f"{key} risk is {value['risk'] or 'unanswered'}").pack(fill=tk.X)
            else:
                ttk.Label(self.scroll_frame, text=f"{key} is {value or 'unanswered'}").pack(fill=tk.X)

class Application(tk.Tk):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    
        # creat dictionary to keep track of all inputs
        self._vars = {
            'Name': tk.StringVar(),
            'Age': tk.IntVar(),
            'Image Path': tk.StringVar(),
            'Fluoride Exposure 1': {'risk': tk.StringVar(), 'Patient Education':''},
            'Fluoride Exposure 2': {'risk': tk.StringVar(), 'Patient Education':''},
            'Fluoride Exposure 3': {'risk': tk.StringVar(), 'Patient Education':''},
            'Sugary Food and Drinks': {'risk': tk.StringVar(), 'Patient Education':''},
            'Dental Home': {'risk': tk.StringVar(), 'Patient Education':''},
            'Special Health Needs': {'risk': tk.StringVar(), 'Patient Education':''},
            'Chemo or Radiation Therapy': {'risk': tk.StringVar(), 'Patient Education':''},
            'Eating Disorders': {'risk': tk.StringVar(), 'Patient Education':''},
            'Medications that reduce salivary flow': {'risk': tk.StringVar(), 'Patient Education':''},
            'Drug or Alcohol Abuse': {'risk': tk.StringVar(), 'Patient Education':''},
            'Teeth Missing due to Caries': {'risk': tk.StringVar(), 'Patient Education':''},
            'Dental Appliances': {'risk': tk.StringVar(), 'Patient Education':''},
            'Output Image Path': '',
            'Number of Caries': '',
        }

        #title shown on window
        self.title("Caries Detection Application")
        self.columnconfigure(0, weight=1)

        # Label for the application
        ttk.Label(
           self, text="AI Caries Detection",
           font=("TKDefaultFont", 25)   
        ).grid(row=0)

        # input form
        self.inputform = InputForm(self, var_dict=self._vars, submit_callback=self.open_results_window)
        self.inputform.grid(row=1, padx=10, sticky=(tk.W + tk.E))

    def open_results_window(self, data):

        # get the image to be processed
        image_path = data.get('Image Path', '')

        # assigned variables 
        processed_image, caries_count = self.dummy_ai(image_path)
        
        # Update 'form_data' with AI processing results
        data.update({
            'Output Image Path': processed_image,
            'Number of Caries': caries_count
        })

        ResultsWindow(self, data)


    def dummy_ai(self, img_path):
        from roboflow import Roboflow
        rf = Roboflow(api_key="API_KEY")
        project = rf.workspace().project("MODEL_ENDPOINT")
        model = project.version(VERSION).model
        # infer on a local image
        print(model.predict(img_path, confidence=40, overlap=30).json())
        num_caries = 3
        return img_path, num_caries


if __name__ == "__main__":
    app = Application()
    app.mainloop()
         