import time

from selenium_tests.base import BaseSeleniumTests
from selenium.webdriver.support.ui import Select
from wagtail.core.models import Site
from iogt_users.factories import AdminUserFactory
from home.factories import SectionFactory
from questionnaires.factories import SurveyFactory, SurveyFormFieldFactory
from selenium_tests.pages import QuestionnairePage, QuestionnaireResultsPage, LoginPage

class QuestionnaireInputsSeleniumTests(BaseSeleniumTests):

    def setUp(self):
        Site.objects.all().delete()
        self.setup_blank_site()
        self.user = AdminUserFactory()
        self.section01 = SectionFactory(parent=self.home, owner=self.user)
        

    def test_single_submission(self):
        self.survey01 = SurveyFactory(
            parent=self.section01, 
            owner=self.user,
            allow_multiple_submissions = False
            )
        SurveyFormFieldFactory(
            page=self.survey01, 
            required = True,  
            default_value='',  
            field_type='singleline', 
        )
        self.visit_page(self.survey01)
        survey_page = QuestionnairePage(self.selenium)
        survey_page.enter_text("Testing some singleline text")
        survey_page.submit_response()
        revisit_page = self.visit_page(self.survey01)
        self.assertIn("You have already completed this survey.", revisit_page.get_content_text())

    def test_multiple_submission(self):
        self.survey01 = SurveyFactory(
            parent=self.section01, 
            owner=self.user,
            allow_multiple_submissions = True,
            thank_you_text="[{\"type\": \"paragraph\", \"value\": \"<p>Thankyou for completing the survey</p>\"}]"
            )
        SurveyFormFieldFactory(
            page=self.survey01, 
            required = True,  
            default_value='',  
            field_type='singleline', 
        )
        self.visit_page(self.survey01)
        survey_page = QuestionnairePage(self.selenium)
        survey_page.enter_text("Testing some singleline text")
        survey_page.submit_response()
        results_page = QuestionnaireResultsPage(self.selenium)
        self.assertIn("Thankyou for completing the survey", results_page.get_content_text())
        self.visit_page(self.survey01)
        survey_page = QuestionnairePage(self.selenium)
        survey_page.enter_text("Testing some singleline text")
        survey_page.submit_response()
        results_page = QuestionnaireResultsPage(self.selenium)
        self.assertIn("Thankyou for completing the survey", results_page.get_content_text())

    def test_multiple_submission(self):
        self.survey01 = SurveyFactory(
            parent=self.section01, 
            owner=self.user,
            allow_multiple_submissions = True,
            thank_you_text="[{\"type\": \"paragraph\", \"value\": \"<p>Thankyou for completing the survey</p>\"}]"
            )
        SurveyFormFieldFactory(
            page=self.survey01, 
            required = False,  
            default_value='',  
            field_type='singleline', 
        )
        SurveyFormFieldFactory(
            page=self.survey01, 
            required = True,
            choices = "A|B|C",  
            default_value='',  
            field_type='checkboxes', 
        )
        self.visit_page(self.survey01)
        survey_page = QuestionnairePage(self.selenium)
        self.assertIn("OPTIONAL", survey_page.get_content_text())
        survey_page.submit_response()
        self.assertIn("This field is required.", survey_page.get_content_text())
        survey_page.select_checkboxes("B")
        survey_page.submit_response()
        results_page = QuestionnaireResultsPage(self.selenium)
        self.assertIn("Thankyou for completing the survey", results_page.get_content_text())

    def test_multiple_page_survey(self):
        self.survey01 = SurveyFactory(
            parent=self.section01, 
            owner=self.user,
            multi_step = True,
            thank_you_text="[{\"type\": \"paragraph\", \"value\": \"<p>Thankyou for completing the survey</p>\"}]"
            )
        SurveyFormFieldFactory(
            page=self.survey01, 
            required = False,  
            default_value='',  
            field_type='singleline',
            page_break = True 
        )
        SurveyFormFieldFactory(
            page=self.survey01, 
            required = False,
            choices = "A|B|C",  
            default_value='',  
            field_type='checkboxes', 
        )
        self.visit_page(self.survey01)
        survey_page = QuestionnairePage(self.selenium)
        survey_page.submit_response()
        survey_page.submit_response()
        results_page = QuestionnaireResultsPage(self.selenium)
        self.assertIn("Thankyou for completing the survey", results_page.get_content_text())

    def test_survey_require_login(self):
        self.survey01 = SurveyFactory(
            parent=self.section01, 
            owner=self.user,
            allow_anonymous_submissions = False,
            thank_you_text="[{\"type\": \"paragraph\", \"value\": \"<p>Thankyou for completing the survey</p>\"}]"
            )
        SurveyFormFieldFactory(
            page=self.survey01, 
            required = True,  
            default_value='',  
            field_type='singleline',
            page_break = True 
        )
        
        self.visit_page(self.survey01)
        survey_page = QuestionnairePage(self.selenium)
        survey_page.login_button_submit()
        login_page = LoginPage(self.selenium)
        login_page.login_user(self.user)
        self.visit_page(self.survey01)
        survey_page = QuestionnairePage(self.selenium)
        results_page = QuestionnaireResultsPage(self.selenium)
        survey_page.enter_text("Testing some singleline text")
        survey_page.submit_response()
        self.assertIn("Thankyou for completing the survey", results_page.get_content_text())
        
        



        
        
        
