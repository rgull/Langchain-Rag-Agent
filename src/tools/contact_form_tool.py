from langchain_core.tools import StructuredTool
from pydantic import BaseModel, Field
from typing import Optional

import requests

class ContactForm(BaseModel):
    """Schema for the contact form submission."""
    
    name: str = Field(
        description="The full name of the contact person"
    )
    email: str = Field(
        description="The primary email address for communication"
    )
    phone: str = Field(
        description="The contact phone number"
    )
    company: str = Field(
        description="The name of the business or company"
    )
    businessType: str = Field(
        alias="business_type", # Helpful if your API uses camelCase but you prefer snake_case
        description="The category of business, e.g., Restaurant, Retail, etc."
    )
    city: str = Field(description="The city where the business is located")
    country: str = Field(description="The country of operation")
    numberOfStores: str = Field(
        description="The total number of store locations (as a string)"
    )
    message: Optional[str] = Field(
        default=None, 
        description="Any additional details or the specific request message"
    )

    class Config:
        # This allows the model to accept both 'businessType' and 'business_type'
        populate_by_name = True

class ContactFormInput(BaseModel):
    form: ContactForm = Field(description="Complete contact form payload")

def submit_contact_form(form : ContactForm):
    
    url = "https://api.ordervez.com/api/contact"
    payload = form.model_dump()

    try:
        response = requests.post(url,json=payload)
        response.raise_for_status() 
        response = response.json()
        return f"Success {response.get("success")}: The form was submitted. Message: {response.get("message")}"
    except Exception as e:
        return f"Error: Failed to submit form. Message: {response.get("message")}, Details: {str(e)}"

contact_form_tool = StructuredTool.from_function(func=submit_contact_form,
                                                 name="submit_contact_form",
                                                 description="Submits a business contact form with company. This tool is for company registration.",
                                                 args_schema=ContactFormInput)


