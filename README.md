# TravelVista: Your Personalized Travel Planner with Literary Escapades

Well!! How about simplifying your travel planning and giving you a smooth experience when you are still grappling around with the thought about places.

Smooth and Mind Boggling isn't it??

TravelVista presents a unique interface which provides the user an enriching experience where they can write their thoughts or even keywords, and based on this our system will take you through a fulfilling set of choices which you can easily go through and at your fingertip.

System is going to provide the user:

* List of cities
* Hotel or Probable Accommodation Choices 
* Nearby site tourist destinations or probable adventure itinerary

Based on these three choices, the system will look out for you and give you a set of itinerary choices for your whole journey and budget as well.

User can have their pick and solidify their travel plans and the best part is you came to this platform with those confusing thoughts and going out with one of the best experiences.

Sounds Fun !!

Do explore our website and get to know TravelVista .... with the power of LLMs.

## Technical Aspects

* External CSV is used for Langchain Model to search upon the necessary dataset, for "cities", "hotels" and "places to visit".
* For all three components, the API is created using Flask, and Langchain is used to search for the query in the external dataset used at the backend.
* BERT is used as an LLM along with Langchain to generate the answers to the user prompts.
* Augmented Dataset is used to give necessary context for the Langchain model to perform better and gain useful insights from the data which we have.
* Dataset is restricted to India right now for all the three contents which we are going to present through our system.


