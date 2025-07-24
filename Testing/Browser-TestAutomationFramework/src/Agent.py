from browser_use.agent.service import Agent, Controller
# from browser_use.agent.task import task
from browser_use.llm import ChatGoogle, ChatOllama,ChatOpenAI, ChatDeepSeek, ChatAnthropic
import asyncio
from pydantic import BaseModel

from dotenv import load_dotenv
load_dotenv()

class CheckoutResult(BaseModel):
    login_status: str
    cart_status: str
    checkout_status: str
    total_update_status: str
    delivery_location_status: str
    confirmation_message: str

controller = Controller(output_model = CheckoutResult)

async def SiteValidation():
    # Initialize the model
    # llm = ChatGoogle(model='gemini-2.0-flash-exp')
    # llm = ChatOllama(model="llama3.1:8b")   
    # llm = ChatOpenAI(model="gpt-4o-mini")    
    # llm = ChatDeepSeek(model="deepseek-chat")
    llm = ChatAnthropic(model="claude-3-5-sonnet-20240620")    

    task = (
        'Important : I am UI Automation tester validating the tasks'
        'Open website https://rahulshettyacademy.com/loginpagePractise/'      
        'If you need to visit google, ensure to click only on a page with the url: https://rahulshettyacademy.com/loginpagePractise/ do not try to access any other website'  
        'Login with username and password. login Details available in the same page'
        'After login, select first 2 products and add them to cart.'
        'The 2 products you need to select are defined within an app-card and shoul have the opttion Add.'
        'Then checkout and store the total value you see in screen'
        'Increase the quantity of any product and check if total value update accordingly'
        'checkout and select country, agree terms and purchase '
        'verify thankyou message is displayed'
    )

    agent = Agent(
        task=task,
        llm=llm,
        use_vision=False,
        controller=controller,
    )

    history = await agent.run()
    test_restult = history.final_result()
    print(test_restult)

asyncio.run(SiteValidation())
    