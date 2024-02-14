"""This is a simple version of the app that is gui for the caries detection algorithum"""


from pathlib import Path
from PIL import Image, ImageTk
import tkinter as tk
from tkinter import filedialog
from tkinter import ttk


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
    def __init__(self, *args, **kwargs):
        super().__init__(text="User Info", *args, **kwargs)

        # create dictionary to hold the UserInfo variables
        self._vars = {
          'Name': tk.StringVar(),
          'Age': tk.IntVar()
        }
      
        for i in range(2):
          self.columnconfigure(i, weight=1)
        
        # set up labelinput for name
        LabelInput(
          self, label="Name",
          input_class=ttk.Entry,
          var=self._vars['Name']
        ).grid(row=0, column=0, padx=20, pady=10)

        LabelInput(
          self, label='Age',
          var=self._vars['Age'],
          input_class=ttk.Spinbox,
          input_args={"from_": 6, "to": 150, "increment": 1}
        ).grid(row=0, column=1, padx=20)

class PicUpload(ttk.LabelFrame):

    """Set up the frame for image upload"""
    # the frame contains one entry widget for typing in file path
    # one button to open up filedialog for selecting path
    # tk.StringVar to tie the entry box path with the filedialog path
    # a widget underneath to display the thumnail of the selected jpg
    def __init__(self, *args, **kwargs):
        super().__init__(text="Upload pictures", *args, **kwargs)

        # path entry box will be wider
        # button on the same column as entry box, but takes up less space
        # display pictures should take up the entire wideth of the frame
        self.columnconfigure(0, weight=4)
        self.columnconfigure(1, weight=1)

        # configure tkvariable for the file path
        self.file_path_var = tk.StringVar()

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
          filetypes=[('PNG files', '*.png')]
       )
       if file_path:
          self.file_path_var.set(file_path)
          self.display_image(file_path)

    def display_image(self, file_path):
       """Load and display the image in the label"""
       # Open the image file
       with Image.open(file_path) as img:
          img.thumbnail((200,200))
          photo = ImageTk.PhotoImage(img)

          self.image_label.config(image=photo)
          self.image_label.image = photo

class CRA(ttk.LabelFrame):
    """Set up the frame for Caries Risk Assessment"""
    # The question dictionary will be stored here
    # In the form of {q1:{'low': answer, 'moderate': answer, 'high': answer}, q2:{}.....}
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.columnconfigure(0, weight=1)

        question_dict={
           "Do you consume any water, praticularly tap water that contains fluoride?":
           {
                'low': 'yes',
                'moderate': 'no',
                'high': ''
           },
           """Does the toothpaste you use contain fluoride? Please note that unless otherwise specified as fluoride-free, popular brands such as Colgate or Crest typically contain fluoride.""":
           {
                'low': 'yes',
                'moderate': 'no',
                'high': ''
           },
           """Do you consume any fluoride supplements?""":
           {
                'low': 'yes',
                'moderate': 'no',
                'high': ''  
           },
           """Do you consume sugary foods or beverages, including juices, carbonated or non-carbonated soft drinks, energy drinks, or medicinal syrups? If yes, are these consumed primarily during meal times, or do you have frequent exposure throughout the day?""":
           {
                'low':'Primarily during mealtimes',
                'moderate': '',
                'high': 'frequent exposures between meal'
           },
           """Do you have a regular dental office that you visit for your ongoing dental care needs??""":
           {
                'low':'yes',
                'moderate': 'no',
                'high': ''
           },
           """Do you or your caregivers experience any challenges in performing adequate oral health care due to special healthcare needs, developmental, physical, medical, or mental disabilities?""":
           {
                'low':'no',
                'moderate': 'yes and age>14',
                'high': 'yes and age 6-14'
           },
           """Have you undergone chemothreapy or radiation therapy?""":
           {
                'low':'no',
                'moderate': '',
                'high': 'yes'
           },
           """Do you have a history of any eating disorders?""":
           {
                'low':'no',
                'moderate': 'yes',
                'high': ''
           },
           """Are you currently taking any medications that are known to reduce salivary flow, such as antihistamines (e.g., diphenhydramine), antidepressants (e.g., fluoxetine), antihypertensives (e.g., atenolol), or diuretics (e.g., hydrochlorothiazide)?""":
           {
                'low':'no',
                'moderate': 'yes',
                'high': ''
           },
           """Have you experienced any issues with drug or alcohol abuse?""":
           {
                'low':'no',
                'moderate': 'yes',
                'high': ''
           },
           """Have you had any teeth extracted due to caries in the past 36 months?""":
           {
                'low':'no',
                'moderate': '',
                'high': 'yes'
           },
           """Do you currently use any dental appliances, such as complete dentures, partial dentures, bridges, crowns, implants, or braces?""":
           {
                'low':'no',
                'moderate': 'yes',
                'high': ''
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
        for question_num, (question, answers) in enumerate(question_dict.items(), start=1):
           question_input = CariesQuestionInput(self, question, question_num, answers, tk.StringVar())
           question_input.grid(sticky=(tk.W + tk.E))
    
class CariesQuestionInput(tk.Frame):
    """Widgent containing question and radiobutton for the various caries question"""
    def __init__(
        self, parent, question, question_num, answers, risk_status,
        *args, **kwargs
        ):
        self.risk = risk_status
        super().__init__(parent, **kwargs)

        # Set up the column width
        self.columnconfigure(0, weight=3)
        self.columnconfigure(1, weight=1)
        
        # setting up a question frame
        self.question_frame = tk.Frame(self)
        self.question_frame.grid(column=0, sticky='we')
        self.question_frame.columnconfigure(0, weight=1)

        # Setting up label to display the question
        self.question_label = tk.Label(
           self.question_frame,
           text= str(question_num) + '. ' + question,
           justify="left",
           anchor='nw',
           wraplength='1000'
        )
        self.question_label.grid(column=0, row=0, rowspan=1, padx=0, pady=10, sticky=(tk.W + tk.E))

        # self.bind('<Configure>', self.adjust_wraplength(self.question_frame))

        # setting up the answer choices with radiobutton
        self.input = tk.Frame(self)
        for c in range(3):
            self.input.columnconfigure(c, weight=1)

        for r, a in answers.items():
            if not a:
                continue
            button = ttk.Radiobutton(
            self.input, value=r, text=a, var=self.risk
            )
            if r == 'low':
               button.grid(column=0, row=1, sticky=(tk.E), padx=10)
            if r == 'moderate':
               button.grid(column=1, row=1, sticky=(tk.E), padx=10)
            if r == 'high':
               button.grid(column=2, row=1, sticky=(tk.E), padx=10)
        self.input.grid(column=1, row=0, padx=0, pady=10, sticky=(tk.W + tk.E))
    
    def adjust_wraplength(self, parent, event=None, initial_width=None):
        """Dynamically adjust the wraplength of the label."""
        self.question_label.config(wraplength=parent.winfo_width())

class Application(tk.Tk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    
        #title shown on window
        self.title("Caries Detection Application")
        self.columnconfigure(0, weight=1)

        # Label for the application
        ttk.Label(
           self, text="AI Caries Detection",
           font=("TKDefaultFont", 25)   
        ).grid(row=0)

        # setting up frame for userinfo
        self.userinfo = UserInfo(self)
        self.userinfo.grid(row=1, padx=10, sticky=(tk.W + tk.E))

        # setting up frame for picture upload
        self.picupload = PicUpload(self)
        self.picupload.grid(row=2, padx=10, sticky=(tk.W + tk.E))

        # setting up frame for CRA
        self.CRA = CRA(self)
        self.CRA.grid(row=3, padx=10, sticky=(tk.W + tk.E))


if __name__ == "__main__":
    app = Application()
    app.mainloop()
         