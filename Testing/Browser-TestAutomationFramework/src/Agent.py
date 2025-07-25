from browser_use.agent.service import Agent, Controller
from browser_use.browser.context import BrowserContext
from browser_use.agent.views import ActionResult

# from browser_use.agent.task import task
from browser_use.llm import ChatGoogle, ChatOllama,ChatOpenAI, ChatDeepSeek, ChatAnthropic
import asyncio
from pydantic import BaseModel

from dotenv import load_dotenv
load_dotenv()

# Define the output model for the controller
class CheckoutResult(BaseModel):
    login_status: str
    cart_status: str
    checkout_status: str
    total_update_status: str
    delivery_location_status: str
    confirmation_message: str

controller = Controller(output_model = CheckoutResult)


# Using playwright
@controller.action('Open base website')
async def open_website(browser: BrowserContext):
    page = await browser.get_current_page()
    await page.goto('https://rahulshettyacademy.com/loginpagePractise/')

# Using playwright
@controller.action("Get Attribute and url of the page")
async def get_attr_url(browser: BrowserContext):
    page = await browser.get_current_page()
    current_url = page.url
    attr = await page.get_by_text("Shop Name").get_attribute("class")
    print(f'Current URL: {current_url}')
    print(f'Attribute: {attr}')
    return ActionResult(extracted_content = f'Current URL: {current_url}, Attribute: {attr}')

async def SiteValidation():
    # Initialize the model
    # llm = ChatGoogle(model='gemini-2.0-flash-exp')
    # llm = ChatGoogle(model='models/gemini-2.5-flash-lite')
    # llm = ChatOllama(model="llama3.1:8b")   
    # llm = ChatOpenAI(model="gpt-4o-mini")    
    # llm = ChatDeepSeek(model="deepseek-chat")
    llm = ChatAnthropic(model="claude-3-5-sonnet-20240620")    

    task = """
        Important: I am UI Automation tester validating the tasks.
        Open base website
        Ensure you are in the website https://rahulshettyacademy.com/loginpagePractise/ and do not visit any other page.
        Login with username and password. Login details available in the same page.
        Get Attribute and url of the page
        After login, select first 2 products and add them to cart
        Then checkout and store the total value you see on screen
        Increase the quantity of any product and check if total value updates accordingly
        Checkout and select country, agree terms and purchase
        Verify thank you message is displayed
        """

    agent = Agent(
        task=task,
        llm=llm,
        use_vision=False,
        controller=controller,
    )

    history = await agent.run()
    history.save_to_file('site_validation_history.json')
    test_result = history.final_result()
    print(test_result)
    validated_result =CheckoutResult.model_validate_json(test_result)
    print(validated_result)

    assert validated_result.confirmation_message == "Thank you! Your order will be delivered in next few weeks :-)."

asyncio.run(SiteValidation())
    