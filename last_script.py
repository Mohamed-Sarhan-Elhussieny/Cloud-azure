class Patient:
    """
    A comprehensive class to store patient data.
    """
    def __init__(self, name,mou ,Polyuria_colour,age, sex, infaction,hemopt,address, occupation, marital_status, children, is_smoker, alcohol_user,duration_of_smoking,num_of_cigrates ,parent_is_smoker,Tea_addict,Pet_owner,is_eating,Polyuria,Dysuria,breathe_odor,vomiting,constipation,Diarrhea,Jaundice,blotting,chest_pain,cough,fever,vomiting_blood,conscious_level,cyanosis,edema,heart,last_reading):
        self.name = name
        self.age = age
        self.sex = sex  # New attribute: 'male' or 'female'
        self.address = address
        self.occupation = occupation
        self.marital_status = marital_status
        self.children = children
        self.smoker = is_smoker
        self.duration = duration_of_smoking 
        self.cigarettes_per_day =  num_of_cigrates
        self.alcohol_user = alcohol_user
        self.parent_is_smoker = parent_is_smoker
        self.Tea_addict= Tea_addict
        self.Pet_owner = Pet_owner
        self.is_eating = is_eating
        self.Polyuria = Polyuria
        self.Polyuria_colour = Polyuria_colour
        self.Dysuria = Dysuria
        self.infaction = infaction
        self.vomiting = vomiting
        self.last_reading = last_reading
        self.constipation = constipation
        self.Diarrhea = Diarrhea
        self.Jaundice = Jaundice
        self.blotting = blotting
        self.chest_pain =chest_pain
        self.cough = cough
        self.fever = fever
        self.vomiting_blood = vomiting_blood
        self.conscious_level = conscious_level
        self.hemopt = hemopt
        self.breathe_odor = breathe_odor
        self.cyanosis = cyanosis
        self.edema = edema
        self.mou = mou
        self.heart = heart
        self.smoke = {
            'smoking': {
                'is_smoker': is_smoker,
                'cigarettes_per_day': self.cigarettes_per_day,
                'duration': self.duration
            }
        }
        self.chief_complaint = None
        self.medical_history = {}
        self.current_medications = {}
        self.family_history = {}

#####################################################################################################
    def add_chief_complaint(self, complaint, duration, onset, severity,releaving_factor):

        self.chief_complaint = {
            "Complaint": complaint,
            "Duration": duration,
            "Onset": onset,
            "Severity": severity,
            "releaving_factor":releaving_factor
        }
#############################################################################################################


    def add_hpi(self, hpi_details):

        self.hpi = hpi_details    


#############################################################################################################


    def add_medical_history(self, condition, details, blood_transfusions, last_time, percentage,other, operation=None):
        
        self.medical_history.update({

            "condition": condition,

            "details": details,

            "last_time": last_time,

            "percentage":percentage,

            "other" : other,

            "blood_transfusions": blood_transfusions,

            "operation": operation
        })

##################################################################################################################


    def add_medication(self, response):

        self.current_medications = {

            "response" : response

    }


####################################################################################################################       
    def add_family_history(self,family,illness):

        self.family_history = {
            "family":family,
            "illness":illness
        }

######################################################################################################################

class PatientQA:
    def __init__(self, patient):
        self.patient = patient


        self.qa_mapping = {

            'personal_info': {
                'keywords': ['جوزك بيدخن','ريقك','بتدخن','سخن','لون','عامل اي','ازيك','شغال اي','عمر','عدوي','عدوات','اسم', 'سن', 'ساكن', 'شغل', 'متزوج', 'اولاد', 'تدخين', 'كحول', 'تدخن', 'مدخن', 'اطفال', 'عيال', 'بتشتغل', 'متجوز', 'جواز', 'كام','سجاير','معدل','سيجاره','شاي','قهوه','حيوانات','فطار','فطر','فطرتي','غدا','اتغديتي','عشا','اتعشيتي','أكلتي','اكل','حمام','بول','ازي','حرقان','نفس','ترجيع','امساك','اسهال','صفرا','انتفاخ','صدر','كحه','سخونيه','دم','دوخه','وعي','بلغم','زرقان','ازرق','زرق','نفخ','ورم','قلب','ضربات','قرايه','تراكمي'],
                'response_generator': self.personal_response
            },

            'chief_complaint': {
                'keywords': ['مده','بتشتكي', 'مشكلة', 'معاناة', 'بقالها', 'من امتي', 'ظهرت', 'شده', 'اللي جابك',' أمتي','معاك ازاي','التعب دا بقاله اد اي','المرض بدا معاك ازاي','التعب دا لاحظته ازاي ',' بالتدريج','تدريجي','فجأه','مستشفي','العياده','التعب ','بدأت','مستمره','شكوه','تعبك',' قد ايه','بيزيد ولا بيقل', 'زيد','يقل','ريح','تدريج'],
                'response_generator': self.chief_complaint_response
            },
            'hpi': {
                'keywords': ['اعراض', 'تحليل', 'علاج', 'اعراض اضافية', 'تفاصيل', 'تاريخ','وجع','تحاليل','مسكنات','الم','سمع','وصف','تحسن'],
                'response_generator': self.hpi_response
            },


            'medical_history': {
                'keywords': ['مرض', 'مزمن', 'مستشفى', 'روحت المستشفى','برشام','انسولين', ' وحده ',' اخر مره','ضغط','اخر','مره'],
                'response_generator': self.medical_history_response
            },

            'operations_and_blood': {
                'keywords': ['عمليات', 'عملية', 'نقل دم', 'مضاعفات'],
                'response_generator': self.operations_response
            },
            #'drug_intake': {
            #    'keywords': ['ادوية', 'حساسية من دواء', 'مدة العلاج'],
            #    'response_generator': self.drug_intake_response
            #},
            'similar_attacks': {
                'keywords': ['نوبات', 'حالة مماثلة', 'حوادث', 'صدمات'],
                'response_generator': self.similar_attacks_response
            },
             'medications': {
                'keywords': ['سلامه'],
                'response_generator': self._get_medications_response
            },
             'family_history': {
                'keywords': ['عيلة', 'مرض وراثي', 'أهل',  'قريب','قرايب','عيله'],
                'response_generator': self.get_family_history_response
            }
            
        }


    def normalize_text(self, text):
        """Normalize Arabic text for better matching"""
        import re
        if not text:
            return ''
        
        # Remove diacritics and extra spaces
        text = re.sub(r'[ًٌٍَُِّْ]', '', text)
        
        # Normalize Arabic letter variations
        text = text.replace('أ', 'ا').replace('إ', 'ا').replace('آ', 'ا')
        text = text.replace('ى', 'ي')
        
        # Convert to lowercase and remove extra spaces
        return re.sub(r'\s+', ' ', text.lower().strip())
    



    def match_question(self, question):
        """Match question to appropriate response"""
        normalized_q = self.normalize_text(question)
        
        # Check each question type
        for qa_type, qa_details in self.qa_mapping.items():
            if any(self.normalize_text(keyword) in normalized_q for keyword in qa_details['keywords']):
                return qa_details['response_generator'](question)
        
        return "عيد السؤال تاني "
    


    
    def personal_response(self, question):
        """Generate responses for personal information questions"""
        normalized_q = self.normalize_text(question)
        
        # Additional logic for sex-related questions
        if any(keyword in normalized_q for keyword in ['جنس', 'نوع']):
            return f"{'رجل' if self.patient.sex == 'male' else 'امرأة'}"
        
        if any(keyword in normalized_q for keyword in ['اسم', 'بتسمى']):
            return f"اسمي {self.patient.name}"
        
        elif any(keyword in normalized_q for keyword in ['عامل اي','ازيك','ازي']):
            return f"بخير يا دكتور الحمد الله ماشي الحال"
        
        elif any(keyword in normalized_q for keyword in ['عمرك','سن', 'عمر']):
            return f"عندي {self.patient.age} سنة"
        
        elif any(keyword in normalized_q for keyword in ['ساكن', 'سكن']):
            return f"أنا ساكن في {self.patient.address}"
        
        elif any(keyword in normalized_q for keyword in ['شغال اي','شغل', 'شغلك', 'بتشتغل']):
            return f"أنا  {self.patient.occupation}"
        
        elif any(keyword in normalized_q for keyword in ['متزوج', 'جواز','متجوز']):
            return f"{'نعم أنا متجوز 'if self.patient.marital_status else 'لا انا اعزب'}"
        
        elif any(keyword in normalized_q for keyword in ['اولاد', 'عيال','اطفال']):
            return f"{'لدي 4 أطفال' if self.patient.marital_status else 'ليس لدي أطفال'}"
        
        elif any(keyword in normalized_q for keyword in ['تدخين', 'سجاير', 'تدخن', 'مدخن','بتدخن']):
            return f"{'نعم، أنا أدخن منذ عشرين عامًا، وفي الفترة الأخيرة كنت أدخن حوالي علبة يوميًا.' if self.patient.smoker else 'لا مش بداخن'}"

        elif any(keyword in normalized_q for keyword in ['جوزك بيدخن']):
            return f"{' اه جوزي بيدخن' if self.patient.parent_is_smoker else 'لا جوزي مش بيدخن'}"
        
        elif any(keyword in normalized_q for keyword in ['شاي','قهوه']):          
            return f"{'اه بشرب شاي و قهوه كتير حوالي 5 كوبيات فاليوم' if self.patient.Tea_addict else 'لا مليش تقل عالشاي و القهوة حوالي كوبايتين بس فاليوم لما ببقي مصدعة'}"
        
        elif any(keyword in normalized_q for keyword in ['حيوانات']):         
            return f"{' نعم عندي قطة اسمها مشمشه' if self.patient.Pet_owner else 'لا مش بربي اي حيوانات'}"   
          
        elif any(keyword in normalized_q for keyword in ['فطار','فطر','فطرتي','غدا','اتغديتي','عشا','اتعشيتي','أكلتي','اكل']):
            return f"{'نعم، لقد أكلت قبل أن آتي' if self.patient.is_eating else 'آخر مرة أكلتُ كانت أمس في الليل'}"               
        
        elif any(keyword in normalized_q for keyword in ['حمام']):
            return f"{' نعم، لقد دخلتُ الحمام حوالي خمس مرات منذ أمس، وأشرب الكثير من الماء لأنني أشعر بعطش شديد.' if self.patient.Polyuria else 'لا، أنا أدخل بشكل عادي، أي حوالي ثلاث مرات.'}" 

        elif any(keyword in normalized_q for keyword in ['حرقان']):
            return f"{'نعم.' if self.patient.Dysuria else 'لا، عادي، لا أشعر بشيء.'}"  

        elif any(keyword in normalized_q for keyword in ['لون']):
            return f"{'نعم، أصبح لون البول أكثر غمقانًا..' if self.patient.Polyuria_colour  else 'لا، عادي.'}"    

        elif any(keyword in normalized_q for keyword in ['نفس']):
            return f"{'نعم.' if self.patient.breathe_odor else 'لا مش باخد بالي عادي'}" 

        elif any(keyword in normalized_q for keyword in ['ترجيع']):
            return f"{'أَتَقَيَّأُ كُلَّمَا أَكَلْتُ، وَلَا يُوجَدُ دَمٌ '  if self.patient.vomiting else 'لا'}"
         

        elif any(keyword in normalized_q for keyword in ['امساك']):
            return f"{'ايوه عندي امساك' if self.patient.constipation else 'لا'}"
        
        elif any(keyword in normalized_q for keyword in ['اسهال']):
            return f"{'ايوه عندي اسهال' if self.patient.Diarrhea else 'لا'}"

        elif any(keyword in normalized_q for keyword in ['صفرا']):
            return f"{'ايوه عندي صفرا' if self.patient.Jaundice else 'لا'}"    

        elif any(keyword in normalized_q for keyword in ['انتفاخ']):
            return f"{'ايوه عندي انتفاخ' if self.patient.blotting else 'لا'}" 

        elif any(keyword in normalized_q for keyword in ['صدر']):
            return f"{'ايوه عندي الم في الصدر' if self.patient.chest_pain else 'لا'}"     
            
        elif any(keyword in normalized_q for keyword in ['كحه']):
            return f"{'ايوه عندي كحه' if self.patient.cough else 'لا'}"  
        
        elif any(keyword in normalized_q for keyword in ['بلغم']):
            return f"{'  نعم، أُعَانِي مِنْ كُحَّةٍ مُصَاحَبَةٍ بِبَلْغَمٍ. '  if self.patient.hemopt else 'لا'}"  
        
        elif any(keyword in normalized_q for keyword in ['سخونيه','سخن']):
            return f"{'ايوه عندي سخونيه' if self.patient.fever else 'لا'}" 

        elif any(keyword in normalized_q for keyword in ['زرقان','ازرق','زرق']):
            return f"{'ايوه عندي زرقان' if self.patient.cyanosis else 'لا'}" 
        
        elif any(keyword in normalized_q for keyword in ['نفخ','ورم']):
            return f"{'نعم، أشعر أنَّ جَسَدِي يَتَوَرَّمُ' if self.patient.edema else 'لا'}" 
        
        elif any(keyword in normalized_q for keyword in ['قلب','ضربات']):
            return f"{'إِنَّ ضَرَبَاتِ قَلْبِي سَرِيعَةٌ.' if self.patient.heart else 'لا'}"
        
        elif any(keyword in normalized_q for keyword in ['دوخه','وعي']):
            return f"{'نعم، لقد فقدتُ الوعي' if self.patient.conscious_level else 'أَشْعُرُ بِدُوَارٍ خَفِيفٍ وَأَحِسُّ أَنَّنِي أَتَعَرَّقُ قَلِيلًا.'}"   

        elif any(keyword in normalized_q for keyword in ['قرايه','تراكمي']):
            return f"{'لقد أجريت تحليل التراكمي منذ فترة، لكنني لا أتذكر نتيجته 'if self.patient.last_reading else 'لقد أجريت تحليل التراكمي منذ فترة، لكنني لا أتذكر نتيجته'}"                 

        elif any(keyword in normalized_q for keyword in ['عدوي','عدوات']):
            return f"{'لقد أصبتُ بنزلة برد شديدة منذ فترة.' if self.patient.infaction else 'لم أُصب بأي عدوى منذ فترة طويلة.'}"

        elif any(keyword in normalized_q for keyword in ['ريقك']):
            return f"{'أشعر بأن حلقي جاف' if self.patient.mou else 'لا'}" 
        

        elif any(keyword in normalized_q for keyword in ['معدل', 'كام']):
         # إذا كان مدخنًا، يتم إرجاع عدد السجائر اليومية
               if self.patient.smoker:
                   if self.patient.smoke['smoking']['cigarettes_per_day'] is not None:
                     return f"بشرب حوالي {self.patient.smoke['smoking']['cigarettes_per_day']} سيجارة في اليوم."
                   else:
                     return "عدد السجائر اليومية غير معروف."
               else:
                 return "لا مش بدخن"
               
        #elif 'مده' in normalized_q or ' امتى' in normalized_q:
         # إذا كان مدخنًا، يتم إرجاع مدة التدخين
         #       if self.patient.smoker:
          #         if self.patient.smoke['smoking']['duration'] is not None:
           #          return f"أنا بدخن من حوالي {self.patient.smoke['smoking']['duration']} سنين."
            #       else:
             #        return "مدة التدخين غير معروفة."
              #  else:
               #  return "أنا لا أدخن."

        elif any(keyword in normalized_q for keyword in ['كحول', 'شرب']):
            return f"{'اه انا بشرب كحوليات' if self.patient.alcohol_user else 'لا مش BASHRAB كحوليات'}"
        return "ارجع لل personal history فيه مشكله"
    
    ###################################################################################################
    
    def chief_complaint_response(self, question):
        """Handle questions about current medical complaint"""
        normalized_q = self.normalize_text(question)
        complaint_details = self.patient.chief_complaint


        if any(keyword in normalized_q for keyword in ['بتشتكي','مشكلة','اللي جابك','مستشفي','العياده','شكوه','تعبك']):
        #if 'بتشتكي' in normalized_q or 'مشكلة' in normalized_q:
            return f"{complaint_details['Complaint']}"
        

        
        elif any(keyword in normalized_q for keyword in [' امتي','تعب ','بدأت','مستمره',' قد ايه','مده']):
        #elif 'من امتي' in normalized_q:
            return f" {complaint_details['Duration']} "
        
        

        elif any(keyword in normalized_q for keyword in ['ظهرت معاك ازاي','المرض بدا معاك ازاي','التعب دا لاحظته ازاي ',' بالتدريج','تدريجي','فجأه','تدريج']):
        #elif 'ظهرت معاك ازاي' in normalized_q:
            return f" المشكله ظهرت  {complaint_details['Onset']}"
        


        elif any(keyword in normalized_q for keyword in ['شده','بيزيد ولا بيقل','زيد','يقل']):
            return f"{complaint_details['Severity']}"
        
        elif any(keyword in normalized_q for keyword in ['ريح']):
            return f"{complaint_details['releaving_factor']}"        
        
        return "ارجع لل complaint response فيه مشكله"
    
    #######################################################################################################
    def hpi_response(self, question):
        """Handle questions about the history of present illness (HPI)"""
        hpi_details = self.patient.hpi
        normalized_q = self.normalize_text(question)
        if any(keyword in normalized_q for keyword in ['اعراض اضافية', 'اعراض', 'وجع', 'الم']):      
            return f"{hpi_details.get('Associated Symptoms')}"
        

        elif 'سمع' in normalized_q:
            return f"{hpi_details.get('radiation')}"
        

        elif 'وصف' in normalized_q:
            return f"{hpi_details.get('char_of_pain')}"
           

        if 'تحليل' in normalized_q or 'تحاليل' in normalized_q:
            return f"{hpi_details.get('Investigation')}"
        

        elif 'علاج' in normalized_q :
            return f"{hpi_details.get('Treatment')}"

        elif 'مسكنات' in normalized_q :
            return f"{hpi_details.get('Painkillers')}"       
        
        
        return "تفاصيل التاريخ المرضي متاحة إذا أردت المزيد من المعلومات."


###########################################################################


    def medical_history_response(self, question):
        """
        Handle questions about the patient's medical history.
        """
        medical_detail = self.patient.medical_history
        normalized_q = self.normalize_text(question)

        if 'مرض' in normalized_q or 'مزمن' in normalized_q:
            return f"أنا أعاني من {medical_detail.get('condition')}."
        

        elif 'برشام' in normalized_q  :
            return f" {medical_detail.get('details')}."
        

        elif 'وحده' in normalized_q  :
            return f" {medical_detail.get('percentage')}."
        
        
        elif 'مره' in normalized_q  or 'اخر' in normalized_q:
            return f" {medical_detail.get('last_time')}."
        
        elif 'ضغط' in normalized_q  :
            return f" {medical_detail.get('other')}."


        return "لدي تاريخ طبي شامل. هل لديك سؤال محدد أكثر؟"
    



#############################################################################   

    def operations_response(self, normalized_q):
        """
        Handle questions about operations and blood transfusions.
        """
        medical_detail = self.patient.medical_history

        if 'عملية' in normalized_q or 'عمليات' in normalized_q:
            return "آه، وَلَدْتُ قَيْصَرِيًّا، أَحْمَدُ ابْنِي." if medical_detail.get('operation') else "لا، لَمْ أَجْرِ أَيَّةَ عَمَلِيَّاتٍ"

        if 'نقل دم' in normalized_q:
            return "آه، أخَدتُ كِيسَ دَمٍ تَبرَّعَ به ابْنُ أَخُوي." if medical_detail.get('blood_transfusions') else "لا، لَمْ أَحْتَجْ لِنَقْلِ دَمٍ."

        return "لم أتعرض لمضاعفات بعد أي عملية أو إجراء."
    


#############################################################################

    def drug_intake_response(self, normalized_q):

        #if 'ادوية' in normalized_q or 'مسكنات' in normalized_q:
        #    return "أتناول أدوية لعلاج الحالة بانتظام."

        if 'حساسية' in normalized_q:
            return "نعم، لدي حساسية تجاه بعض الأدوية."

        return "لا أتناول أدوية بشكل منتظم حاليًا."
    

################################################################################

    def similar_attacks_response(self, normalized_q):
        """
        Handle questions about similar attacks or previous incidents.
        """
        if 'نوبات' in normalized_q or 'حالة مماثلة' in normalized_q:
            return "نعم، واجهت حالة مشابهة لهذه من قبل."

        if 'حوادث' in normalized_q or 'صدمات' in normalized_q:
            return "لا، لم أتعرض لأي حوادث أو صدمات."

        return "هل يمكنك توضيح السؤال أكثر؟"   
    

    
    def _get_medications_response(self, normalized_q):
        """Handle questions about current medications"""

        rre = self.patient.current_medications
        if 'سلامه' in normalized_q :
            return "أسأل الله أن يمنحك السلامة يا دكتور." 





##############################################################################################

    def get_family_history_response(self, question):
        """Handle questions about family medical history."""
        normalized_q = self.normalize_text(question)
        family_history = self.patient.family_history

        if 'العيله' in normalized_q :
            return "آه، أَبُويا عِندَهُ الضَّغْط والسُّكَّر، وَأُمِّي لَا." if family_history.get('family') else "لا، مَحَدِّش فِي العيلة عِندَهُ أَيّ أَمْراضٍ مزمِنة."

        return " لا الحمد الله"

    #    return "ال family history"
    

        #if not family_history:
        #    return "لا يوجد لدي معلومات عن التاريخ العائلي."

        # Specific conditions check
        #if 'سكر' in normalized_q or 'ضغط' in normalized_q:
        #    for relation, condition in family_history.items():
        #        if 'سكر' in condition:
        #            return f"اه، {relation} لديه سكر."
        #        if 'ضغط' in condition:
        #            return f"نعم، {relation} لديه ضغط."
        #   return "لا يوجد أحد في العائلة يعاني من السكر أو الضغط حسب سجلاتي."

        # Check for specific family relations like الأب والأم
        #if 'قرايب' in normalized_q:
        #     return "نعم، الأب والأم قرايب."


        # General response for family history
        #history_summary = ", ".join([f"{relation}: {condition}" for relation, condition in family_history.items()])
        #return f"التاريخ العائلي هو: {history_summary}."

    
    

# Patient initialization with more detailed information
# Updated patient initialization with sex
